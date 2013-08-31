# -*- coding: utf-8 -*-

from django.utils.functional import cached_property
from .. import base

from whoosh import fields


class Field(base.Field):
    type = None
    default_kwargs = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs

        if self.default_kwargs is not None:
            for key, value in self.default_kwargs.items():
                self._kwargs.setdefault(key, value)

    @cached_property
    def native_type(self):
        if self.type is None:
            raise RuntimeError("type attr can not be None")

        return self.type(**self._kwargs)


class IDField(Field):
    type = fields.ID
    default_kwargs = {"stored": True}


class KeyworkdField(Field):
    type = fields.KEYWORD


class TextField(Field):
    type = fields.TEXT


class IntegerField(Field):
    type = fields.NUMERIC


class FloatField(Field):
    type = fields.NUMERIC
    default_kwargs = {"numtype": float}


class BooleanField(Field):
    type = fields.BOOLEAN


class DateTimeField(Field):
    type = fields.DATETIME
