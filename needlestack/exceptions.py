# -*- coding: utf-8 -*-

class NeedleStackException(Exception):
    pass


class IndexDoesNotExists(NeedleStackException):
    pass


class IndexAlreadyExists(NeedleStackException):
    pass


