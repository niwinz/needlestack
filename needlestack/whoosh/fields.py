# -*- coding: utf-8 -*-

from django.utils.functional import cached_property
from .. import base

from whoosh import fields


class Field(base.Field):
    type = None
    default_kwargs = None

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    @cached_property
    def native_type(self)
        if self.type is None:
            raise RuntimeError("type attr can not be None")

        if self.default_kwargs is not None:
            self._kwargs.update(self.default_kwargs)

        return self.type(*self._args, **self._kwargs)


class TextField(Field):
    type = fields.TEXT


class IntegerField(Field):
    type = fields.NUMERIC


class FloatField(Field):
    type = fields.NUMERIC
    default_kwargs = {"numtype": float}


class BooleanField(Field):
    type = fields.BOOLEAN
