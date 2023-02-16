# Python 3 server example
import csv
from http.server import BaseHTTPRequestHandler, HTTPServer
import io
from furl import furl
import ujson

from src.api.fetcher import Fetcher
from src.api.parser import Parser
from src.api.endpoint import ApiEndpoint
from src.api.v2.disposers.contracts.request import ContractRequest
from src.api.v2.disposers.contracts.response import ContractResponse
from src.api.v2.disposers.contracts.mapper import ContractMapper


hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        edrpou = '00013480'
        since = '2022-12-01'

        self.send_response(200)
        # self.send_header("Content-type", "application/json")
        self.send_header("Content-type", "text/csv")
        # self.send_header('Content-Disposition', 'attachment; name="contracts"; filename="contracts.csv')
        self.end_headers()

        api = ApiEndpoint(
            url=furl('https://api.spending.gov.ua/api/v2/disposers/contracts'),
            request_type=ContractRequest,
            response_type=ContractResponse,
        )

        fetcher = Fetcher(api=api)
        parser = Parser(api=api)

        request = ContractRequest(
            disposerId=edrpou,
            documentDateFrom=since,
            documentDateTo=None,
        )

        http_response = fetcher.get(request)
        response = parser.parse(http_response)

        extracted_responses = [ContractMapper.transform(item) for item in response]

        buffer = io.StringIO()

        writer = csv.DictWriter(buffer, delimiter=';', fieldnames=ContractMapper.fieldnames())
        writer.writeheader()
        writer.writerows(extracted_responses)
        #
        buffer.seek(0)
        self.wfile.write(buffer.read().encode('utf_8'))

        # buffer.close()
        # self.wfile.write(ujson.dumps(extracted_responses).encode('utf_8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

