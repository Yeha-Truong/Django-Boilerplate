from more_itertools import collapse
from rest_framework.views import exception_handler as rest_exception_handler

from . import utils


def exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = rest_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        data = response.data
        message = collapse(data.values())
        data = utils.generateHttpResponse(error=data, message=message)

        response.data = data

    return response
