# Plan (steps): [feature name]

<!--
Plan format: steps — mental prep and build-order breakdown, not the full three-layer onion.
Hard rail: ~2 pages max (~1,000 words / ~80 lines). Plain language; no jargon without a one-line definition.
Delete this comment block before handoff.
Upgrade to full spec: /sage-plan full
-->

## Run metadata

| Field | Value |
|-------|-------|
| Plan format | **steps** |
| Branch | `feat/...` |
| Workflow profile | `…` (tentative) |
| Stack (from codebase) | … |

---

## The problem in plain terms

[3–5 short sentences. What is wrong or missing, who cares, why now. No acronyms unless defined.]

---

## Concepts you need first

| Term / idea | What it means here (one line) |
|-------------|-------------------------------|
| … | … |

Only list concepts required to understand the steps below. Order easiest → harder.

---

## Build steps (do in order)

Each step is one small, finishable chunk. Stop after any step if something is unclear.

### Step 1 — [short title]

| | |
|--|--|
| **Do** | … |
| **Why now** | … |
| **Touches** | files, services, or stores (names only, no deep design) |
| **Done when** | … |
| **Nearby systems** | what larger part of the app/infra this connects to |

### Step 2 — [short title]

| | |
|--|--|
| **Do** | … |
| **Why now** | … |
| **Touches** | … |
| **Done when** | … |
| **Nearby systems** | … |

[Continue numbered steps. Prefer 5–12 steps; merge if more.]

---

## What could affect this later

[Bullets: scale, auth, deploy, other teams, data migration — things to keep in mind while building, not blockers today.]

---

## Still unclear?

| Question | Why it matters |
|----------|----------------|
| … | … |

---

## Next

- Build step 1 yourself, or run **`/sage-plan full`** when ready for the full three-layer plan and SDLC handoff.
- To run what exists so far: [minimal CLI if repo already has scripts, else "after Step N"]
