from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path

from scripts.validate_skill import (
    DEFAULT_SKILL,
    REPO_ROOT,
    REQUIRED_PATHS,
    capture_skill,
    manifest_bytes,
    parse_frontmatter,
    validate_provenance,
    validate_snapshot,
)

FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(os.path, "isjunction", lambda _path: False)
    return path.is_symlink() or bool(is_junction(path))


def _validate_output_path(output_dir: Path) -> None:
    current = output_dir
    while not current.exists() and current != current.parent:
        current = current.parent
    for candidate in (current, *current.parents):
        if _is_link_or_junction(candidate):
            raise ValueError(f"output path traverses a link or junction: {candidate}")


def build_release(
    output_dir: Path, skill_root: Path = DEFAULT_SKILL
) -> tuple[Path, Path]:
    snapshot, capture_errors = capture_skill(skill_root)
    errors = capture_errors + validate_snapshot(snapshot)
    if skill_root.resolve() == DEFAULT_SKILL.resolve():
        errors.extend(validate_provenance(snapshot=snapshot))
    if errors:
        raise ValueError("invalid skill:\n" + "\n".join(errors))
    if set(snapshot) != REQUIRED_PATHS:
        raise ValueError("source tree differs from the anchored release file list")

    skill_text = snapshot["SKILL.md"].decode("utf-8")
    metadata = parse_frontmatter(skill_text)
    version = metadata["metadata"]["version"]
    name = str(metadata["name"])
    ordered = tuple(
        (relative, snapshot[relative]) for relative in sorted(REQUIRED_PATHS)
    )
    manifest_payload = manifest_bytes(snapshot)

    output_dir = Path(os.path.abspath(output_dir))
    _validate_output_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{name}-{version}.zip"
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    if archive.exists() or checksum.exists():
        raise FileExistsError("refusing to overwrite an existing release artifact")

    with zipfile.ZipFile(
        archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as bundle:
        for relative, payload in ordered:
            info = zipfile.ZipInfo(f"{name}/{relative}", FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            bundle.writestr(
                info,
                payload,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
        info = zipfile.ZipInfo(f"{name}/manifest.json", FIXED_TIMESTAMP)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        info.create_system = 3
        bundle.writestr(
            info,
            manifest_payload,
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )

    digest = file_sha256(archive)
    with checksum.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(f"{digest}  {archive.name}\n")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic LCFR frontend skill archive"
    )
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "dist")
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    args = parser.parse_args()
    archive, checksum = build_release(args.output, args.skill.resolve())
    print(archive)
    print(checksum)
    print(file_sha256(archive))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
