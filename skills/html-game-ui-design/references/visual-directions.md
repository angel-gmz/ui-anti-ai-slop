# Visual directions

How to arrive at a direction that could only belong to one game. Nothing here is a style to copy; these are ways of finding one.

## Contents

- Finding the world source
- Outside references
- Material vocabularies
- Shape language
- Type
- Palette
- Icons
- Signature
- Worked examples of the reasoning

## Finding the world source

Ask what the interface *is* inside the fiction. Players accept UI most easily when it reads as an object the world would contain.

- What does the character carry, wear or sit in front of? A satchel, a wrist device, a ledger, a dashboard, a deck of cards.
- Who made it, with what tools, how long ago? Factory-stamped, hand-lettered, salvaged, ceremonial, a child's craft project.
- How has it aged? New and waxy, sun-faded, grease-marked, repaired with tape.

A stylised or abstract game still has an answer. A minimalist puzzle game's interface might be "museum wall labels" or "a printed board-game rulebook"; a neon arcade game's might be "the vacuum-fluorescent display of a 1980s car stereo", which is a far more specific thing than "neon".

## Outside references

Name one real-world, non-game reference. It supplies proportions, type habits and color relationships that no amount of genre knowledge will.

Places to look: transport signage and timetables, scientific instruments, packaging and labels, maps and nautical charts, textiles and embroidery, tickets and paper money, record sleeves, field guides, playing cards and tarot, circus and wrestling posters, aircraft placards, pharmacy and laboratory glassware, hand-painted shop signs, school exercise books, stamps and postmarks, control rooms, sports scoreboards, embroidered patches, ceramic tiles.

Take from the reference its *rules*: how it frames a number, how it separates sections, how many colors it allows itself. Do not paste its imagery.

## Material vocabularies

Each material implies edges, joins, light and wear. Pick one primary and at most one secondary; mixing five is as shapeless as having none.

| Material | Edges and joins | Surface | Wear |
|---|---|---|---|
| Paper and card | cut, torn, folded, pinned, taped, stitched binding | fibre grain, ruled lines, ink bleed | creases, stains, dog-ears |
| Painted metal | chamfers, rivets, welded seams, bolted plates | flat enamel with a hard highlight | chips to bare metal at corners |
| Wood | planks, pegs, carved recesses, rope lashing | grain along the length | rounded edges, scratches |
| Stone and ceramic | chiselled bevels, inlay, mortar lines | speckle, glaze | cracks, moss, worn carving |
| Cloth and leather | stitches, hems, grommets, patches | weave, embossing | fraying, fading |
| Glass and CRT | bezels, screws, curved face | scanlines, phosphor bloom, reflections | burn-in, flicker |
| Moulded plastic | parting lines, clipped panels, soft chamfers | flat color, slight gloss | stickers, scuffs |
| Print and ink | registration marks, halftone, overprint | flat spot colors, misregistration | none; it is new each time |
| Light itself (projected, holographic) | no edges; lines and brackets only | additive color, noise, parallax | interference, dropout |

"Light itself" is where most sci-fi lands by default. If choosing it, give it a source and a limitation (a monochrome amber projector with a low refresh rate) so it stops being generic cyan glow.

## Shape language

Decide the silhouette vocabulary and what each shape *means*, then hold to it.

- Assign shapes to roles: for example, chamfered plates for information, tabs for navigation, a pennant for the primary action, circles only for things on cooldown.
- Vary the corner treatment on purpose. One corner cut, three square is a shape. All four rounded by the same radius is a default.
- Let some elements have no container. A number with an icon and a hard outline, sitting directly on the scene, is often stronger than a boxed one.
- Use asymmetry. A panel with a tab on one side, a title that overhangs its frame, a bar that tapers.

## Type

Three jobs, usually two families:

- **Display**: titles, big numbers, button labels. Carries the character. Can be eccentric.
- **Reading**: dialogue, descriptions, tooltips. Must be comfortable at length; pick a real text face.
- **Numerals**: counters and stats. Tabular figures, strong shapes, distinguishable 0/O, 1/l, 5/6/8 at a glance.

Choose by what the world source would have used: a stamped label uses a condensed gothic, a ledger uses a slab or a script, a toy uses a rounded heavy sans, an instrument uses engraved caps. Then set it the way that source would: tracking, case, size contrast, alignment.

Faces that have become reflexes, and so need a reason when used: Inter, Roboto, Poppins, Montserrat and system-ui for anything; Press Start 2P for anything retro; Orbitron and Audiowide for anything sci-fi; Cinzel for anything fantasy; Bangers for anything comic. They are not banned. They are simply the first result, and a deliberate alternative almost always fits the specific game better.

A starting map of Google Fonts by character, to choose from and move beyond. Vary the choice between projects; do not settle on favourites.

