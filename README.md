# Shoot Dino

Shoot Dino is a browser-playable Three.js prototype game about driving a pickup truck through a Jurassic-style arena while fighting waves of dinosaurs.

## Features

- Third-person pickup truck driving with acceleration, reverse, turning, inertia, and camera follow.
- Mouse-aimed machine guns with muzzle flash, recoil, bullet tracers, and raycast hit detection.
- Wave-based dinosaur encounters with multiple enemy types, including ground dinosaurs and flying pteranodons.
- Dynamic wave scenery with changing biomes, roads, vegetation, rocks, and weather effects.
- Persistent translucent HUD for health, score, wave number, remaining dinosaurs, and anti-air charges.
- Simple anti-air weapon and dinosaur summon controls.
- Source-level regression tests covering important gameplay behaviors.

## Quick Start

Open `index.html` in a modern browser.

Because the game imports Three.js from a CDN, an internet connection may be required the first time the page loads.

## Controls

- `W` - drive forward
- `S` - reverse
- `A` / `D` - turn
- Mouse move - aim
- Left mouse button - fire machine gun
- `Q` - use anti-air weapon
- `E` - summon dinosaurs when they are out of view
- `R` - restart

## Development

Run regression tests:

```powershell
python src\tests\game_regression_tests.py
```

Check JavaScript syntax extracted from `index.html`:

```powershell
python -c "from pathlib import Path; s=Path('index.html').read_text(encoding='utf-8'); start=s.index('<script type=\"module\">')+len('<script type=\"module\">'); end=s.index('</script>', start); Path('tmp_check.mjs').write_text(s[start:end], encoding='utf-8')"
node --check tmp_check.mjs
Remove-Item tmp_check.mjs
```

## Project Structure

```text
.
├── index.html                    # Game source and UI
├── src/tests/game_regression_tests.py # Source-level gameplay regression checks
├── AGENTS.md                     # Agent/developer guidance
└── README.md                     # Project documentation
```

## Notes

This is a prototype built with simple procedural geometry and browser APIs. It intentionally avoids copyrighted game assets.
