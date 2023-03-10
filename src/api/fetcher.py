from dataclasses import asdict
from copy import deepcopy

import requests

from src.api.endpoint import ApiEndpoint


class Fetcher:

    def __init__(self, api: ApiEndpoint) -> None:
        self.api = api

    def get(self, request):
        url = deepcopy(self.api.url)
        http_response = requests.get(
            url.add(asdict(request)).url
        )

        return http_response

    def get_url(self, request):
        url = deepcopy(self.api.url)
        return url.add(asdict(request)).url