- Stamped, industrial, signage: Saira Condensed, Barlow Condensed, Big Shoulders Display, Staatliches, Teko, Archivo Narrow
- Technical, instrument, terminal: Chakra Petch, IBM Plex Mono, Share Tech Mono, Space Mono, Major Mono Display
- Pixel and low-resolution: Silkscreen, Pixelify Sans, VT323, DotGothic16
- Book, ledger, old print: Spectral, EB Garamond, Cormorant, IM Fell English, Vollkorn, Alegreya, Fraunces
- Slab and poster: Alfa Slab One, Zilla Slab, Bitter, Rubik Mono One, Bungee
- Blackletter and carved: Grenze Gotisch, Pirata One, Almendra, Metamorphous, UnifrakturCook
- Typewriter and dossier: Special Elite, Courier Prime
- Rounded, toy, friendly: Fredoka, Baloo 2, Lilita One, Titan One, Sniglet
- Contemporary display: Syne, Unbounded, Archivo Black
- Maximum legibility, young or mixed readers: Atkinson Hyperlegible, Lexend, Andika

When web fonts cannot be loaded, do not fall back to the generic sans. Choose a system stack with character (`Georgia`, `"Iowan Old Style"`, `Rockwell`, `"Courier New"`, `Impact`, `"Trebuchet MS"`, `Copperplate`) and lean on case, tracking, weight contrast and an SVG-drawn title.

## Palette

Game palettes carry meaning, so assign roles before choosing hues.

- **Ground**: what panels are made of. Rarely pure black or the dark navy `#0f172a` family; tint it toward the world (bottle green, oxblood, wet slate, bone).
- **Ink**: text and line. Rarely pure white.
- **Signal**: one color reserved for "act here" and "this matters now". If everything glows, nothing does.
- **Gameplay semantics**: health, energy, currency, rarity tiers, teams, damage types. Fix these once and never reuse them decoratively. Pair every one with a second cue (shape, icon, pattern, position).

Take the palette from the outside reference or from the game's art, and keep it small: ground, ink, signal, two or three semantic colors and their darker edges. Check the UI against the scene; it has to separate from the playfield without fighting it, which usually means the UI is flatter and more limited in hue than the world behind it.

Lighting is part of the palette. Pick one light direction and apply it to every bevel, lip and shadow. Hard, offset shadows read as objects; large soft blurs read as web cards.

## Icons

Icons do more to make a UI feel authored than any other single element, and emoji or a stock line-icon set undo it faster than anything else.

- One style across the set: filled silhouettes, or chunky outline, or pixel, or stencil. Same grid, same stroke weight, same corner treatment.
- Draw for the smallest size they appear at. A 24px icon holds one idea and two or three shapes.
- Derive the drawing style from the material: stencil cut-outs for painted metal, ink stamps for paper, bitmap for low-resolution displays.
- Build from simple geometry. Circles, rectangles and polygons combined cleanly beat an ambitious freehand path. See `craft-techniques.md`.

## Signature

One detail carries the identity: the way the health bar is a row of fishing floats, a wax seal that stamps on confirm, a cursor that is the character's hand, a ticket-punch transition between screens. Choose one, make it excellent, and keep everything else quiet enough that it is noticed.

## Worked examples of the reasoning

These show the chain of thought from brief to direction. They are not templates; a second game in the same genre should end somewhere else.

**A top-down space shooter.** Default: cyan hologram HUD, Orbitron, glowing bars. Asking what the pilot actually sits in gives a cramped cockpit built by the lowest bidder. Outside reference: Soviet-era aircraft instrument panels. Result: cream and turquoise enamel plates with black engraved caps, analogue-style segmented gauges, one red warning lamp as the signal color, labels in a condensed gothic, hazard stripes only on the thing that can kill you. Signature: gauges with a needle that overshoots and settles.

**A cosy fishing-village RPG.** Default: parchment panels with a gold serif. Asking what the character carries gives a tackle box and a tide-table booklet. Outside reference: mid-century tinned-fish labels. Result: flat spot-color print in three inks with slight misregistration, tabbed card dividers for menus, item slots as compartments in a tackle tray, a rounded slab face for titles and a warm book face for dialogue. Signature: items are fish-tin labels.

**A deck-building strategy game about city planning.** Default: dark navy panels, neon accents, glass cards. World source: the planner's desk. Outside reference: 1970s transit maps and zoning plans. Result: off-white drafting paper, fine black rules, color only as flat zoning fills, cards as index cards with a punched corner and a typewritten code, resources shown as rubber-stamp tallies. Signature: playing a card stamps it onto the map.

**A times-tables game for seven-year-olds.** Default: candy gloss buttons, rainbow gradients, emoji stars. World source: the classroom craft table. Outside reference: cut-paper collage and sticker charts. Result: construction-paper shapes with visible scissor edges and a small drop shadow, answers on sticky notes, progress as a sticker chart, a heavy rounded face for numbers with very clear 6 and 9. Signature: stars are foil stickers that peel on with a slight curl.
