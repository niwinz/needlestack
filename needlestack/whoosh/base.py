# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import os
import os.path

from django.utils import six
from whoosh import filedb
from whoosh.writing import AsyncWriter

from .. import base
from .. import utils
from .. import exceptions

from . import fields
from . import result


class Whoosh(base.SearchBackend):
    def __init__(self, storage='whoosh.filedb.filestore.FileStorage',
                 *args, **kwargs):

        storage_cls = utils.load_class(storage)
        self._storage = storage_cls(*args, **kwargs)
        self._storage.create()

    def exists_index(self, index):
        index = base._resolve_index(index)
        return self._storage.index_exists(index.get_name())

    def create_index(self, index, overwrite=False):
        index = base._resolve_index(index)

        if not overwrite and self.exists_index(index):
            raise exceptions.IndexAlreadyExists(
                    "index {0} already exists".format(index.get_name()))

        return self._storage.create_index(indexname=index.get_name(),
                                          schema=index.get_schema())
    def delete_index(self, index):
        # Whoosh does not implement individual index removing
        # mechanism
        pass

    def delete_all_indexes(self):
        self._storage.clean()

    def update(self, index, document, **options):
        index = base._resolve_index(index)

        ix = storage.open_index(indexname=index.get_name())
        writer = AsyncWriter(ix)

        adapted_document = index.adapt_document(document)
        writer.update_document(**adapt_document)
        writer.commit()

    def update_bulk(self, index, documents):
        index = base._resolve_index(index)

        index.ix = storage.open_index(indexname=index.get_name())
        writer = AsyncWriter(ix)

        adapted_documents = (index.adapt_document(doc)
                                for doc in documents)
        for doc in adapted_documents:
            writer.update_document(**doc)

        writer.commit()

    def search(self, query_string, index, parser=None, **kwargs):
        index = base._resolve_index(index)
        if parser is None:
            parser = MultifieldParser(fieldnames=index.get_searchable_fieldnames(),
                                      schema=index.get_schema())

        query = parser.parse(query_string)
        return self._search(query, index, **kwargs)

    def _search(self, query, index, method="search"):
        with index.get_searcher() as searcher:
            return getattr(searcher, method)(query, **kwargs)
