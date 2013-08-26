# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from importlib import import_module

from django.conf import settings
from django.utils import six
from django.utils.functional import cached_property

from . import base
from . import exceptions


_indexes = {}
_indexes_loaded = False


def _register_index(cls):
    _indexes[cls.get_name()] = cls

def _get_all_indexes():
    return list(_indexes.values())


def _load_all_indexes():
    global _indexes_loaded

    # If already loaded, do nothing
    if _indexes_loaded:
        return

    for app_path in settings.INSTALLED_APPS:
        try:
            mod = import_module(app_path + ".indexes")
        except ImportError:
            pass

    _indexes_loaded = True


def _get_index(name):
    if name not in _indexes:
        raise exceptions.IndextDoesNotExists("{0} does not exists".format(name))
    return _indexes[name]


class Options(object):
    """
    Simple class for store some metadata
    on a Index class.
    """

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.models = set()

    def attach_model(self, model):
        self.models.add(model)


class MetaIndex(type):
    def __new__(tcls, name, bases, attrs):
        params = attrs.pop('_params', {})
        fields = {}

        for name, field in attrs.items():
            if isinstance(field, base.Field):
                fields[name] = value
                value.set_name(name)

        attrs["_meta"] = Options(params=params, fields=fields)
        cls = super(MetaIndex, tcls).__new__(tcls, name, bases, attrs)

        # register index in a global namespace
        _register_index(cls)

        return cls


class BaseIndex(object):
    @property
    def opened(self):
        return getattr(self._meta, "opened", False)

    @opened.setter
    def opened(self, value):
        assert isinstance(value, bool), "value must be a bool type"
        self._meta.opened = value

    @classmethod
    def get_name(cls):
        if "name" not in cls._meta.params:
            cls._meta.params["name"] = utils.un_camel(cls.__name__)
        return cls._meta.params["name"]


class Index(six.with_metaclass(MetaIndex, BaseIndex)):
    pass
