from __future__ import annotations

from dataclasses import replace

from .core import EcosystemState, Transfer, apply_internal_transfers


def reference_step(
    state: EcosystemState,
    transfers: tuple[Transfer, ...] = (),
    *,
    utility_delta: float = 0.0,
    quality_delta: float = 0.0,
) -> EcosystemState:
    """Slow, obvious reference transition.

    This function is intentionally boring. Optimized simulation engines should
    be differentially tested against reference behavior before they are trusted.
    """
    moved = apply_internal_transfers(state, transfers)
    return replace(
        moved,
        t=state.t + 1,
        user_utility=state.user_utility + utility_delta,
        service_quality=state.service_quality + quality_delta,
    )
