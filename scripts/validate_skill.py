from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomllib
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = REPO_ROOT / "skills" / "lcfr-frontend-stack"
SKILL_NAME = "lcfr-frontend-stack"
SKILL_VERSION = "1.0.0"
REQUIRED_METADATA = {
    "name": SKILL_NAME,
    "license": "MIT",
}
REQUIRED_PATHS = frozenset(
    {
        "SKILL.md",
        "LICENSE",
        "references/design-and-brand.md",
        "references/implementation-and-interaction.md",
        "references/methodology.md",
        "references/provenance.md",
        "references/release-contract.md",
        "references/responsive-and-accessibility.md",
        "references/skill-map.md",
        "references/visual-evidence.md",
        "templates/brief.md",
        "templates/release-evidence.md",
        "templates/system-contract.md",
        "templates/verification-matrix.md",
    }
)
OPTIONAL_PATHS = frozenset({"manifest.json"})
FORBIDDEN_PATTERNS = {
    "private Windows path": re.compile(r"(?:[A-Za-z]:\\|C:/Users/)", re.IGNORECASE),
    "secret material": re.compile(
        r"(?:BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})"
    ),
}
PATH_REFERENCE = re.compile(r"`((?:references|templates)/[^`]+)`")
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or not parts[2].strip():
        raise ValueError("SKILL.md frontmatter must close before a non-empty body")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise TypeError("SKILL.md frontmatter must be a mapping")
    return data


def capture_skill(skill_root: Path) -> tuple[dict[str, bytes], list[str]]:
    snapshot: dict[str, bytes] = {}
    errors: list[str] = []
    if not skill_root.is_dir():
        return snapshot, [f"missing skill directory: {skill_root}"]

    for path in sorted(skill_root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            errors.append(
                f"symlinks are not distributable: {path.relative_to(skill_root)}"
            )
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(skill_root).as_posix()
        if relative.startswith("/") or "\\" in relative or ".." in relative.split("/"):
            errors.append(f"non-canonical skill path: {relative}")
            continue
        snapshot[relative] = path.read_bytes()
    return snapshot, errors


def validate_snapshot(snapshot: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    actual = set(snapshot)
    missing = sorted(REQUIRED_PATHS - actual)
    unexpected = sorted(actual - REQUIRED_PATHS - OPTIONAL_PATHS)
    if missing:
        errors.append(f"missing required files: {missing}")
    if unexpected:
        errors.append(f"unexpected skill files: {unexpected}")

    decoded: dict[str, str] = {}
    for relative, payload in snapshot.items():
        try:
            decoded[relative] = payload.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 distributed file: {relative}")

    skill_text = decoded.get("SKILL.md")
    metadata: dict[str, object] = {}
    if skill_text is not None:
        try:
            metadata = parse_frontmatter(skill_text)
        except (TypeError, ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    for key, expected in REQUIRED_METADATA.items():
        if metadata.get(key) != expected:
            errors.append(f"frontmatter {key!r} must equal {expected!r}")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.startswith("Use for "):
        errors.append("frontmatter description must start with 'Use for '")
    if isinstance(description, str) and len(description) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")
    metadata_block = metadata.get("metadata")
    version = (
        metadata_block.get("version") if isinstance(metadata_block, dict) else None
    )
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("metadata.version must be strict x.y.z SemVer")
    elif version != SKILL_VERSION:
        errors.append(f"metadata.version must equal release version {SKILL_VERSION}")

    for relative, payload in decoded.items():
        if not payload.strip():
            errors.append(f"empty file: {relative}")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(payload):
                errors.append(f"{label} found in {relative}")
        if relative.endswith(".md"):
            for target in PATH_REFERENCE.findall(payload):
                if target not in actual:
                    errors.append(f"broken bundled path in {relative}: {target}")

    if "manifest.json" in decoded:
        try:
            manifest = json.loads(decoded["manifest.json"])
            entries = manifest.get("files", [])
            indexed = {entry["path"]: entry for entry in entries}
            expected_manifest_paths = actual - OPTIONAL_PATHS
            if set(indexed) != expected_manifest_paths:
                errors.append("manifest file inventory does not match the skill tree")
            for relative in sorted(expected_manifest_paths & set(indexed)):
                payload = snapshot[relative]
                if indexed[relative].get("bytes") != len(payload):
                    errors.append(f"manifest byte count mismatch: {relative}")
                digest = hashlib.sha256(payload).hexdigest()
                if indexed[relative].get("sha256") != digest:
                    errors.append(f"manifest hash mismatch: {relative}")
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"invalid manifest.json: {exc}")

    return errors


def validate_skill(skill_root: Path = DEFAULT_SKILL) -> list[str]:
    snapshot, errors = capture_skill(skill_root)
    return errors + validate_snapshot(snapshot)


def validate_provenance(repo_root: Path = REPO_ROOT) -> list[str]:
    path = repo_root / "provenance.toml"
    if not path.is_file():
        return ["missing provenance.toml"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        skill = data["skill"]
        entries = data["files"]
        indexed = {entry["path"]: entry for entry in entries}
    except (KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        return [f"invalid provenance.toml: {exc}"]

    errors: list[str] = []
    if skill.get("name") != SKILL_NAME or skill.get("version") != SKILL_VERSION:
        errors.append(
            "provenance skill name/version does not match the release contract"
        )
    if skill.get("release_tag") != f"frontend-stack-v{SKILL_VERSION}":
        errors.append("provenance release tag does not match the skill version")
    if set(indexed) != REQUIRED_PATHS:
        errors.append("provenance file inventory does not match the release contract")
    for relative, entry in indexed.items():
        if entry.get("license") != "MIT":
            errors.append(f"non-MIT or missing licence in provenance: {relative}")
        origin = entry.get("origin")
        if not isinstance(origin, str) or not origin.strip().startswith("LCFR"):
            errors.append(f"missing LCFR origin in provenance: {relative}")
    changelog = repo_root / "CHANGELOG.md"
    if (
        not changelog.is_file()
        or f"Frontend Stack {SKILL_VERSION}"
        not in changelog.read_text(encoding="utf-8")
    ):
        errors.append("changelog does not contain the current frontend-stack version")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the public LCFR frontend skill"
    )
    parser.add_argument("skill", nargs="?", type=Path, default=DEFAULT_SKILL)
    parser.add_argument(
        "--skip-provenance",
        action="store_true",
        help="Validate an extracted archive without the repository provenance file",
    )
    args = parser.parse_args()
    skill_root = args.skill.resolve()
    errors = validate_skill(skill_root)
    if not args.skip_provenance and skill_root == DEFAULT_SKILL.resolve():
        errors.extend(validate_provenance())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"validated {skill_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
