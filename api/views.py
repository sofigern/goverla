import csv
import ujson
from django.http import HttpResponse

from furl import furl
from django.shortcuts import render

from src.api.endpoint import ApiEndpoint
from src.api.fetcher import Fetcher
from src.api.parser import Parser
from src.api.v2.disposers.contracts.mapper import ContractMapper
from src.api.v2.disposers.contracts.request import ContractRequest
from src.api.v2.disposers.contracts.response import ContractResponse

from src.api.v2.transactions.mapper import TransactionsMapper
from src.api.v2.transactions.request import TransactionsRequest
from src.api.v2.transactions.response import TransactionsResponse
from datetime import datetime, timedelta

from src.api.v2.check_documents.prozoro_document_check import find_matching_documents
from src.api.v2.check_documents.lotForm import LotForm


def index(request):
    return render(request, 'index.html')


def contracts_api(request):
    request_params = {}
    context = {}

    for key in request.GET:
        request_params[key.lower()] = request.GET[key]

    context['request_params'] = request_params

    if all(key in request_params for key in ['disposerid', 'startdate', 'enddate']):
        api = ApiEndpoint(
            url=furl('https://api.spending.gov.ua/api/v2/disposers/contracts'),
            request_type=ContractRequest,
            response_type=ContractResponse,
        )

        fetcher = Fetcher(api=api)

        http_request = ContractRequest(
            disposerId=request_params['disposerid'],
            documentDateFrom=request_params['startdate'],
            documentDateTo=request_params['enddate'],
        )

        context['request_urls'] = ujson.dumps([fetcher.get_url(http_request)])
        context['mapper_type'] = 'contracts'
        context['mapper_path'] = 'documents'
        

    return render(
        request,
        'contracts/contracts.html',
        context,
    )

MAPPER_BY_TYPE = {
    'contracts': ContractMapper,
    'transactions': TransactionsMapper,
}

def post_csv(request):
    mapper_type = request.POST['mapper_type']
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{mapper_type}.csv"'},
    )
    mapper = MAPPER_BY_TYPE[mapper_type]
    fieldnames = mapper.fieldnames()
    responses = ujson.loads(request.POST['response_json'])
    extracted_responses = [mapper.transform(item) for item in responses]
    writer = csv.DictWriter(response, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extracted_responses)

    return response


def goverla(request):
    return render(request, 'goverla.html')


def base(request):
    return render(request, 'base.html')


# вьюшки для перевірки документів Prozoro

def lot_view(request):
    matching_docs = []
    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            lot_ids = form.cleaned_data['lot_id'].split(',')
            for lot_id in lot_ids:
                matching_docs.extend(find_matching_documents(lot_id.strip()))
    else:
        form = LotForm()
    context = {'form': form, 'matching_docs': matching_docs}
    return render(request,
                  'doc_check/lot_form.html',
                  context)


# вьюшка для трансакції з апі spending.gov.ua

def transactions_api(request):
    request_params = {}
    # response_json = ''
    context = {}

    for key in request.GET:
        request_params[key.lower()] = request.GET[key]

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
        # results = []
        context['request_urls'] = []
        for query in queries:
            api_transactions = ApiEndpoint(
                url=furl('https://api.spending.gov.ua/api/v2/api/transactions/'),
                request_type=TransactionsRequest,
                response_type=TransactionsResponse,
            )

            fetcher = Fetcher(api=api_transactions)
            # parser = Parser_Transactions(api=api_transactions)

            http_request = TransactionsRequest(
                payers_edrpous=query['payers_edrpous'],
                startdate=query['startdate'],
                enddate=query['enddate'],
            )
            fetcher.get_url(http_request)
            context['request_urls'].append(fetcher.get_url(http_request))
        context['request_urls'] = ujson.dumps(context['request_urls'])
        context['mapper_type'] = 'transactions'
        context['mapper_path'] = ''
    return render(
        request,
        'transactions/transactions.html',
        context,

    )

# вьюшка для помилки 500


def my_custom_error500_view(request, exception):
    return render(request, '500.html', status=500)
