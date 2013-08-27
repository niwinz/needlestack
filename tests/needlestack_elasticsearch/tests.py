# -*- coding: utf-8 -*-

import unittest
from needlestack.connections import manager

from needlestack import base
from needlestack import exceptions
from needlestack.elasticsearch import fields
from needlestack.elasticsearch import index


class Index1(index.Index):
    content = fields.TextField()

class Index2(index.Index):
    content = fields.TextField()
    id = fields.IDField()


class BasicTests(unittest.TestCase):
    def test_get_default_connection(self):
        from needlestack.elasticsearch.base import ElasticSearch
        connection = manager.get_connection("default")

        self.assertIsInstance(connection, ElasticSearch)

    def test_get_default_connection_twice(self):
        connection1 = manager.get_connection()
        connection2 = manager.get_connection()

        self.assertEqual(connection1, connection2)

    def test_get_inexistent_connection(self):
        from django.core.exceptions import ImproperlyConfigured

        with self.assertRaises(ImproperlyConfigured):
            connection = manager.get_connection("inexistent")


class BasicIndexClassTests(unittest.TestCase):
    def test_index_name(self):
        class SomeIndex1(base.Index):
            _options = {"name": "some_index"}

        class SomeIndex2(base.Index):
            pass

        SomeIndex1.__name__ = "SomeIndex1"
        SomeIndex2.__name__ = "SomeIndex2"

        self.assertEqual(SomeIndex1.get_name(), "some_index")
        self.assertEqual(SomeIndex2.get_name(), "some_index2")

    def test_opened_methods(self):
        class SomeIndex(base.Index):
            pass

        SomeIndex.__name__ = "SomeIndex"

        self.assertFalse(SomeIndex.is_opened())

        SomeIndex.mark_opened()
        self.assertTrue(SomeIndex.is_opened())

        SomeIndex.mark_closed()
        self.assertFalse(SomeIndex.is_opened())


class IndexElasticSearchTests(unittest.TestCase):
    def test_create_destroy_index(self):
        connection = manager.get_connection()
        connection.create_index(Index1)

        with self.assertRaises(exceptions.IndexAlreadyExists):
            connection.create_index(Index1)

        connection.delete_index(Index1)


class IndexingDocumentsInElasticSearchTests(unittest.TestCase):
    def setUp(self):
        connection = manager.get_connection()
        connection.create_index(Index2)

    def tearDown(self):
        connection = manager.get_connection()
        connection.delete_index(Index2)

    def test_index_documents(self):
        connection = manager.get_connection()
        connection.update(Index2, {"id": "1", "content": "Kaka"})

        result = connection.search({"query": {"match_all":{}}}, index=Index2)
