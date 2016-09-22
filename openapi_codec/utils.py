def get_method(link):
    method = link.action.lower()
    if not method:
        method = 'get'
    return method


def get_encoding(link):
    encoding = link.encoding
    has_body = any([get_location(link, field) in ('form', 'body') for field in link.fields])
    if not encoding and has_body:
        encoding = 'application/json'
    elif encoding and not has_body:
        encoding = ''
    return encoding


def get_location(link, field):
    location = field.location
    if not location:
        if get_method(link) in ('get', 'delete'):
            location = 'query'
        else:
            location = 'form'
    return location
