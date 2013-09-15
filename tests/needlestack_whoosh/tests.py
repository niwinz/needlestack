# -*- coding: utf-8 -*-

import pprint
import unittest

from needlestack.connections import manager

from needlestack import base
from needlestack import exceptions
from needlestack.whoosh import fields
from needlestack.whoosh import index

class Index1(index.Index):
    content = fields.TextField()


class Index2(index.Index):
    content = fields.TextField()
    id = fields.IDField()


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
