# Multi-Tenant Auth & Per-Tenant Keys

> Increment 1 toward a live, production-ready state where a real end user can log in and use Aureon OS
> with **their own** keys — safely isolated from every other user, and from the single-operator default.

## The three identities

Every request to `/api/*` (and `/mcp/*`) is resolved to exactly one identity by
[`aureon/operator/identity.py`](../../aureon/operator/identity.py) `resolve_identity()`, which the
operator gate ([`operator_server.py`](../../aureon/operator/operator_server.py) `_gate`) evaluates once
per request and stashes on `g.tenant` / `g.is_admin`:

| Identity | How | `g.tenant` | Plane |
|:---|:---|:---:|:---|
| **open** | neither secret configured | `None` | single-operator (dev / offline) — **unchanged** |
| **admin** | static `AUREON_OPERATOR_API_KEY` bearer | `None` | the instance control plane (global keystore, `os.environ`) |
| **tenant** | a valid Supabase HS256 JWT | JWT `sub` | that user's **isolated** plane |

**Zero-regression invariant.** When `AUREON_SUPABASE_JWT_SECRET` is unset, the tenant branch is never
reached — the gate behaves byte-for-byte like the old static-key `check_bearer`: open when no key is set,
bearer-required when it is. Turning tenancy on is purely additive.

## Per-tenant key isolation

Provider / connection keys live in [`aureon/operator/keystore.py`](../../aureon/operator/keystore.py),
Fernet-encrypted. Every function takes an optional `tenant`:

- `tenant=None` → the global store `~/.aureon/provider_keys.json.enc` (admin / single-operator) — unchanged.
- a tenant → an **isolated file** `~/.aureon/tenants/<tenant>/provider_keys.json.enc`. The `<tenant>`
  segment is sanitized (`_safe_tenant`: strict whitelist, else SHA-256 hash) so a crafted `sub` can never
  escape the tenants directory.

One tenant can never read, test, or apply another's keys; a tenant view never merges the instance
`os.environ` keys (so admin secrets are never shown to a user).

### The one invariant that prevents a leak

`apply_to_env()` injects keys into the **shared process `os.environ`**. That is fine for the single
global operator, but it is the *only* way one user's key could bleed into another user's reasoning. So:

> **A tenant write NEVER calls `apply_to_env()` / `_rebuild_switchboard()` and NEVER mutates
> `os.environ` or the shared `_operator.providers`.** ([`operator_server.py`](../../aureon/operator/operator_server.py)
> forks every `providers_*` / `connections_*` route on `g.tenant` exactly here.)

This is enforced and regression-tested in
[`tests/test_operator_tenant_keys.py`](../../tests/test_operator_tenant_keys.py)
(`test_tenant_write_never_mutates_os_environ`).

## Frontend

[`frontend/src/services/apiClient.ts`](../../frontend/src/services/apiClient.ts) now attaches the
end-user session bearer to every `/api/*` call via an injectable `authTokenProvider`, wired once in
[`main.tsx`](../../frontend/src/main.tsx) to `supabase.auth.getSession()`. No session ⇒ no header ⇒
unchanged. The capability pages (Operator Chat, Providers, Connections) route through `apiClient`, so the
tenant token flows to the backend.

## What ships now vs. what's next (honest)

**Ships:** end-user identity end-to-end; each user's keys **stored, managed, and live-tested** in full
isolation; the single-operator default unchanged.

**Deferred (immediate follow-up):** per-user **live reasoning** — `/api/cognition/reason` and
`/api/operator/respond` still run on the *instance's* configured models, because the cognition engine is a
process singleton (mesh join, thought-bus, Queen conscience) whose per-tenant lifecycle is a deeper
refactor. The env-free seam is already in place —
[`providers.build_provider_set_from_entries()`](../../aureon/operator/providers.py) builds a switchboard
from a tenant's keys with **no `os.environ` touch** — so the follow-up is
`AureonOperator(providers=build_provider_set_from_entries(keystore.load(tenant)))`, not an adapter rewrite.

Other follow-ups: per-tenant crypto keys; SSE stream tenancy (`EventSource` cannot carry an Authorization
header, so `/api/*/stream` stays on the admin/global plane — the console chat uses POST, which is covered);
migrating the sign-up Binance-key capture off Supabase onto the tenant keystore.

## Configure

| Variable | Effect |
|:---|:---|
| `AUREON_SUPABASE_JWT_SECRET` | **On/off switch** for tenancy. Unset ⇒ single-operator, unchanged. |
| `AUREON_OPERATOR_API_KEY` | The admin/operator static bearer (control plane). |
| `VITE_REQUIRE_AUTH=1` | Frontend: require a Supabase login to reach the console (build-time). |
| `VITE_SUPABASE_*` / `SUPABASE_*` | Supabase project URL + keys (see `docs/SAAS_INTEGRATION_READINESS.md`). |

## Reproduce the isolation proof

```bash
AUREON_LLM_OFFLINE=1 AUREON_SUPPRESS_IMPORT_SIDE_EFFECTS=1 \
  pytest tests/test_operator_tenant_keys.py -q
```

Asserts: tenant B can't see tenant A's key · a tenant write leaves `os.environ` untouched · admin uses the
global store · a tenant can live-test their own key · the identity matrix · open-mode backward-compat.
