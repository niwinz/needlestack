# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, absolute_import

import sys

from needlestack.base import _get_all_indexes, _load_all_indexes
from needlestack.connection import manager
from needlestack.exceptions import (IndexAlreadyExists,
                                    IndexDoesNotExists)

_min_verbosity_level = 1


def sync_indexes(backend="default", verbosity=0):
    """
    Synchronize all registred indexes to backend.
    """

    if verbosity >= _min_verbosity_level:
        print("Syncronizing indexes...", file=sys.stderr)

    _load_all_indexes()
    indexes = _get_all_indexes()

    connection = manager.get_connection(backend)
    for index in indexes:
        try:
            connection.create_index(index)
            if verbosity > 0:
                print("Creating index '{0}'".format(index.get_name()), file=sys.stderr)
        except IndexAlreadyExists:
            if verbosity > 0:
                print("Index '{0}' already exists.".format(index.get_name()), file=sys.stderr)


def drop_indexes(backend="default", verbosity=0):
    """
    Delete all registred indexes from backend.
    """

    if verbosity >= _min_verbosity_level:
        print("Droping all registred indexes from current backend...", file=sys.stderr)

    connection = manager.get_connection(backend)

    _load_all_indexes()
    indexes = _get_all_indexes()

    for index in indexes:
        try:
            connection.drop_index(index)
            if verbosity > 0:
                print("Deleting index '{0}'".format(index.get_name()), file=sys.stderr)
        except IndexDoesNotExists:
            if verbosity > 0:
                print("Index '{0}' does not exist.".format(index.get_name()), file=sys.stderr)
