# Project Guidelines

## Scope
- This repo is a book project: every meaningful content change should keep book pages, runnable examples, and tests aligned.
- Use Traditional Chinese with Taiwan wording for reader-facing prose unless a file already establishes another language.

## Chapter Workflow
- When adding or expanding a chapter, update the chapter page, exercises, matching `examples/chNN/`, matching `tests/test_chNN*.py`, and any affected summaries in `book/index.md`, `book/myst.yml`, and `README.md`.
- Keep chapter implementations minimal and reproducible. Prefer small, testable functions over notebook-only logic.

## Build And Test
- Install dependencies with `python -m pip install -r requirements.txt` and `python -m pip install -e .`.
- Validate changes with `python -m pytest -q` and `powershell -ExecutionPolicy Bypass -File .\scripts\build_book.ps1` when content, examples, tests, or book config changes.
- Before release work, run the VS Code task `Release Check` and then review `publication/RELEASE_CHECKLIST.md` for manual items.

## Conventions
- Each chapter directory under `book/chapters/` should contain `index.md` and `exercises.md`.
- Each published chapter should have a corresponding example package in `examples/` and at least one matching test file in `tests/`.
- Prefer portable scripts that rely on the active Python environment instead of user-specific absolute paths.