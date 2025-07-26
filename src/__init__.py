from aqt import mw
from aqt.qt import QAction, QActionGroup, QMenu

from .config_manager import get_config
from .scheduler import init_scheduler

config = get_config()


def set_mode_disable_same_day_reviews():
    config.disable_same_day_reviews = True
    config.min_lifelong_workload = False


def set_mode_min_lifelong_workload():
    config.min_lifelong_workload = True
    config.disable_same_day_reviews = False


# Main menu
menu = mw.form.menuTools.addMenu("Adaptive Retention Scheduler")

# Submenu for exclusive choice
mode_menu = QMenu("Mode", mw)
menu.addMenu(mode_menu)

# Create exclusive action group
mode_group = QActionGroup(mode_menu)
mode_group.setExclusive(True)

# Radio-style option 1
action_disable_same_day_reviews = QAction(
    "Only disable same-day reviews", mw, checkable=True
)
action_disable_same_day_reviews.setChecked(config.disable_same_day_reviews)
action_disable_same_day_reviews.triggered.connect(set_mode_disable_same_day_reviews)
mode_group.addAction(action_disable_same_day_reviews)
mode_menu.addAction(action_disable_same_day_reviews)

# Radio-style option 2
action_min_lifelong_workload = QAction("Minimize lifelong workload", mw, checkable=True)
action_min_lifelong_workload.setChecked(config.min_lifelong_workload)
action_min_lifelong_workload.triggered.connect(set_mode_min_lifelong_workload)
mode_group.addAction(action_min_lifelong_workload)
mode_menu.addAction(action_min_lifelong_workload)

init_scheduler()
