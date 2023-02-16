import argparse
import csv

from furl import furl

from src.api.fetcher import Fetcher
from src.api.parser import Parser
from src.api.endpoint import ApiEndpoint
from src.api.v2.disposers.contracts.request import ContractRequest
from src.api.v2.disposers.contracts.response import ContractResponse
from src.api.v2.disposers.contracts.mapper import ContractMapper

parser = argparse.ArgumentParser(description='Collect contracts by EDRPOU')

parser.add_argument('--edrpou', help='The EDRPOU')
parser.add_argument('--since', help='The starting date (included) in format YYYY-MM-DD')
parser.add_argument('--till', help='The ending date (included) in format YYYY-MM-DD')

args = parser.parse_args()

api = ApiEndpoint(
    url=furl('https://api.spending.gov.ua/api/v2/disposers/contracts'),
    request_type=ContractRequest,
    response_type=ContractResponse,
)

fetcher = Fetcher(api=api)
parser = Parser(api=api)

request = ContractRequest(
    disposerId=args.edrpou,
    documentDateFrom=args.since,
    documentDateTo=args.till,
)

http_response = fetcher.get(request)
response = parser.parse(http_response)

extracted_responses = [ContractMapper.transform(item) for item in response]

with open('response.csv', 'w') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=ContractMapper.fieldnames())
    writer.writeheader()
    writer.writerows(extracted_responses)


