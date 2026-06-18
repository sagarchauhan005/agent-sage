# Plan: Rate limit error response leaks internal user ID

## Run metadata

| Field | Value |
|-------|-------|
| Branch | `fix/rate-limit-message-leak` |
| Workflow profile | `hotfix` |
| Route after plan | `build` |
| Stack | **From codebase:** Node.js + Express (`package.json`, `src/middleware/rateLimit.js`) |

## Layer 1 — Problem & requirements

**Problem:** The 429 response body from `rateLimit.js` includes the raw internal `userId` in the error message string. A user reported seeing another account's numeric ID in their own error response during a load test, which is a privacy/security leak even though no PII beyond an opaque ID is exposed.

**Goals:** Stop leaking any internal identifier in the 429 response body. No behavior change to rate limiting itself.

**Non-goals:** Not changing rate limit thresholds, storage backend, or retry-after logic.

| ID | Requirement | Type |
|----|-------------|------|
| FR-1 | 429 response body contains no internal `userId`, only a generic message and `retryAfter` | functional |
| NFR-1 | Fix ships without a deploy/migration; logging still has internal ID for debugging | non-functional |

**Assumptions:** The internal ID appears only in `rateLimit.js` line 42's template string, confirmed by repo grep for `userId` near `429`.

**Open questions:** None.

**Success criteria:** Manual + automated test confirms 429 body never contains `userId`; server logs still record it for ops.

## Layer 2 — Functional specification

**Primary flow:** Client exceeds rate limit → server returns `429` with `{ "error": "rate_limited", "retryAfter": <seconds> }` → server log line still includes `userId` for debugging.

**Alternate flows:** None — single response shape regardless of which limiter (IP or user) triggered.

| Req | Behavior that satisfies it |
|-----|----------------------------|
| FR-1 | Response body builder strips `userId`, returns only `error` and `retryAfter` |

| Edge / failure | Expected external behavior | In scope? |
|----------------|----------------------------|-----------|
| Limiter triggered by IP (no userId) | Same response shape, unaffected | yes |
| Existing client parses old body shape | Only removes a field clients should not have relied on; `error`/`retryAfter` keys unchanged | yes |

**Failure callouts**

| What breaks | User/system sees | Blast radius | Mitigate in scope? |
|-------------|------------------|----------------|--------------------|
| None expected — pure removal of a field | n/a | Single response builder function | accept |

## Layer 3 — Technical specification

| Component | Responsibility |
|-----------|----------------|
| `src/middleware/rateLimit.js` | Builds 429 response body; remove `userId` from the returned object, keep it in the `logger.warn` call |

**Data model (direction):** None — no schema or storage change.

**Integrations:** None.

**Security:** Removes an internal ID from an external-facing response; no new secrets or authz change.

**Ops touch:** None — no deploy phase in this profile.

## How to run (terminal / CLI)

| Step | Framework / tooling | Barebone / fallback |
|------|---------------------|---------------------|
| Install deps | `npm install` | — |
| Start (dev) | `npm run dev` | `node src/server.js` |
| Run feature | Hit any rate-limited route 11x in 60s | `for i in $(seq 1 11); do curl -s localhost:3000/api/ping; done` |
| Smoke verify | `npm run dev`, trigger limiter | Last response body has no `userId` key |

**Example invocation:** `curl -s -i localhost:3000/api/ping` after exceeding the limit → expect `429` with body `{"error":"rate_limited","retryAfter":30}`.

**Env vars (if any):** None.

## Planned test cases

| ID | Req | Scenario | Expected | Type |
|----|-----|----------|----------|------|
| T-1 | FR-1 | User-keyed limiter triggers | 429 body has no `userId` key | unit |
| T-2 | FR-1 | IP-keyed limiter triggers | 429 body unchanged (no `userId` to begin with) | unit |
| T-3 | NFR-1 | Limiter triggers | Server log line still contains `userId` | integration |
