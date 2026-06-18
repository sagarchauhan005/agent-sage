# Build: Rate limit error response leaks internal user ID

## Scope implemented

Backend only, per plan: removed `userId` from the 429 response body in `src/middleware/rateLimit.js`. Logging untouched.

## Files changed

- `src/middleware/rateLimit.js` — response body builder no longer includes `userId`
- `test/middleware/rateLimit.test.js` — added T-1, T-2, T-3 from plan

## APIs and UI components added

None — existing `429` response shape narrowed, no new endpoints or components.

## Tests added (pass/fail)

| Test | Result |
|------|--------|
| T-1 user-keyed limiter, no userId in body | pass |
| T-2 IP-keyed limiter, body unchanged | pass |
| T-3 server log still contains userId | pass |

`npm test -- rateLimit` → 3 passed, 0 failed.

## Frontend build run confirmation

Not applicable — no frontend files touched.

## 3P API mock setup

Not applicable.

## Local commits made

- `fix(rate-limit): stop leaking internal userId in 429 response body`
