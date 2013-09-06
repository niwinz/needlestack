# -*- coding: utf-8 -*-

class ResultItem(object):
    def __init__(self, result_item):
        self._data = tuple(result_item.items())


class SearchResult(object):
    def __init__(self, result):
        self._items = [ResultItem(x) for x in result]
