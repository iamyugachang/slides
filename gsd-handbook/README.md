# GSD × SDLC Handbook

繁體中文互動手冊，以原創遊戲化習慣 app「Habit Quest」為貫穿案例：每日任務、XP、角色升級、裝備、劇情。

- Published path: https://iamyugachang.github.io/slides/gsd-handbook/
- Source content: `content.py`; deterministic static generator: `build.py`
- Build: `python3 gsd-handbook/build.py` from repository root
- Preview: `python3 -m http.server 8765 --directory .`
- Static checks: Python compilation, JavaScript syntax, generated local links and fragment IDs.
- Browser visual/interaction checks were not run: the user requested direct publication without preview.
- No runtime dependencies, third-party scripts, external fonts, or analytics.
- Progress and workbook answers remain in localStorage; export is a local Markdown download.

## Scope

The deliverable is a handbook, not the complete Habit Quest application. Product rules, roadmap, interview answers and acceptance tests are explicitly educational examples. The interactive XP widget is an isolated rule illustration.

## Evidence baseline

Checked 2026-09-22: npm `@opengsd/gsd-core@1.14.0`, GitHub release `v1.14.0`, tagged command/configuration docs, and actual installer output in an isolated temporary folder. npm engines require Node >=24 and npm >=10 despite some prose docs saying Node 18/22. Full Codex install emits skills, agent TOMLs and hook/config files. An unrelated global defaults write was blocked by this environment; core local installation succeeded. A full application lifecycle was not run to validate the handbook.

Community reports are attributed anecdotes about the broader GSD family, not controlled benchmarks or proof about this exact fork/version. Links and verification limits are shown in the site and `sources.json`.

## Design

Cool blue field guide: ink #182643, cobalt #2957d5, cloud #f1f5fc, white #ffffff, slate #53627c, orange #a65318. System Chinese sans body, serif restrained chapter display, monospace command labels. Persistent chapter rail; each chapter has a purpose, action, example and exit check. Signature: a progression path that connects product XP to learning milestones without turning the handbook into a game dashboard.

## Deployment

Existing GitHub Pages source is `main:/`; no changes to repository-level Pages settings are needed. Generated static files are committed. No private paths, tokens or personal runtime settings are published.
