from dataclasses import asdict

import requests

from src.api.endpoint import ApiEndpoint


class Fetcher:

    def __init__(self, api: ApiEndpoint) -> None:
        self.api = api

    def get(self, request):
        http_response = requests.get(
            self.api.url.add(asdict(request)).url
        )

        return http_response
