"""P6: Lighthouse severity is Γ-aware — the same anomaly matters more when the
organism's shared coherence is already low. Amplify-only (caution is the
conservative direction), capped at 1.0, and untouched when the field is dark.
"""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest

from aureon.analytics.aureon_lighthouse import (
    LighthouseEvent,
    LighthouseEventType,
    LighthousePatternDetector,
)

_FIELD = "aureon.core.hnc_field.read_canonical_field"


def _event(severity: float) -> LighthouseEvent:
    return LighthouseEvent(
        event_type=LighthouseEventType.ANOMALY_DETECTED,
        timestamp=time.time(),
        severity=severity,
        symbols=["BTC/USD"],
        message="test anomaly",
    )


def _cf(gamma: float):
    from aureon.core.hnc_field import CanonicalField

    return CanonicalField(available=True, symbolic_life_score=gamma,
                          coherence_gamma=gamma, lambda_t=0.5, source="test")


def _dark():
    from aureon.core.hnc_field import CanonicalField

    return CanonicalField()


def _emit(det: LighthousePatternDetector, ev: LighthouseEvent) -> LighthouseEvent:
    det._emit_event(ev)
    return det.recent_events[-1]


def test_low_gamma_amplifies_severity():
    det = LighthousePatternDetector()
    with patch(_FIELD, lambda *a, **k: _cf(0.0)):
        got = _emit(det, _event(0.4))
    assert got.severity == pytest.approx(0.6), "Γ=0 → 1.5× amplification"
    assert got.data["canonical_gamma"] == pytest.approx(0.0)


def test_high_gamma_leaves_severity_untouched():
    det = LighthousePatternDetector()
    with patch(_FIELD, lambda *a, **k: _cf(1.0)):
        got = _emit(det, _event(0.4))
    assert got.severity == pytest.approx(0.4), "a calm field never REDUCES severity"


def test_amplified_severity_is_capped_at_one():
    det = LighthousePatternDetector()
    with patch(_FIELD, lambda *a, **k: _cf(0.1)):
        got = _emit(det, _event(0.9))
    assert got.severity == pytest.approx(1.0)


def test_dark_field_passes_measured_severity_unchanged():
    det = LighthousePatternDetector()
    with patch(_FIELD, lambda *a, **k: _dark()):
        got = _emit(det, _event(0.4))
    assert got.severity == pytest.approx(0.4)
    assert "canonical_gamma" not in got.data
