from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from scripts.build_skill_release import build_release
from scripts.validate_skill import (
    DEFAULT_SKILL,
    REQUIRED_PATHS,
    capture_skill,
    parse_frontmatter,
    portable_path_errors,
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


def test_installed_manifest_is_required(tmp_path: Path) -> None:
    archive, _ = build_release(tmp_path / "output")
    installed = tmp_path / "installed"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(installed)
    skill = installed / "lcfr-frontend-stack"
    (skill / "manifest.json").unlink()
    assert "installed skill is missing manifest.json" in validate_skill(skill)


@pytest.mark.parametrize(
    "tampered_manifest",
    [
        b"[]\n",
        b'{"format":999,"name":"wrong","version":"99.0.0","license":"Proprietary","files":[]}\n',
    ],
)
def test_installed_manifest_identity_fails_closed(
    tmp_path: Path, tampered_manifest: bytes
) -> None:
    archive, _ = build_release(tmp_path / "output")
    installed = tmp_path / "installed"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(installed)
    skill = installed / "lcfr-frontend-stack"
    (skill / "manifest.json").write_bytes(tampered_manifest)
    errors = validate_skill(skill)
    assert errors == ["manifest does not match the installed payload bytes"]


def test_provenance_detects_source_byte_drift() -> None:
    snapshot, capture_errors = capture_skill(DEFAULT_SKILL)
    assert capture_errors == []
    snapshot["LICENSE"] += b"drift"
    assert any(
        "provenance hash mismatch: LICENSE" in error
        for error in validate_provenance(snapshot=snapshot)
    )


def test_malformed_frontmatter_fails_closed() -> None:
    snapshot, capture_errors = capture_skill(DEFAULT_SKILL)
    assert capture_errors == []
    snapshot["SKILL.md"] = b"---\nname: [invalid\n---\nbody\n"
    assert validate_snapshot(snapshot)


def test_duplicate_frontmatter_keys_fail_closed() -> None:
    snapshot, capture_errors = capture_skill(DEFAULT_SKILL)
    assert capture_errors == []
    text = snapshot["SKILL.md"].decode("utf-8")
    snapshot["SKILL.md"] = text.replace(
        "name: lcfr-frontend-stack", "name: lcfr-frontend-stack\nname: shadow"
    ).encode("utf-8")
    assert any("duplicate key" in error for error in validate_snapshot(snapshot))


@pytest.mark.parametrize(
    ("prefix", "replacement", "expected"),
    [
        (b"\xef\xbb\xbf", b"", "UTF-8 BOM"),
        (b"", b"\r\n", "only LF line endings"),
    ],
)
def test_noncanonical_text_encoding_fails_closed(
    prefix: bytes, replacement: bytes, expected: str
) -> None:
    snapshot, capture_errors = capture_skill(DEFAULT_SKILL)
    assert capture_errors == []
    payload = snapshot["LICENSE"]
    snapshot["LICENSE"] = prefix + (
        payload.replace(b"\n", replacement) if replacement else payload
    )
    assert any(expected in error for error in validate_snapshot(snapshot))


def test_nonportable_archive_paths_fail_closed() -> None:
    errors = portable_path_errors(
        {
            "../escape.md",
            "NUL.txt",
            "references/Case.md",
            "references/case.md",
            "trailing-space ",
            "drive:C.md",
            "back\\slash.md",
        }
    )
    assert len(errors) >= 6


def test_clean_room_install_refuses_existing_target(tmp_path: Path) -> None:
    archive, _ = build_release(tmp_path / "output")
    staging = tmp_path / "staging"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(staging)
    source = staging / "lcfr-frontend-stack"
    target = tmp_path / "client" / "skills" / "lcfr-frontend-stack"
    target.parent.mkdir(parents=True)
    shutil.copytree(source, target)
    sentinel = target / "user-content.txt"
    sentinel.write_text("preserve me", encoding="utf-8")
    with pytest.raises(FileExistsError):
        shutil.copytree(source, target)
    assert sentinel.read_text(encoding="utf-8") == "preserve me"
    errors = validate_skill(target)
    assert any("unexpected skill files" in error for error in errors)
    assert any("manifest does not match" in error for error in errors)


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


def test_skill_root_symlink_is_rejected_when_supported(tmp_path: Path) -> None:
    source = copy_skill(tmp_path / "source")
    linked = tmp_path / "linked"
    try:
        linked.symlink_to(source, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable on this runner")
    assert any(
        "skill root is a link or junction" in error for error in validate_skill(linked)
    )


@pytest.mark.skipif(os.name != "nt", reason="Windows junction test")
def test_source_junction_is_rejected(tmp_path: Path) -> None:
    candidate = copy_skill(tmp_path / "candidate")
    external = tmp_path / "external-references"
    shutil.copytree(candidate / "references", external)
    shutil.rmtree(candidate / "references")
    result = subprocess.run(
        ["cmd.exe", "/c", "mklink", "/J", str(candidate / "references"), str(external)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"junction creation unavailable: {result.stderr}")
    with pytest.raises(ValueError, match="links and junctions are not allowed"):
        build_release(tmp_path / "output", candidate)


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
