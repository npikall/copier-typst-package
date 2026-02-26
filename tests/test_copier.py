from datetime import datetime
from pathlib import Path

import pytest
from conftest import FullUserAnswers as UserAnswers
from copier import run_copy

CURRENT_YEAR = datetime.today().year  # noqa: DTZ002


@pytest.fixture(scope="session")
def session_tmp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("main")


def test_copier_links_all_files_correct(
    session_tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = UserAnswers()
    cwd = Path(__file__).resolve().parent.parent

    # Run copier with the given context
    run_copy(
        src_path=str(cwd),
        dst_path=session_tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    want: list[str] = [
        ".typstignore",
        ".pre-commit-config.yaml",
        "CHANGELOG.md",
        "Justfile",
        "LICENSE",
        "README.md",
        "typst.toml",
        "template/main.typ",
        "src/lib.typ",
        "docs/docs.typ",
        "docs/thumbnail.typ",
        ".github/ISSUE_TEMPLATE/1-bug.md",
        ".github/ISSUE_TEMPLATE/2-feature.md",
        ".github/ISSUE_TEMPLATE/3-docs.md",
        ".github/ISSUE_TEMPLATE/4-change.md",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/workflows/release_github.yml",
        ".copier-answers.yml",
    ]

    # Check all expected files get copied
    for file in want:
        assert (session_tmp_path / file).exists()

    # Check if more than expected number of files got copied
    for file in session_tmp_path.rglob("*"):
        if file.is_dir():
            continue
        rel_path = str(file.relative_to(session_tmp_path))
        assert rel_path in want


def test_readme_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "README.md").read_text()
    want = "# foobar"
    assert want in got


def test_docs_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "docs/docs.typ").read_text()
    want = "#heading(outlined: false)[foobar]"
    assert want in got


def test_thumbnail_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "docs/thumbnail.typ").read_text()
    want = "= foobar"
    assert want in got


def test_lib_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "src/lib.typ").read_text()
    want = f"Copyright (c) {CURRENT_YEAR} jdoe"
    assert want in got


def test_main_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "template/main.typ").read_text()
    cases = [
        "foobar",
        '#import "@preview/foobar:0.1.0": *',
    ]
    for want in cases:
        assert want in got


def test_typst_toml_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "typst.toml").read_text()
    cases = [
        'name = "foobar"',
        'authors = ["jdoe"]',
        'repository = "https://github.com/jdoe/foobar.git"',
    ]
    for want in cases:
        assert want in got


def test_license_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "LICENSE").read_text()
    want = f"Copyright (c) {CURRENT_YEAR} jdoe"
    assert want in got
