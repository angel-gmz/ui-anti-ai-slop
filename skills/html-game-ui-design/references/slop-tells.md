# Slop tells

The defaults that make a game interface read as generated, why each one does, and what to do instead. Use it to audit work before delivering, to explain a scanner finding, and to review UI someone else made.

A tell is not a banned technique. It is a choice that appears when nobody chose. Any of these can be right for a particular game if the written direction calls for it; what makes it a tell is arriving at it by default.

## Contents

- Severity
- Recording a deliberate exception
- Surfaces and shape
- Type
- Color and light
- Icons and imagery
- Layout
- Components
- Motion
- Input and behaviour
- Copy
- Second-order tells: genre defaults

## Severity

- **P0**: recognised at a glance as generated or as a web app. Fix before delivering.
- **P1**: reads as generic when several appear together. Fix unless the direction names it as a choice.
- **P2**: polish. A missing detail that authored UI usually has.

IDs in `code` are checked by `scripts/slop_scan.py`. Rows without an ID can only be judged by eye.

## Recording a deliberate exception

When the direction really does call for something the scanner flags, say so in the file, and the scanner reports it as waived instead of failing:

```css
/* slop-ok: glass-panels  the HUD is a frosted visor, named in the direction */
```

Use this rarely. Needing more than one or two waivers usually means the direction is a default in disguise.

## Surfaces and shape

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `glass-panels` (P0): translucent panels with `backdrop-filter: blur` | The signature look of generated dashboards; it has no material and blurs the playfield the player needs to see | Opaque or cut-out surfaces built from the direction's material; over the scene, use plates or outlined text |
| `one-shape` (P1): every surface is a rounded rectangle; no `clip-path`, `border-image` or mask anywhere | One radius everywhere is the browser's shape, not the game's; nothing signals its role by silhouette | A shape vocabulary: chamfers, tabs, notches, pennants, torn or stitched edges, assigned by role |
| `pill-everything` (P1): fully rounded pills for bars, buttons and tags | The stock "modern app" shape | Shapes from the material; pills only if the world is made of capsules |
| `soft-web-shadow` (P1): large, blurred, low-opacity drop shadows | Floating-card elevation is a web metaphor | Hard, offset shadows and lips from one light direction, or no shadow |
| Panels of flat translucent black or navy with a 1px light border | A div with a background, not an object | Give surfaces an edge, a face, a corner finish and a little texture |
| Everything boxed | Web layouts box content; game HUDs often sit directly on the scene | Unboxed icon plus outlined numeral for glance values; boxes for explore-tier screens |
| Identical padding and gap on every element | Reads as a component library | Vary density by tier: tight for glance, roomy for reading |

## Type

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `default-font` (P0): Inter, Roboto, Arial, Helvetica, system-ui or bare `sans-serif` as the first family, or no font chosen | The typeface of every web app; it carries no world | A display face and a reading face chosen from the world source, loaded explicitly |
| `reflex-genre-font` (P1): Press Start 2P, Orbitron, Audiowide, Cinzel, Bangers, Poppins, Montserrat | The first search result for "retro", "sci-fi", "fantasy", "comic", "friendly" | A face that fits this specific game; see the type map in `visual-directions.md` |
| `gradient-text` (P1): titles filled with a gradient via `background-clip: text` | The generated-landing-page headline | Lettering with construction: outline, extrusion, emblem, texture, or drawn SVG |
| `no-tabular-nums` (P2): changing numbers in proportional figures | Counters jitter sideways as they tick | `font-variant-numeric: tabular-nums` on every value that changes |
| One family, one weight, sizes close together | No hierarchy; everything speaks at the same volume | Strong size and weight contrast between display and reading text |
| Display face used for paragraphs | Dialogue and descriptions become tiring | A real reading face for anything longer than a label |
| Thin, mid-grey secondary text | A web habit that vanishes on a moving scene or a TV | Dim by hue and size, keep contrast; outline text over the scene |

