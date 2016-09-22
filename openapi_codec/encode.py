from coreapi.compat import urlparse
from openapi_codec.utils import get_method, get_encoding, get_location


def generate_swagger_object(document):
    """
    Generates root of the Swagger spec.
    """
    parsed_url = urlparse.urlparse(document.url)

    return {
        'swagger': '2.0',
        'info': _get_info_object(document),
        'paths': _get_paths_object(document),
        'host': parsed_url.netloc,
        'schemes': [parsed_url.scheme]
    }


def _get_info_object(document):
    return {
        'title': document.title,
        'version': ''  # Required by the spec
    }


def _get_paths_object(document):
    paths = {}

    # Top-level links. We do not include a swagger 'tag' for these.
    for operation_id, link in document.links.items():
        if link.url not in paths:
            paths[link.url] = {}

        method = get_method(link)
        operation = _get_operation(link, operation_id)
        paths[link.url].update({method: operation})

    # Second-level links. We include a swagger 'tag' for these.
    for tag, object_ in document.data.items():
        if not hasattr(object_, 'links'):
            continue

        for operation_id, link in object_.links.items():
            if link.url not in paths:
                paths[link.url] = {}

            method = get_method(link)
            operation = _get_operation(link, operation_id, tags=[tag])
            paths[link.url].update({method: operation})

    return paths


def _get_operation(link, operation_id, tags=None):
    encoding = get_encoding(link)

    operation = {
        'operationId': operation_id,
        'description': link.description,
        'responses': _get_responses(link),
        'parameters': _get_parameters(link, encoding)
    }
    if encoding:
        operation['consumes'] = [encoding]
    if tags:
        operation['tags'] = tags
    return operation


def _get_parameters(link, encoding):
    """
    Generates Swagger Parameter Item object.
    """
    parameters = []
    properties = {}
    required = []

    for field in link.fields:
        location = get_location(link, field)
        if location == 'form':
            if encoding in ('multipart/form-data', 'application/x-www-form-urlencoded'):
                parameter = {
                    'name': field.name,
                    'required': field.required,
                    'in': 'formData',
                    'description': field.description,
                    'type': 'string'
                }
                parameters.append(parameter)
            else:
                schema_property = {
                    'description': field.description
                }
                properties[field.name] = schema_property
                if field.required:
                    required.append(field.name)
        elif location == 'body':
            if encoding == 'application/octet-stream':
                # https://github.com/OAI/OpenAPI-Specification/issues/50#issuecomment-112063782
                schema = {'type': 'string', 'format': 'binary'}
            else:
                schema = {}
            parameter = {
                'name': field.name,
                'required': field.required,
                'in': location,
                'description': field.description,
                'schema': schema
            }
            parameters.append(parameter)
        else:
            parameter = {
                'name': field.name,
                'required': field.required,
                'in': location,
                'description': field.description,
                'type': 'string'
            }
            parameters.append(parameter)

    if properties:
        parameters.append({
            'name': 'data',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': properties,
                'required': required
            }
        })

    return parameters


def _get_in(link, field):
    in_location = get_location(link, field)
    if in_location == 'form':
        return 'formData'
    return in_location


def _get_responses(link):
    """
    Returns minimally acceptable responses object based
    on action / method type.
    """
    template = {'description': ''}
    if link.action == 'post':
        return {'201': template}
    if link.action == 'delete':
        return {'204': template}
    return {'200': template}
