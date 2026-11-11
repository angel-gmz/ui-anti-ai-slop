---
name: html-game-ui-design
description: Designs and builds HTML/CSS/JS interfaces for video games (HUDs, title and main menus, pause and settings screens, inventories, dialogue boxes, shops, card hands, level select, win and game-over screens) so they look like part of the game instead of a generic AI-generated web app. Use whenever the user asks to create, restyle, review or fix UI for a browser or HTML5 game, whether plain DOM, an HTML overlay on a Phaser, PixiJS or Three.js canvas, or React, Vue or Svelte components. Use it when the user mentions a HUD, health bar, game menu, inventory, title screen or game-over screen, or complains that a game interface looks generic, like a dashboard, like a website, or like AI slop. Also use it when building a complete small HTML game, because its interface needs the same care. Covers action and arcade, RPG and narrative, strategy and card, and casual and educational games.
license: MIT
metadata:
  version: "0.1.0"
---

# HTML game UI design

Left to its defaults, a model builds game UI out of web-app habits: rounded cards with soft shadows, a blurred glass panel in each corner, a system font, emoji for icons, a pill-shaped gradient progress bar for health, and one fade-in on everything. It works, and it belongs to no game. Players read it instantly as a dashboard with a game behind it.

Game UI artists start somewhere else. They decide what the interface is *made of* in the game's world, they give the screen to the playfield, and they make every change of state felt. This skill is that process, plus a catalog of the defaults to refuse.

The same applies whatever the stack. Write plain HTML/CSS/JS unless the project already uses a framework; everything here maps directly to components.

## Workflow

Follow these in order. Steps 1 and 2 are thinking, and they decide whether the result is generic; do not skip them to get to code sooner.

### 1. Read the game

Before any markup, pin down what is already true. Take it from the user's brief and any existing code or art; ask only if something that changes the design is missing.

- **Fantasy**: who the player is and what the world is made of.
- **Playfield and camera**: where the action happens on screen, and which regions must stay clear.
- **Verbs and rhythm**: what the player does, and how often they look at each piece of information. Something read ten times a second is designed differently from something read once a session.
- **Context**: platform, input (mouse, touch, keyboard, gamepad), viewing distance, orientation.
- **Existing art**: if the game has sprites, a palette or a logo, the UI direction is *extracted* from them (sample the colors, match the pixel density and line weight), not invented beside them.

### 2. Commit to a direction

Write the direction down before building, in this form, and show it to the user in the reply so they can redirect early:

```
DIRECTION: <two or three word name>
World source:  what object this interface is in the fiction (a field journal, a cockpit panel, a toy box lid)
Outside ref:   one real-world, non-game reference (a 1960s rail timetable, hand-painted fruit crate labels)
Material:      what surfaces are made of and how pieces are joined (riveted tin, stitched canvas, cut paper)
Shape:         the silhouette vocabulary (chamfered plates, torn edges, tabs, pennants); never only rounded rectangles
Type:          display face / reading face / numerals, and why each fits
Palette:       ground, ink, one signal color, plus the gameplay-meaning colors (rarity, teams, damage)
Icons:         drawing style, weight, grid
Motion:        the character of movement (snappy and mechanical, soft and springy, stepped like old hardware)
Signature:     the one detail a player would remember
Refusing:      two or three defaults deliberately left out
```

Two things make a direction specific:

- **Pull the outside reference from beyond games.** A direction built only from "fantasy RPG UI" reproduces the average of every fantasy RPG. A direction built from "a herbalist's pressed-flower ledger" cannot be average.
- **Distrust the genre default.** Parchment with a gold serif for fantasy, cyan holograms for sci-fi, a chunky pixel font for anything retro, candy gloss for casual: these are the first idea everyone has, which makes them the second layer of generic. Use one only when the brief asks for it, and then push it somewhere particular. The useful question is: *what would this world actually build its instruments and documents from?*

If the user already gave art direction, follow it and fill in only the gaps. For a large or open-ended project, offer two or three short directions and let the user pick; for a small request, choose one, state it, and build.

Read `references/visual-directions.md` when the direction does not come easily or when the first idea is a genre default.

### 3. Lay out by attention

Space on a game screen is paid for in the player's attention, so allocate it by how often each thing is read.

- **Glance tier** (many times a minute: health, ammo, timer, resources): at the edges and corners, readable by shape, length and position without reading text. Prefer five pips to "5/5".
- **Read tier** (now and then: objectives, prompts, dialogue): appears when relevant, then gets out of the way.
- **Explore tier** (deliberate: inventory, map, settings): its own screen or drawer, entered on purpose, where density is welcome.

Keep the playfield clear. During active play, persistent HUD should cover a small part of the screen, and nothing sits where the action is. Group related values into one or two clusters with unequal weight; four equal boxes in four corners is a dashboard layout.

