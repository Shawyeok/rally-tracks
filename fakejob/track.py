import random
import os
import time


class QueryParamSource:
    # We need to stick to the param source API
    # noinspection PyUnusedLocal
    def __init__(self, track, params, **kwargs):
        self._params = params
        self.infinite = True
        cwd = os.path.dirname(__file__)

    # We need to stick to the param source API
    # noinspection PyUnusedLocal
    def partition(self, partition_index, total_partitions):
        return self


class UpdateKeywordParamSource(QueryParamSource):
    def params(self):
        id = str(random.randint(1, 10000000))
        ts = round(time.time() * 1000)
        path = "/job/_update/{}".format(id)
        if "refresh" in self._params:
            path += "?refresh=" + self._params["refresh"]
        result = {
            "method": "POST",
            "path": path,
            "body": {
                "doc": {
                    "keyword": "rallytest {} {}".format(id, ts),
                    "modifyTime": ts
                }
            }
        }
        return result

def register(registry):
    registry.register_param_source("update-keyword-param-source", UpdateKeywordParamSource)
