# ui-anti-ai-slop

Agent Skills that make Claude design HTML game interfaces that look like part of the game, not like a generic AI-generated web app.

Ask a model for a game HUD and you usually get the same thing: translucent glass panels in the four corners, a system font, emoji for icons, a pill-shaped gradient bar for health, and one fade-in on everything. It works, and it belongs to no game. This repository holds a skill that replaces those defaults with the process a game UI artist follows.

It currently contains one skill, `html-game-ui-design`. More may follow.

> **Status: v0.1.0, early draft.** The structure is validated against the Agent Skills specification, the CSS techniques have been rendered and checked in a browser, and the scanner has been tested against generic and non-generic samples. The skill has not yet been benchmarked against a no-skill baseline. Test cases for that are included in the repo.

## What the skill does

`html-game-ui-design` covers HUDs, title and pause menus, settings, inventories, dialogue boxes, shops, card hands, level select, and win and game-over screens, for action, RPG, strategy and card, and casual and educational games. It is stack-agnostic: plain HTML/CSS/JS by default, an HTML overlay on a Phaser, PixiJS or Three.js canvas, or components in React, Vue or Svelte.

It gives Claude a seven-step workflow:

1. **Read the game.** Fantasy, playfield, verbs, platform and input, and any existing art.
2. **Commit to a direction.** A short written brief: what object the interface is inside the fiction, one real-world reference from outside games, material, shape language, type, palette, icon style, motion, a signature detail, and the defaults being refused.
3. **Lay out by attention.** Glance, read and explore tiers, with the playfield kept clear.
4. **Build from tokens and construction.** Surfaces with edges, faces and texture made from `clip-path`, `border-image`, layered shadows and inline SVG, with no image files needed.
5. **Make state changes felt.** Distinct states for every control and visible feedback for every value that changes.
6. **Wire input.** Keyboard, gamepad and touch, with focus drawn as a game cursor.
7. **Audit before delivering.** A bundled scanner plus four visual tests.

Steps 1 and 2 are where generic output is prevented. The rest is craft.

## Repository layout

```
ui-anti-ai-slop/
├── skills/
│   └── html-game-ui-design/
│       ├── SKILL.md                         the workflow
│       ├── references/
│       │   ├── visual-directions.md         finding a direction that fits one game
│       │   ├── genre-patterns.md            screens and components per genre
│       │   ├── craft-techniques.md          CSS and JS: frames, textures, bars, buttons, icons, motion
│       │   ├── input-and-accessibility.md   keyboard, gamepad, touch, readability, color
│       │   └── slop-tells.md                catalog of generic defaults, why each reads as generic, what to do instead
│       ├── scripts/
│       │   └── slop_scan.py                 dependency-free scanner for those defaults
│       └── evals/                           five test cases, one per genre plus a "fix this HUD" case
├── dist/
│   └── html-game-ui-design.zip              ready to upload in the Claude apps
├── docs/
│   ├── GUIDE.md                             installation and usage guide (English)
│   └── GUIA.es.md                           guía de instalación y uso (español)
└── .claude-plugin/                          plugin and marketplace manifests for Claude Code
```

## Install

Full instructions, prerequisites and troubleshooting are in the [installation and usage guide](docs/GUIDE.md) ([en español](docs/GUIA.es.md)). The short version:

**Claude apps (web, desktop, Cowork).** Download [`dist/html-game-ui-design.zip`](dist/html-game-ui-design.zip), then go to Customize > Skills, click "+", choose "Create skill", then "Upload a skill", and select the ZIP.

**Claude Code, as a plugin.**

```bash
claude plugin marketplace add angel-gmz/ui-anti-ai-slop
claude plugin install game-ui-anti-slop@ui-anti-ai-slop
```

**Claude Code, as a plain skill.** Copy `skills/html-game-ui-design` into `~/.claude/skills/` to use it everywhere, or into `.claude/skills/` inside a project to share it with that project's team.

