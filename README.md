# EDRDataInterface
The interface between [`edr_server`](https://github.com/ADAQ-AQI/edr-server) and real-world datasets that you wish to serve.

## Overview

This is an interface between real-world datasets that you wish to serve using EDR, and the abstract implementation of a server found in [`edr_server`](https://github.com/ADAQ-AQI/edr-server). The interface presents an abstract reference implementation for the interface (including any common functionality for the interface), and a single concrete implementation (called `dummy`). This demonstrates how the interface could be used in practice to represent your data.

## Using it

Duplicate the `dummy` implementation and customise it to connect to and serve your data. In [`edr_server`](https://github.com/ADAQ-AQI/edr-server), specify the name of your concrete implementation in [`config.yml`](https://github.com/ADAQ-AQI/edr-server/blob/main/etc/config.yml) in the entry `data.interface.name`.
