# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from threading import local

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import utils


class ConnectionManager(object):
    def __init__(self):
        self._connections = local()

    def load_backend(self, alias="default"):
        # TODO: more exceptions checks on obtain connections

        try:
            conf = getattr(settings, "NEEDLESTACK_CONNECTIONS")
        except AttributeError as e:
            raise ImproperlyConfigured("needlestack not configured") from e

        _conf = conf[alias]

        cls = utils.load_class(_conf["backend"])
        params = _conf["options"]

        return (cls, params)

    def get_connection(self, alias):
        if hasattr(self._connections, alias):
            return getattr(self._connections, alias)

        cls, params = self.load_backend(alias)
        instance = cls(**params)

        setattr(self._connections, alias, instance)
        return instance

    def __getattr__(self, alias):
        return self.get_connection(alias)


manager = ConnectionManager()
