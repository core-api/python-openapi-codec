import uuid

import coreapi
from openapi_codec.converters import DocumentToOpenAPIConverter

from .compat import mock, TestCase


class TestGetInfoObject(TestCase):
    def setUp(self):
        self.document = coreapi.Document(title='Example API')
        converter = DocumentToOpenAPIConverter(self.document)
        self.sut = converter._get_info_object()

    def test_title(self):
        self.assertDictContainsSubset({'title': self.document.title}, self.sut)

    def test_version(self):
        """
        Ensures that the version is provided since it is a required field.
        """
        self.assertDictContainsSubset({'version': ''}, self.sut)


class TestGetPathsObject(TestCase):
    def setUp(self):
        self.path = '/users'
        self.document = coreapi.Document(
            content={
                'users': {
                    'create': coreapi.Link(
                        action='post',
                        url=self.path
                    ),
                    'list': coreapi.Link(
                        action='get',
                        url=self.path
                    )
                }
            }
        )
        self.sut = DocumentToOpenAPIConverter(self.document) \
            ._get_paths_object()

    def test_url_is_converted_to_key(self):
        self.assertIn(self.path, self.sut)

    def test_actions_are_converted_to_keys_under_url(self):
        expected = [
            link.action for link in self.document.data['users'].values()
        ]
        self.assertCountEqual(expected, self.sut[self.path].keys())


class TestGetParameters(TestCase):
    def setUp(self):
        self.field = coreapi.Field(
            name='email',
            required='true',
            location='query',
            description='A valid email address.'
        )
        patcher = mock.patch.object(
            DocumentToOpenAPIConverter,
            '_convert_location_to_in'
        )
        self.location_mock = patcher.start()
        self.addCleanup(patcher.stop)

        self.sut = DocumentToOpenAPIConverter \
            ._get_parameters([self.field])[0]

    def test_expected_fields(self):
        self.assertDictContainsSubset(
            {
                'name': self.field.name,
                'required': self.field.required,
                'in': self.location_mock.return_value,
                'description': self.field.description,
                'type': 'string'  # Everything is a string for now.
            },
            self.sut
        )


class TestConvertLocationToIn(TestCase):
    def setUp(self):
        self.sut = DocumentToOpenAPIConverter._convert_location_to_in

    def test_form_is_converted_to_formdata(self):
        self.assertEqual('formData', self.sut('form'))

    def test_random_string_is_returned_as_is(self):
        """
        Asserts that any input (other than form) is returned as-is,
        since the Swagger Parameter object `in` property maps 1:1 with
        the Field.location property,
        """
        expected = str(uuid.uuid4())
        self.assertEqual(expected, self.sut(expected))


class TestGetResponses(TestCase):
    def setUp(self):
        self.sut = DocumentToOpenAPIConverter._get_responses

    def test_post(self):
        self.assertDictEqual({'201': {'description': ''}}, self.sut('post'))

    def test_delete(self):
        self.assertDictEqual({'201': {'description': ''}}, self.sut('post'))

    def test_default(self):
        self.assertDictEqual(
            {'200': {'description': ''}},
            self.sut(uuid.uuid4())
        )
