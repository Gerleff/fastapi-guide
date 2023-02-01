# fastapi-guide
## 00 Intro
Before proceed, make sure you have good undestanding about:
* Python basics
* _asyncio_ (also _threading_, _multiprocessing_)
* OSI (The Open Systems Interconnection model)
* HTTP (https://developer.mozilla.org/en/docs/Web/HTTP)

### 00 unicorn_app
In this module we are constructing simple ASGI web-application with Uvicorn support
The purpose of module is to understand which functionality is incapsulated into _uvicorn.run(...)_ and to review requirements towards asynchronious web framework before diving into one (**FastAPI**).

Supporting materials:
* Uvicorn docs (https://www.uvicorn.org/#why-asgi)
* ASGI intro (https://asgi.readthedocs.io/en/latest/introduction.html)

### 01 simple_app
In this module we are constructing simple FastAPI application
The purpose of module is to understand which functionality is provided by FastAPI by default for very simple functionality

Supporting materials:
* FastAPI docs (https://fastapi.tiangolo.com)

### 02 openapi_extended_app
In this module we are exploring features of OpenAPI docs generation
