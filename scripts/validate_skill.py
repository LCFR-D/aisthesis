from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tomllib
import unicodedata
from pathlib import Path, PurePosixPath

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = REPO_ROOT / "skills" / "aisthesis"
SKILL_NAME = "aisthesis"
SKILL_VERSION = "1.0.0"
REQUIRED_METADATA = {"name": SKILL_NAME, "license": "MIT"}
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
}
ALLOWED_METADATA = {"author", "version", "tags"}
REQUIRED_PATHS = frozenset(
    {
        "SKILL.md",
        "LICENSE",
        "references/methodology.md",
        "references/direction-and-taste.md",
        "references/design-and-brand.md",
        "references/systems-and-product-ui.md",
        "references/pattern-and-stack-intelligence.md",
        "references/typography-and-copy.md",
        "references/prototyping-and-rich-media.md",
        "references/implementation-and-interaction.md",
        "references/repeatable-animation-systems.md",
        "references/responsive-and-accessibility.md",
        "references/visual-evidence.md",
        "references/release-contract.md",
        "references/provenance.md",
        "references/capability-map.md",
        "references/external-capability-ledger.md",
        "templates/brief.md",
        "templates/design-direction.md",
        "templates/experience-architecture.md",
        "templates/system-contract.md",
        "templates/design-system.yaml",
        "templates/motion-contract.yaml",
        "templates/verification-matrix.md",
        "templates/accessibility-audit.md",
        "templates/issue-ledger.md",
        "templates/audit-report.md",
        "templates/release-evidence.md",
    }
)
OPTIONAL_PATHS = frozenset({"manifest.json"})
FORBIDDEN_PATTERNS = {
    "private Windows path": re.compile(r"(?:[A-Za-z]:\\|C:/Users/)", re.IGNORECASE),
    "private workspace": re.compile(
        r"(?:E:/Hermes|AppData/Local/hermes)", re.IGNORECASE
    ),
    "credential material": re.compile(
        r"(?:PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})"
    ),
    "credential assignment": re.compile(
        r"(?im)^\s*(?:api[_-]?key|token|password|secret|connection[_-]?string)\s*="
    ),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
WINDOWS_DEVICES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: MappingNode, deep: bool = False
) -> dict[object, object]:
    loader.flatten_mapping(node)
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def parse_frontmatter(text: str) -> dict[str, object]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    loader = UniqueKeyLoader(match.group(1))
    try:
        data = loader.get_single_data()
    finally:
        loader.dispose()
    if not isinstance(data, dict):
        raise TypeError("frontmatter must be a mapping")
    return data


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def is_link_or_junction(path: Path) -> bool:
    if path.is_symlink() or (
        hasattr(os.path, "isjunction") and os.path.isjunction(path)
    ):
        return True
    if os.name == "nt":
        try:
            attributes = path.lstat().st_file_attributes
        except (AttributeError, OSError):
            return False
        return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    return False


def portable_path_errors(paths: set[str] | frozenset[str]) -> list[str]:
    errors: list[str] = []
    folded: dict[str, str] = {}
    for relative in sorted(paths):
        if (
            not relative
            or relative.startswith("/")
            or "\\" in relative
            or ":" in relative
            or any(ord(character) < 32 for character in relative)
            or unicodedata.normalize("NFC", relative) != relative
            or PurePosixPath(relative).as_posix() != relative
        ):
            errors.append(f"non-portable release path: {relative!r}")
            continue
        for segment in relative.split("/"):
            if (
                segment in {"", ".", ".."}
                or segment.endswith((".", " "))
                or segment.split(".", 1)[0].upper() in WINDOWS_DEVICES
            ):
                errors.append(f"non-portable release path segment: {relative!r}")
        key = relative.casefold()
        if key in folded and folded[key] != relative:
            errors.append(f"case-fold path collision: {folded[key]!r}, {relative!r}")
        folded[key] = relative
    return errors


