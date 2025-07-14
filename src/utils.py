from anki import cards_pb2
from anki.cards import Card
from anki.stats import (
    CARD_TYPE_REV,
    QUEUE_TYPE_DAY_LEARN_RELEARN,
    QUEUE_TYPE_LRN,
    QUEUE_TYPE_NEW,
    QUEUE_TYPE_PREVIEW,
    QUEUE_TYPE_REV,
    QUEUE_TYPE_SUSPENDED,
    REVLOG_CRAM,
    REVLOG_LRN,
    REVLOG_RELRN,
    REVLOG_RESCHED,
    REVLOG_REV,
)

BackendCard = cards_pb2.Card


def get_decay(card: Card):
    return getattr(card, "decay", 0.5) or 0.5


def is_valid_fsrs6_params(fsrs_params):
    return isinstance(fsrs_params, (list, tuple)) and len(fsrs_params) == 21


def is_valid_fsrs5_params(fsrs_params):
    return isinstance(fsrs_params, (list, tuple)) and len(fsrs_params) == 19


def is_valid_fsrs4_params(fsrs_params):
    return isinstance(fsrs_params, (list, tuple)) and len(fsrs_params) == 17
