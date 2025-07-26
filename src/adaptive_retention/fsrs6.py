import math
from typing import Optional

try:
    from ..fsrs_utils.fsrs6 import (
        D_MAX,
        D_MIN,
        S_MAX,
        S_MIN,
        _fsrs_simulate_wrapper,
    )
    from ..fsrs_utils.types import State
    from ..knowledge_ema.fsrs6 import exp_knowledge_gain
    from ..search_algorithms.unimodel import (
        brent_search,
        golden_section_search,
        grid_search,
    )
except ImportError:
    from fsrs_utils.fsrs6 import (
        D_MAX,
        D_MIN,
        S_MAX,
        S_MIN,
        _fsrs_simulate_wrapper,
    )
    from fsrs_utils.types import State
    from knowledge_ema.fsrs6 import exp_knowledge_gain
    from search_algorithms.unimodel import (
        brent_search,
        golden_section_search,
        grid_search,
    )

TARGET_STABILITY = 36500
D_FACTOR = 3
S_FACTOR = 1
S_MIN_IDX = math.floor(math.log(S_MIN) * S_FACTOR)
RETENTION_LOW = 0.75
RETENTION_HIGH = 0.90
MAX_ITERATIONS = 20
SEARCH_ITERATIONS = 4
SEARCH_ITERATIONS_EVAL = 8

cache = {}


def _expected_workload_until_retired_dp(
    state: State, fsrs_params: tuple
) -> Optional[tuple[float, float]]:
    decay = -fsrs_params[20]
    factor = 0.9 ** (1 / decay) - 1
    fsrs_simulate_with_params = _fsrs_simulate_wrapper(fsrs_params)

    difficulties = [i / D_FACTOR for i in range(D_MIN * D_FACTOR, D_MAX * D_FACTOR + 1)]
    stabilities = [
        math.exp(i / S_FACTOR)
        for i in range(
            math.floor(math.log(S_MIN) * S_FACTOR),
            math.ceil(math.log(S_MAX) * S_FACTOR) + 1,
        )
    ]

    def _calc_workload(f, state: State, desired_retention: float) -> float:
        alpha = (desired_retention ** (1 / decay) - 1) / factor
        t_review = state.stability * alpha

        # Disable same-day reviews
        t_review = max(1, round(t_review))

        next_states = fsrs_simulate_with_params(state, t_review=t_review)

        workload = 0
        for prob, next_state, workload_next in next_states:
            workload_all = workload_next

            if next_state.stability < TARGET_STABILITY:
                # Bilinear interpolation
                i_float = (next_state.difficulty - 1) * D_FACTOR
                i0 = min(int(math.floor(i_float)), len(difficulties) - 2)
                i1 = i0 + 1
                wi = i_float - i0

                j_float = math.log(next_state.stability) * S_FACTOR - S_MIN_IDX
                j0 = max(0, int(math.floor(j_float)))
                j1 = j0 + 1
                wj = j_float - j0  # wj may be negative

                f00 = f[i0][j0]
                f01 = f[i0][j1]
                f10 = f[i1][j0]
                f11 = f[i1][j1]

                interpolated = (
                    (1 - wi) * (1 - wj) * f00
                    + (1 - wi) * wj * f01
                    + wi * (1 - wj) * f10
                    + wi * wj * f11
                )
                workload_all += interpolated

            workload += prob * workload_all

        return workload

    def _init_f():
        f = [[1 for _ in range(len(stabilities))] for _ in range(len(difficulties))]

        # Compute the expected workload for each state
        for _ in range(MAX_ITERATIONS):
            delta = 0
            for i, difficulty in enumerate(difficulties):
                for revj, stability in enumerate(reversed(stabilities)):
                    j = len(stabilities) - 1 - revj
                    state = State(difficulty, stability)
                    old = f[i][j]
                    f[i][j] = golden_section_search(
                        lambda r: _calc_workload(f, state, r),
                        lo=RETENTION_LOW,
                        hi=RETENTION_HIGH,
                        max_iter=SEARCH_ITERATIONS,
                    )[0]
                    delta += (old - f[i][j]) ** 2

            # Early stopping if f has converged
            if delta <= 1:
                break

        # Return None if the algorithm fails to converge
        if delta > 1:
            return None

        return f

    if fsrs_params not in cache:
        cache[fsrs_params] = _init_f()

    f = cache[fsrs_params]

    if f is None:
        return None

    def _expected_workload(state: State) -> Optional[tuple[float, float]]:
        result = golden_section_search(
            lambda r: _calc_workload(f, state, r),
            lo=RETENTION_LOW,
            hi=RETENTION_HIGH,
            max_iter=SEARCH_ITERATIONS_EVAL,
        )

        return result

    return _expected_workload(state)


def find_optimal_desired_retention(
    state: State, fsrs_params: tuple
) -> Optional[tuple[float, float]]:
    if len(fsrs_params) != 21:
        raise ValueError("Only FSRS==6 is supported")

    if not 1 <= state.difficulty <= 10:
        raise ValueError("Difficulty must be in [1, 10]")

    if state.stability <= 0:
        raise ValueError("Stability must be positive")

    result = _expected_workload_until_retired_dp(state, fsrs_params)

    return result


if __name__ == "__main__":
    # Example usage
    # stabilities = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
    # for stability in stabilities:
    # state = State(difficulty=10.0, stability=stability)

    state = State(difficulty=1.0, stability=3.0)
    fsrs_params = (
        0.0100,
        0.0100,
        2.2209,
        99.9975,
        4.9538,
        0.6577,
        7.9751,
        0.0000,
        3.0601,
        0.1544,
        1.5607,
        1.3220,
        0.0953,
        0.2975,
        1.6218,
        0.3676,
        4.0111,
        0.9264,
        0.1766,
        0.0000,
        0.5000,
    )
    print(f"Result: {find_optimal_desired_retention(state, fsrs_params)}")
