# Get all the required dependencies here:
# Run 'bash scripts/install-deps.sh' to install all dependencies automatically.
# tt:       https://typst-community.github.io/tytanic/quickstart/install.html
# uvx:      https://docs.astral.sh/uv/getting-started/installation/
# gotpm:    https://github.com/npikall/gotpm
# typst:    https://github.com/typst/typst#installation
# typstyle: https://github.com/typst/typstyle
# typst-package-check: https://github.com/typst/package-check#using-this-tool

root := justfile_directory()
export TYPST_ROOT := root

[default]
_default:
    @just --list --unsorted

alias i := install
alias u := uninstall
alias ip := install-preview
alias up := uninstall-preview
alias fmt := format

# install the pre-commit hooks
hooks-install:
    uvx prek install

# run pre-commit hooks
hooks:
    uvx prek run -a

# generate manual
docs:
    typst compile docs/docs.typ docs/docs.pdf

# generate the thumbnail
thumbnail:
    typst compile docs/thumbnail.typ thumbnail.png

# compile the template
template:
    typst compile template/main.typ

# format the .typ files
format:
    typstyle -i --wrap-text .

# run test suite
test *args:
    tt run {{ args }}

# update test cases
test-update *args:
    tt update {{ args }}

# install the library into "@local"
install *args:
    gotpm install {{ args }}

# install the library into "@preview"
install-preview *args:
    gotpm install -n preview {{ args }}

# uninstall the library from "@local"
uninstall *args:
    gotpm uninstall {{ args }}

# uninstall the library from "@preview"
uninstall-preview *args:
    gotpm uninstall -n preview {{ args }}

# publish a package to the typst universe
publish *args:
    gotpm publish {{ args }}

# package the library into the specified destination folder
dist target="dist":
    GOTPM_INSTALL_DIR="{{ target }}" gotpm install

# run typst package checker
check:
    just dist
    -typst-package-check check dist
    rm -rf dist

# run ci suite (test, doc, thumbnail)
ci: test docs thumbnail check

# update the package version
_bump incr="patch":
    gotpm bump {{ incr }} --indent

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

# write the changelog from commit messages (gh:pawamoy/git-changelog)
changelog version=`gotpm bump -c`:
    uvx git-changelog -Tio CHANGELOG.md -B="{{ version }}" -c conventional

_commit_and_tag version=`gotpm bump --show-current`:
    git add .
    git commit -m "chore(release): bumped version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release [target:<major|minor|patch> or semver]
release target: test check
    @just _ensure_clean
    @just _bump {{ target }}
    @just changelog
    @just docs
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
