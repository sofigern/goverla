from dataclasses import dataclass
from typing import Optional


@dataclass
class Transactions:
    id: int
    doc_vob: Optional[str]
    doc_vob_name: Optional[str]
    doc_number: str
    doc_date: str
    doc_v_date: str
    trans_date: str
    amount: float
    amount_cop: int
    currency: str
    payer_edrpou: str
    payer_name: str
    payer_account: str
    payer_mfo: Optional[str]
    payer_bank: Optional[str]
    recipt_edrpou: str
    recipt_name: str
    recipt_account: str
    recipt_bank: Optional[str]
    recipt_mfo: Optional[str]
    payment_details: Optional[str]
    doc_add_attr: str
    region_id: int
    payment_type: str
    payment_data: Optional[str]
    source_id: int
    kekv: Optional[int]
    kpk: str
    contractId: Optional[str]
    contractNumber: Optional[str]
    budgetCode: str
