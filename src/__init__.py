from aqt import mw
from aqt.qt import QAction

from .config_manager import get_config
from .scheduler import init_scheduler

config = get_config()


def toggle_enabled():
    config.enabled = not config.enabled
    action_enabled.setChecked(config.enabled)


menu = mw.form.menuTools.addMenu("Adaptive Retention Scheduler")

action_enabled = QAction("Enabled", mw, checkable=True)
action_enabled.setChecked(config.enabled)
action_enabled.triggered.connect(toggle_enabled)


menu.addAction(action_enabled)

init_scheduler()
