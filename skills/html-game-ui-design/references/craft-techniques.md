# Craft techniques

Working CSS and JS for building game surfaces without image files. The snippets show *technique*. Their colors, sizes and shapes are placeholders: replace every value from the written direction, and do not ship a snippet's look as the design.

## Contents

- Stage and layering
- Tokens
- Panels and frames
- Textures
- Text and numerals
- Bars, pips and meters
- Buttons
- Icons
- Motion and feedback
- Screen flow and sound hooks

## Stage and layering

A fixed-resolution stage scaled to fit, with the game canvas below and the UI above:

```html
<div class="stage">
  <canvas id="game" width="1280" height="720"></canvas>
  <div class="ui"><!-- HUD and menus --></div>
</div>
```

```css
html, body { margin: 0; height: 100%; overflow: hidden; background: #000; }
.stage { position: absolute; left: 50%; top: 50%; width: 1280px; height: 720px;
         transform-origin: center; user-select: none; -webkit-user-select: none; touch-action: none; }
.stage canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
.ui { position: absolute; inset: 0; pointer-events: none; }
.ui > * { pointer-events: auto; }           /* only real controls take input */
```

```js
const stage = document.querySelector('.stage');
function fit() {
  const s = Math.min(innerWidth / 1280, innerHeight / 720);
  stage.style.transform = `translate(-50%, -50%) scale(${s})`;
}
addEventListener('resize', fit); fit();
```

For pixel art, design at the low resolution, scale by whole numbers only (`Math.max(1, Math.floor(s))`), and set `image-rendering: pixelated` on canvases and images. For a fluid layout skip the scaling, anchor clusters to edges, and pad them with `max(16px, env(safe-area-inset-left))` and its siblings.

Things that make a page stop feeling like a web page: no text selection, no image dragging (`draggable="false"`), no scrollbars, no context menu on the stage, and no default cursor over the game if the direction calls for a custom one (`cursor: url(...) x y, auto`).

## Tokens

Put the direction into custom properties first. Name by role, not by value.

```css
:root {
  --ground: #233029;  --ground-edge: #101a14;
  --ink: #efe6cf;     --ink-dim: #a99f84;
  --signal: #e8572a;
  --hp: #c8402f;  --energy: #3f8fb0;  --coin: #d9a520;
  --edge: 3px;  --cut: 12px;
  --font-display: "Saira Condensed", Impact, sans-serif;
  --font-read: "Spectral", Georgia, serif;
  --t-press: 60ms;  --t-pop: 160ms;  --t-open: 200ms;
  --ease-snap: cubic-bezier(.2, 1.5, .4, 1);   /* overshoots, then settles */
  --ease-out: cubic-bezier(.2, .8, .2, 1);
}
```

## Panels and frames

**Chamfered plate with a true edge.** `clip-path` also clips borders and box-shadows, so build the edge from two layers and put the drop shadow on a wrapper with `filter`.

```css
.plate-wrap { filter: drop-shadow(0 4px 0 rgba(0,0,0,.45)); }      /* hard, offset: reads as an object */
.plate { position: relative; isolation: isolate; padding: 14px 18px; color: var(--ink);
  background: var(--ground-edge);
  clip-path: polygon(var(--cut) 0, 100% 0, 100% calc(100% - var(--cut)),
                     calc(100% - var(--cut)) 100%, 0 100%, 0 var(--cut)); }
.plate::before { content: ""; position: absolute; inset: var(--edge); z-index: -1;
  --c: calc(var(--cut) - var(--edge) * .6);                          /* keeps the diagonal edge the same width */
  background: var(--ground);
  clip-path: polygon(var(--c) 0, 100% 0, 100% calc(100% - var(--c)),
                     calc(100% - var(--c)) 100%, 0 100%, 0 var(--c)); }
```

Change which corners are cut, add a notch or a tab by adding polygon points, and vary the shape by role.

**Bevel and lip with layered shadows.** Inset shadows with zero blur draw hard highlights and shade from one light direction.

```css
.slab { background: var(--ground); border: var(--edge) solid var(--ground-edge);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.14),     /* top highlight */
              inset 0 -3px 0 rgba(0,0,0,.28),          /* bottom shade */
              0 4px 0 var(--ground-edge); }            /* thickness below */
```

**Nine-slice frame from an inline SVG.** `border-image` stretches the edges and keeps the corners, exactly like a nine-slice sprite. Draw the frame in a small SVG and URL-encode it (`#` becomes `%23`, `<` `%3C`, `>` `%3E`).

