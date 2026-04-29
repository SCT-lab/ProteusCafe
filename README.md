# CAFÉ PROTEUS — Build Prompt & Spec

---

## Overview

CAFÉ PROTEUS is a single self-contained HTML file. Canvas is **750×520px** with a **220px sidebar** on the right for a chat log.

**Visual target:** is based on a GTA2 top-down pixel art style. We suggest you study GTA2 screenshots before writing any code. The design considers wide dark roads, chunky pixel vehicles, clear building interiors visible from above. Warm Stardew Valley interior aesthetic inside the buildings — large floor tiles, dark upper wall band with golden X-brace window panels, chunky wooden furniture with drop shadows.

![Café Proteus overview](https://github.com/SCT-lab/ProteusCafe/blob/main/Cafe1.png)
---


## Structure

- Large floor tiles (28px, two alternating tones)
- Upper wall band (30px tall): dark wood with evenly spaced golden window panels, each with an X-brace cross drawn inside
- Horizontal wood rail separating upper band from floor
- Dark wood border strips on left and right walls
- Drawn in strict painter's order: floor → back wall band → far furniture → near furniture → sprites

### TL — CAFÉ PROTEUS

Warm amber floor (`#c07828` / `#a86020`). Service counter across the top interior wall — dark espresso wood with a bright brass top surface, espresso machine left, pastry display case right. Two rectangular wooden tables in the lower half, each with 4 chairs (2 above, 2 below — back chairs drawn first so front chairs overlap the agent's legs). Corner plant. Chalkboard menu on left wall.

---

## Agents (café only, never move)

Five agents seated inside the café at fixed pixel coordinates:

| Agent | Colour | Seat |
|-------|--------|------|
| HERO | cyan `#22dddd` | table left, left chair |
| SHADOW | magenta `#dd44cc` | table left, right chair |
| MIRROR | green `#44dd66` | table right, left chair |
| ANON | yellow `#dddd22` | table right, right chair |
| CODEC | orange `#ff8833` | behind service counter on stool |

Each agent is a **seated pixel sprite**: chair back visible behind them, torso in their colour, skin-tone head (8×8px), two pixel eyes, 1px black outline. Name tag floats above them (4px Press Start 2P font, coloured border matching agent colour, black fill).

### Agent System Prompts

- **HERO:** Idealistic, believes avatars genuinely transform identity via the Proteus Effect, earnest and passionate
- **SHADOW:** Cynical, thinks the Proteus Effect is pure performance not real change, sharp and sardonic
- **MIRROR:** Jungian, believes avatars reveal the hidden self rather than create a new one, philosophical
- **ANON:** Believes no-identity is the truest self, cryptic and fragmented
- **CODEC:** World-weary barista, thinks tech companies profit from identity fluidity, dry and observational

---

## NPCs

| Room | NPCs |
|------|------|
| Sole City | CLERK (blue), CUST (orange) — wandering slowly |
| Thread | STYLIST (pink), SHOPPER (teal), BROWSE (yellow) — wandering |
| Call Nexus | OP-1, OP-2, OP-3 (muted blue, seated at desks), MGR (red, standing) |

Walking NPCs move slowly. Seated NPCs stay fixed at their desk.

---

## Pixel Sprite Spec (GTA2 scale)

### People — agents, NPCs, pedestrians

- Total height: **14px**
- Head: 6×6px, skin tone
- Body: 8×8px, character colour, darker shade inset for shirt detail
- Legs: visible on standing/walking sprites only, 3px each
- Drop shadow: 6×2px ellipse, 30% opacity, 2px below feet
- 1px black outline on head and body

### Vehicles

| Type | Horizontal | Vertical |
|------|-----------|---------|
| Car | 22×13px | 13×22px |
| Bus | 40×14px | 14×40px |

**Car anatomy:** 

body fill → darker roof panel inset 2px → white windscreen strip → 2×2px headlights front → 2×2px red taillights rear → 1px black outline → drop shadow offset +2+2
---

## Vehicles

Cars and buses drive around the perimeter road only. Each side has two lanes (one per direction). Vehicles wrap off-screen and re-enter the other side. Each lane has 2–3 vehicles staggered. Use ~8 different saturated body colours. Speed variation: **0.8–1.4px per frame**.

---

## Pedestrians

Walk along the inner kerb of the perimeter road only (the strip between road edge and building wall):

- Left/right kerb: walk vertically
- Top/bottom kerb: walk horizontally
- Wrap at canvas edges
- **12 pedestrians total**, 3 per side
- Distinct bright colours

---
## Discussion Engine

User types a topic into the textarea and hits TRANSMIT (or Enter). Agents respond in a randomised order — **CODEC always last**.

For each agent:

1. Call `https://api.anthropic.com/v1/messages` with model `claude-sonnet-4-20250514`, `max_tokens: 1000`, the agent's system prompt, and the full conversation history so agents can respond to each other
2. Show a **speech bubble** above the agent: dark fill, coloured border matching agent colour, 4px Press Start 2P text, word-wrapped to 110px wide, tail pointing down to agent head. Bubble fades out slowly over ~8 seconds.
3. Add entry to **sidebar log**: agent name in their colour, response text below in muted warm tone

### Sidebar Style

- Background: `#120c08`
- Borders: `#3a2a18`
- Font: Press Start 2P, 5px throughout

---

## Draw Order (strict, every frame)

1. Road + kerbs + lane markings
2. All four room floors
3. All four room back wall bands (upper panels with X-braces)
4. All four room far furniture (counters, shelves, desks — top of room)
5. All four room near furniture (tables + chairs — **back row first**, then table surface, then front chairs)
6. Seated NPCs at their stations
7. Walking NPCs
8. Agents
9. Vehicles (on road, drawn over kerb)
10. Pedestrians
11. Speech bubbles (always on top)

> `ctx.imageSmoothingEnabled = false` — hard pixel edges everywhere, no gradients anywhere.

---

## Font

**Press Start 2P** from Google Fonts for all text.

```html
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
```

---

## Key Rules

- No gradients anywhere — flat colours only
- Every sprite must be anchored to furniture or ground (no floating)
- Agents are seated: chair back overlaps their lower body, feet not visible
- Vehicles never enter the inner area — road perimeter only
- Pedestrians never enter buildings — kerb strip only
- NPCs never leave their assigned room
- Speech bubbles clamp to canvas edges, never overflow
