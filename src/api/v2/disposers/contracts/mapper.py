from src.api.v2.mapper import Mapper, Transformation


class ContractMapper(Mapper):

    _path = 'documents'

    _map = {
        'documentNumber': Transformation(),
        'documentDate': Transformation(),
        'amount': Transformation(),
        'currency': Transformation(),
        'signDate': Transformation(),
    }
