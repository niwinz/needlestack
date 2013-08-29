# -*- coding: utf-8 -*-

from .. import base
from . import fields


class Index(base.Index):
    """
    ElasticSearch subclass of Index.
    """

    @classmethod
    def get_doc_type(cls):
        options = cls._meta.options
        if "type" in options:
            return options["type"]
        return cls.get_name()

    @classmethod
    def get_mappings(cls):
        type_options = {"properties": {}}

        for field_name, field in cls._meta.fields.items():
            if isinstance(field, fields.IDField):
                type_options["_id"] = field.mapping
            else:
                type_options["properties"][field_name] = field.mapping

        return {cls.get_doc_type(): type_options}

    @classmethod
    def adapt_document(cls, document, keep_id=False):
        result_doc = {}
        id = None

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

        return (id, result_doc)
