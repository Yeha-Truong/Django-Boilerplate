from more_itertools import collapse

from . import utils


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        # logging.error(msg="Handled by middleware: ")

        # return HttpResponse(
        #     utils.generateHttpResponse(
        #         error="uwu! Something's wrong with our server, uwu!"
        #     ),
        #     status=500,
        # )
        pass


class ResponseFormatterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_template_response(self, request, response):
        hasRenderType = hasattr(response, "accepted_media_type")
        if hasRenderType:
            accepted_media_type = response.accepted_media_type
            if accepted_media_type == "application/json":
                hasData = hasattr(response, "data")
                if hasData:
                    data = response.data
                    isDict = isinstance(data, dict)
                    isStr = isinstance(data, str)
                    skip = True

                    if isDict:
                        skip = False
                        hasSkipStatus = "skipResponseFormatter" in data

                        if hasSkipStatus:
                            skip = data["skipResponseFormatter"]
                            del data["skipResponseFormatter"]

                    elif isStr:
                        skip = False

                    if not skip:
                        if response.status_code >= 200 and response.status_code < 300:
                            data = {
                                "result": data,
                                "error": None,
                                "message": None,
                            }
                        elif response.status_code >= 400:
                            message = None
                            if isDict:
                                message = collapse(data.values())
                            else:
                                message = data
                            data = {
                                "result": None,
                                "error": data,
                                "message": message,
                            }

                        response.data = data
        return response