```css
.frame { border: 12px solid transparent; background: var(--ground) padding-box;
  border-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='36' height='36'%3E%3Crect width='36' height='36' fill='%23233029'/%3E%3Crect x='1.5' y='1.5' width='33' height='33' fill='none' stroke='%23c9a45c' stroke-width='3'/%3E%3Crect x='6.5' y='6.5' width='23' height='23' fill='none' stroke='%235a4320'/%3E%3Cpath d='M0 0h9v9H0zM27 0h9v9h-9zM0 27h9v9H0zM27 27h9v9h-9z' fill='%23c9a45c'/%3E%3C/svg%3E") 12 / 12px stretch; }
```

**Hardware and ornament with pseudo-elements.** Rivets, pins, corner brackets and stitches are small repeated marks:

```css
.riveted { background-image: radial-gradient(circle at 10px 10px, #0006 0 2.5px, transparent 3px),
                             radial-gradient(circle at calc(100% - 10px) 10px, #0006 0 2.5px, transparent 3px); }
.stitched { outline: 2px dashed var(--ink-dim); outline-offset: -8px; }
.bracketed::before, .bracketed::after { content: ""; position: absolute; width: 14px; height: 14px;
  border: 3px solid var(--signal); }
.bracketed::before { left: -4px; top: -4px; border-right: 0; border-bottom: 0; }
.bracketed::after { right: -4px; bottom: -4px; border-left: 0; border-top: 0; }
```

**Irregular edges** (torn paper, cut card): a `clip-path: polygon()` with slightly uneven points along one edge, or a `mask` using a repeating SVG zigzag.

## Textures

Flat fills read as "div". A little grain, weave or scanline, kept subtle, gives a surface.

```css
/* grain or paper fibre: SVG turbulence as a tiling overlay */
.grain::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .35; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }

/* scanlines for a display surface */
.scanlines { background-image: repeating-linear-gradient(0deg, rgba(0,0,0,.22) 0 1px, transparent 1px 3px); }

/* hatching, hazard stripes, ruled paper: repeating gradients */
.hazard { background-image: repeating-linear-gradient(-45deg, #1b1b1b 0 10px, #e2b100 10px 20px); }
.ruled  { background-image: repeating-linear-gradient(0deg, transparent 0 27px, rgba(40,60,120,.25) 27px 28px); }

/* halftone dots */
.halftone { background-image: radial-gradient(circle, rgba(0,0,0,.3) 1.2px, transparent 1.6px); background-size: 6px 6px; }
```

Lower `baseFrequency` (around `.02` to `.08`) gives blotches and stains; stretch it on one axis (`baseFrequency='.02 .6'`) for wood grain or brushed metal. Put texture on a pseudo-element so text stays crisp.

## Text and numerals

```css
.num   { font-family: var(--font-display); font-variant-numeric: tabular-nums; }   /* digits keep their width, so counters do not jitter */
.label { font-family: var(--font-display); text-transform: uppercase; letter-spacing: .12em; font-size: 12px; }

/* text that must read over any background: a real outline, not a blurred glow */
.outlined { color: var(--ink); -webkit-text-stroke: 5px #14100a; paint-order: stroke fill; }

/* fallback or pixel style: hard offset shadows */
.hard-shadow { text-shadow: 2px 0 #000, -2px 0 #000, 0 2px #000, 0 -2px #000, 2px 3px 0 #000; }
```

Load fonts explicitly and keep the fallback stack deliberate:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@500;800&family=Spectral:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
```

A counter that rolls to its new value:

```js
function rollTo(el, to, ms = 400) {
  const from = +el.dataset.v || 0, t0 = performance.now();
  el.dataset.v = to;
  (function step(t) {
    const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
    el.textContent = Math.round(from + (to - from) * e).toLocaleString();
    if (k < 1) requestAnimationFrame(step);
  })(t0);
}
```

Title lettering deserves more than a heading: set it large in the display face, then add construction (an outline plus an extruded hard shadow, a baseline rule, a small emblem, letters with individual rotation), or draw it as inline SVG text on a path.

## Bars, pips and meters

Drive every meter from one custom property so JS only sets a number: `el.style.setProperty('--v', hp / maxHp)`.

**Segmented bar with a trailing ghost.** The fill moves at once; the ghost follows late, so the player sees how much was lost.

```html
<div class="bar" role="meter" aria-label="Hull" aria-valuemin="0" aria-valuemax="100" aria-valuenow="62" style="--v:.62">
  <i class="ghost"></i><i class="fill"></i>
