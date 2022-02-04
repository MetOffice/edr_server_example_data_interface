# EDRDataInterface
The interface between [`edr-server`](https://github.com/ADAQ-AQI/edr-server) and real-world datasets that you wish to serve.

## Overview

This is an interface between real-world datasets that you wish to access via EDR (Environmental Data Retrieval) and the server implementation provided by [`edr_server`](https://github.com/ADAQ-AQI/edr-server). This interface provides a single dummy concrete implementation of the abstract interface provided in [edr-server/abstract_data_interface](...) that demonstrates how to utilise the abstract data interface to serve contents of actual datasets using `edr-server`.

## Using it

There are two options for using this interface:

1. fork it
1. copy into an existing codebase

### 1. Fork it

You can fork this repo and define your own concrete interface based on the example given in `dummy`:

* fork the repo to another GitHub Org
* duplicate the `dummy` directory and rename it relevant to the data you wish to serve
* replace the dummy example code with code that accesses your own data. Make sure to strictly follow the interface contract that `dummy` demonstrates or the EDR Server will error when you run it
* update the EDR Server config item `data.interface.name` with the name of the directory you created.

This option is good if you don't already have a mature codebase providing access to the datasets you wish to serve.

### 2. Copy into an existing codebase

You can also follow the interface pattern demonstrated by `dummy` but replicate the interface within an existing codebase:

* create a new directory within your existing codebase
* copy all the contents of `dummy` to this new directory and modify the code to access your own datasets. Make sure to strictly follow the interface contract or the EDR Server will error when you run it
* update the EDR Server config item `data.interface.path` with the importable path to the new directory you created.

This option is good if you already have a mature codebase for accessing your datasets and you do not wish to duplicate code for serving these datasets using EDR.
