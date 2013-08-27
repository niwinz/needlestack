# -*- coding: utf-8 -*-

import unittest


class BasicTests(unittest.TestCase):
    def test_get_default_connection(self):
        from needlestack.connections import manager
        from needlestack.elasticsearch.base import ElasticSearch
        connection = manager.get_connection("default")

        self.assertIsInstance(connection, ElasticSearch)

    def test_get_default_connection_twice(self):
        from needlestack.connections import manager
        connection1 = manager.get_connection()
        connection2 = manager.get_connection()

        self.assertEqual(connection1, connection2)

    def test_get_inexistent_connection(self):
        from django.core.exceptions import ImproperlyConfigured
        from needlestack.connections import manager

        with self.assertRaises(ImproperlyConfigured):
            connection = manager.get_connection("inexistent")
