# -*- coding: utf-8 -*-

import pprint
import unittest

from whoosh import qparser

from needlestack import base
from needlestack import exceptions
from needlestack.connections import manager
from needlestack.whoosh import fields
from needlestack.whoosh import index


class Index1(index.Index):
    content = fields.TextField()


class Index2(index.Index):
    content = fields.TextField()
    id = fields.IDField()


class Index3(index.Index):
    id = fields.IDField()
    tags = fields.KeyworkdField()
    content = fields.TextField()
    is_active = fields.BooleanField()
    number = fields.IntegerField()
    rate = fields.FloatField()
    text = fields.NGramWordsField()


class BasicTests(unittest.TestCase):
    def test_get_default_connection(self):
        from needlestack.whoosh.base import Whoosh
        connection = manager.get_connection("default")

        self.assertIsInstance(connection, Whoosh)

    def test_get_default_connection_twice(self):
        connection1 = manager.get_connection()
        connection2 = manager.get_connection()

        self.assertEqual(connection1, connection2)

    def test_get_inexistent_connection(self):
        from django.core.exceptions import ImproperlyConfigured

        with self.assertRaises(ImproperlyConfigured):
            connection = manager.get_connection("inexistent")


class IndexWhooshTests(unittest.TestCase):
    def test_create_destroy_index(self):
        connection = manager.get_connection()

        connection.create_index(Index1)

        with self.assertRaises(exceptions.IndexAlreadyExists):
            connection.create_index(Index1)

        connection.delete_index(Index1)


class IndexingDocumentsInWhooshTests(unittest.TestCase):
    def setUp(self):
        connection = manager.get_connection()
        connection.delete_all_indexes()
        connection.create_index(Index2)

    def tearDown(self):
        connection = manager.get_connection()
        connection.delete_all_indexes()

    def test_index_document(self):
        connection = manager.get_connection()

        connection.update(Index2, {"id": "1", "content": "Kaka"})

        response = connection.search("Kaka", index=Index2)
        self.assertEqual(len(response), 1)

    def test_index_document_using_string_resolve(self):
        connection = manager.get_connection()
        connection.update("index2", {"id": "1", "content": "Kaka"})

        response = connection.search("Kaka", index="index2")
        self.assertEqual(len(response), 1)

    def test_update_document(self):
        connection = manager.get_connection()

        connection.update("index2", {"id": "1", "content": "Kaka1"})
        connection.update("index2", {"id": "1", "content": "Kaka2"})
        response = connection.search("*", index="index2")

        self.assertEqual(len(response), 1)
        self.assertEqual(response.items[0].data["content"], "Kaka2")


class IndexingComplexDocumentsInWhooshTests(unittest.TestCase):
    def setUp(self):
        connection = manager.get_connection()
        connection.delete_all_indexes()
        connection.create_index(Index3)

    def tearDown(self):
        connection = manager.get_connection()
        connection.delete_all_indexes()

    def _create_document(self, id=1):
        document = {
            "id": str(id),
            "tags": "foo{0}, bar{0}".format(id),
            "content": "this is some content-{0}".format(id),
            "is_active": (id % 2 == 0),
            "number": id+1,
            "rate": id + 0.2,
            "text": "special content for ngram with id {0}".format(id),
        }

        return document

    def test_index_document_01(self):
        doc = self._create_document(id=1)

        connection = manager.get_connection()
        connection.update("index3", doc)

        result = connection.search("Kaka", index="index3")
        self.assertEqual(len(result), 0)

        result = connection.search("this is", index="index3")
        self.assertEqual(len(result), 0)

        result = connection.search("speci", index="index3")
        self.assertEqual(len(result), 1)

    def test_index_document_with_custom_parser_01(self):
        parser = qparser.QueryParser("text", Index3.get_schema())
        doc = self._create_document(id=1)

        connection = manager.get_connection()
        connection.update("index3", doc)

        result = connection.search("speci", index="index3", parser=parser)
        self.assertEqual(len(result), 1)

    def test_index_document_with_custom_parser_02(self):
        parser = qparser.QueryParser("number", Index3.get_schema())

        doc1 = self._create_document(id=1)
        doc2 = self._create_document(id=2)

        connection = manager.get_connection()
        connection.update("index3", doc1)
        connection.update("index3", doc2)

        result = connection.search("2", index="index3", parser=parser)
        self.assertEqual(len(result), 1)

        result = connection.search("2 OR 3", index="index3", parser=parser)
        self.assertEqual(len(result), 2)

    def test_index_document_with_custom_parser_03(self):
        parser = qparser.QueryParser("tags", Index3.get_schema())

        doc1 = self._create_document(id=1)
        doc2 = self._create_document(id=2)

        connection = manager.get_connection()
        connection.update("index3", doc1)
        connection.update("index3", doc2)

        result = connection.search("foo1", index="index3", parser=parser)
        self.assertEqual(len(result), 1)

        result = connection.search("foo1 OR bar2", index="index3", parser=parser)
        self.assertEqual(len(result), 2)
