from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import pytest

from scripts.build_skill_release import build_release
from scripts.validate_skill import (
    DEFAULT_SKILL,
    REQUIRED_PATHS,
    capture_skill,
    parse_frontmatter,
    validate_provenance,
    validate_skill,
    validate_snapshot,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_skill(destination: Path) -> Path:
    return Path(shutil.copytree(DEFAULT_SKILL, destination))


def test_frontend_stack_skill_is_valid() -> None:
    assert validate_skill() == []
    assert validate_provenance() == []
    metadata = parse_frontmatter(
        (DEFAULT_SKILL / "SKILL.md").read_text(encoding="utf-8")
    )
    assert metadata["name"] == "lcfr-frontend-stack"
    assert metadata["metadata"]["author"] == "LCFR"
    assert metadata["metadata"]["version"] == "1.0.0"


def test_release_archive_is_reproducible_and_self_contained(tmp_path: Path) -> None:
    first, first_checksum = build_release(tmp_path / "one")
    second, second_checksum = build_release(tmp_path / "two")

    assert sha256(first) == sha256(second)
    assert first_checksum.read_text(encoding="ascii").split()[0] == sha256(first)
    assert second_checksum.read_text(encoding="ascii").split()[0] == sha256(second)

    with zipfile.ZipFile(first) as bundle:
        names = bundle.namelist()
        assert all(name.startswith("lcfr-frontend-stack/") for name in names)
        assert all("\\" not in name and ".." not in Path(name).parts for name in names)
        assert "lcfr-frontend-stack/SKILL.md" in names
        assert "lcfr-frontend-stack/LICENSE" in names
        assert "lcfr-frontend-stack/manifest.json" in names
        manifest = json.loads(bundle.read("lcfr-frontend-stack/manifest.json"))
        assert manifest["name"] == "lcfr-frontend-stack"
        assert manifest["version"] == "1.0.0"
        assert {entry["path"] for entry in manifest["files"]} == REQUIRED_PATHS
        for relative in REQUIRED_PATHS:
            assert (
                bundle.read(f"lcfr-frontend-stack/{relative}")
                == (DEFAULT_SKILL / relative).read_bytes()
            )
        extracted = tmp_path / "installed"
        bundle.extractall(extracted)

    assert validate_skill(extracted / "lcfr-frontend-stack") == []


@pytest.mark.parametrize("relative", sorted(REQUIRED_PATHS))
def test_every_release_file_is_independently_required(
    tmp_path: Path, relative: str
) -> None:
    candidate = copy_skill(tmp_path / "candidate")
    (candidate / relative).unlink()
    snapshot, capture_errors = capture_skill(candidate)
    assert capture_errors == []
    assert any(
        "missing required files" in error for error in validate_snapshot(snapshot)
    )


def test_unexpected_file_cannot_enter_release(tmp_path: Path) -> None:
    candidate = copy_skill(tmp_path / "candidate")
    (candidate / ".env").write_text("NOT_A_REAL_SECRET=value\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unexpected skill files"):
        build_release(tmp_path / "output", candidate)


def test_builder_refuses_to_overwrite_release_artifacts(tmp_path: Path) -> None:
    build_release(tmp_path / "output")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        build_release(tmp_path / "output")


def test_installed_manifest_detects_byte_drift(tmp_path: Path) -> None:
    archive, _ = build_release(tmp_path / "output")
    installed = tmp_path / "installed"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(installed)
    skill = installed / "lcfr-frontend-stack"
    with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
        stream.write("\nmaterial drift\n")
    assert any("manifest" in error for error in validate_skill(skill))


def test_malformed_frontmatter_fails_closed() -> None:
    snapshot, capture_errors = capture_skill(DEFAULT_SKILL)
    assert capture_errors == []
    snapshot["SKILL.md"] = b"---\nname: [invalid\n---\nbody\n"
    assert validate_snapshot(snapshot)


def test_output_symlink_is_rejected_when_supported(tmp_path: Path) -> None:
    real_output = tmp_path / "real"
    real_output.mkdir()
    linked_output = tmp_path / "linked"
    try:
        linked_output.symlink_to(real_output, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable on this runner")
    with pytest.raises(ValueError, match="link or junction"):
        build_release(linked_output)


def test_public_skill_contains_no_private_paths_or_secret_tokens() -> None:
    payload = "\n".join(
        path.read_text(encoding="utf-8")
        for path in DEFAULT_SKILL.rglob("*")
        if path.is_file()
    )
    assert "C:/Users/" not in payload
    assert ":\\" not in payload
    assert "PRIVATE KEY" not in payload
    assert "Kinetograph repository" not in payload