def capture_skill(skill_root: Path) -> tuple[dict[str, bytes], list[str]]:
    lexical_root = Path(os.path.abspath(skill_root))
    if is_link_or_junction(lexical_root):
        return {}, [f"skill root is a link or junction: {lexical_root}"]
    for ancestor in lexical_root.parents:
        if is_link_or_junction(ancestor):
            return {}, [f"source path traverses a link or junction: {ancestor}"]
    root = lexical_root.resolve(strict=True)
    snapshot: dict[str, bytes] = {}
    errors: list[str] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if is_link_or_junction(path):
            errors.append(f"links and junctions are not allowed: {relative}")
        elif path.is_file():
            snapshot[relative] = path.read_bytes()
        elif not path.is_dir():
            errors.append(f"non-regular skill entry: {relative}")
    actual = set(snapshot)
    unexpected = actual - REQUIRED_PATHS - OPTIONAL_PATHS
    if unexpected:
        errors.append(f"unexpected skill files: {sorted(unexpected)}")
    errors.extend(portable_path_errors(actual))
    return snapshot, errors


def manifest_bytes(snapshot: dict[str, bytes]) -> bytes:
    source = {
        path: payload for path, payload in snapshot.items() if path != "manifest.json"
    }
    metadata = parse_frontmatter(source["SKILL.md"].decode("utf-8"))
    version = str(metadata["metadata"]["version"])
    manifest = {
        "files": [
            {"path": path, "sha256": sha256_bytes(payload), "size": len(payload)}
            for path, payload in sorted(source.items())
        ],
        "format": 1,
        "license": "MIT",
        "name": metadata["name"],
        "version": version,
    }
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def validate_snapshot(
    snapshot: dict[str, bytes], *, require_manifest: bool = False
) -> list[str]:
    errors: list[str] = []
    actual = set(snapshot)
    missing = REQUIRED_PATHS - actual
    unexpected = actual - REQUIRED_PATHS - OPTIONAL_PATHS
    if missing:
        errors.append(f"missing required files: {sorted(missing)}")
    if unexpected:
        errors.append(f"unexpected skill files: {sorted(unexpected)}")
    if require_manifest and "manifest.json" not in actual:
        errors.append("installed skill is missing manifest.json")
    errors.extend(portable_path_errors(actual))
    if missing:
        return errors

    decoded: dict[str, str] = {}
    for relative, payload in snapshot.items():
        if payload.startswith(b"\xef\xbb\xbf"):
            errors.append(f"UTF-8 BOM is not allowed: {relative}")
        if b"\r" in payload:
            errors.append(f"only LF line endings are allowed: {relative}")
        try:
            decoded[relative] = payload.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"file is not UTF-8: {relative}")
    if "SKILL.md" not in decoded:
        return errors

    try:
        metadata = parse_frontmatter(decoded["SKILL.md"])
    except (TypeError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"invalid frontmatter: {exc}")
        return errors

    if set(metadata) - ALLOWED_FRONTMATTER:
        errors.append(
            f"unsupported frontmatter fields: {sorted(set(metadata) - ALLOWED_FRONTMATTER)}"
        )
    for key, expected in REQUIRED_METADATA.items():
        if metadata.get(key) != expected:
            errors.append(f"frontmatter {key!r} must equal {expected!r}")
    description = metadata.get("description")
    if (
        not isinstance(description, str)
        or not description.startswith("Use for ")
        or description != description.strip()
        or len(description) > 1024
    ):
        errors.append("description must be a trimmed, useful 'Use for …' trigger")
    compatibility = metadata.get("compatibility")
    if not isinstance(compatibility, str) or not compatibility.strip():
        errors.append("compatibility must be a non-empty string")
    nested = metadata.get("metadata")
    if not isinstance(nested, dict):
        errors.append("metadata must be a mapping")
        nested = {}
    elif set(nested) - ALLOWED_METADATA:
        errors.append(
            f"unsupported metadata fields: {sorted(set(nested) - ALLOWED_METADATA)}"
        )
    if nested.get("author") != "LCFR":
        errors.append("metadata.author must equal 'LCFR'")
    version = nested.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append("metadata.version must be strict x.y.z SemVer")
    elif version != SKILL_VERSION:
        errors.append(f"metadata.version must equal release version {SKILL_VERSION}")
    tags = nested.get("tags")
    if not isinstance(tags, str) or not tags.strip():
        errors.append("metadata.tags must be a non-empty string")

    for relative, payload in decoded.items():
        if not payload.strip():
            errors.append(f"empty file: {relative}")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(payload):
                errors.append(f"{label} found in {relative}")
        if relative.endswith(".md"):
            for target in MARKDOWN_LINK.findall(payload):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = target.split("#", 1)[0]
                resolved = (PurePosixPath(relative).parent / target_path).as_posix()
                if (
                    target_path.startswith("/")
                    or ".." in PurePosixPath(target_path).parts
                ):
                    errors.append(f"non-contained link in {relative}: {target}")
                elif resolved not in actual:
                    errors.append(f"broken relative link in {relative}: {target}")

    if "manifest.json" in snapshot:
        try:
            expected = manifest_bytes(snapshot)
        except (
            KeyError,
            TypeError,
            ValueError,
            UnicodeDecodeError,
            yaml.YAMLError,
        ) as exc:
            errors.append(f"unable to reproduce manifest: {exc}")
        else:
            if snapshot["manifest.json"] != expected:
                errors.append("manifest does not match the installed payload bytes")
    return errors


