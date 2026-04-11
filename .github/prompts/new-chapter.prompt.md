---
name: "New Chapter"
description: "Use when creating a new chapter scaffold with matching book pages, examples, tests, TOC, and summaries."
argument-hint: "Chapter number, theme, and real-world scenario"
agent: "Chapter Workflow"
model: "GPT-5 (copilot)"
---
Create a new chapter scaffold for this repository using the provided chapter number, theme, and real-world scenario.

Requirements:
- Create or update the chapter book pages under `book/chapters/chNN-.../`.
- Create the matching example package under `examples/chNN/`.
- Create at least one matching test file under `tests/`.
- Update `book/myst.yml`, `book/index.md`, and `README.md` when the new chapter changes navigation or progress summaries.
- Keep reader-facing prose in Traditional Chinese with Taiwan wording.
- Keep code examples minimal, runnable, and easy to test.

Validation:
- Run `pytest -q` when tests are added or changed.
- Run `powershell -ExecutionPolicy Bypass -File .\scripts\build_book.ps1` when book pages or TOC change.

Return:
- The files created or updated.
- The validation performed.
- Any manual follow-up still needed.