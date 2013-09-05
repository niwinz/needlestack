# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, absolute_import

import sys
import warnings

from needlestack.base import _get_all_indexes, _load_all_indexes
from needlestack.connection import manager
from needlestack.exceptions import (IndexAlreadyExists,
                                    IndexDoesNotExists)

_min_verbosity_level = 1


def command(func):
    @functools.wraps(func)
    def _decorator(*args, **kwargs):
        # Inject manager as kwargs
        kwargs["manager"] = manager
        return func(*args, **kwargs)
    return _decorator


@command
def sync_indexes(backend="default", verbosity=0, **kwargs):
    """
    Synchronize all registred indexes to backend.
    """

    manager = kwargs["manager"]

    if verbosity >= _min_verbosity_level:
        print("Syncronizing indexes...", file=sys.stderr)

    connection = manager.get_connection(backend)
    for index in manager.get_all_indexes():
        try:
            connection.create_index(index)
            if verbosity > 0:
                print("Creating index '{0}'".format(index.get_name()), file=sys.stderr)
        except IndexAlreadyExists:
            if verbosity > 0:
                print("Index '{0}' already exists.".format(index.get_name()), file=sys.stderr)


@command
def drop_indexes(index=None, drop_all=False, backend="default", verbosity=0, **kwargs):
    """
    Delete all registred indexes from backend.

    :param str/list index: pass a list or one index for drop one concrete index.
    :param bool drop_all: run drop all available indexes (not only registred)

    :param backend: what backend use for execute this command
    :param verbosity: what verbosity set for this command execution
    """

    manager = kwargs["manager"]

    if verbosity >= _min_verbosity_level:
        print("Droping all registred indexes from current backend...", file=sys.stderr)

    connection = manager.get_connection(backend)
    if connection.vendor == "whoosh":
        warning_msg = ("Whoosh backend does not support real drop index command. "
                       "Alternatively it clears index content but does not eliminate it. "
                       "For real droping whoosh indexes, remove the index directory.")
        warnings.warn(warning_msg, DeprecationWarning)

    if drop_all:
        connection.delete_all_indexes()
    else:
        for index in manager.get_all_indexes():
            try:
                connection.drop_index(index)
                if verbosity > 0:
                    print("Deleting index '{0}'".format(index.get_name()), file=sys.stderr)
            except IndexDoesNotExists:
                if verbosity > 0:
                    print("Index '{0}' does not exist.".format(index.get_name()), file=sys.stderr)