**Other agents.** The skill follows the open [Agent Skills](https://agentskills.io) format, so any agent that reads `SKILL.md` folders can use it. Copy `skills/html-game-ui-design` into that agent's skills directory.

## Use

Once installed, Claude loads the skill on its own when a request is about game UI. Describe the game, not just the widget:

```
I'm making a top-down boat racing arcade game in Phaser 3 (1280x720 canvas).
I need the HUD as HTML over the canvas: speed, a turbo bar, race position, lap,
race time, and a pause menu. Keyboard or gamepad.
```

```
This is the HUD for my tower defense game, a walled city built inside the
skeleton of a giant beast. It works but it looks like a generic web page.
Redo it so it looks like part of the game. Don't break the JavaScript hooks.
```

Claude replies with the direction it chose in a few lines, then the files. If the direction is not what you had in mind, say so before it goes further; it is cheap to change at that point.

In Claude Code you can also call the skill by name: `/html-game-ui-design` when installed as a plain skill, or `/game-ui-anti-slop:html-game-ui-design` when installed as a plugin.

## The scanner

`slop_scan.py` can be used on its own, on any HTML, CSS or JS game UI. It needs Python 3.8 or later and nothing else.

```bash
python skills/html-game-ui-design/scripts/slop_scan.py path/to/ui
python skills/html-game-ui-design/scripts/slop_scan.py path/to/ui --json
python skills/html-game-ui-design/scripts/slop_scan.py path/to/ui --strict
```

It reports findings at three levels. P0 findings are recognised at a glance as generated or as a web app: emoji used as icons, blurred glass panels, purple gradients, a generic or missing typeface, and focus outlines removed with nothing in their place. P1 findings read as generic when several appear together, such as only rounded rectangles, glow on everything, `transition: all`, stock icon libraries and native form controls. P2 findings are missing polish, such as proportional numerals on counters and placeholder copy.

The exit code is 1 when any P0 finding remains, and with `--strict` when any P0 or P1 remains, so it can run in CI. A deliberate exception is recorded in the source with a comment, and is then reported as waived:

```css
/* slop-ok: glass-panels  the HUD is a frosted visor, named in the direction */
```

The checks are heuristics over source text. A clean scan means no obvious defaults were found. It does not mean the interface is good; the skill pairs the scanner with visual checks for that reason.

## Test cases

`skills/html-game-ui-design/evals/` holds five cases in the layout that `claude plugin eval` reads: a racing HUD, an RPG inventory and dialogue box, a deckbuilder hand, level screens for a children's fractions game, and a rewrite of a deliberately generic tower defense HUD. With Claude Code installed, run them from the skill folder. These are real, billed model runs.

```bash
cd skills/html-game-ui-design
claude plugin eval . --allow-tools Write,Edit,Bash --scaffold
```

## Contributing

Issues and pull requests are welcome. The most useful contributions are new tells for the catalog with the reason they read as generic and a concrete alternative, scanner rules with a sample that triggers them, and test cases from real projects. Keep `SKILL.md` under 500 lines and put detail in `references/`.

## Related work

This skill sits between two groups of existing skills that do not overlap. Game UI skills such as [`game-ui-frontend`](https://github.com/openai/plugins) and [`game-ui-ux`](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) cover layout and architecture but stay high-level on visual craft or target Godot and Unity. Anti-slop design skills such as [avoid-ai-design](https://github.com/funboy322/avoid-ai-design), [unslop-ui-skill](https://github.com/claudiusararu/unslop-ui-skill), [anti-slop-design-skills](https://github.com/jhuse25/anti-slop-design-skills) and [claude-design-skill](https://github.com/jiji262/claude-design-skill) target landing pages and web apps. The idea of a catalog of tells with a reason and a fix, and of committing to a named direction before writing code, comes from that second group.

## License

[MIT](LICENSE) © 2026 angel-gmz
