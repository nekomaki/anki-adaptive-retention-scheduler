try:
    from ..fsrs_utils.fsrs5 import DECAY
    from ..fsrs_utils.types import State
except ImportError:
    from fsrs_utils.fsrs5 import DECAY
    from fsrs_utils.types import State

from .fsrs6 import (
    find_optimal_desired_retention as find_optimal_desired_retention_v6,
)


def find_optimal_desired_retention(
    state: State, fsrs_params: tuple
) -> tuple[float, float]:
    fsrs_params = tuple(fsrs_params) + (0.0, -DECAY)

    return find_optimal_desired_retention_v6(
        state,
        fsrs_params=fsrs_params,
    )
