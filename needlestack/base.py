# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import


class SearchBackend(object):
    def update(self, *args, **kwargs):
        """
        Method that creates or updates some document
        on the search engine.
        """
        raise NotImplementedError()

    def search(self, *args, **kwargs):
        """
        Makes a search and return a result.
        """
        raise NotImplementedError()

    def flush(self):
        """
        Send flush/commit command to the
        search engine.
        """
        raise NotImplementedError()


class Field(object):
    """
    Base class for any field.
    """

    name = None

    def __init__(self, **kwargs)
        self.options = kwargs

    def set_name(self, name):
        self.name = name
