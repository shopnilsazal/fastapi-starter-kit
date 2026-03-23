# Contributing

Contributions are welcome. Please follow the steps below to get set up and submit a pull request.

## Setup

```bash
git clone https://github.com/shopnilsazal/fastapi-starter-kit.git
cd fastapi-starter-kit
uv sync
pre-commit install
pre-commit install --hook-type commit-msg
```

## Workflow

1. Fork the repository
2. Create a branch from `main`: `git checkout -b feat/my-feature`
3. Make your changes
4. Ensure all checks pass: `pre-commit run --all-files`
5. Commit following the convention below
6. Open a pull request targeting `main`

Keep pull requests small and focused on a single concern.

## Commit Message Convention

This project enforces **Conventional Commits** via gitlint. The format is:

```
<type>: <description>
```

**Allowed types:**

`story` · `epic` · `fix` · `feat` · `chore` · `docs` · `style` · `refactor` · `perf` · `test` · `revert` · `ci` · `build`

**Rules:**

- Title must be 5–90 characters
- No "WIP" in the title
- Merge, revert, fixup, and squash commits are automatically ignored

**Examples:**

```
feat: add user authentication endpoint
fix: resolve database connection timeout on startup
docs: add cache usage examples
chore: upgrade ruff to v0.8.0
```

## Code Quality

All Python code must pass Ruff linting and formatting checks. These run automatically as pre-commit hooks, or manually:

```bash
ruff check . --fix   # lint with auto-fix
ruff format .        # format
```

Line length limit is 100 characters (configured in `ruff.toml`).

## Tests

The project includes pytest as a dev dependency. Add tests for any new functionality under a `tests/` directory following the existing structure.

```bash
uv run pytest
```
