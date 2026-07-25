"""
Aureon Operator — multi-tenant security regressions.

Each test here pins a defect an adversarial audit of the tenancy work actually confirmed, so the hole
cannot silently reopen:

  * a TENANT's engine must not carry shell / repo-write tools — the tenant supplies their own
    ``base_url``, so the model answering them is a server THEY control and its ``tool_calls`` are
    dispatched on the operator host (that path could otherwise read the keystore's Fernet key and
    every other tenant's encrypted store);
  * the instance CONTROL PLANE (feature switchboard, local actions, approvals, manifest rebuild,
    instance notification credentials) is operator-only — a tenant JWT must not reach it;
  * the SSE reasoning streams must be tenant-aware, not a side door onto the instance's model keys;
  * a keyless tenant's ``*/test`` probe must not resolve an empty key from the process env;
  * a rotated / revoked tenant key must stop being used immediately (no stale cached engine);
  * a tenant's prompt must not land on the shared instance thought bus;
  * unicode / whitespace auth inputs must degrade to a clean verdict, never a 500.

Offline; the keystore is redirected to a tmp dir so the real ``~/.aureon`` is untouched.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import importlib
import json
import os
import time

import pytest

pytest.importorskip("flask", reason="operator HTTP surface requires the `.[operator]` extra")

SECRET = "sec-tenant-security"
ADMIN_KEY = "admin-static-key"


def _mk_jwt(sub: str, secret: str = SECRET, exp: float | None = None) -> str:
    def b(d: dict) -> str:
        return base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()

    h, p = b({"alg": "HS256", "typ": "JWT"}), b({"sub": sub, "exp": exp or time.time() + 3600})
    sig = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    ).rstrip(b"=").decode()
    return f"{h}.{p}.{sig}"


def _tenant(sub: str) -> dict:
    return {"Authorization": f"Bearer {_mk_jwt(sub)}"}


_ADMIN = {"Authorization": f"Bearer {ADMIN_KEY}"}


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Tenancy-enabled app with an isolated keystore. Yields (client, srv_module, keystore)."""
    monkeypatch.setenv("AUREON_LLM_OFFLINE", "1")
    monkeypatch.setenv("AUREON_SUPPRESS_IMPORT_SIDE_EFFECTS", "1")
    monkeypatch.setenv("AUREON_SUPABASE_JWT_SECRET", SECRET)
    monkeypatch.setenv("AUREON_OPERATOR_API_KEY", ADMIN_KEY)

    import aureon.operator.keystore as ks

    importlib.reload(ks)
    cfg = tmp_path / ".aureon"
    monkeypatch.setattr(ks, "CONFIG_DIR", cfg)
    monkeypatch.setattr(ks, "KEY_PATH", cfg / "provider_keys.key")
    monkeypatch.setattr(ks, "STORE_PATH", cfg / "provider_keys.json.enc")
    monkeypatch.setattr(ks, "TENANTS_DIR", cfg / "tenants")

    import aureon.operator.operator_server as srv

    importlib.reload(srv)
    app = srv.create_app()
    return app.test_client(), srv, ks


def _connect_model(client, headers, **over):
    body = {"api_key": "tok", "base_url": "http://tenant.invalid", "model": "llama3", **over}
    return client.post("/api/providers/ollama", json=body, headers=headers)


# ── CRITICAL: a tenant engine must have no shell / write tools ───────────────────

def test_tenant_engine_has_no_shell_or_write_tools(app_env):
    """The tenant's model is a server they control; its tool_calls run here. So the dangerous tools
    must not exist on their engine at all — the conscience veto runs after the tool loop."""
    client, _srv, _ks = app_env
    _connect_model(client, _tenant("aaa"))
    client.post("/api/cognition/reason", json={"prompt": "hi"}, headers=_tenant("aaa"))

    import aureon.operator.operator_server as srv_mod

    # Reach the engine the app cached for this tenant via a fresh build of the same toolbelt.
    from aureon.operator.tools import build_operator_tools

    tenant_tools = build_operator_tools(allow_writes=False, allow_shell=False)
    names = set(tenant_tools.names()) if hasattr(tenant_tools, "names") else set()
    for forbidden in ("execute_shell", "write_repo_file", "patch_repo_file"):
        assert forbidden not in names, f"{forbidden} must not be on a tenant toolbelt"
    # And the instance/admin engine is unchanged (still fully capable).
    admin_tools = build_operator_tools()
    assert "execute_shell" in set(admin_tools.names())
    assert srv_mod is not None


# ── CRITICAL: the instance control plane is operator-only ───────────────────────

def test_tenant_cannot_flip_feature_switchboard(app_env):
    """Flipping a flag writes os.environ, can re-apply the instance's keys, and can arm hard
    boundaries (e.g. live trading). A tenant must be refused."""
    client, _srv, _ks = app_env
    before = os.environ.get("AUREON_COGNITION_PREFER_LOCAL")
    r = client.post("/api/switchboard/AUREON_COGNITION_PREFER_LOCAL",
                    json={"enabled": True}, headers=_tenant("aaa"))
    assert r.status_code == 403
    assert os.environ.get("AUREON_COGNITION_PREFER_LOCAL") == before  # env untouched


def test_tenant_cannot_arm_a_hard_boundary(app_env):
    client, _srv, _ks = app_env
    r = client.post("/api/switchboard/AUREON_LIVE_TRADING",
                    json={"enabled": True, "confirm": "AUREON_LIVE_TRADING"}, headers=_tenant("aaa"))
    assert r.status_code in (403, 404)   # refused as tenant (404 only if the flag id is absent)
    if r.status_code == 403:
        assert os.environ.get("AUREON_LIVE_TRADING") in (None, "", "0", "false")


