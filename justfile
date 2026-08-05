# Default command lists all available recipes
[default]
_default:
    @just --list

alias c := clean
alias l := lint
alias q := check
alias t := test
alias fmt := format

# run the linter [arg:<full|concise|...>]
lint arg="concise":
    uv run ruff check . --fix --output-format="{{ arg }}"

# run the formatter
format:
    uv run ruff format .

# run the type checker [arg:<full|concise|...>]
types arg="concise":
    uv run ty check --output-format="{{ arg }}"

# lint, format and type-check [arg:<full|concise|...>]
check *arg="concise":
    -@just lint "{{ arg }}"
    -@just format
    -@just types "{{ arg }}"

# run the tests
test *args:
    uv run pytest tests/

# run the tests in different Python versions
testall *args:
    uv run --python=3.10 pytest {{ args }}
    uv run --python=3.12 pytest {{ args }}
    uv run --python=3.14 pytest {{ args }}

# run the formatter, linter, typechecker and the tests
ci python="3.12":
    uv run --python={{ python }} ruff format .
    uv run --python={{ python }} ruff check . --fix
    uv run --python={{ python }} ty check .
    uv run --python={{ python }} pytest tests/

# remove build artifacts
clean:
    rm -fr build/
    rm -fr site/
    rm -fr dist/
    rm -fr .eggs/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +
    find . -name '.cache' -exec rm -fr {} +
    rm -f .coverage
    rm -fr htmlcov/
    rm -fr .pytest_cache

# install dependencies in local venv
venv:
    uv sync --all-groups --all-extras

# render template to a temp dir for manual inspection
render:
    copier copy . ./rendered --overwrite --trust --defaults -r HEAD \
        --data project=foobar \
        --data git_user="John Doe" \
        --data git_email=john.doe@mail.com \
        --data copyright_license=MIT

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

_set_version target:
    case "{{ target }}" in \
        [0-9]*.[0-9]*.[0-9]*) \
            uv version {{ target }} ;; \
        *) \
            uv version --bump {{ target }} ;; \
    esac
    uv lock

# write the changelog from commit messages (gh:pawamoy/git-changelog)
changelog version=`uv version --short`:
    uvx git-changelog -Tio CHANGELOG.md -B="{{ version }}" -c conventional

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md
    git commit -m "chore(release): bumped version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release [target:<major|minor|patch|...> or semver]
release target: test
    @just _ensure_clean
    @just _set_version {{ target }}
    @just changelog "v`uv version --short`"
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
