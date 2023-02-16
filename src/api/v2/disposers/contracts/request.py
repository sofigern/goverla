from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class ContractRequest:

    disposerId: List[str]  # ЄДРПОУ розпорядників
    documentDateFrom: date  # Діапазон пошуку за датою документа (дата з, включно)
    documentDateTo: date  # Діапазон пошуку за датою документа (дата по, включно)
