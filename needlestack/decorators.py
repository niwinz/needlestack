# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import functools
from django.db import signals

from .connections import manager
from .index import _get_index, _load_all_indexes


def register_with_index(cls=None, name=None, alias="default"):
    if cls is None:
        return functools.partial(register_with_index, name=name, alias=alias)

    if name is None:
        raise TypeError("name must be not None")

    index = get_index(name)
    index.attach_model(cls)

    def _update(sender, instance, **kwargs):
        connection = manager.get_connection(alias)
        data = connection.get_data_from_model(instance)

    def _delete(sender, instance, **kwargs):
        pass

    update_dispatch_uid = "needlestack_update_{0}".format(cls.__name__.lower())
    delete_dispatch_uid = "needlestack_delete_{0}".format(cls.__name__.lower())

    signals.pre_save.connect(_update, sender=cls, dispatch_uid=update_dispatch_uid)
    signals.pre_delete.connect(_delete, sender=cls, dispatch_uid=delete_dispatch_uid)

    return cls
