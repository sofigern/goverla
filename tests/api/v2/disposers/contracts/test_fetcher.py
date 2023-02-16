from dataclasses import asdict
from unittest import TestCase

from furl import furl

from src.api.fetcher import Fetcher
from src.api.endpoint import ApiEndpoint
from src.api.v2.disposers.contracts.request import ContractRequest
from src.api.v2.disposers.contracts.response import ContractResponse
from src.api.utils.json2csv import json_to_csv


class TestAPIDisposersContractsFetch(TestCase):

    def test_fetch(self):
        edrpou = '00013480'
        documentDateFrom = '2022-12-01'
        documentDateTo = '2022-12-21'

        api = ApiEndpoint(
            url=furl('https://api.spending.gov.ua/api/v2/disposers/contracts'),
            request_type=ContractRequest,
            response_type=ContractResponse,
        )

        fetcher = Fetcher(api=api)

        request = ContractRequest(
            disposerId=edrpou,
            documentDateFrom=documentDateFrom,
            documentDateTo=documentDateTo,
        )

        responses = fetcher.get(request)

        json = [asdict(contract) for contract in responses]
        # csv_rows = json_to_csv(
        #     json=,
        #     destination_path='.',
        #     template_csv_path='/Users/sofigenr/src/goverla/src/api/v2/disposers/contracts/resources/contract_headers_template.csv'
        # )
        pass
