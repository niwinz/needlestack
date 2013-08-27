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
        for name, value in kwargs.items():
            setattr(self, name, value)

    def set_name(self, name):
        self.name = name

    @classmethod
    def from_python(cls, value):
        """
        Method for adapt document value from python
        to backend specific format.
        """
        return value

    @classmethod
    def to_python(cls, value):
        """
        Method for adapt backend specific format to
        native python format.
        """
        return value
