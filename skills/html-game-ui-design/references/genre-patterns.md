# Genre patterns

What each family of game asks of its interface: which screens exist, where attention goes, and where generic output usually goes wrong. Read the section for the game at hand; hybrids borrow from two.

## Contents

- Scaling policy
- Action, arcade and shooter
- RPG, adventure and narrative
- Strategy, management and cards
- Casual, puzzle and educational
- Screens every game has

## Scaling policy

Decide this before layout, because it changes every measurement.

- **Fixed stage, scaled to fit.** Design at one resolution (for example 1280x720 or 1920x1080, or a low resolution such as 320x180 for pixel art, scaled by whole numbers) and scale the whole stage uniformly, letterboxing the remainder. Positions and sizes are in stage pixels. Right for action games, pixel art, and anything where UI must stay locked to the scene.
- **Fluid layout.** Anchor clusters to edges with `position: absolute` or grid, size with `clamp()` and container units, and let dense panels reflow. Right for strategy and management screens, text-heavy RPG menus on desktop, and portrait mobile.
- **Hybrid.** Fixed stage for play, fluid for full-screen menus.

Whichever is chosen, respect safe areas (`env(safe-area-inset-*)`) and keep critical UI off the outer few percent of the screen. The stage-scaling snippet is in `craft-techniques.md`.

## Action, arcade and shooter

The player's eyes are on the playfield and must stay there. The HUD is read in peripheral vision.

**Attention budget.** Persistent HUD well under a fifth of the screen, usually far less. Nothing in the centre or along the path the action takes. One main cluster and at most one smaller one.

**Components**

- **Health and shields**: shape and length, not text. Segments or pips for small totals, a continuous bar with tick marks for large ones. Show damage with a flash, a trailing ghost segment that drains after a delay, and a change in the whole frame (vignette, color shift) when critical.
- **Ammo and charges**: individual pips or a magazine silhouette; a clear empty and reloading state.
- **Score and combo**: tabular numerals that roll up. A combo meter should escalate visibly (size, shake, color step) because it is a reward, and collapse abruptly when lost.
- **Cooldowns**: a radial or vertical wipe over the ability icon, with a distinct "ready" pulse once.
- **Boss bar, objective marker, damage direction**: appear only when relevant, enter with a strong transition, leave cleanly.
- **Minimap or radar**: a shape with a bezel that belongs to the direction, not a rounded square.
- **Contextual prompts**: the input glyph plus one verb, placed near the thing it refers to.

**Usual failures.** Text labels on every value ("HEALTH: 100/100"). Equal-weight panels in each corner. Idle animations on the HUD that compete with the game. Thin grey text over a moving background with no outline or plate. A pause menu that is a centred web modal with a blurred backdrop.

## RPG, adventure and narrative

The player alternates between the world and deliberate, text-heavy screens. Reading comfort and the sense that menus are places matter most.

**Components**

- **Dialogue box**: a speaker nameplate attached to the box in a way that suits the material, text revealed at reading pace with instant-complete on input, a clear "continue" indicator, and choices as a focusable list with the current choice unmistakable. Measure of 45 to 70 characters, generous line height, a real reading face. Leave room for the portrait or for the character on screen.
- **Inventory**: slots are sockets, compartments or hooks, not cards. Empty slots look empty and still belong to the object. Stack counts sit in a fixed corner with an outline. Rarity is carried by the frame shape or an emblem as well as color. Selection shows a detail pane with name, a line of flavour in the world's voice, stats, and comparison against what is equipped.
- **Equipment and character sheet**: a paper-doll or a list with clear slots; stats in aligned columns with tabular numerals; changes previewed with direction and amount.
- **Quest log or journal**: written in the character's or world's voice; active, completed and failed states distinguishable without color.
- **Shop**: buy and sell as two clearly different modes; price, owned count and affordability visible per row; confirmation that feels like a transaction.
- **Map**: a document from the world, with a legend and the player marker as the strongest element.
- **Exploration HUD**: minimal. Health, a quest pointer, a contextual prompt. It can fade when nothing changes.

**Usual failures.** Inventory as a grid of rounded cards with emoji. Dialogue as a chat bubble or a centred modal. Body text in a display face. Every menu the same dark translucent rectangle. Tabs that look like a website's navigation bar.

## Strategy, management and cards

Density is a feature. The player wants many numbers visible at once and compares them constantly, so the craft is in hierarchy, alignment and layered detail.

**Components**

