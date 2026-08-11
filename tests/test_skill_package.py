from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
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
    assert metadata["name"] == "aisthesis"
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
        assert all(name.startswith("aisthesis/") for name in names)
        assert all("\\" not in name and ".." not in Path(name).parts for name in names)
        assert "aisthesis/SKILL.md" in names
        assert "aisthesis/LICENSE" in names
        assert "aisthesis/manifest.json" in names
        manifest = json.loads(bundle.read("aisthesis/manifest.json"))
        assert manifest["name"] == "aisthesis"
        assert manifest["version"] == "1.0.0"
        assert {entry["path"] for entry in manifest["files"]} == REQUIRED_PATHS
        for relative in REQUIRED_PATHS:
            assert (
                bundle.read(f"aisthesis/{relative}")
                == (DEFAULT_SKILL / relative).read_bytes()
            )
        extracted = tmp_path / "installed"
        bundle.extractall(extracted)

    assert validate_skill(extracted / "aisthesis") == []


def test_portable_playwright_adapter_exposes_controlled_cli(tmp_path: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not installed")

    script = DEFAULT_SKILL / "scripts" / "playwright-evidence.mjs"
    help_result = subprocess.run(
        [node, str(script), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert help_result.returncode == 0
    assert "--url" in help_result.stdout
    assert "chromium" in help_result.stdout.lower()
    assert "firefox" in help_result.stdout.lower()
    assert help_result.stderr == ""

    error_result = subprocess.run(
        [node, str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert error_result.returncode == 2
    assert error_result.stdout == ""
    assert error_result.stderr.startswith("ERROR:")
    assert "--url" in error_result.stderr
    assert "Traceback" not in error_result.stderr

    output = tmp_path / "evidence"
    dependency_result = subprocess.run(
        [
            node,
            str(script),
            "--url",
            "https://example.com",
            "--output",
            str(output),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert dependency_result.returncode == 1
    assert dependency_result.stdout == ""
    assert dependency_result.stderr.startswith("ERROR:")
    assert "Playwright is not installed" in dependency_result.stderr
    assert not output.exists()


def test_one_stop_skill_routes_playwright_and_host_tools() -> None:
    skill = (DEFAULT_SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    orchestration = (
        (DEFAULT_SKILL / "references" / "tool-orchestration.md")
        .read_text(encoding="utf-8")
        .lower()
    )
    adapter = (
        (DEFAULT_SKILL / "scripts" / "playwright-evidence.mjs")
        .read_text(encoding="utf-8")
        .lower()
    )

    for term in (
        "playwright",
        "impeccable",
        "taste",
        "custom functions",
        "host tools",
        "chromium",
        "firefox",
        "browser evidence",
    ):
        assert term in skill or term in orchestration
    for term in (
        "createRequire",
        "process.cwd()",
        "chromium",
        "firefox",
        "screenshot",
        "console",
        "requestfailed",
        "pageerror",
        "promise.race",
        "visibleimages",
    ):
        assert term.lower() in adapter


def test_readme_checksum_matches_release_bytes(tmp_path: Path) -> None:
    archive, _ = build_release(tmp_path / "release")
    readme = (DEFAULT_SKILL.parent.parent / "README.md").read_text(encoding="utf-8")
    assert sha256(archive) in readme


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
    skill = installed / "aisthesis"
    with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
        stream.write("\nmaterial drift\n")
    assert any("manifest" in error for error in validate_skill(skill))


def test_installed_manifest_is_required(tmp_path: Path) -> None:
    archive, _ = build_release(tmp_path / "output")
    installed = tmp_path / "installed"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(installed)
    skill = installed / "aisthesis"
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
    skill = installed / "aisthesis"
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
        "name: aisthesis", "name: aisthesis\nname: shadow"
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
    source = staging / "aisthesis"
    target = tmp_path / "client" / "skills" / "aisthesis"
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


def test_readme_install_recipes_guard_linked_parents_before_move() -> None:
    readme = (DEFAULT_SKILL.parent.parent / "README.md").read_text(encoding="utf-8")
    posix_guard = 'assert_no_link_ancestor "$TARGET"'
    posix_move = 'mv "$STAGING/aisthesis" "$TARGET"'
    powershell_guard = "Assert-NoReparseAncestor -Path $Target"
    powershell_move = (
        'Move-Item -LiteralPath (Join-Path $Staging "aisthesis") -Destination $Target'
    )
    assert posix_guard in readme
    assert powershell_guard in readme
    assert readme.index(posix_guard) < readme.index(posix_move)
    assert readme.index(powershell_guard) < readme.index(powershell_move)


def test_public_capability_ledger_covers_every_absorbed_method() -> None:
    ledger = (DEFAULT_SKILL / "references" / "external-capability-ledger.md").read_text(
        encoding="utf-8"
    )
    for method in (
        "Impeccable",
        "Taste",
        "Metis",
        "UI UX Pro Max",
        "Emil",
        "Frontend Design",
        "Hallmark",
        "Popular Web Designs",
        "Aisthesis Judgment",
        "Kinetograph",
        "Scrolltelling QA",
        "Responsive Generated Brand Art",
        "Brand System Development",
        "Consistent Animation Systems",
        "Performance",
        "Dogfood",
        "Requesting Code Review",
        "Claude Design",
        "Design MD",
        "Sketch",
        "Public Release Integrity",
        "Pretext",
        "p5.js",
    ):
        assert method in ledger


def _make_directory_link(link: Path, target: Path) -> None:
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"junction creation unavailable: {result.stderr}")
    else:
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlinks are unavailable on this runner")


def test_documented_posix_guard_rejects_linked_parent(tmp_path: Path) -> None:
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("bash unavailable")
    external = tmp_path / "external"
    external.mkdir()
    linked = tmp_path / "skills"
    _make_directory_link(linked, external)
    target = linked / "aisthesis"
    script = r"""
assert_no_link_ancestor() {
  candidate=$1
  while :; do
    if [ -L "$candidate" ]; then exit 41; fi
    if command -v fsutil.exe >/dev/null 2>&1 && command -v cygpath >/dev/null 2>&1; then
      if fsutil.exe reparsepoint query "$(cygpath -w "$candidate")" >/dev/null 2>&1; then exit 41; fi
    fi
    parent=$(dirname -- "$candidate")
    [ "$parent" != "$candidate" ] || break
    candidate=$parent
  done
}
assert_no_link_ancestor "$1"
mkdir "$1"
"""
    result = subprocess.run(
        [bash, "-c", script, "guard", str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 41
    assert not (external / "aisthesis").exists()


@pytest.mark.skipif(os.name != "nt", reason="PowerShell reparse-point test")
def test_documented_powershell_guard_rejects_linked_parent(tmp_path: Path) -> None:
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if powershell is None:
        pytest.skip("Windows PowerShell unavailable")
    external = tmp_path / "external"
    external.mkdir()
    linked = tmp_path / "skills"
    _make_directory_link(linked, external)
    target = linked / "aisthesis"
    script = r"""
param([string]$Target)
function Assert-NoReparseAncestor {
    param([Parameter(Mandatory)][string]$Path)
    $Current = [System.IO.Path]::GetFullPath($Path)
    while ($true) {
        $Item = Get-Item -LiteralPath $Current -Force -ErrorAction SilentlyContinue
        if ($null -ne $Item) {
            if (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing destination through link or junction: $Current"
            }
        }
        $Parent = [System.IO.Directory]::GetParent($Current)
        if ($null -eq $Parent) { break }
        $Current = $Parent.FullName
    }
}
Assert-NoReparseAncestor -Path $Target
New-Item -ItemType Directory -Path $Target | Out-Null
"""
    probe = tmp_path / "guard.ps1"
    probe.write_text(script, encoding="utf-8")
    result = subprocess.run(
        [powershell, "-NoProfile", "-File", str(probe), "-Target", str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "link or junction" in result.stderr
    assert not (external / "aisthesis").exists()


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


@pytest.mark.parametrize(
    "artifact_name",
    [
        "aisthesis-1.0.0.zip",
        "aisthesis-1.0.0.zip.sha256",
    ],
)
def test_dangling_output_artifact_symlink_is_rejected(
    tmp_path: Path, artifact_name: str
) -> None:
    output = tmp_path / "output"
    output.mkdir()
    external = tmp_path / f"external-{artifact_name.replace('.', '-')}"
    linked_artifact = output / artifact_name
    try:
        linked_artifact.symlink_to(external)
    except OSError:
        pytest.skip("file symlinks are unavailable on this runner")
    with pytest.raises((FileExistsError, ValueError), match="overwrite|link|junction"):
        build_release(output)
    assert linked_artifact.is_symlink()
    assert not external.exists()


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


def test_skill_under_linked_parent_is_rejected(tmp_path: Path) -> None:
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    copy_skill(real_parent / "candidate")
    linked_parent = tmp_path / "linked-parent"
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(linked_parent), str(real_parent)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"junction creation unavailable: {result.stderr}")
    else:
        try:
            linked_parent.symlink_to(real_parent, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlinks are unavailable on this runner")
    with pytest.raises(ValueError, match="source path traverses a link or junction"):
        build_release(tmp_path / "output", linked_parent / "candidate")


def test_cli_rejects_skill_under_linked_parent(tmp_path: Path) -> None:
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    copy_skill(real_parent / "candidate")
    linked_parent = tmp_path / "linked-parent"
    if os.name == "nt":
        junction = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(linked_parent), str(real_parent)],
            check=False,
            capture_output=True,
            text=True,
        )
        if junction.returncode != 0:
            pytest.skip(f"junction creation unavailable: {junction.stderr}")
    else:
        try:
            linked_parent.symlink_to(real_parent, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlinks are unavailable on this runner")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.build_skill_release",
            "--skill",
            str(linked_parent / "candidate"),
            "--output",
            str(tmp_path / "output"),
        ],
        cwd=DEFAULT_SKILL.parents[1],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "source path traverses a link or junction" in result.stderr
    assert "Traceback" not in result.stderr


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
