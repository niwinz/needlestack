# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals

from django.core.management.base import BaseCommand, CommandError
from needlestack import commands


class Command(BaseCommand):
    help = 'Sync all defined indexes with a current backend'
    option_list = BaseCommand.option_list + (
                        make_option('--backend',
                                    action='store',
                                    dest='backend',
                                    default='default'),)

    def handle(self, *args, **options):
        commands.sync_indexes(options["backend"], options["verbosity"])
