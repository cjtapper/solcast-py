**UNOFFICIAL AND UNMAINTAINED**

You can find the official Solcast Python SDK here: https://github.com/Solcast/solcast-api-python-sdk

==========
solcast-py
==========

A Python client library for the Solcast API for photovoltaic power and solar
radiation forecasting.

Installation
============

GitHub install
--------------
.. code-block:: bash

  $ git clone https://github.com/cjtapper/solcast-py
  $ cd solcast-py
  $ python setup.py install

Providing the API key
=====================

An API key is required to use the Solcast API. You can sign up for one at
https://solcast.com.au

There are multiple ways of providing the API key to solcast-py:

Setting an environment variable
-------------------------------
You can set the environment variable ``SOLCAST_API_KEY``:

.. code-block:: bash

  $ export SOLCAST_API_KEY=<insert your API key here> 

To persist this between sessions, add this line to your ``.bashrc`` (or equivalent).

Positional or keyword argument
------------------------------
Alternatively, you can pass the API key as the final positional argument, or the
keyword argument ``api_key``. For example:

.. code-block:: python

   >>> solcast.get_radiation_forecasts(-35, 149, 'INSERTYOURAPIKEYHERE')

or:

.. code-block:: python

   >>> solcast.get_pv_power_forecasts(-35, 149, capacity=2000, api_key='INSERTYOURAPIKEYHERE')

