"""
The Coherence Gate — the living membrane on agent capability.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The hard authority boundary is the OUTER WALL: trade, payment, credentials,
filing, safety-gate bypass refuse early and absolutely. This module is the
INNER MEMBRANE — soft, continuous, and driven by the hive field, not the
individual unit: the live Auris/HNC state (measured Γ, the cosmic advisory,
the lighthouse) decides how far an agent's reach extends THIS turn.

The aperture is not allow/deny — it scales, by NAME:

* ``full``        — the field is clear: all guarded tools, skills, network
* ``reduced``     — coherence is soft: network reach withdrawn, local
                    tools + skills + live state remain
* ``skills_only`` — coherence is low or the advisory is closed: repo
                    reading and skill listing only, nothing that acts
* ``local_only``  — low coherence AND a closed advisory: no tool runs;
                    the agent answers from what it already holds,
                    honestly labeled
* ``refuse``      — every signal is against (Γ below the refuse floor AND
                    the advisory closed AND the lighthouse severe): the
                    turn's expansion is refused outright, with the reasons
                    named on the envelope — never a silent stall

DOCTRINE (the b46 rule, applied to capability): the membrane may only
TIGHTEN on a LIVE field signal. A dark field — no fresh canonical Γ —
restricts nothing and grants nothing new; the hard wall still stands, and
the darkness is recorded on the envelope, never invented around. Individual
agents do not self-authorize; the field decides, and when the field is
silent the aperture simply is not the field's to narrow.

Enforcement sits in the guarded tool registry AFTER the hard boundary:
a tool outside the current aperture is refused with a named coherence-gate
reason, lands on the blocked ledger, parks in the actualization record, and
surfaces in the acquisition outcome — the whole Film-Reel sees the truth.

Gary Leckey · Aureon Institute
"""

from __future__ import annotations

from typing import Any, Dict, Set

__all__ = ["APERTURES", "GAMMA_FULL", "GAMMA_REDUCED", "GAMMA_REFUSE",
           "compute_aperture", "reach_for"]

#: aperture levels, widest to narrowest — a level exists by NAME
APERTURES = ("full", "reduced", "skills_only", "local_only", "refuse")
#: Γ at or above this → the field is clear, full reach
GAMMA_FULL = 0.6
#: Γ below this → skills-only reach
GAMMA_REDUCED = 0.3
#: Γ below this, with the advisory closed AND the lighthouse severe → refuse
GAMMA_REFUSE = 0.15
#: lighthouse severities that close the membrane to introspective reach
_SEVERE = {"critical", "emergency", "severe"}

#: what each aperture may touch — ``None`` means unrestricted
_INTROSPECTIVE_TOOLS = frozenset({"repo_search", "read_repo_file",
                                  "list_repo", "list_skills"})
_NETWORK_TOOLS = frozenset({"web_search", "web_fetch"})


def compute_aperture(gamma: Any, advisory_open: Any,
                     lighthouse_severity: Any) -> Dict[str, Any]:
    """The membrane's decision for one turn, from the live field state.

    ``gamma`` — the canonical coherence Γ, or ``None`` when the field is
    DARK (no fresh reading). ``advisory_open`` — the cosmic advisory gate
    (``None`` = unknown). ``lighthouse_severity`` — the latest lighthouse
    event severity (``None`` = none). Pure and deterministic.
    """
    if gamma is None:
        return {"aperture": "full", "field_status": "canonical_dark",
                "gamma": None,
                "reasons": ["the field is dark — the membrane only tightens "
                            "on a LIVE signal (tighten-only doctrine); the "
                            "hard boundary still stands"]}

    g = float(gamma)
    reasons = []
    aperture = "full"
    if g < GAMMA_FULL:
        aperture = "reduced"
        reasons.append(f"Γ={g:.3f} < {GAMMA_FULL} — network reach withdrawn")
    if g < GAMMA_REDUCED:
        aperture = "skills_only"
        reasons.append(f"Γ={g:.3f} < {GAMMA_REDUCED} — skills-only reach")
    severe = str(lighthouse_severity or "").lower() in _SEVERE
    closed_advisory = advisory_open is False or severe
    if closed_advisory:
        if aperture in ("full", "reduced"):
            aperture = "skills_only"
        reasons.append("the advisory/lighthouse holds the membrane at "
                       f"skills-only reach (advisory_open={advisory_open}, "
                       f"lighthouse={lighthouse_severity})")
    if g < GAMMA_REDUCED and closed_advisory:
        aperture = "local_only"
        reasons.append("low coherence AND a closed advisory — no tool runs; "
                       "the agent answers from what it already holds")
    if g < GAMMA_REFUSE and advisory_open is False and severe:
        aperture = "refuse"
        reasons.append(f"every signal is against (Γ={g:.3f} < {GAMMA_REFUSE}, "
                       "advisory closed, lighthouse severe) — the turn's "
                       "expansion is refused, named, never silent")
    return {"aperture": aperture, "field_status": "live", "gamma": round(g, 6),
            "advisory_open": advisory_open,
            "lighthouse": lighthouse_severity,
            "reasons": reasons or [f"Γ={g:.3f} — the field is clear, full reach"]}


def reach_for(aperture: str, all_tools: Set[str]) -> Set[str] | None:
    """The tool names the aperture admits — ``None`` means unrestricted."""
    if aperture == "full":
        return None
    if aperture == "reduced":
        return set(all_tools) - set(_NETWORK_TOOLS)
    if aperture == "skills_only":
        return set(all_tools) & set(_INTROSPECTIVE_TOOLS)
    if aperture in ("local_only", "refuse"):
        return set()
    raise ValueError(f"unknown aperture '{aperture}' — apertures exist by "
                     f"name: {', '.join(APERTURES)}")
