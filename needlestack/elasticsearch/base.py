# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import pprint

import pyelasticsearch
import pyelasticsearch.exceptions

from .. import base
from .. import exceptions

from . import fields


# Private utils methods

def _get_doc_type_from_index(index):
    options = index._meta.options
    if "type" in options:
        return options["type"]
    return index.get_name()


def _get_mappings_from_index(index):
    type_options = {"properties": {}}

    for field_name, field in index._meta.fields.items():
        if isinstance(field, fields.IDField):
            type_options["_id"] = field.mapping
        else:
            type_options["properties"][field_name] = field.mapping

    doc_type = _get_doc_type_from_index(index)
    return {doc_type: type_options}


def _adapt_document_for_index(index, document):
    result_doc = {}
    id = None

    for attr_name, attr_value in document.items():
        if attr_name not in index._meta.fields:
            continue

        field = index._meta.fields[attr_name]
        if isinstance(field, fields.IDField):
            id = field.from_python(attr_value)
        else:
            result_doc[field.index_name] = field.from_python(attr_value)

    return (id, result_doc)


class ElasticSearch(base.SearchBackend):
    _es = None # ElasticSearch backend connection
    _default_settings = None # default index settings

    def __init__(self, urls, settings, *args, **kwargs):
        self._default_settings = settings
        self._es = pyelasticsearch.ElasticSearch(urls, *args, **kwargs)

    def get_data_from_model(self, index, model):
        data = {}

        for field_name in index._meta.fields:
            data[field_name] = getattr(model, field_name, None)

        return data

    def update(self, index, document, **options):
        """
        Method for create or update document on the
        index.
        """

        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', _get_doc_type_from_index(index))

        id, adapted_document = _adapt_document_for_index(index, document)

        if id:
            options.setdefault("id", id)

        self._es.index(index_name, index_doc_type, adapted_document, **options)

    def get(self, index, id, **options):
        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', _get_doc_type_from_index(index))
        return self._es.get(index_name, index_doc_type, id, **options)

    def delete_index(self, index):
        index_name = index.get_name()
        try:
            self._es.delete_index(index_name)
        except pyelasticsearch.exceptions.ElasticHttpNotFoundError as e:
            raise exceptions.IndextDoesNotExists("{0} not found".format(index_name)) from e

    def create_index(self, index, settings=None):
        mappings = _get_mappings_from_index(index)

        options = self._default_settings.copy()
        if settings is not None:
            options.update(settings)

        final_settings = {"mappings": mappings}
        if settings:
            final_settings["settings"] = settings

        #pprint.pprint(final_settings)
        try:
            self._es.create_index(index.get_name(), final_settings)
        except pyelasticsearch.exceptions.IndexAlreadyExistsError as e:
            raise exceptions.IndexAlreadyExists("{0} already exists".format(index.get_name()))

    def open_index(self, index):
        """
        Method that open an index.
        """

        if not index.opened:
            index.opened = True
            self._es.open_index(index.get_name())

    def close_index(self, index):
        """
        Method that closes an index.
        """

        if index.opened:
            index.opened = False
            self._es.close_index(index.get_name())

    def search(self, query, index=None, **kwargs):
        if index is not None and issubclass(index, base.Index):
            index = index.get_name()

        return self._es.search(query, index=index, **kwargs)
