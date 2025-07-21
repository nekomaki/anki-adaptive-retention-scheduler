from functools import lru_cache

from aqt import mw

addon_identifier = mw.addonManager.addonFromModule(__name__)


class Config(object):
    def __init__(self):
        self.data = mw.addonManager.getConfig(addon_identifier)

    @property
    def min_lifelong_workload(self):
        return self.data.get("min_lifelong_workload")

    @min_lifelong_workload.setter
    def min_lifelong_workload(self, value):
        self.data["min_lifelong_workload"] = value
        self.save()

    @property
    def disabled_same_day_review(self):
        return self.data.get("disabled_same_day_review")

    @disabled_same_day_review.setter
    def disabled_same_day_review(self, value):
        self.data["disabled_same_day_review"] = value
        self.save()

    def save(self):
        mw.addonManager.writeConfig(addon_identifier, self.data)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
