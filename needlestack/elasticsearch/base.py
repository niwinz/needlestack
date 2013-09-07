# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import pprint

from django.utils import six

import pyelasticsearch
import pyelasticsearch.exceptions

from .. import base
from .. import exceptions

from . import fields
from . import result


class ElasticSearch(base.SearchBackend):
    vendor = "elasticsearch"

    _es = None # ElasticSearch backend connection
    _default_settings = None # default index settings

    def __init__(self, urls, settings, *args, **kwargs):
        self._default_settings = settings
        self._es = pyelasticsearch.ElasticSearch(urls, *args, **kwargs)

    def get_data_from_model(self, index, model):
        index = base._resolve_index(index)

        data = {}

        for field_name in index._meta.fields:
            data[field_name] = getattr(model, field_name, None)

        return data

    def update(self, index, document, **options):
        """
        Method for create or update document on the
        index.
        """

        index = base._resolve_index(index)

        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', index.get_doc_type())

        id, adapted_document = index.adapt_document(document)

        if id:
            options.setdefault("id", id)

        self._es.index(index_name, index_doc_type, adapted_document, **options)

    def update_bulk(self, index, documents, **options):
        index = base._resolve_index(index)

        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', index.get_doc_type())

        adapted_documents = [doc for id, doc in
                                (index.adapt_document(doc, keep_id=True)
                                    for doc in documents)]

        self._es.bulk_index(index_name, index_doc_type, adapted_documents,
                            id_field="_id", **options)

    def get(self, index, id, **options):
        index = base._resolve_index(index)

        index_name = index.get_name()
        index_doc_type = options.pop('doc_type', index.get_doc_type())
        return self._es.get(index_name, index_doc_type, id, **options)

    def delete_index(self, index):
        index = base._resolve_index(index)

        index_name = index.get_name()
        try:
            self._es.delete_index(index_name)
        except pyelasticsearch.exceptions.ElasticHttpNotFoundError as e:
            raise exceptions.IndexDoesNotExists("{0} not found".format(index_name)) from e

    def delete_all_indexes(self):
        raise NotImplementedError("TODO")

    def create_index(self, index, settings=None):
        index = base._resolve_index(index)

        mappings = index.get_mappings()

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
        index = base._resolve_index(index)

        if not index.opened:
            index.opened = True
            self._es.open_index(index.get_name())

    def close_index(self, index):
        """
        Method that closes an index.
        """
        index = base._resolve_index(index)

        if index.opened:
            index.opened = False
            self._es.close_index(index.get_name())

    def search(self, query, index=None, **kwargs):
        """
        Send query to elasticsearch and return a result.

        :param dict query: elasticsearch dsl query.
        :param index.Index index: a index to use for search.
        :param int offset: same as 'from' param of elasticsearch api.
        :param int size: number of element to get.

        :returns: search result response instance.
        :rtype: :py:`~needlestack.elasticsearch.result.SearchResult`
        """

        index = base._resolve_index(index)

        if index is not None:
            index = index.get_name()

        if "offset" in kwargs:
            kwargs["es_from"] = kwargs.pop("offset")

        result_data = self._es.search(query, index=index, **kwargs)
        return result.SearchResult(result_data)

    def refresh(self, index):
        index = base._resolve_index(index)
        self._es.refresh(index.get_name())
