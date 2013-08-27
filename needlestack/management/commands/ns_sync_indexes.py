# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals

import sys

from django.core.management.base import BaseCommand, CommandError

from needlestack.base import _get_all_indexes
from needlestack.connection import manager
from needlestack.exceptions import IndexAlreadyExists


class Command(BaseCommand):
    help = 'Sync all defined indexes with a current backend'
    option_list = BaseCommand.option_list + (
                        make_option('--backend',
                                    action='store',
                                    dest='backend',
                                    default='default'),)

    def handle(self, *args, **options):
        print("Syncronizing indexes...", file=sys.stderr)

        connection = manager.get_connection(options["backend"])
        for index in _get_all_indexes()
            try:
                connection.create_index(index)
                print("Creating index '{0}'".format(index.get_name()), file=sys.stderr)
            except IndexAlreadyExists:
                print("Index '{0}' already exists.".format(index.get_name()), file=sys.stderr)
