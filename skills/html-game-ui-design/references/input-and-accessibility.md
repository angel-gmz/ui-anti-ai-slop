# Input and accessibility

A game menu that only works with a mouse, or a HUD that only works for one kind of eyesight, is unfinished. These are also the places where generated UI most often shows that nobody played it.

## Contents

- Focus is a game cursor
- Keyboard navigation
- Gamepad
- Touch
- Input prompts
- Readability
- Color and meaning
- Motion, shake and flashing
- Semantics
- Text length and localisation
- Checklist

## Focus is a game cursor

Every menu has exactly one focused element at all times, and it is the most visible thing on the screen. Draw focus as part of the fiction: a pointing hand, brackets, a lifted and lit plate, an underline that slides between items, a selector arrow. Removing the outline without a replacement leaves keyboard and gamepad players blind; the browser's default ring looks like a web form.

```css
.item:focus-visible { outline: none; }                       /* allowed only because the next rule replaces it */
.item { position: relative; }
.item:focus-visible::before { content: ""; position: absolute; left: -22px; top: 50%; width: 12px; height: 14px; margin-top: -7px;
                              background: var(--signal); clip-path: polygon(0 0, 100% 50%, 0 100%);   /* a drawn cursor, not a text glyph */
                              animation: nudge 600ms steps(2) infinite; }
@keyframes nudge { 50% { transform: translateX(3px); } }
```

Hover and focus should look the same or nearly so, and moving the mouse over an item should move focus to it, so there are never two highlighted items.

When a screen opens, focus goes to the sensible default (Resume on pause, the safe option on a confirmation). When it closes, focus returns to where it came from.

## Keyboard navigation

Arrows move, Enter or Space confirms, Escape goes back. Tab should also work but is not the primary scheme.

A small spatial navigator that moves focus to the nearest focusable element in the pressed direction works for lists, grids and irregular layouts alike:

```js
const DIRS = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] };

function moveFocus(dx, dy, scope = document) {
  const items = [...scope.querySelectorAll('button:not(:disabled), [tabindex="0"]')].filter(e => e.offsetParent);
  const cur = document.activeElement;
  if (!items.includes(cur)) return items[0]?.focus();
  const c = center(cur);
  let best = null, bestScore = Infinity;
  for (const el of items) {
    if (el === cur) continue;
    const p = center(el), ax = (p.x - c.x) * dx + (p.y - c.y) * dy;       // distance along the direction
    if (ax <= 1) continue;                                                 // not in that direction
    const off = Math.abs((p.x - c.x) * dy) + Math.abs((p.y - c.y) * dx);   // sideways drift
    const score = ax + off * 3;
    if (score < bestScore) { best = el; bestScore = score; }
  }
  best?.focus();
}
function center(el) { const r = el.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; }

addEventListener('keydown', e => {
  const d = DIRS[e.key];
  if (d) { e.preventDefault(); moveFocus(d[0], d[1], currentScreen()); }
});
```

`currentScreen()` returns the top of the screen stack, so focus cannot leave an open menu. Decide whether lists wrap at the ends and apply it everywhere. Sliders and steppers take Left and Right to change value while focused. Show hotkeys on the controls they trigger.

## Gamepad

The Gamepad API is polled. Map it to the same actions as the keyboard so there is one navigation code path:

```js
let prev = {};
function pollPad() {
  const pad = navigator.getGamepads?.()[0];
  if (pad) {
    const now = {
      up: pad.buttons[12]?.pressed || pad.axes[1] < -0.5,  down: pad.buttons[13]?.pressed || pad.axes[1] > 0.5,
      left: pad.buttons[14]?.pressed || pad.axes[0] < -0.5, right: pad.buttons[15]?.pressed || pad.axes[0] > 0.5,
      confirm: pad.buttons[0]?.pressed, back: pad.buttons[1]?.pressed, pause: pad.buttons[9]?.pressed,
    };
    for (const k in now) if (now[k] && !prev[k]) onAction(k);       // fire on press, not while held
    prev = now;
  }
  requestAnimationFrame(pollPad);
}
pollPad();

function onAction(a) {
  setInputMode('pad');
  if (a === 'confirm') document.activeElement?.click();
  else if (a === 'back') closeTopScreen();
  else if (a === 'pause') togglePause();
  else moveFocus(...{ up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[a], currentScreen());
}
```

Add key repeat for held directions if lists are long (a first delay near 350ms, then every 90ms or so).

## Touch

