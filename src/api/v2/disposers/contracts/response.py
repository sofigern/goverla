from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Signature:
    caAddress: str


@dataclass
class Address:
    city: str
    countryId: int
    countryName: str
    district: Optional[str]
    districtCity: Optional[str]
    house: str
    housing: Optional[str]
    office: Optional[str]
    regionId: int
    regionName: str
    street: str


@dataclass
class Contractor:
    address: Address
    contractorType: int
    firstName: str
    identifier: str
    lastName: str
    middleName: str
    name: str


@dataclass
class Specification:
    cpvCode: Optional[str]
    itemCost: float
    itemCount: float
    itemDimension: str
    specCode: Optional[str]
    specificationName: str


@dataclass
class ProcurementItem:
    cpvCode: str
    nameUa: str


@dataclass
class ContractResponse:

    id: int
    edrpou: str
    documentNumber: str
    documentDate: str
    signDate: str
    signature: Signature
    amount: float
    currency: str
    currencyAmountUAH: Optional[float]
    contractors: List[Contractor]
    fromDate: str
    toDate: str
    subject: str
    noTerm: bool
    pdvInclude: bool
    pdvAmount: Optional[float]
    tender: bool
    reason: Optional[str]
    specifications: List[Specification]
    isCpvVat: bool
    procurementItems: List[ProcurementItem]
