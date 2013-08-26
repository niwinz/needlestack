# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import pyelasticsearch
import pyelasticsearch.exceptions

from .. import base
from .. import exceptions

from . import fields


# Private utils methods

def _get_doc_type_from_index(index):
    params = index._meta.params
    if "type" in params:
        return params["type"]
    return index.get_name()


def _get_mappings_from_index(index):
    mapping = {}

    for field_name, field in index._meta.fields.items():
        mapping[field_name] = field.mapping

    doc_type = _get_doc_type_from_index(index)
    return {doc_type: {"properties": mapping}}


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

        TODO: additional documentation for possible
        options for elasticsearch search backend.
        """

        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', _get_doc_type_from_index(index))
        self._es.index(index_name, index_doc_type, document, **options)

    def get(self, index, id, **options):
        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', _get_doc_type_from_index(index))
        return self._es.get(index_name, index_doc_type, id, **options)

    def delete_index(self, index):
        index_name = index.get_name()
        try:
            self._es.delete_index(index_name)
        except: pyelasticsearch.exceptions.ElasticHttpNotFoundError as e:
            raise exceptions.IndextDoesNotExists("{0} not found".format(index_name)) from e

    def create_index(self, index, settings=None):
        mappings = _get_mappings_from_index(index)

        options = self._default_settings.copy()
        if settings is not None:
            options.update(settings)

        final_settings = {
            "mappings": mappings,
            "settings": options,
        }

        try:
            self._es.create_index(index.get_name(), final_settings)
        except pyelasticsearch.exceptions.IndexAlreadyExistsError as e:
            raise exceptions.IndexAlreadyExists("{0} already exists".format(index.get_name()))

    def open_index(self, index):
        """
        Method that open an index.
        """

        if not index.opened
            index.opened = True
            self._es.open_index(index.get_name())

    def close_index(self, index):
        """
        Method that closes an index.
        """

        if index.opened:
            index.opened = False
            self._es.close_index(index.get_name())

    def search(self, query, index=None, doc_type=None, **kwargs):
        return self._es.search(query, index, doc_type, **kwargs)
