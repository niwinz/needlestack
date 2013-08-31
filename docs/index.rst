needlestack
===========

Modular search api for Django.

.. note::

    This package experiment and does not have stable code.


This package is like django-haystack but significant differences on the philosofy. One of main
differences is that **needlestack** is not django orm centred.

Full list of **needlestack** goals:

- Access to mostly all features of each supported backend.
- Python3 as main language but with python2.7 support for some time.
- Small and clean codebase as possible.
- Not centred on django orm (can index documents from other data sources)
- Any other good idea?


.. note::

    **needlestack** does not provide simple way to switching from one search backend to other.
    Each supported backend has own features and distinct way to declare indexes. This has advantages
    and disadvantages, but how many times we change the search backend?

    This approach allows avoid implementing a common feature group of all supported backends  so allowing
    to give more low level and feature complete access of each supported backend.


Supported backends and their documentation:
-------------------------------------------

.. toctree::
    :maxdepth: 1

    elasticsearch/index
