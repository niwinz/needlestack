# -*- coding: utf-8 -*-

class NeedleStackException(Exception):
    pass


class IndextDoesNotExists(NeedleStackException):
    pass


class IndexAlreadyExists(NeedleStackException):
    pass


