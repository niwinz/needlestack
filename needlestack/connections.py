# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from threading import local

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import utils
from . import base


class ConnectionManager(object):
    __instance = None

    # Make this class as singleton
    def __new__(cls):
        if self.__instance is None:
            self.__instance = super(ConnectionManager, cls).__new__(cls)
        return self.__instance

    def __init__(self):
        self._connections = local()

    def load_backend(self, alias="default"):
        try:
            conf = getattr(settings, "NEEDLESTACK_CONNECTIONS")
        except AttributeError as e:
            raise ImproperlyConfigured("needlestack not configured") from e

        if alias not in conf:
            raise ImproperlyConfigured("connection with alias {0} "
                                       "does not exists".format(alias))
        _conf = conf[alias]

        cls = utils.load_class(_conf["engine"])
        params = _conf["options"]

        return (cls, params)

    def get_connection(self, alias="default"):
        if hasattr(self._connections, alias):
            return getattr(self._connections, alias)

        # Implicit index loading on new connection is created
        base._load_all_indexes()

        cls, params = self.load_backend(alias)
        instance = cls(**params)

        setattr(self._connections, alias, instance)
        return instance

    def get_all_indexes(self):
        base._load_all_indexes()
        return base._get_all_indexes()

    def get_index_by_name(self, name):
        base._load_all_indexes()
        return base._get_index_by_name(name)

    def __getattr__(self, alias):
        return self.get_connection(alias)


manager = ConnectionManager()