## Color and light

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `purple-gradient` (P0): gradients running through purple, violet or indigo to blue or pink | The single most recognised generated-UI look | Flat spot colors or a gradient with a physical cause (a sky, a heated edge, a gauge range) |
| `glow-spam` (P1): blurred zero-offset glows on text, borders and bars throughout | "Neon" as a substitute for a direction; when everything glows, nothing is emphasised | Reserve glow for one emissive thing; build the rest from solid edges |
| `saas-ground` (P2): the dark slate and navy family (`#0f172a`, `#1e293b`, `#111827`) as the base | The default dark theme of web frameworks | A ground tinted toward the world: bottle green, oxblood, wet slate, bone, ink blue |
| Cyan and magenta accents on near-black | The default "gamer" or "cyberpunk" palette | A palette taken from the outside reference or the game's art |
| Rainbow of saturated accent colors with equal weight | No signal color; nothing tells the player where to act | One signal color, a few semantic colors with fixed meanings |
| Light from everywhere: highlights on top of one element, bottom of another | Surfaces do not share a world | One light direction for every bevel, lip and shadow |
| Meaning carried by color only (rarity, teams, good or bad) | Unreadable for many players, and looks unfinished | Pair color with shape, emblem, pattern or position |

## Icons and imagery

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `emoji-icons` (P0): emoji for hearts, coins, swords, stars, settings | Different on every platform, off-palette, and the fastest giveaway of all | Inline SVG silhouettes in one drawn style |
| `stock-icon-set` (P1): Lucide, Heroicons, Feather, Font Awesome, Material icons | Thin, even-stroke app icons bring a productivity tool's voice | A small custom set built from simple geometry in the direction's style |
| Icons in mixed styles: some outlined, some filled, some detailed | Looks assembled from sources | One grid, one weight, one corner treatment |
| Text glyphs as icons (stars, hearts, arrows, check marks typed as characters) | Font-dependent and uncontrollable | Draw them |
| Empty colored squares or initials standing in for item art | Placeholder left in | Simple silhouettes per item type; a consistent "unknown item" mark |
| Decorative gradient blobs, particle starfields or grid floors behind menus | Generic atmosphere unrelated to the game | The game's own scene, or a surface from the world source |

## Layout

| Tell | Why it reads as generic | Instead |
|---|---|---|
| Four equal panels in four corners | A dashboard; no hierarchy of attention | One main cluster, at most one smaller; place by how often things are read |
| Persistent header bar, sidebar and footer | App chrome around a viewport | Edge-anchored clusters; full-width bars only where the genre needs them (strategy resource bars) |
| HUD covering the centre or the action's path | The interface competes with the game | Keep the playfield clear; move detail to explore-tier screens |
| Centred column of content with a max width | A web page | Compose against the scene; anchor to edges, overlap, hang elements off frames |
| Pause, inventory and dialogue as centred modals over a dimmed, blurred page | The web's modal pattern | Screens built from the world source that enter from an edge or replace the view |
| Responsive reflow that rearranges the HUD at breakpoints | Players learn positions; moving them breaks that | A scaled fixed stage, or fluid anchoring that keeps relative positions |
| UI over an empty dark rectangle | Nothing to protect or contrast with, so it becomes a dashboard | A stand-in playfield in the game's palette |

## Components

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `native-controls` (P1): `<progress>`, `<select>` and other stock form controls | The browser's widgets, styled by the operating system | Meters, steppers, dials and sliders drawn in the direction, with the same semantics via ARIA |
| `labelled-values` (P2): "Health: 100/100", "Score: 0" | Text where shape would be read faster | Bar length, pips, icon plus numeral; exact numbers only where the player needs them |
| Health as a rounded bar with a red-to-green gradient | The SaaS progress bar | Segments, pips, a gauge, a container that drains; a ghost trail on damage; a distinct critical state |
| Inventory as a grid of rounded cards | A product listing | Sockets, compartments, hooks or pages with clear empty slots and a detail pane |
| Rarity as a colored 1px border or glow | The lowest-effort signal, and color-only | Frame shape, emblem or pip count as well as color |
| Dialogue as a chat bubble or centred card | Messaging-app pattern | A box in the material with an attached nameplate, paced text and a continue mark |
| Settings as a web form with stock toggles | The place web habits return | Controls as objects: levers, notched tracks, dials, with values shown |
| Buttons that all look alike | No hierarchy of action | One primary shape; quieter forms for the rest; lists without boxes |
| Win screen as a centred card with confetti and one button | The generated celebration | A staged sequence: result, rewards counted in one by one, then the next action |
| Tooltips as small dark rounded bubbles | Library default | Tooltips with the panel's material, a clear anatomy and layered detail |
| Toast notifications sliding in at a corner | App notifications | Events shown in the world's manner: a stamped notice, a radio line, a log entry |

