from dataclasses import dataclass
from typing import Optional, Any, List
from src.api.v2.disposers.contracts.mapper import Transformation


class TransactionsMapper:

    _map = {
        'id': Transformation(),
        'trans_date': Transformation(),
        'amount': Transformation(),
        'currency': Transformation(),
        'payer_edrpou': Transformation(),
        'payer_name': Transformation(),
        'payer_account': Transformation(),
        'recipt_edrpou': Transformation(),
        'recipt_name': Transformation(),
        'recipt_account': Transformation(),
        'payment_details': Transformation(),
        'kekv': Transformation(),
        'kpk': Transformation(),
        'contractId': Transformation(),
        'contractNumber': Transformation(),
        'budgetCode': Transformation(),
    }

    @classmethod
    def transform(cls, data):
        extract = {}
        for path, transformation in cls._map.items():
            value = getattr(data, path, transformation.default)
            name = transformation.name
            if not name:
                name = path.split('.')[-1]
            extract[name] = value
        return extract

    @classmethod
    def fieldnames(cls) -> List[str]:
        fieldnames = []
        for path, transformation in cls._map.items():
            name = transformation.name
            if not name:
                name = path.split('.')[-1]
            fieldnames.append(name)
        return fieldnames