</div>
```

```css
.bar { --seg: 10; position: relative; width: 240px; height: 16px; background: #0007;
  -webkit-mask: repeating-linear-gradient(90deg, #000 0 calc(100% / var(--seg) - 3px), transparent 0 calc(100% / var(--seg)));
          mask: repeating-linear-gradient(90deg, #000 0 calc(100% / var(--seg) - 3px), transparent 0 calc(100% / var(--seg))); }
.bar i { position: absolute; inset: 0; transform-origin: left; transform: scaleX(var(--v)); }
.bar .fill  { background: var(--hp); transition: transform 80ms linear; }
.bar .ghost { background: var(--ink); transition: transform 500ms 250ms var(--ease-out); }
.bar.hit .fill { animation: flash 120ms steps(2) 1; }
@keyframes flash { 50% { filter: brightness(3); } }
```

**Other shapes**

```css
.slant  { clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }            /* skewed ends */
.ticks::after { content: ""; position: absolute; inset: 0;                               /* quarter marks drawn over the fill */
  background-image: repeating-linear-gradient(90deg, transparent 0 24%, #000a 24% 25%); }
.radial { border-radius: 50%;                                                            /* cooldown wipe over an icon */
  background: conic-gradient(rgba(0,0,0,.65) calc(var(--v) * 1turn), transparent 0); }
.gauge  { border-radius: 50%;                                                            /* ring gauge */
  background: conic-gradient(var(--energy) calc(var(--v) * 1turn), #0006 0);
  -webkit-mask: radial-gradient(circle, transparent 58%, #000 60%); mask: radial-gradient(circle, transparent 58%, #000 60%); }
```

**Pips** for small totals are separate elements, so each can animate on its own:

```html
<div class="pips" aria-label="Lives: 3 of 5"><b class="on"></b><b class="on"></b><b class="on"></b><b></b><b></b></div>
```

```css
.pips { display: flex; gap: 4px; }
.pips b { width: 14px; height: 18px; background: #0007; clip-path: polygon(50% 0, 100% 30%, 100% 100%, 0 100%, 0 30%); }
.pips b.on { background: var(--hp); }
.pips b.lost { animation: pip-out 300ms var(--ease-out) forwards; }
@keyframes pip-out { 30% { transform: scale(1.5); filter: brightness(3); } 100% { transform: scale(1); background: #0007; } }
```

Give low values a state of their own (a color step, a pulse on the frame, a vignette on the stage) so danger is felt without reading the bar.

## Buttons

A game button is an object that moves when pressed. Build a face and a lip; pressing removes the lip and shifts the face down by the same amount.

```css
.btn { --lip: 5px; font: 800 20px/1 var(--font-display); letter-spacing: .08em; text-transform: uppercase;
  color: var(--ground-edge); background: var(--signal); border: 0; padding: 14px 28px 16px; cursor: pointer;
  box-shadow: inset 0 2px 0 rgba(255,255,255,.3), 0 var(--lip) 0 #8a2f12;
  transition: transform var(--t-press), box-shadow var(--t-press), filter var(--t-press); }
.btn:hover  { filter: brightness(1.08); }
.btn:active { transform: translateY(var(--lip)); box-shadow: inset 0 2px 0 rgba(255,255,255,.3), 0 0 0 #8a2f12; }
.btn:focus-visible { outline: 3px solid var(--ink); outline-offset: 4px; }      /* then restyle into the fiction: brackets, a cursor, a lifted plate */
.btn:disabled { background: #6b6b63; color: #2b2b28; box-shadow: none; transform: translateY(var(--lip)); cursor: default; }
.btn[aria-pressed="true"], .btn.selected { background: var(--ink); }
```

Design the states as different *objects*: disabled is flattened and drained, not just faded; selected is latched down or marked; focus is a cursor from the game's world. Make the hierarchy by shape and size: one primary shape for the main action, quieter shapes for everything else. Menu lists often need no button boxes at all, only type, a cursor and a strong focused state.

## Icons

Inline SVG, one sprite sheet, `currentColor` fills, one style. Build from simple geometry on a fixed grid.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 21 3 12V6l3-3h3l3 3 3-3h3l3 3v6z"/></symbol>
  <symbol id="i-coin"  viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6l5 6-5 6-5-6z" fill="var(--ground-edge)"/></symbol>
  <symbol id="i-bolt"  viewBox="0 0 24 24"><path d="M14 2 5 13h6l-2 9 10-12h-6z"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 2 4 5v7c0 5 3.5 8 8 10 4.5-2 8-5 8-10V5z"/></symbol>
</svg>

<svg class="icon" aria-hidden="true"><use href="#i-heart"/></svg>
```

```css
.icon { width: 24px; height: 24px; fill: currentColor; flex: none; }
```

Guidelines that keep a set coherent:

- Straight segments and whole-number coordinates make a faceted, stamped look that holds at small sizes; add curves only where the direction calls for them.
- One idea per icon and no more than two tones (shape plus one cut-out).
- Same optical size: fill the 24 grid to about 20 units in the larger dimension.
- For pixel directions, draw icons as `<rect>` cells on an 8 or 12 unit grid with `shape-rendering="crispEdges"`.
- Add an outline with `paint-order: stroke; stroke: #000; stroke-width: 3; stroke-linejoin: round` when icons sit directly on the scene.

Never use emoji as icons: they render differently on every platform, ignore the palette, and are the most recognisable sign of generated UI. Do not import a general-purpose line icon set either; it brings a web app's voice with it.

## Motion and feedback

Timing by meaning. These are starting points to tune by eye:

| Event | Duration | Character |
|---|---|---|
| Hover or focus move | 60-100ms | immediate; no travel |
| Press | 40-80ms | down fast, release slightly slower |
| Value pop on change | 120-180ms | scale up to about 1.25 and back, overshoot ease |
| Damage flash | 80-120ms | stepped brightness, no easing |
| Hit shake | 150-250ms | a few pixels, decaying |
| Panel or menu open | 140-220ms | from its anchor edge, slight overshoot |
| Panel close | about two thirds of open | no overshoot |
| List stagger | 20-40ms per item | cap the total near 300ms |
| Reward sequence | 600-1500ms in total | staged beats, each with its own pop |

```css
@keyframes pop   { 40% { transform: scale(1.25); } }
@keyframes shake { 20% { transform: translate(-4px, 2px); } 40% { transform: translate(3px, -2px); }
                   60% { transform: translate(-2px, 1px); } 80% { transform: translate(1px, 0); } }
@keyframes rise  { from { transform: translateY(12px); opacity: 0; } }
.popped { animation: pop var(--t-pop) var(--ease-snap); }
.menu > * { animation: rise var(--t-open) var(--ease-out) backwards; animation-delay: calc(var(--i) * 30ms); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 1ms !important; animation-iteration-count: 1 !important; transition-duration: 1ms !important; }
}
```

Retrigger a CSS animation from JS by removing the class, forcing layout, and adding it again:

```js
function retrigger(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
```

Principles:

- Animate `transform`, `opacity` and `filter` only; they do not cause layout.
- Name the properties in `transition`. `transition: all` animates things that should snap and is a sign nobody chose.
- Match easing to the material: mechanical things use short linear or stepped moves (`steps(3)`), springy things overshoot, paper settles.
- Low-resolution and retro directions move in steps and whole pixels, not smooth sub-pixel tweens.
- The resting HUD does not move. Idle loops are reserved for the one thing that needs attention now.
- Gains travel: a collected coin flies to the counter and the counter pops when it lands. A fly-to is an absolutely positioned clone animated between two `getBoundingClientRect()` positions.
- Offer a setting to reduce screen shake and flashes, and never flash more than three times a second.

## Screen flow and sound hooks

Keep screens in a small stack so Escape or B always goes back one level, and focus returns to where it was:

```js
const stack = [];
function open(screen)  { stack.at(-1)?.el.setAttribute('inert', ''); const last = document.activeElement;
                         stack.push({ el: screen, last }); screen.hidden = false; screen.querySelector('[data-autofocus], button')?.focus(); }
function close()       { const top = stack.pop(); if (!top) return; top.el.hidden = true;
                         stack.at(-1)?.el.removeAttribute('inert'); top.last?.focus(); }
addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
```

Pause the game loop while an explore-tier screen is open, and when the tab is hidden (`visibilitychange`).

UI sound does half the work of feedback. Even if no audio exists yet, leave hooks so it can be attached without touching the markup again:

```js
document.addEventListener('focusin', e => e.target.matches('button, [role="menuitem"]') && emit('ui:move'));
document.addEventListener('click',   e => e.target.closest('button') && emit('ui:confirm'));
function emit(name) { document.dispatchEvent(new CustomEvent(name)); }
```
