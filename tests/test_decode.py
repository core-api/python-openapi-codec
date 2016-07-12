from coreapi import Document
from openapi_codec import OpenAPICodec
import os


test_filepath = os.path.join(os.path.dirname(__file__), 'petstore.json')


def test_decode():
    test_content = open(test_filepath, 'rb').read()
    codec = OpenAPICodec()
    document = (codec.load(test_content))
    assert isinstance(document, Document)
    assert set(document.keys()) == set(['pet', 'store', 'user'])
    assert document.title == 'Swagger Petstore'
