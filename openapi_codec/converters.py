from six.moves.urllib.parse import urlparse


class DocumentToOpenAPIConverter(object):
    def __init__(self, document):
        self.document = document

    def convert(self):
        return self._generate_swagger_object()

    def _generate_swagger_object(self):
        """
        Generates root of the Swagger spec.
        """
        parsed_url = urlparse(self.document.url)

        return {
            'swagger': '2.0',
            'info': self._get_info_object(),
            'paths': self._get_paths_object(),
            'host': parsed_url.netloc,
        }

    def _get_info_object(self):
        return {
            'title': self.document.title,
            'version': ''  # Required by the spec
        }

    def _get_paths_object(self):
        paths = {}
        for tag, object_ in self.document.data.items():
            if not hasattr(object_, 'links'):
                continue

            for link in object_.links.values():
                if link.url not in paths:
                    paths[link.url] = {}

                operation = self._get_operation(tag, link)
                paths[link.url].update({link.action: operation})

        return paths

    @classmethod
    def _get_operation(cls, tag, link):
        return {
            'tags': [tag],
            'description': link.description,
            'responses': cls._get_responses(link.action),
            'parameters': cls._get_parameters(link.fields)
        }

    @classmethod
    def _get_parameters(cls, fields):
        """
        Generates Swagger Parameter Item object.
        """
        return [
            {
                'name': field.name,
                'required': field.required,
                'in': cls._convert_location_to_in(field.location),
                'description': field.description,
                'type': 'string'
            }
            for field in fields
        ]

    @classmethod
    def _convert_location_to_in(cls, location):
        """
        Translates the CoreAPI field `location` into the Swagger `in`.
        The values are all the same with the exception of form -> formData.
        """
        if location == 'form':
            return 'formData'

        return location

    @classmethod
    def _get_responses(cls, action):
        """
        Returns minimally acceptable responses object based
        on action / method type.
        """
        template = {'description': ''}
        if action == 'post':
            return {'201': template}
        if action == 'delete':
            return {'204': template}

        return {'200': template}
