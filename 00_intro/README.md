# fastapi-guide
## 00 Intro
Before proceed, make sure you have good undestanding about:
* Python basics
* _asyncio_ module (also _threading_, _multiprocessing_)
* OSI (The Open Systems Interconnection model)
* HTTP (https://developer.mozilla.org/en/docs/Web/HTTP)
* RESTful (https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
* English language on read-the-docs level

### 00 unicorn_app
In this module we are constructing simple ASGI web-application with Uvicorn support
The purpose of module is to understand which functionality is incapsulated into _uvicorn.run(...)_ and to review requirements towards asynchronious web framework before diving into one (**FastAPI**).

Supporting materials:
* asyncio server docs (https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server)
* Uvicorn docs (https://www.uvicorn.org/#why-asgi)
* ASGI intro (https://asgi.readthedocs.io/en/latest/introduction.html)

### 01 simple_app
In this module we are constructing simple FastAPI application
The purpose of module is to understand which functionality is provided by FastAPI by default for very simple functionality

Supporting materials:
* FastAPI docs (https://fastapi.tiangolo.com)

### 02 openapi_extended_app
In this module we are exploring features of OpenAPI docs generation
