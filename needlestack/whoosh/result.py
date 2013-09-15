# -*- coding: utf-8 -*-

class ResultItem(object):
    def __init__(self, result_item):
        self._data = tuple(result_item.items())

    @property
    def data(self):
        return dict(self._data)


class SearchResult(object):
    def __init__(self, result):
        self._items = tuple([ResultItem(x) for x in result])

    @property
    def items(self):
        return self._items

    def __len__(self):
        return len(self._items)