- **Resource bar**: icon, amount in tabular numerals, and the rate of change. Group related resources; do not box each one. Flash and tick when an amount changes; warn before it runs out.
- **Selection and detail panel**: docked to an edge, consistent anatomy (portrait or icon, name, key stats, actions). Actions are a grid with hotkeys printed on them.
- **Build and production menus**: categories as tabs that belong to the material; each option shows cost, time and why it is unavailable.
- **Tooltips**: the workhorse. Appear fast, never cover the thing they describe, and layer: a one-line summary first, detail on hold or on a second level. Keywords inside a tooltip can open their own.
- **Tables and lists**: aligned columns, right-aligned numbers, sortable where it helps, zebra or rule lines from the direction.
- **Minimap, alerts, event log**: alerts are few, prioritised, and clickable to their source.
- **Turn structure**: whose turn, what phase, and the end-turn control as the single largest affordance, with a distinct state when actions remain.

**Cards**

- Anatomy in a fixed order so the eye learns it: cost (top corner), name, art window, type line, rules text, stats (bottom corners). Cost and stats sit in shapes distinct from each other.
- The frame carries type or faction through shape and pattern as well as color.
- Rules text is small and must be the most legible thing on the card: reading face, strong contrast, keywords in bold.
- **Hand**: a fan or overlapping row; the hovered or focused card rises, straightens and enlarges so that it is fully readable; neighbours make room. Playable cards are marked; unaffordable ones are subdued but readable.
- **Play**: dragging shows valid targets; release has anticipation and impact; the card goes somewhere (board, discard) visibly.
- Draw pile, discard pile and energy are objects on the table with counts.

**Usual failures.** A sidebar and top bar laid out like an admin console. Every number in its own rounded card. Cards as glass rectangles with a gradient border. Tooltips as default browser titles or generic dark bubbles. No hotkeys shown. Numbers that jitter because figures are proportional.

## Casual, puzzle and educational

Short sessions, often on a phone held in one hand, often by someone who does not think of themselves as a gamer. The interface must be obvious, tactile and generous with feedback.

**Layout.** Portrait first unless told otherwise. Primary actions in the lower half within thumb reach; status at the top. Touch targets at least 48px, primary actions considerably larger. Nothing depends on hover.

**Components**

- **Buttons**: physical. A face and a lip that compresses on press, with a clear shape hierarchy between the one primary action and everything else.
- **Level select**: a path, map, shelf or album that shows progress as a journey; locked, available, current and completed states readable at a glance; stars or medals as objects from the direction.
- **In-level HUD**: moves or time, goal progress, a pause control. Goals are shown as pictures with counts.
- **Win and lose screens**: a staged sequence, not a static panel. Result first, then rewards counted up one after another, then the next action. Losing is brief and points to retry.
- **Currency and rewards**: counters at a fixed place; gains travel from where they were earned to the counter, which pops on arrival.
- **Tutorial prompts**: show with a pointing hand or highlight; few words.

**Educational games**

- Feedback on answers is immediate, specific and never punishing: show what the right answer was and let the learner continue. Avoid red crosses with buzzers as the only response.
- Reading level and type: a highly legible face, large size, short sentences, unambiguous numerals and letterforms. Support read-aloud hooks where relevant.
- Progress is framed as growth (collection filling, path travelled), not as failure counts.
- Keep decoration from competing with the problem being solved; the question is the playfield.

**Usual failures.** Glossy gradient buttons with a white highlight band and rainbow palette. Emoji stars and trophies. A win screen that is a centred card with confetti and a single "Continue" button. Tiny close buttons in corners. A level select that is a grid of numbered rounded squares.

## Screens every game has

- **Title screen**: the game's name as lettering, not as a heading with gradient text; a small number of options; the world visible behind. The first screen sets the direction, so the signature belongs here.
- **Pause**: instant, clearly distinct from play, built from the same material as the rest. Resume is the default focus.
- **Settings**: grouped (audio, video, controls, accessibility), with controls drawn in the direction (a slider is a lever, a dial, a notched track), values shown, and immediate effect. This screen is where web habits return most easily: no stock toggles and select boxes.
- **Confirmations and errors**: short, in the world's voice, with the safe option focused.
- **Loading and transitions**: transitions belong to the fiction (a page turn, an iris, a shutter, a wipe in the direction of travel).
- **Game over and results**: say what happened, show what was earned, offer the next action with focus already on it.

Interface copy follows the same rule as visuals. Write in the world's voice where it adds character ("Cast off" for start, "Stow" for store), stay plain where clarity matters (settings, confirmations), and avoid the stock phrases: "Welcome to", "Embark on an epic adventure", "Get Started", exclamation marks on every line.
