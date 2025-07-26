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
    def disable_same_day_reviews(self):
        return self.data.get("disable_same_day_reviews")

    @disable_same_day_reviews.setter
    def disable_same_day_reviews(self, value):
        self.data["disable_same_day_reviews"] = value
        self.save()

    def save(self):
        mw.addonManager.writeConfig(addon_identifier, self.data)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
