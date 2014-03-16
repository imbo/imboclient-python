[![Build Status](https://travis-ci.org/andreasrs/ImboclientPython.png?branch=master)](https://travis-ci.org/andreasrs/ImboclientPython)

Python client for Imbo
======================

A client for Imbo written in Python


License
=======

Copyright (c) 2013, Andreas Søvik <arsovik@gmail.com>

Licensed under the MIT License


Installation
============

Package will be deployed to pip repositories shortly, after a few backwards-compatible-break-inducing changes have been made to this client. See list of current issues on Github for an overview.
Until then you can install it directly from Github:

pip install git+git://github.com/andreasrs/ImboclientPython.git

Only Python 2.7 is tested/verified at the moment, virtualenv is recommended.

USAGE
=====

For a quick overview of the current functionality refer to the integration tests that perform simple operations with the client (self._client) [here](https://github.com/andreasrs/ImboclientPython/blob/master/imboclient/test/integration/test_client.py)

The basic operations work at the moment, but the return-values from various functions are a bit incosistent and will be fixed in the near future.


Develop/Contribute to Python client for Imbo
============================================

Get the code and install dependencies:
    git clone git@github.com:andreasrs/ImboclientPython.git
    cd ImboclientPython && make install

Run the unit testsuite:
    make test

run the integration testsuite (NOTE: this requires a running imbo-instance as specified in imboclient/test/integration/config.py):
    make integration-test

Contributions are very welcome, but please make sure your pull requests have test coverage.
