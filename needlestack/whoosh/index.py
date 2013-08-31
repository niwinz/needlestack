# -*- coding: utf-8 -*-

from .. import base
from . import fields

from whoosh import qparser


class Index(base.Index):
    @classmethod
    def get_mappings(cls):
        pass

    @classmethod
    def adapt_document(cls, document, keep_id=False):
        result_doc = {}

        for attr_name, attr_value in document.items():
            if attr_name not in cls._meta.fields:
                continue

            field = cls._meta.fields[attr_name]
            if isinstance(field, fields.IDField):
                id = field.from_python(attr_value)
                if keep_id:
                    result_doc[field.index_name] = field.from_python(attr_value)

            else:
                result_doc[field.index_name] = field.from_python(attr_value)

        return result_doc

    def make_query(cls, fields, term, **kwargs):
        """
        Shortcut method for create search query object.
        """
        parser = qparser.MultifieldParser(fieldnames=fields, **kwargs)
        return parser.parse(term)
