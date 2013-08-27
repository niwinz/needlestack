# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import functools
import re

from importlib import import_module
from django.core.exceptions import ImproperlyConfigured


def load_class(path):
    """
    Load class from path.
    """

    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except AttributeError as e:
        raise ImproperlyConfigured('Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured(
                'Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))

    return klass


def un_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
