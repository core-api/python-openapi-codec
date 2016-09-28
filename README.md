# OpenAPI Codec

**An OpenAPI codec for Core API.**

[![travis-image]][travis]
[![pypi-image]][pypi]

## Introduction

This is a Python [Core API][coreapi] codec for the [Open API][openapi] schema format, also known as "Swagger".

## Installation

Install using pip:

    $ pip install openapi-codec

## Creating Swagger schemas

To create a swagger schema from a `coreapi.Document`, use the codec directly.

    >>> from openapi_codec import OpenAPICodec
    >>> codec = OpenAPICodec()
    >>> schema = codec.encode(document)

## Using with the Python Client Library

Install `coreapi` and the `openapi-codec`.

    $ pip install coreapi
    $ pip install openapi-codec

To use the Python client library to interact with a service that exposes a Swagger schema,
include the codec in [the `decoders` argument][decoders].

    >>> from openapi_codec import OpenAPICodec
    >>> from coreapi.codecs import JSONCodec
    >>> from coreapi import Client
    >>> decoders = [OpenAPICodec(), JSONCodec()]
    >>> client = Client(decoders=decoders)

If the server exposes the schema without properly using an `application/openapi+json` content type, then you'll need to make sure to include `format='openapi'` on the initial request,
to force the correct codec to be used.

    >>> schema = client.get('http://petstore.swagger.io/v2/swagger.json', format='openapi')

At this point you can now start to interact with the API:

    >>> client.action(schema, ['pet', 'addPet'], params={'photoUrls': [], 'name': 'fluffy'})

## Using with the Command Line Client

Once the `openapi-codec` package is installed, the codec will automatically become available to the command line client.

    $ pip install coreapi-cli
    $ pip install openapi-codec
    $ coreapi codecs show
    Codec name   Media type                 Support              Package
    corejson   | application/coreapi+json | encoding, decoding | coreapi==2.0.7
    openapi    | application/openapi+json | encoding, decoding | openapi-codec==1.1.0
    json       | application/json         | decoding           | coreapi==2.0.7
    text       | text/*                   | decoding           | coreapi==2.0.7
    download   | */*                      | decoding           | coreapi==2.0.7

If the server exposes the schema without properly using an `application/openapi+json` content type, then you'll need to make sure to include `format=openapi` on the initial request, to force the correct codec to be used.

    $ coreapi get http://petstore.swagger.io/v2/swagger.json --format openapi
    <Swagger Petstore "http://petstore.swagger.io/v2/swagger.json">
        pet: {
            addPet(photoUrls, name, [status], [id], [category], [tags])
            deletePet(petId, [api_key])
            findPetsByStatus(status)
            ...

At this point you can start to interact with the API.

    $ coreapi action pet addPet --param name=fluffy --param photoUrls=[]
    {
        "id": 201609262739,
        "name": "fluffy",
        "photoUrls": [],
        "tags": []
    }

Use the `--debug` flag to see the full HTTP request and response.

    $ coreapi action pet addPet --param name=fluffy --param photoUrls=[] --debug
    > POST /v2/pet HTTP/1.1
    > Accept-Encoding: gzip, deflate
    > Connection: keep-alive
    > Content-Length: 35
    > Content-Type: application/json
    > Accept: application/coreapi+json, */*
    > Host: petstore.swagger.io
    > User-Agent: coreapi
    >
    > {"photoUrls": [], "name": "fluffy"}
    < 200 OK
    < Access-Control-Allow-Headers: Content-Type, api_key, Authorization
    < Access-Control-Allow-Methods: GET, POST, DELETE, PUT
    < Access-Control-Allow-Origin: *
    < Connection: close
    < Content-Type: application/json
    < Date: Mon, 26 Sep 2016 13:17:33 GMT
    < Server: Jetty(9.2.9.v20150224)
    <
    < {"id":201609262739,"name":"fluffy","photoUrls":[],"tags":[]}

    {
        "id": 201609262739,
        "name": "fluffy",
        "photoUrls": [],
        "tags": []
    }

[travis-image]: https://secure.travis-ci.org/core-api/python-openapi-codec.svg?branch=master
[travis]: http://travis-ci.org/core-api/python-openapi-codec?branch=master
[pypi-image]: https://img.shields.io/pypi/v/openapi-codec.svg
[pypi]: https://pypi.python.org/pypi/openapi-codec

[coreapi]: http://www.coreapi.org/
[openapi]: https://openapis.org/
[decoders]: http://core-api.github.io/python-client/api-guide/client/#instantiating-a-client
