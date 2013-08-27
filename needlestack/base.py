# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import


class SearchBackend(object):
    pass


class Field(object):
    """
    Base class for any field.
    """

    name = None

    def __init__(self, **kwargs)
        self.options = kwargs

    def set_name(self, name):
        self.name = name