def validate_skill(
    skill_root: Path = DEFAULT_SKILL, *, require_manifest: bool | None = None
) -> list[str]:
    if require_manifest is None:
        require_manifest = skill_root.resolve() != DEFAULT_SKILL.resolve()
    snapshot, capture_errors = capture_skill(skill_root)
    return capture_errors + validate_snapshot(
        snapshot, require_manifest=require_manifest
    )


def validate_provenance(
    repo_root: Path = REPO_ROOT, snapshot: dict[str, bytes] | None = None
) -> list[str]:
    path = repo_root / "provenance.toml"
    if not path.is_file():
        return ["missing provenance.toml"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        skill = data["skill"]
        generated = data["generated"]
        entries = data["files"]
        indexed = {entry["path"]: entry for entry in entries}
    except (KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        return [f"invalid provenance.toml: {exc}"]

    if snapshot is None:
        snapshot, capture_errors = capture_skill(repo_root / "skills" / SKILL_NAME)
    else:
        capture_errors = []
    source_snapshot = {
        relative: payload
        for relative, payload in snapshot.items()
        if relative != "manifest.json"
    }
    errors = list(capture_errors)
    if skill.get("name") != SKILL_NAME or skill.get("version") != SKILL_VERSION:
        errors.append(
            "provenance skill name/version does not match the release contract"
        )
    if skill.get("release_tag") != f"aisthesis-v{SKILL_VERSION}":
        errors.append("provenance release tag does not match the skill version")
    if set(indexed) != REQUIRED_PATHS or len(indexed) != len(entries):
        errors.append("provenance file inventory does not match the release contract")
    for relative, entry in indexed.items():
        if entry.get("license") != "MIT":
            errors.append(f"non-MIT provenance entry: {relative}")
        origin = entry.get("origin")
        if not isinstance(origin, str) or not origin.strip().startswith("LCFR"):
            errors.append(f"missing LCFR origin in provenance: {relative}")
        payload = source_snapshot.get(relative)
        if payload is None or entry.get("sha256") != sha256_bytes(payload):
            errors.append(f"provenance hash mismatch: {relative}")
    try:
        expected_manifest_hash = sha256_bytes(manifest_bytes(source_snapshot))
    except (KeyError, TypeError, ValueError, UnicodeDecodeError, yaml.YAMLError) as exc:
        errors.append(f"unable to calculate generated manifest provenance: {exc}")
    else:
        if (
            generated.get("path") != "manifest.json"
            or generated.get("origin") != "LCFR deterministic release builder"
            or generated.get("license") != "MIT"
            or generated.get("sha256") != expected_manifest_hash
        ):
            errors.append("generated manifest provenance does not match release bytes")
    changelog = repo_root / "CHANGELOG.md"
    if (
        not changelog.is_file()
        or f"Aisthesis {SKILL_VERSION}" not in changelog.read_text(encoding="utf-8")
    ):
        errors.append("changelog does not contain the current Aisthesis version")
    notices = repo_root / "THIRD_PARTY_NOTICES.md"
    if (
        not notices.is_file()
        or "does **not** redistribute third-party"
        not in notices.read_text(encoding="utf-8")
    ):
        errors.append(
            "third-party notices do not record the non-redistribution boundary"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Aisthesis frontend operating system skill"
    )
    parser.add_argument("skill", nargs="?", type=Path, default=DEFAULT_SKILL)
    args = parser.parse_args()
    errors = validate_skill(args.skill)
    if args.skill.resolve() == DEFAULT_SKILL.resolve():
        errors.extend(validate_provenance())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"validated {args.skill.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
