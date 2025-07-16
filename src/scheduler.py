import anki
from anki.cards import Card
from anki.cards_pb2 import FsrsMemoryState
from aqt import gui_hooks, mw

from .adaptive_retention.fsrs5 import (
    find_optimal_desired_retention as find_optimal_desired_retention_v5,
)
from .adaptive_retention.fsrs6 import (
    find_optimal_desired_retention as find_optimal_desired_retention_v6,
)
from .config_manager import get_config
from .fsrs_utils.fsrs5 import (
    interval_from_retention as interval_from_retention_v5,
)
from .fsrs_utils.fsrs6 import (
    interval_from_retention as interval_from_retention_v6,
)
from .fsrs_utils.types import State
from .utils import is_valid_fsrs5_params, is_valid_fsrs6_params

Learning = anki.scheduler_pb2.SchedulingState.Learning
Review = anki.scheduler_pb2.SchedulingState.Review

config = get_config()


def _on_card_will_show(text: str, card: Card, kind: str) -> str:
    if not config.enabled:
        return text

    if kind != "reviewAnswer":
        return text

    did = card.odid or card.did
    deck_config = mw.col.decks.config_dict_for_deck_id(did)
    fsrs_params_v6 = deck_config.get("fsrsParams6")
    fsrs_params = deck_config.get("fsrsWeights")

    if is_valid_fsrs6_params(fsrs_params_v6):
        find_optimal_desired_retention_func = (
            lambda state: find_optimal_desired_retention_v6(
                state, tuple(fsrs_params_v6)
            )
        )
        interval_from_retention_func = (
            lambda state, retention: interval_from_retention_v6(
                state, retention, -fsrs_params_v6[20]
            )
        )
    elif is_valid_fsrs5_params(fsrs_params):
        find_optimal_desired_retention_func = (
            lambda state: find_optimal_desired_retention_v5(state, tuple(fsrs_params))
        )
        interval_from_retention_func = (
            lambda state, retention: interval_from_retention_v5(state, retention)
        )
    else:
        return text

    def _update_normal(normal):
        kind = normal.WhichOneof("kind")

        memory_state = None

        if kind == "new":
            memory_state = None
        if kind == "review":
            if normal.review.HasField("memory_state"):
                memory_state = normal.review.memory_state
        elif kind == "learning":
            if normal.learning.HasField("memory_state"):
                memory_state = normal.learning.memory_state
        elif kind == "relearning":
            if normal.relearning.review.HasField("memory_state"):
                memory_state = normal.relearning.review.memory_state
        else:
            raise ValueError(f"Unknown normal kind: {kind}")

        if memory_state is None:
            return

        state = State(float(memory_state.difficulty), float(memory_state.stability))

        retention = find_optimal_desired_retention_func(state)[1]
        interval = interval_from_retention_func(state, retention)

        normal.ClearField(kind)

        if interval < 1:
            # Disable same-day reviews
            normal.review.CopyFrom(
                Review(
                    scheduled_days=1,
                    memory_state=FsrsMemoryState(
                        difficulty=state.difficulty,
                        stability=state.stability,
                    ),
                )
            )
            # normal.learning.CopyFrom(
            #     Learning(
            #         scheduled_secs=int(interval * 86400),
            #         memory_state=FsrsMemoryState(
            #             difficulty=state.difficulty,
            #             stability=state.stability,
            #         ),
            #     )
            # )
        else:
            normal.review.CopyFrom(
                Review(
                    scheduled_days=round(interval),
                    memory_state=FsrsMemoryState(
                        difficulty=state.difficulty,
                        stability=state.stability,
                    ),
                )
            )

    _update_normal(mw.reviewer._v3.states.again.normal)
    _update_normal(mw.reviewer._v3.states.hard.normal)
    _update_normal(mw.reviewer._v3.states.good.normal)
    _update_normal(mw.reviewer._v3.states.easy.normal)

    return text


def init_scheduler():
    gui_hooks.card_will_show.append(_on_card_will_show)
