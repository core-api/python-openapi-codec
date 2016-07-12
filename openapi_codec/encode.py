from coreapi.compat import urlparse


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
    }


def _get_info_object(document):
    return {
        'title': document.title,
        'version': ''  # Required by the spec
    }


def _get_paths_object(document):
    paths = {}
    for tag, object_ in document.data.items():
        if not hasattr(object_, 'links'):
            continue

        for link in object_.links.values():
            if link.url not in paths:
                paths[link.url] = {}

            operation = _get_operation(tag, link)
            paths[link.url].update({link.action: operation})

    return paths


def _get_operation(tag, link):
    return {
        'tags': [tag],
        'description': link.description,
        'responses': _get_responses(link),
        'parameters': _get_parameters(link.fields)
    }


def _get_parameters(fields):
    """
    Generates Swagger Parameter Item object.
    """
    return [
        {
            'name': field.name,
            'required': field.required,
            'in': _convert_location_to_in(field),
            'description': field.description,
            'type': 'string'
        }
        for field in fields
    ]


def _convert_location_to_in(field):
    if field.location == 'form':
        return 'formData'
    return field.location


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
