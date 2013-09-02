# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from whoosh.fields import Schema

from .. import base
from . import fields



class Index(base.Index):
    @classmethod
    def get_mappings(cls):
        attrs = {}
        for field_name, field in cls._meta.fields.items():
            attrs[field_name] = field.native_type

        return Schema(**attrs)

    @classmethod
    def adapt_document(cls, document):
        result_doc = {}

        for attr_name, attr_value in document.items():
            if ((attr_name.startswith("_stored_") and attr_name[8:] in cls._meta.fields)
                    or attr_name in cls._meta.fields):

                field = cls._meta.fields[attr_name]
                result_doc[field.name] = field.from_python(attr_value)

        return result_doc
