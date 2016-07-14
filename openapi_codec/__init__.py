import json

from coreapi.codecs.base import BaseCodec
from coreapi.compat import force_bytes
from coreapi.document import Document
from coreapi.exceptions import ParseError
from openapi_codec.encode import generate_swagger_object
from openapi_codec.decode import _parse_document


__version__ = "1.0.0"


class OpenAPICodec(BaseCodec):
    media_type = "application/openapi+json"
    supports = ['encoding', 'decoding']

    def load(self, bytes, base_url=None):
        """
        Takes a bytestring and returns a document.
        """
        try:
            data = json.loads(bytes.decode('utf-8'))
        except ValueError as exc:
            raise ParseError('Malformed JSON. %s' % exc)

        doc = _parse_document(data, base_url)
        if not isinstance(doc, Document):
            raise ParseError('Top level node must be a document.')

        return doc

    def dump(self, document, **kwargs):
        data = generate_swagger_object(document)
        return force_bytes(json.dumps(data))
