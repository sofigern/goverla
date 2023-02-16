from dacite import from_dict
from src.api.endpoint import ApiEndpoint


class Parser:

    def __init__(self, api: ApiEndpoint) -> None:
        self.api = api

    def parse(self, http_response):
        result = None
        if http_response.status_code == 200:
            json_response = http_response.json()
            result = []
            for contract_json in json_response['documents']:
                result.append(from_dict(self.api.response_type, contract_json))

        return result