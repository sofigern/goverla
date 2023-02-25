import csv
from dataclasses import asdict
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
from src.api.v2.check_documents.prozoro_document_check import find_matching_documents
from src.api.v2.check_documents.lotForm import LotForm


def index(request):
    return render(request, 'api/index.html')


def api(request):
    request_params = {}
    response_json = ''
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
        parser = Parser(api=api)

        http_request = ContractRequest(
            disposerId=request_params['disposerid'],
            documentDateFrom=request_params['startdate'],
            documentDateTo=request_params['enddate'],
        )

        http_response = fetcher.get(http_request)
        response = parser.parse(http_response)
        context['response_json'] = ujson.dumps([asdict(r) for r in response])
        context['csv_button'] = True
        context['fieldnames'] = ujson.dumps(ContractMapper.fieldnames())
        context['csv_response'] = ujson.dumps([ContractMapper.transform(item) for item in response])

    return render(
        request,
        'api/api.html',
        context,
    )


def post_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    fieldnames = ujson.loads(request.POST['fieldnames'])
    extracted_responses = ujson.loads(request.POST['csv_json'])

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
    return render(request, 'doc_check/lot_form.html', context)
