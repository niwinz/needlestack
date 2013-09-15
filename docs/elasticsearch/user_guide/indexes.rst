=======
Indexes
=======

The first unit of work of needlestack is a Index object. Unlike haystack,
with needlestack each defined index is represented as separate index on the
search backend (ElasticSearch).

Also, indexes aren't created automatically. You must execute **ns_sync_indexes** for
create indexed (defined on your django project) on elasticsearch. Needlestack exposes
more commands, and you can see :ref:`Commands <commands>` section.

This is a simple example of index definition:

.. code-block:: python

    from needlestack.elasticsearch import index
    from needlestack.elasticsearch import fields

    class MyIndex(index.Index):
        id = fields.IDField()
        content = fields.TextField()

You should put this index definition on your **some_app/indexes.py** file, otherwise
on you execute `ns_sync_indexes` command, indexes defined in other location, not
be syncronized.

You can see all available fields for elastisearch on :ref:`Fields <elasticsearch-fields>`
section.


.. note::

    Each backend available on needlestack have own fields and indexes, and you can not
    use eg. whoosh indexes with elasticsearch backend.