Decide the scaling policy explicitly: a fixed-resolution stage scaled to fit (best for action games and pixel art) or a fluid layout (best for dense strategy screens and portrait mobile). Read `references/genre-patterns.md` for the screens, components and attention budget of the genre at hand.

### 4. Build from tokens and construction

Put the direction into CSS custom properties first (colors by role, type, edge width, corner cut, timing), then build components from them, so the whole interface changes together.

Construct surfaces instead of styling boxes. A panel has an edge, a face, a way its corners are finished and a relationship to light. Use `clip-path`, `border-image` with an inline SVG, layered `box-shadow`, masks, pseudo-elements and SVG noise to get there without image files. Draw icons as inline SVG silhouettes in one consistent style. Read `references/craft-techniques.md` for working snippets of all of these: frames, textures, bars, numerals, buttons, icons and stage scaling.

Give the UI something to sit on. If there is no real game yet, draw a stand-in playfield (a simple canvas or CSS scene in the game's palette). A HUD over an empty dark rectangle cannot be judged and always looks like a dashboard.

Fill it with content from the fiction: real item names, plausible numbers, in-world wording. "Rusty Harpoon, 14 dmg" teaches the eye more than "Item 1".

### 5. Make state changes felt

A game communicates through change. For each interactive element, design rest, hover, focus, pressed, selected and disabled as distinct states. For each value, design what happens when it changes: the health bar flashes and leaves a trailing ghost, the counter pops and rolls, the picked-up item travels to its slot.

Keep the resting HUD still, spend motion on change, and vary timing and easing by meaning instead of applying one transition everywhere. Respect `prefers-reduced-motion` by keeping the state change and removing the travel. Timings and patterns are in `references/craft-techniques.md`.

### 6. Wire input

Menus are operated with arrows, Enter and Escape, and with a gamepad when the game supports one; many players never touch the mouse. Focus is drawn as part of the fiction (a cursor, brackets, a lifted plate), never removed. Touch targets are sized for thumbs. Meaning is never carried by color alone. Read `references/input-and-accessibility.md` before building any menu, and for the focus-navigation and gamepad snippets.

### 7. Audit before delivering

Run the scanner, which is bundled in this skill's folder, on the files written:

```bash
python scripts/slop_scan.py <file-or-folder>
```

Fix every P0 finding and every P1 finding that was not a deliberate choice named in the direction. When the direction really does call for something the scanner flags, record it in the source with a `slop-ok: <rule-id> <reason>` comment so it is reported as waived; needing more than one or two waivers means the direction is a default in disguise. If Python is not available, walk through `references/slop-tells.md` by hand instead.

The scanner only catches defaults that can be seen in code, so a clean scan means "no obvious defaults", not "good". Then check the result by eye, with a screenshot if a browser tool is available:

- **Swap test**: if another game's title were dropped in, would anything look wrong? If not, the UI has no identity yet.
- **Dashboard test**: hide the playfield. If what remains could be an analytics app, the surfaces and layout are still web habits.
- **Squint test**: blurred or at thumbnail size, are the glance-tier values still distinguishable by shape and position?
- **Direction test**: is every line of the written direction visible on screen, including the signature?

Read `references/slop-tells.md` for the full catalog, with the reason each tell reads as generic and what to do instead.

## Reviewing or fixing an existing UI

When the user brings UI that looks generic: run the scanner, read the code, and list what was found by severity with the reason for each. Then write a direction (step 2) from the game's fiction and existing art, confirm it with the user if the change is large, and rebuild surfaces, type, icons and motion from it. Keep the game's logic and the element hooks it depends on (ids, data attributes, event handlers) intact; the visual layer is what changes.

## Delivering

- For a standalone piece, deliver one self-contained HTML file with inline CSS and JS. Web fonts may come from Google Fonts with a deliberate fallback stack; never rely on a font that is not loaded.
- For an existing project, follow its structure and framework, and keep UI in the DOM layer above the canvas unless it must live in the scene.
- State the direction in the reply in a few lines, then say what was built and anything the user should check (for example, a gamepad). Do not narrate the audit.

## Reference files

| File | Read it when |
|---|---|
| `references/visual-directions.md` | Choosing or sharpening a direction; material vocabularies; type pairing |
| `references/genre-patterns.md` | Laying out screens for action, RPG, strategy and card, or casual and educational games |
| `references/craft-techniques.md` | Writing the CSS and JS: frames, textures, bars, numerals, buttons, icons, motion, scaling |
| `references/input-and-accessibility.md` | Building any menu; keyboard, gamepad and touch; readability and color |
| `references/slop-tells.md` | Auditing; understanding a scanner finding; reviewing someone else's UI |
