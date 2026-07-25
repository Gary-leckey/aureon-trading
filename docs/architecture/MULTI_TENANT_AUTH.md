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
isolation; the single-operator default unchanged; and **per-user live reasoning** — a signed-in user's
own model drives their own `/api/cognition/reason` and `/api/operator/respond`.

## The two planes (what a tenant may NOT do)

`g.is_admin` is true for the admin bearer and for the open single-operator default; it is false only
for a signed-in end user. The **instance control plane is operator-only** and enforced (not merely
computed) — a tenant JWT gets `403` from:

| Route | Why it's operator-only |
|:---|:---|
| `POST /api/switchboard/<flag>` | writes `os.environ`, can re-apply the instance's own keys, can **arm hard boundaries** (e.g. live trading) |
| `POST /api/action` | touches the host machine |
| `POST /api/approvals/<id>` | the director's desk — the human gate on big plays |
| `POST /api/manifests/refresh` | instance-wide rebuild |
| `POST /api/notifications/telegram` | the *instance's* bot identity (a tenant may still pass their own `botToken`) |

An adversarial audit of this work confirmed that computing `g.is_admin` without enforcing it left every
one of those reachable by any valid tenant token. The regression suite
[`tests/test_operator_tenant_security.py`](../../tests/test_operator_tenant_security.py) pins each one.

### Per-user live reasoning

When a request carries a tenant, `operator_server` builds a **request-scoped engine from that tenant's
keystore** via [`providers.build_provider_set_from_entries()`](../../aureon/operator/providers.py) (which
reads explicit keys and never touches `os.environ`), and caches it per tenant in a **bounded LRU** (max 8).
Three properties keep it safe and leak-free:

- **Read-only toolbelt — a hard boundary.** A tenant supplies their own `base_url`, so the model
  answering their turn is a server **they** control, and whatever `tool_calls` it returns get dispatched
  on the operator host. The conscience veto runs *after* the tool loop, so it cannot undo a side effect.
  Therefore a tenant engine is built with `build_operator_tools(allow_writes=False, allow_shell=False)` —
  `execute_shell`, `write_repo_file` and `patch_repo_file` **do not exist** on it. (Before this was
  enforced, a hostile endpoint could have read the keystore's Fernet key and every tenant's store.)
- **Isolated bus** — per-tenant engines get an `_IsolatedBus`: `subscribe` is a no-op (so cached engines
  can't accumulate organism callbacks) *and* `publish`/`recall` are no-ops, so a tenant's prompt and
  answer never land in the shared instance thought bus. `join_mesh=False` keeps them off the mesh.
- **Tenant-plane conscience** — the ethical gate always runs, but the Queen publishes each verdict
  (quoting the action, i.e. the user's prompt). So the tenant plane uses its own conscience instance with
  `_thought_bus` detached: identical judgement, nothing written into shared instance memory.
- **Honest keyless reply** — a signed-in user with no model of their own gets a clear "add a key" response
  on **every** entrypoint — `reason`, `respond`, and both SSE streams — **never** the instance's models
  (that would spend the operator's keys on a stranger). The same rule governs `*/test` probes: a tenant
  with no stored key gets an honest verdict rather than an empty key, which the adapters would otherwise
  resolve from the process env.
- **Revocation takes effect at once** — every tenant credential write/delete drops that tenant's cached
  engines, so a rotated or revoked key stops being spent on the next request.

The admin/open plane (`g.tenant is None`) still uses the shared instance engine, byte-for-byte as before.

**Deferred (follow-ups):** per-tenant crypto keys; SSE stream tenancy (`EventSource` cannot carry an
Authorization header, so `/api/*/stream` stays on the admin/global plane — the console chat uses POST,
which is covered); migrating the sign-up Binance-key capture off Supabase onto the tenant keystore.

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