## Motion

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `transition-all` (P1): `transition: all` | Nobody decided what moves; layout properties animate by accident | Name the properties and give each a duration that fits its meaning |
| `card-hover-lift` (P1): hover that raises an element with `translateY(-Npx)` and a bigger shadow | The web card hover | Hover and focus as a game cursor state; press as a physical compression |
| `uniform-easing` (P2): only `ease` or `ease-in-out`, no custom curves or steps | Everything moves with the same soft feel | Easing by material: overshoot for springy, stepped for mechanical or retro, quick-out for paper |
| `no-reduced-motion` (P1): animation with no `prefers-reduced-motion` handling | Unfinished, and unusable for some players | Keep state changes, remove travel and shake |
| Fade-in on everything at page load | Scroll-reveal habits | Entrances from an anchor edge with character; most of the HUD simply present |
| Values that change with no reaction | The UI displays state but does not communicate change | Flash, pop, ghost trail, roll, travel |
| Idle animations on resting HUD elements | Competes with the game for the eye | Still at rest; movement means something changed |
| Smooth sub-pixel tweens in a pixel-art game | Breaks the resolution the art established | Stepped timing and whole-pixel moves |

## Input and behaviour

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `focus-removed` (P0): `outline: none` with no focus style anywhere | Keyboard and gamepad players cannot see where they are | A focus state drawn as the game's cursor |
| `no-focus-style` (P1): buttons exist but nothing styles focus | Mouse-only thinking | Same as above; focus and hover share a look |
| `div-buttons` (P1): click handlers on `div` or `span` | Not focusable, not activatable from keys or pad | `<button>` elements |
| `selectable-stage` (P2): no `user-select: none` on the game surface | Dragging selects text and images like a document | Disable selection and dragging on the stage |
| Menus that cannot be driven with arrows, Enter and Escape | Nobody played it | Spatial navigation and a screen stack |
| Hover-only tooltips and actions | Fails on touch and pad | Focus and tap equivalents |
| Disabled shown only by lowering opacity | Ambiguous over a varied scene | A distinct flattened, drained state |
| Small touch targets, close buttons in corners | Desktop habits on a phone | 48px minimum; primary actions in thumb reach |

## Copy

| Tell | Why it reads as generic | Instead |
|---|---|---|
| `stock-copy` (P2): "Welcome to", "Get Started", "Embark on an epic adventure", "Unleash", lorem ipsum | Marketing boilerplate | The world's voice for flavour, plain words for function |
| `stock-copy` (P2): "Player 1", "Item 1", "Epic Sword", "Level 1" as content | Placeholder data | Names, numbers and descriptions that belong to this game |
| Exclamation marks and emoji in labels | Forced excitement | Let motion and sound carry excitement |
| Title Case web labels ("View Details", "Learn More") | Website calls to action | Game verbs: Equip, Stow, Cast off, Retry |

## Second-order tells: genre defaults

Once the first layer is removed, the next default is the genre's own cliche. The scanner cannot see these; the direction step exists to catch them.

| Genre | The default | What to ask |
|---|---|---|
| Fantasy | Parchment, gold trim, a Roman-capital serif, ornate corners | Which culture, craft and century made these objects? Carved bone, dyed felt, enamel, bark? |
| Sci-fi | Cyan lines on black, hexagons, angular brackets, thin caps | Who manufactures this equipment, and how cheap, old or military is it? |
| Retro and pixel | One blocky pixel font, white-bordered black boxes | Which machine and year? Its real palette, resolution and character set? |
| Horror | Red on black, distressed type, dripping edges | What ordinary object becomes unsettling here? Hospital forms, a child's drawing, tape labels? |
| Casual | Candy gloss, bubbly white-outlined type, sunbursts | What is the toy made of? Felt, cardboard, clay, stickers, enamel pins? |
| Cyberpunk | Magenta and cyan neon, glitch effects | What do advertising, bureaucracy and street repair look like in this city? |
| Educational | Primary colors, cartoon mascots, stars | What does the subject itself look like? Maps for geography, instruments for science, craft paper for arithmetic? |
| Strategy | Dark steel panels with blue highlights | What does the commander, planner or merchant actually work at? A sand table, a ledger, a drafting board? |
