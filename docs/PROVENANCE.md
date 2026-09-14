# PROVENANCE — gameforge

Consolidated 2026-09-13 by Alice (Muse) for Stephen. Clean-copy merge:
each source was copied verbatim at the recorded HEAD into `games/<name>/`,
except the curated exclusions listed below. No code was modified in the
merge (only relocation). All source repositories are archived on GitHub
with full history intact — nothing was deleted.

## Sources

| Source repo | HEAD | Merged as | Notes |
|---|---|---|---|
| CrazyDubya/ChessAlive | dbbc5ce5754e9b01ada6390106c1db0a544128e2 | games/chess-alive/ | Base repo (renamed to gameforge). Full Python chess + LLM commentary. |
| CrazyDubya/144mb | 15a7df3fd57d33b008f555a86b54a657ff13f5ec | games/floppy-144mb/ | Six C games for 1.44MB-floppy contest. Committed generated `scene_pixels.h` headers kept (needed to build). |
| CrazyDubya/SurgeProtocol | d20fdd110cd20bd1aecf8819fce77e71c6c96c59 | games/surge-protocol/ | Cyberpunk courier MMORPG (Cloudflare Workers + Preact frontend). |
| CrazyDubya/QRGames | 05f4ef61411712c5aca81fd14f9f61d9089a6cc6 | games/qr-games/ | QR-code lobby party games (Express + WebSocket). |
| CrazyDubya/game-implementations-collection | 3ce13ac6a6aaa4d57796fd452a66a3b301c8d3c3 | games/game-implementations/ | Educational Python games (Pong, DiceCards, QuantumChess, 4X components). |
| CrazyDubya/mazes-multi-tool | 4b60fa4a913960b2d94012995de24496c1754f6c | games/mazes/ | Maze generation + AI toolkit. Curated (see below). |
| CrazyDubya/genesis-physics-sim | 54ff987d140ed141829e6a9c1e555a433386ad48 | games/physics-demos/ | Genesis-framework physics demos (robot arm, elastic dragon, fluid sim). |
| CrazyDubya/Taverna | fdac428e4c11e39cf67d0e6101c71ced358e1788 | games/taverna/ | LLM-driven text RPG "The Living Rusted Tankard" (FastAPI server, Three.js demo, JSON world data, tests, CI). Curated: 30 stale root planning/analysis docs excluded (see below); they stay in the archived source. |
| CrazyDubya/Mystery | b2f0fad0573ecb0abba7a211bb6eafe0e2bb7514 | games/taverna/docs/code-review/ | Taverna's code-review & refactoring documentation companion (not a game): review reports, refactoring plans, before/after examples. Folded in as docs under the taverna merge. |

## Curated exclusions (kept in the archived source repo)

- mazes-multi-tool: `record/replays/*.mp4`, `krge_screenrecord/replays/*.mp4`
  (committed screen recordings) and the entire vendored
  `krge_screenrecord/ffmpeg/` source tree (~8,567 files, ~100MB). Build
  artifact / third-party source, not project code.


- taverna: the ~30 stale root planning/analysis docs (roadmaps, sprint trackers,
  swarm analyses, phase summaries — everything matching the repo README's note
  that only `TODO.md` and `docs/` are current). Full list: CODE_QUALITY_ANALYSIS.md,
  COMPREHENSIVE_CODE_REVIEW.md, COPILOT_SWARM_ANALYSIS_REPORT.md,
  DEVELOPMENT_SPRINT_TRACKER.md, FUNCTIONAL_TESTING_CHECKLIST.md,
  GAMESTATEFILES_CLEANUP_SUMMARY.md, GAMESTATE_CONSOLIDATION.md,
  IMMEDIATE_ACTION_PLAN.md, IMMERSIVE_GAMEPLAY_FEATURES.md, IMPLEMENTATION_ROADMAP.md,
  LLM_INTEGRATION_ENHANCEMENTS.md, MULTI_PERSPECTIVE_SWARM_ANALYSIS.md,
  MULTI_PHASE_DEVELOPMENT_PLAN.md, P0_P1_IMPLEMENTATION_SUMMARY.md,
  P0_P1_P2_FINAL_SUMMARY.md, P0_P1_SESSION_SUMMARY.md, PERFORMANCE_OPTIMIZATIONS.md,
  PHASE_0_RESULTS.md, PROJECT_STRATEGIC_EVALUATION.md, QUALITY_IMPROVEMENT_PLAN.md,
  ROADMAP_VISUAL_SUMMARY.md, SCHIZO_MODE_MULTI_PERSPECTIVE_ANALYSIS.md,
  SPRINT_QUALITY_FOCUS.md, SWARM_ANALYSIS_REPORT.md, TAVERNA_COMPREHENSIVE_ANALYSIS.md,
  TAVERNA_EVOLUTION_ROADMAP.md, TAVERN_LIVING_ATMOSPHERE_ROADMAP.md,
  TECHNICAL_ARCHITECTURE_IMPROVEMENTS.md, THREE_JS_ENHANCEMENT_GUIDE.md,
  USER_EXPERIENCE_IMPROVEMENTS.md. All remain intact in the archived source repo.

## Per-game manifests

Each game keeps its own dependency manifest (`pyproject.toml`,
`package.json`, `requirements.txt`, Makefiles). There is no unified
environment; install per game as its README describes.