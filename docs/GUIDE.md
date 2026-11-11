# Installation and usage guide

How to install the `html-game-ui-design` skill in Claude and get good results from it. [Versión en español](GUIA.es.md).

## Contents

- [Which installation do I need?](#which-installation-do-i-need)
- [Claude apps: web, desktop and Cowork](#claude-apps-web-desktop-and-cowork)
- [Claude Code: install as a plugin](#claude-code-install-as-a-plugin)
- [Claude Code: install as a plain skill](#claude-code-install-as-a-plain-skill)
- [Other agents](#other-agents)
- [Using the skill](#using-the-skill)
- [Running the scanner yourself](#running-the-scanner-yourself)
- [Updating and removing](#updating-and-removing)
- [Troubleshooting](#troubleshooting)

## Which installation do I need?

| You use | Install this way |
|---|---|
| Claude in the browser, the desktop app, or Cowork | Upload the ZIP ([Claude apps](#claude-apps-web-desktop-and-cowork)) |
| Claude Code, and you want updates with one command | Plugin ([as a plugin](#claude-code-install-as-a-plugin)) |
| Claude Code, and you want to read or edit the skill files | Plain skill ([as a plain skill](#claude-code-install-as-a-plain-skill)) |
| Another agent that supports Agent Skills | Copy the folder ([other agents](#other-agents)) |

Skills enabled in your Claude account also load in recent versions of Claude Code when you sign in with the same account, so uploading the ZIP once can cover both.

## Claude apps: web, desktop and Cowork

**Before you start.** Skills need code execution to be turned on. On individual plans, open Settings > Capabilities and enable "Code execution and file creation". On Team and Enterprise plans, an owner controls this under Organization settings > Plugins & skills; if you cannot upload a skill, ask an owner to check that skills are enabled there.

**Steps**

1. Download [`dist/html-game-ui-design.zip`](../dist/html-game-ui-design.zip) from this repository. On its GitHub page, use the download button; do not unzip it.
2. In Claude, open **Customize > Skills** (`claude.ai/customize/skills`).
3. Click the **+** button, then **Create skill**.
4. Choose **Upload a skill** and select the ZIP.
5. The skill appears in your list. Make sure its toggle is on.

To share it with colleagues on a Team or Enterprise plan, open the skill's three-dot menu and choose **Share**.

**If you build the ZIP yourself**, the archive must contain the skill folder at its top level, and the folder name must match the skill's name:

```
html-game-ui-design.zip
└── html-game-ui-design/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

From the repository root:

```bash
# macOS and Linux
cd skills && zip -r ../html-game-ui-design.zip html-game-ui-design -x "*/evals/*" "*/__pycache__/*"
```

```powershell
# Windows 10 and later (PowerShell or cmd)
tar -a -c -f html-game-ui-design.zip -C skills html-game-ui-design
```

## Claude Code: install as a plugin

This repository is also a plugin marketplace with one plugin, `game-ui-anti-slop`. From a terminal:

```bash
claude plugin marketplace add angel-gmz/ui-anti-ai-slop
claude plugin install game-ui-anti-slop@ui-anti-ai-slop
```

Check that it is there:

```bash
claude plugin details game-ui-anti-slop
```

The component inventory should list one skill, `html-game-ui-design`. If Claude Code was already running, run `/reload-plugins` in that session or restart it.

You can do the same from inside a session with the `/plugin` command, which opens a panel for adding marketplaces and installing plugins.

Installed this way, the skill's full name is `/game-ui-anti-slop:html-game-ui-design`.

## Claude Code: install as a plain skill

Use this when you want the files where you can read and change them.

**For every project on your machine** (personal skill):

```bash
# macOS and Linux
git clone https://github.com/angel-gmz/ui-anti-ai-slop.git
mkdir -p ~/.claude/skills
cp -r ui-anti-ai-slop/skills/html-game-ui-design ~/.claude/skills/
```

```powershell
# Windows PowerShell
git clone https://github.com/angel-gmz/ui-anti-ai-slop.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ui-anti-ai-slop\skills\html-game-ui-design "$env:USERPROFILE\.claude\skills\"
```

**For one project, shared with its team** (project skill): copy the same folder into `.claude/skills/` at the root of the game's repository and commit it.

```
your-game/
└── .claude/
    └── skills/
        └── html-game-ui-design/
            └── SKILL.md
```

Claude Code notices new and changed skills in these folders during a session. If the `skills` folder itself did not exist when the session started, run `/reload-skills`.

Installed this way, the skill's name is `/html-game-ui-design`.

## Other agents

The skill follows the open [Agent Skills specification](https://agentskills.io/specification), which other coding agents also read. Copy `skills/html-game-ui-design` into the skills directory your agent uses; its documentation will say where that is. The scanner is plain Python and works anywhere.

## Using the skill

### It loads on its own

You do not need to name the skill. Claude reads its description and loads it when a request is about game interface work: a HUD, a menu, an inventory, a title screen, a card hand, or a complaint that a game's UI looks generic. In Claude Code you can also call it explicitly with the names given above, and in any Claude app you can simply say "use the html-game-ui-design skill".

### What to tell Claude

The skill's first step is reading the game, so the more of this you give, the more specific the result:

| Tell it | Example |
|---|---|
| The fantasy | "You are the apprentice of a lighthouse keeper on a storm-battered island in the 1890s" |
| The playfield | "Top-down, the boat stays near the centre, the track scrolls" |
| What the player does and watches | "Speed and turbo constantly, lap and position now and then" |
| Platform and input | "Desktop browser, keyboard or gamepad" or "phone, portrait, touch" |
| The stack | "Phaser 3 canvas at 1280x720 with HTML on top" or "plain HTML, no build step" |
| Existing art, if any | Attach a screenshot, sprites or a palette |
| What to deliver | "One HTML file with a stand-in background so I can see it working" |

A request that names only the widget ("make me a health bar") still works, but Claude then has to invent the world, and you will want to check the direction it picked.

### What you get back

1. **A direction**, in a few lines: what the interface is in the game's world, a real-world reference, material, shapes, typefaces, palette, icon style, motion, one signature detail, and the defaults it is refusing.
2. **The files**, built from that direction, with drawn SVG icons, constructed surfaces, feedback when values change, and keyboard and gamepad navigation.
3. **A short note** on what was built and anything you should test yourself, such as a physical gamepad.

Before delivering, Claude runs the bundled scanner and fixes what it finds.

### Steering the direction

The direction is the cheapest place to change course. If it is not right, reply before asking for anything else:

```
Less military. The stall owner is an old woman who paints her own signs.
```

```
Keep the direction but the reading typeface is too formal for kids.
```

```
Give me three different directions for this game in a few lines each and let me pick.
```

For a large project, ask for the three options up front.

### Fixing an existing interface

Give Claude the file and say what must not break:

```
Here is my HUD. It looks like a generic web page. Redo the visuals so it belongs
to the game (a walled city inside a giant beast's skeleton). Keep the ids and the
functions setHealth, setGold and selectTower working, the game loop calls them.
```

Claude scans the file, tells you what makes it look generic and why, proposes a direction, and rebuilds the visual layer while keeping your hooks.

### Example requests

```
Build the in-round screen for a deckbuilder about running a night-market food
stall: a hand of five cards, heat available this turn, draw and discard piles,
coins, reputation, customers waiting, and End Turn. One HTML file, mouse first,
keyboard too.
```

```
Two screens for a fractions game for 8 to 10 year olds, phone in portrait:
a level select with 12 levels in 3 worlds, and a level-complete screen with
stars and coins. One HTML file where I can switch between them.
```

```
Review the pause menu in src/ui/pause.html against the skill and tell me what
reads as generic. Don't change anything yet.
```

## Running the scanner yourself

The scanner works on any game UI source, with or without Claude. It needs Python 3.8 or later.

```bash
python slop_scan.py path/to/file-or-folder
```

| Option | Effect |
|---|---|
| `--json` | Machine-readable output |
| `--strict` | Exit with 1 on P1 findings as well as P0 |
| `--help` | Usage |

It reads `.html`, `.css`, `.scss`, `.js`, `.jsx`, `.ts`, `.tsx`, `.vue` and `.svelte` files and skips `node_modules`, `dist` and `build`. Each finding has a rule ID that is explained in `references/slop-tells.md`.

Findings come at three levels. P0 is recognised at a glance as generated or as a web app: emoji as icons, blurred glass panels, purple gradients, a generic or missing typeface, and focus removed with nothing in its place. P1 reads as generic when several appear together. P2 is missing polish.

When a flagged choice is deliberate, record it in the source so the scanner reports it as waived instead of failing:

```css
/* slop-ok: glass-panels  the HUD is a frosted visor, named in the direction */
```

A clean scan means no obvious defaults were found. It is not a judgement of quality.

## Updating and removing

**Claude apps.** Download the new ZIP and upload it again. To remove the skill, open it in Customize > Skills, turn it off, open the three-dot menu and choose Delete.

**Claude Code plugin.**

```bash
claude plugin marketplace update ui-anti-ai-slop            # fetch the latest listing
claude plugin update game-ui-anti-slop@ui-anti-ai-slop      # update the plugin

claude plugin uninstall game-ui-anti-slop@ui-anti-ai-slop   # remove the plugin
claude plugin marketplace remove ui-anti-ai-slop            # remove the marketplace and its plugins
```

**Claude Code plain skill.** Pull the repository and copy the folder again, or delete the `html-game-ui-design` folder from `~/.claude/skills/` or `.claude/skills/`.

## Troubleshooting

**The upload is rejected because the folder name does not match.** The ZIP must contain a folder named exactly `html-game-ui-design` at its top level, with `SKILL.md` directly inside it. Zipping the files without their folder, or zipping the whole repository, causes this.

**The upload is rejected because of the description.** The skill's description is written to the Agent Skills limit of 1,024 characters. If your Claude app asks for a shorter one, open `SKILL.md`, replace the `description:` line with the following, and zip the folder again:

```yaml
description: Designs and builds HTML/CSS/JS video game UI (HUDs, menus, inventories, dialogue, cards) that looks like part of the game, not a generic AI-made web app. Use for any browser game interface.
```

**There is no option to upload a skill.** Code execution or skills are turned off for your account or organization. See "Before you start" above.

**Claude does not use the skill.** Check that its toggle is on, then mention game UI plainly in the request or name the skill. Very short requests ("make a button") may not trigger any skill.

**The scanner does not run.** In the Claude apps it runs in Claude's own code execution environment and needs nothing from you. In Claude Code it needs Python 3.8 or later on your machine; on Windows the command may be `py` instead of `python`. Without Python, Claude falls back to checking against the catalog by hand.

**The result still looks generic.** Look at the direction Claude wrote. If it names a genre default (parchment and gold for fantasy, cyan holograms for sci-fi, a pixel font for anything retro), ask for a different one and give it something concrete about your world to work from.

**Fonts look wrong when opening the file offline.** The files load typefaces from Google Fonts and fall back to a chosen system font without a connection. Ask Claude to embed the fonts or to pick system-only typefaces if the game must work offline.
