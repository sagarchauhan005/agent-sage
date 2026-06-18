# Release report: Rate limit error response leaks internal user ID

## Branch name

`fix/rate-limit-message-leak`

## Commits made

- `fix(rate-limit): stop leaking internal userId in 429 response body`

## PR URL

`https://github.com/example-org/example-repo/pull/412` (after user approval)

## Secret scan result

Clean — no `.env`, tokens, or credentials in the diff (2 files changed: middleware + test).
