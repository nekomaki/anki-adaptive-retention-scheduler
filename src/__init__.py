from aqt import mw
from aqt.qt import QAction, QActionGroup, QMenu

from .config_manager import get_config
from .scheduler import init_scheduler

config = get_config()


def set_mode_disabled_same_day_review():
    config.disabled_same_day_review = True
    config.min_lifelong_workload = False


def set_mode_min_lifelong_workload():
    config.min_lifelong_workload = True
    config.disabled_same_day_review = False


# Main menu
menu = mw.form.menuTools.addMenu("Adaptive Retention Scheduler")

# Submenu for exclusive choice
mode_menu = QMenu("Mode", mw)
menu.addMenu(mode_menu)

# Create exclusive action group
mode_group = QActionGroup(mode_menu)
mode_group.setExclusive(True)

# Radio-style option 1
action_disabled_same_day_review = QAction("Disable same-day review", mw, checkable=True)
action_disabled_same_day_review.setChecked(config.disabled_same_day_review)
action_disabled_same_day_review.triggered.connect(set_mode_disabled_same_day_review)
mode_group.addAction(action_disabled_same_day_review)
mode_menu.addAction(action_disabled_same_day_review)

# Radio-style option 2
action_min_lifelong_workload = QAction(
    "Minimize lifelong workload (Deprecated)", mw, checkable=True
)
action_min_lifelong_workload.setChecked(config.min_lifelong_workload)
action_min_lifelong_workload.triggered.connect(set_mode_min_lifelong_workload)
mode_group.addAction(action_min_lifelong_workload)
mode_menu.addAction(action_min_lifelong_workload)

init_scheduler()
