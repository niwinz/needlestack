=============
Configuration
=============

The first step to get it work, you must configure your django application with elasticsearch
connection parameters.

This is a simple example of a basic configuration for ElasticSearch backend:

.. code-block:: python

    NEEDLESTACK_CONNECTIONS = {
        "default": {
            "engine": "needlestack.elasticsearch.base.ElasticSearch",
            "options": {
                "urls": "http://localhost:9200",
                "settings": {}
            }
        }
    }


**settings** attribute should contain any kwargs that pyelasticsearch_ accepts on
it's constructor.

.. _pyelasticsearch: http://pyelasticsearch.readthedocs.org/en/latest/api/#pyelasticsearch.ElasticSearch