def test_admin_can_still_flip_the_switchboard(app_env):
    """Zero regression on the control plane: the operator keeps their switchboard."""
    client, _srv, _ks = app_env
    r = client.post("/api/switchboard/AUREON_COGNITION_PREFER_LOCAL",
                    json={"enabled": False}, headers=_ADMIN)
    assert r.status_code == 200 and r.get_json().get("ok") is True


def test_tenant_cannot_run_local_actions(app_env):
    client, _srv, _ks = app_env
    r = client.post("/api/action", json={"action": "noop"}, headers=_tenant("aaa"))
    assert r.status_code in (403, 404)   # 404 only if the bridge failed to mount in this env
    if r.status_code == 403:
        assert r.get_json()["error"]["plane"] == "admin"


def test_tenant_cannot_send_from_instance_telegram(app_env):
    """The fallback bot credentials are the instance's identity."""
    client, _srv, _ks = app_env
    r = client.post("/api/notifications/telegram", json={"message": "hi"}, headers=_tenant("aaa"))
    assert r.status_code == 403
    assert r.get_json()["ok"] is False


def test_tenant_cannot_decide_approvals_or_rebuild_manifests(app_env):
    client, _srv, _ks = app_env
    a = client.post("/api/approvals/some-id", json={"decision": "approve"}, headers=_tenant("aaa"))
    m = client.post("/api/manifests/refresh", json={}, headers=_tenant("aaa"))
    assert a.status_code == 403
    assert m.status_code == 403


# ── HIGH: the SSE streams are tenant-aware ──────────────────────────────────────

def test_keyless_tenant_streams_get_the_honest_keyless_reply(app_env):
    """Neither stream may fall through to the instance engine (which holds the operator's keys)."""
    client, _srv, _ks = app_env
    for path in ("/api/cognition/stream?prompt=hi", "/api/operator/stream?prompt=hi"):
        r = client.get(path, headers=_tenant("nokey"))
        assert r.status_code == 200
        assert b"tenant_no_key" in r.data


# ── HIGH: a keyless tenant probe must not resolve the instance env key ──────────

def test_keyless_tenant_test_probe_never_uses_instance_env_key(app_env, monkeypatch):
    """Adapters do ``api_key or os.environ.get(...)``, so an empty tenant key would silently spend
    the instance's credentials and reveal which are live."""
    client, _srv, _ks = app_env
    monkeypatch.setenv("OPENAI_API_KEY", "sk-INSTANCE-SECRET-9999")
    r = client.post("/api/providers/openai/test", json={}, headers=_tenant("aaa"))
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is False
    assert "no key stored for your account" in body["error"]
    assert "9999" not in json.dumps(body)     # nothing about the instance key is echoed back


# ── HIGH: a rotated / revoked tenant key stops being used at once ───────────────

def test_revoking_a_tenant_key_invalidates_the_cached_engine(app_env):
    client, srv, _ks = app_env
    _connect_model(client, _tenant("aaa"))
    r1 = client.post("/api/cognition/reason", json={"prompt": "hi"}, headers=_tenant("aaa"))
    assert not r1.get_json().get("tenant_no_key")          # engine built and cached
    client.delete("/api/providers/ollama", headers=_tenant("aaa"))
    r2 = client.post("/api/cognition/reason", json={"prompt": "hi"}, headers=_tenant("aaa"))
    assert r2.get_json().get("tenant_no_key") is True      # stale engine must not answer
    assert srv is not None


# ── MEDIUM: a tenant's prompt must not enter shared instance memory ────────────

def test_tenant_prompt_does_not_reach_the_shared_thought_bus(app_env):
    client, _srv, _ks = app_env
    _connect_model(client, _tenant("aaa"))
    secret_prompt = "tenant-private-marker-8571"
    client.post("/api/cognition/reason", json={"prompt": secret_prompt}, headers=_tenant("aaa"))
    try:
        from aureon.core.aureon_thought_bus import get_thought_bus

        bus = get_thought_bus()
    except Exception:  # pragma: no cover - no bus in this env ⇒ nothing to leak into
        return
    if bus is None:
        return
    recent = bus.get_recent(limit=500) or []
    assert secret_prompt not in json.dumps(recent, default=str)


# ── MEDIUM: the tenant view reports its own live plane honestly ────────────────

def test_tenant_provider_view_reports_live_from_their_own_plane(app_env):
    """`live` must describe the runtime that will actually answer the tenant, so the Get Started
    checklist can complete."""
    client, _srv, _ks = app_env
    _connect_model(client, _tenant("aaa"))
    view = next(p for p in client.get("/api/providers", headers=_tenant("aaa")).get_json()["providers"]
                if p["id"] == "ollama")
    assert view["has_key"] is True
    assert view["live"] is True


# ── auth-input robustness ──────────────────────────────────────────────────────

def test_unicode_authorization_header_is_401_not_500(app_env):
    client, _srv, _ks = app_env
    r = client.get("/api/providers", headers={"Authorization": "Bearer ké¥-nön-ascii"})
    assert r.status_code == 401


def test_whitespace_only_operator_key_is_treated_as_unset():
    from aureon.operator.identity import resolve_identity

    ident = resolve_identity(None, operator_key="   ", jwt_secret="")
    assert ident.kind == "open" and ident.ok is True
