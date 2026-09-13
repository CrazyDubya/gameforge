# gameforge

A catalog monorepo of Stephen's public game projects. Each game lives
under `games/<name>/` with its own README, dependencies, and tests —
nothing is functionally integrated; this is one roof, not one codebase.

## Games

| Game | What it is | Stack |
|---|---|---|
| [chess-alive](games/chess-alive/) | Full chess where every piece has an LLM personality giving in-character commentary. PvP, PvC (Stockfish), CvC, PvL, LvL, LvC | Python, pytest |
| [floppy-144mb](games/floppy-144mb/) | Six complete C games written for a 1.44MB-floppy contest (convoy, deepscan, switchyard, last-light, microcolony, ten-paces). Each binary must stay under 1,474,560 bytes | C (zig toolchain) |
| [surge-protocol](games/surge-protocol/) | Text-based cyberpunk courier MMORPG on Cloudflare Workers (Hono, D1, Durable Objects, R2) + Preact/Vite frontend | TypeScript, vitest |
| [qr-games](games/qr-games/) | Party games (bingo, trivia) with QR-code lobby: host creates lobby, players join by scanning, real-time via WebSocket | Node.js, jest |
| [game-implementations](games/game-implementations/) | Educational Python games: Pong variants, DiceCards, QuantumChess prototype, 4X strategy components | Python |
| [mazes](games/mazes/) | Maze generation (5 algorithms) + AI toolkit (LLM clients, synthetic data, board-game generator) | Python |
| [physics-demos](games/physics-demos/) | Genesis-framework physics demos (robot arm, elastic dragon, fluid sim) | Python |

## Running a game

Each game is self-contained — see its own README. Dependency manifests
(`pyproject.toml`, `package.json`, `requirements.txt`, Makefiles) are
per-game; there is no top-level install.

## Provenance

See [docs/PROVENANCE.md](docs/PROVENANCE.md) for source repositories,
commit SHAs, and what was curated out at merge time.
