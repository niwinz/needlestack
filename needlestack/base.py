# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from importlib import import_module
import threading
import inspect

from django.conf import settings
from django.utils import six
from django.utils.functional import cached_property

from . import exceptions
from . import utils

_local = threading.local()


def _register_index(cls):
    if not hasattr(_local, "indexes"):
        _local.indexes_map = {}

    _local.indexes_map[cls.get_name()] = cls


def _load_all_indexes():
    if getattr(_local, "indexes_loaded", True):
        return

    for app_path in settings.INSTALLED_APPS:
        try:
            mod = import_module(app_path + ".indexes")
        except ImportError:
            pass

    _local.indexes_loaded = True
    _local.indexes = tuple(_local.indexes_map.values())


def _get_all_indexes():
    return _local.indexes_list


def _resolve_index(index):
    if index is None:
        return index
    elif isinstance(index, six.string_types):
        return _get_index_by_name(index)
    elif inspect.isclass(index):
        if issubclass(index, Index):
            return index

    raise TypeError("invalid type for index parameter")


def _get_index_by_name(name):
    if name not in _local.indexes_map:
        raise exceptions.IndextDoesNotExists("{0} does not exists".format(name))
    return _local.indexes_map[name]


class Field(object):
    """
    Base class for any field.
    """

    name = None

    def __init__(self, **kwargs):
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
        options = attrs.pop('_options', {})
        abstract = attrs.pop('_abstract', False)

        fields = {}
        for _name, field in attrs.items():
            if isinstance(field, Field):
                fields[_name] = field
                field.set_name(_name)

        attrs["_meta"] = Options(options=options, fields=fields)
        cls = super(MetaIndex, tcls).__new__(tcls, name, bases, attrs)

        if not abstract and fields:
            # register index in a global namespace
            _register_index(cls)

        return cls


class BaseIndex(object):
    _abstract = True

    @classmethod
    def mark_opened(cls):
        cls._meta.opened = True

    @classmethod
    def mark_closed(cls):
        cls._meta.opened = False

    @classmethod
    def is_opened(cls):
        return getattr(cls._meta, "opened", False)

    @classmethod
    def get_name(cls):
        if "name" not in cls._meta.options:
            cls._meta.options["name"] = utils.un_camel(cls.__name__)
        return cls._meta.options["name"]


class Index(BaseIndex, metaclass=MetaIndex):
    pass


class SearchBackend(object):
        pass
