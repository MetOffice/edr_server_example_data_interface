# About the `dummy` dataset

The dummy dataset exists for the sole purpose of demonstrating how to write a data interface for the EDR Server to allow the EDR Server to present and serve the contents of the dataset to users of the server.

## Important

The interface for the dummy dataset should not be considered a reference interface. It is simply an interface that enables the fake data provided in `dataset.py` (as a series of inter-referenced dictionaries of metadata and two functions for generating trigonometric data) to be translated into the interface expected by the EDR Server.

## About the interface to the EDR Server

The interface between the EDR Server and any data interface is composed of a series of predefined classes in predefined Python modules, which return predefined dataclass instances. The classes, modules and dataclasses are all provided in the abstract data interface section of the EDR Server library. 

The abstract data interface provides the abstract implementations of all these elements, which must be subclassed in any concrete data interface, such as the `dummy` data interface here. All classes have a `data` method, which returns one or more concrete instances of a dataclass, which is defined by each `data` method's type hint. This hint _must not be ignored_ as the dataclass(es) returned contain all the information necessary to populate the JSON template appropriate for the request that has been made of the server. If the data interface returns the wrong thing, the server will error.

## What is needed

Thus, of all the things presented in this dummy interface, you do need to replicate the following elements in an interface to your own data:

* the `__init__.py` file needs to import all top-level classes that are used by the server, otherwise the programmatic imports will fail in the server code.
* You need to have a Python module in place for each of the elements of the EDR specification expected by the server. The list currently is:
  * `admin.py` - for requesting a updated set of collections metadata files
  * `capabilities.py` and `service.py` - for handling capabilities and service requests
  * `locations.py` - for handling locations requests, and
  * `items.py` - for handling item requests.
* Each of these Python modules also needs valid implementations of one or more Python classes that are importable by the server and have a `data` method that returns one or more dataclass instances containing the information needed for populating a JSON template to use as the response to the server request. The list of classes currently is:
  * `admin.py` - `RefreshCollections` (which does not have a `data` method due to having a slightly different purpose)
  * `capabilities.py` and `service.py` - `API` (not currently implemented), `Capabilities`, `Conformance` and `Service`
  * `locations.py` - `Locations` and `Location`
  * `items.py` - `Items` and `Item`.
* Many of the abstract implementations of these classes contain other methods as well that are often not implemented in the abstract. This implies that the functionality will be needed for all concrete instances of these classes, but will be bespoke to each instance. Sometimes a reference implementation is provided, but you may override the reference implementation if your use-case requires it.
* You can also add other methods to these classes that enable the interface to your data to function, if they are required, but you will need to eventually call them within your implementation of the `data` method for that class to ensure these methods are utilised.
* **You will need to provide your own code that loads your data that you wish to serve and translates it to match these interfaces. This code will be unique for every dataset served, which is why this code cannot be embedded into the EDR Server, but instead needs a separate interface for each dataset.**

## What isn't needed

* Everything not in the list above.
* Notably, this includes `dataset.py` and all its contents, which are just there to provide something to serve.
* Any code within any of the classes that's specifically there to interface with `dataset.py`, or any of its contents.
