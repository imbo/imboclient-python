[![Build Status](https://travis-ci.org/imbo/imboclient-python.svg?branch=python3)](https://travis-ci.org/imbo/imboclient-python)
Python client for Imbo
======================

A client for Imbo written in Python for 3.4+


Installation
============

Install it directly from Github:

    pip install git+git://github.com/imbo/imboclient-python.git

Package will be deployed to pip repositories shortly, after a few planned backwards-compatible-break-inducing changes have been made to this client. See list of current issues on Github for an overview.


Usage
=====

For a quick overview of the current functionality refer to the integration tests that perform simple operations with the client (self._client) [here](https://raw.githubusercontent.com/imbo/imboclient-python/master/imboclient/test/unit/test_client.py)

The basic operations work at the moment, but the return-values from various functions are a bit incosistent and will be fixed in the near future.


Develop/Contribute to Python client for Imbo
============================================

Get the code and install dependencies:

    git clone git@github.com:imbo/imboclient-python.git
    cd imboclient-python && make install

Run the unit testsuite:

    make test

run the integration testsuite (NOTE: this requires a running imbo-instance as specified in imboclient/test/integration/config.py):

    make integration-test

- Keep it simple and easy to understand
- Solid test coverage
- PEP8

License
=======

Copyright (c) 2013, Andreas Søvik <arsovik@gmail.com>

Licensed under the MIT License



Contributions are very welcome, but please make sure your pull requests have test coverage.
