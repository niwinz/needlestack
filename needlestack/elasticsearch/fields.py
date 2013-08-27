# -*- coding: utf-8 -*-

from .. import base


class Field(base.Field):
    type = None

    def __init__(self, stored=True, index_name=None, analyzed=True, term_vector="no",
                 boost=1.0, analyzer=None, index_analyzer=None, search_analyzer=None,
                 ignore_above=None, include_in_all=True, **kwargs):

        super(Field, self).__init__(**kwargs)

        assert term_vector in ["no", "yes", "with_offsets", "with_positions",
                               "with_positions_offsets"], "term_vector has invalid value"

        self.term_vector = term_vector
        self.stored = stored
        self.analyzed = analyzed
        self.boost = boost
        self.index_name = index_name
        self.analyzer = analyzer
        self.index_analyzer = index_analyzer
        self.search_analyzer = search_analyzer
        self.ignore_above = ignore_above
        self.include_in_all = include_in_all

    def set_name(self, name):
        if self.index_name is None:
            self.index_name = name
        super(Field, self).set_name(name)

    @property
    def mapping(self):
        mapping = {
            "type": self.type,
            "store": self.stored,
            "index": "analyzed" if self.analyzed else "not_analyzed",
            "boost": self.boost,
        }

        if self.analyzer:
            mapping["analyzer"] = self.analyzer

        if self.index_name:
            mapping["index_name"] = self.index_name

        if self.include_in_all:
            mapping["include_in_all"] = self.include_in_all

        # "ignore_above": self.ignore_above,
        # "search_analyzer": self.search_analyzer,
        # "index_analyzer": self.index_analyzer,

        return mapping


class IDField(base.Field):
    def __init__(self, store=False):
        self.store = store
        self.index_name = "_id"

    @property
    def mapping(self):
        mapping = {
            "type": "string",
            "store": self.store,
            "index": "not_analyzed",
        }

        return mapping


class TextField(Field):
    type = "string"


class IntegerField(Field):
    type = "long"


class FloatField(Field):
    type = "double"


class BooleanField(Field):
    type = "boolean"


class ArrayField(Field):
    type = "array"
