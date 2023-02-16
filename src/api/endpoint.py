from furl import furl


class ApiEndpoint:

    def __init__(
        self,
        url: furl,
        request_type,
        response_type,
    ):
        self.url = url
        self.request_type = request_type
        self.response_type = response_type
