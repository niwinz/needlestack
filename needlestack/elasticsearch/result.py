# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.utils.functional import cached_property


class SearchResult(object):
    def __init__(self, result):
        self._result = result

    @property
    def raw_data(self):
        return self._result

    @cached_property
    def data(self):
        if "_source" in self._result:
            return self._result["_source"]
        elif "fields" in self._result:
            return self._result["fields"]

        raise RuntimeError("This result object does not have valid data")

    @property
    def score(self):
        return self._result["_score"]

    @property
    def index_name(self):
        return self._result["_index"]

    @property
    def id(self):
        return self._result["_id"]

    @property
    def doc_type(self):
        return self._result["_type"]


class SearchResponse(object):
    def __init__(self, result):
        self._result = result

    @property
    def timed_out(self):
        return self._result["timed_out"]

    @property
    def total_results(self):
        return self._result["hits"]["total"]

    @property
    def max_score(self):
        return self._result["hits"]["max_score"]

    @property
    def shards_info(self):
        return self._result["_shards"]

    @property
    def raw_data(self):
        return self._result

    @cached_property
    def results(self):
        return list(self.iter_results())

    def __len__(self):
        return len(self._result["hits"]["hits"])

    def iter_results(self):
        for hit in self._result["hits"]["hits"]:
            yield SearchResult(hit)
