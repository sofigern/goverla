from src.api.v2.mapper import Transformation, Mapper


class TransactionsMapper(Mapper):

    _path = 'transactions'
    # Do we want None string for none values?
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
