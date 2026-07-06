# AGENTS.md

## Project Overview
- This repository contains a browser-playable Three.js 3D prototype game: a pickup truck hunting dinosaurs in a Jurassic-style arena.
- The game is implemented as a mostly self-contained `index.html` file.
- Regression checks live in `src/tests/game_regression_tests.py` and use source-level assertions for important gameplay behavior.

## Development Commands
- Run regression tests:
  ```powershell
  python src\tests\game_regression_tests.py
  ```
- Check JavaScript syntax inside `index.html`:
  ```powershell
  python -c "from pathlib import Path; s=Path('index.html').read_text(encoding='utf-8'); start=s.index('<script type=\"module\">')+len('<script type=\"module\">'); end=s.index('</script>', start); Path('tmp_check.mjs').write_text(s[start:end], encoding='utf-8')"
  node --check tmp_check.mjs
  Remove-Item tmp_check.mjs
  ```
- Run locally by opening `index.html` in a modern browser.

## Coding Guidelines
- Keep the game simple and self-contained unless a change explicitly requires splitting files.
- Preserve existing gameplay behavior unless the task asks to change it.
- When changing gameplay, add or update regression tests in `src/tests/game_regression_tests.py` first, then update `index.html`.
- Prefer small, surgical changes over broad refactors.
- Do not add copyrighted assets or protected game IP. Use procedural geometry, open-license assets, or clearly documented placeholders.

## Repository Hygiene
- Do not commit temporary generated files such as `tmp_check.mjs`.
- Keep README instructions generic and avoid personal machine paths.
- Before committing, run the regression tests and the JavaScript syntax check.
