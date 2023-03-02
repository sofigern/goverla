import csv
from dataclasses import asdict
from itertools import count

import ujson

from furl import furl
from django.shortcuts import render

from src.api.endpoint import ApiEndpoint
from src.api.fetcher import Fetcher
from src.api.parser import Parser_Transactions

from src.api.v2.transactions.mapper import TransactionsMapper
from src.api.v2.transactions.request import TransactionsRequest
from src.api.v2.transactions.response import TransactionsResponse
from datetime import datetime, timedelta


def transactions_api(request):
    request_params = {}
    response_json = ''
    context = {}

    for key in request:
        request_params[key.lower()] = request[key]

    context['request_params'] = request_params

    if all(key in request_params for key in ['payers_edrpous', 'startdate', 'enddate']):
        startdate = datetime.strptime(request_params['startdate'], '%Y-%m-%d').date()
        enddate = datetime.strptime(request_params['enddate'], '%Y-%m-%d').date()

        if (enddate - startdate).days > 90:
            # Розбиваємо запит на декілька запитів по 90 днів
            queries = []
            while startdate < enddate:
                new_enddate = startdate + timedelta(days=90)
                if new_enddate > enddate:
                    new_enddate = enddate
                queries.append({
                    'payers_edrpous': request_params['payers_edrpous'],
                    'startdate': startdate.strftime('%Y-%m-%d'),
                    'enddate': new_enddate.strftime('%Y-%m-%d'),
                })
                startdate = new_enddate + timedelta(days=1)
        else:
            # Один запит
            queries = [request_params]

        # Опрацьовуємо запити
        results = []
        for query in queries:
            api_transactions = ApiEndpoint(
                url=furl('https://api.spending.gov.ua/api/v2/api/transactions/page/'),
                request_type=TransactionsRequest,
                response_type=TransactionsResponse,
            )

            fetcher = Fetcher(api=api_transactions)
            parser = Parser_Transactions(api=api_transactions)

            http_request = TransactionsRequest(
                payers_edrpous=query['payers_edrpous'],
                startdate=query['startdate'],
                enddate=query['enddate'],
            )

            http_response = fetcher.get(http_request)
            response = parser.parse(http_response)
            results += response
        context['response_json'] = ujson.dumps([asdict(r) for r in results])
        context['csv_button'] = True
        context['fieldnames'] = ujson.dumps(TransactionsMapper.fieldnames())
        context['csv_response'] = ujson.dumps([TransactionsMapper.transform(item) for item in results])

    return context


a = {"payers_edrpous": "00035323", "startdate": "2023-02-01", "enddate": "2023-02-27"}
print(transactions_api(a))
