---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We're prototyping a deckbuilder called "Last Call" where you run a food stall at a night market. Each turn you play dish and trick cards from your hand to serve the customers queueing up. I need the in-round screen as one HTML file (round.html): a hand of 5 cards (each has a cost in "heat", a name, a type, rules text, and some have a satisfaction value), heat available this turn, draw pile and discard pile with counts, coins, reputation, how many customers are waiting, and an End Turn button. Hovering or focusing a card should bring it forward so it's readable. Clicking a card can just play it (remove it from the hand and spend the heat) so we can feel the flow. Mouse first, but keyboard should work too.
