from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class TransactionsRequest:

    payers_edrpous: List[str]  # ЄДРПОУ платника
    startdate: str  # Діапазон пошуку за датою документа (дата з, включно)
    enddate: str  # Діапазон пошуку за датою документа (дата по, включно)