- Targets at least 48px in both dimensions, with space between them; primary actions larger.
- Nothing may depend on hover. Tooltips open on tap or long-press and close on tap elsewhere.
- Primary actions within thumb reach: the lower half in portrait, the lower corners in landscape.
- Keep clear of system gesture areas and notches using `env(safe-area-inset-*)`.
- Feedback on `pointerdown`, not on release, so presses feel instant.
- Set `touch-action: none` on the play surface and `touch-action: manipulation` on controls to stop double-tap zoom.

## Input prompts

Prompts show the glyph for the device last used. Track the mode and let CSS choose:

```js
function setInputMode(m) { document.documentElement.dataset.input = m; }      // 'keys' | 'pad' | 'touch' | 'mouse'
addEventListener('keydown', () => setInputMode('keys'));
addEventListener('pointerdown', e => setInputMode(e.pointerType === 'touch' ? 'touch' : 'mouse'));
```

```html
<span class="prompt"><kbd data-for="keys">E</kbd><kbd data-for="pad">A</kbd> Open</span>
```

```css
kbd[data-for] { display: none; }
[data-input="keys"] kbd[data-for="keys"], [data-input="mouse"] kbd[data-for="keys"],
[data-input="pad"] kbd[data-for="pad"] { display: inline-grid; }
```

Draw the key cap or button glyph in the direction's style; it is another small place where the UI can belong to the game.

## Readability

- **Size.** At a 1080p stage: glance values and labels no smaller than about 24px for a game played from a sofa, 18px at a desk. On phones, body text no smaller than about 16 CSS pixels after scaling. Check the smallest text at the smallest size the stage will be scaled to.
- **Separation from the scene.** Text over the playfield needs a plate, a real outline (`-webkit-text-stroke` with `paint-order: stroke fill`) or a hard shadow. Thin text with a soft glow disappears over a busy scene.
- **Contrast.** Aim for at least 4.5:1 for text against its plate and 3:1 for meaningful shapes. Dim, mid-grey secondary text on a dark panel is a web habit that fails on a TV.
- **Reading text.** Dialogue and descriptions: a reading face, 45 to 70 characters per line, line height near 1.4 to 1.5, left-aligned, not all caps.
- **Numerals.** Tabular figures for anything that changes.

## Color and meaning

Around one player in twelve has some color vision deficiency. Any meaning carried by color needs a second cue:

- Rarity: frame shape, corner emblem or number of pips as well as color.
- Teams and factions: pattern or emblem as well as color.
- Buffs and debuffs: arrow direction and icon as well as green and red.
- Affordable or not: a struck-through cost or a lock as well as dimming.
- Health against shield: different bar shape or texture as well as hue.

Avoid relying on red against green and blue against purple distinctions. Check the palette in greyscale: if two meaningful states merge, add shape.

## Motion, shake and flashing

- Honour `prefers-reduced-motion`: keep the state change, remove travel, parallax and shake.
- Provide in-game toggles for screen shake and flashing where the game uses them.
- Never flash more than three times a second, and avoid large high-contrast full-screen flashes.
- Nothing that conveys required information should exist only as motion; it must also end in a visible state.

## Semantics

DOM game UI gets accessibility cheaply if the right elements are used:

- Anything pressable is a `<button>` (not a `div` with a click handler), so it is focusable and activates with Enter and Space.
- Meters use `role="meter"` or `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax` and a label.
- Decorative SVG is `aria-hidden="true"`; icon-only buttons have an `aria-label`.
- Important events that are otherwise only visual can be mirrored in a visually hidden `aria-live="polite"` region.
- Screens underneath an open menu get `inert`.
- Do not disable zoom on text-heavy screens.

## Text length and localisation

If the game may be translated, text grows by a third or more and word order changes.

- Let labels size their containers; avoid fixed-width shapes that fit one English word exactly.
- Keep text as text, never baked into an image or an SVG path, apart from the title lettering.
- Build sentences with whole-string templates, not concatenated fragments.
- Choose fonts that cover the needed scripts, and name a fallback per script.

## Checklist

- [ ] Every menu can be completed with arrows, Enter and Escape alone.
- [ ] There is always exactly one visibly focused element, drawn in the game's style.
- [ ] Opening a screen sets focus; closing restores it; focus cannot escape an open screen.
- [ ] Gamepad input drives the same actions as the keyboard, if the game supports a gamepad.
- [ ] Touch targets are at least 48px and nothing needs hover.
- [ ] Text over the scene has a plate or an outline; smallest text checked at smallest scale.
- [ ] Changing values use tabular numerals.
- [ ] No meaning is carried by color alone.
- [ ] Reduced motion is respected; shake and flashes can be turned down.
- [ ] Pressable things are buttons; meters have roles and values.
