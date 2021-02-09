from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional

from i4u import Invoice4U
from i4u.classes import GeneralCustomer


@dataclass
class DocumentsRequest:
    Errors: None = None
    Info: None = None
    OpenInfo: None = None
    BranchID: Optional[int] = None
    CommonCacheType: None = None
    CommonCacheTypes: None = None
    Currency: str = 'ILS'
    CustomerID: Optional[int] = None
    CustomerIdOldSystem: None = None
    CustomerName: Optional[str] = None
    DocumentNumber: Optional[int] = None
    DocumentType: Optional[int] = None
    DocumentTypes: Optional[str] = None
    ExectDocumentNumber: Optional[int] = None  # Exact?
    ExtraStatus: Optional[int] = None
    ExtraStatus2: Optional[int] = None
    From: Optional[datetime] = datetime.now() - timedelta(days=30)
    FromActualCreationDate: Optional[datetime] = datetime.now() - timedelta(days=30)
    FromNumber: Optional[int] = None
    FromPaymentDueDate: Optional[datetime] = None  # datetime.now() - timedelta(days=30)
    GeneralClientName: Optional[str] = None
    GeneralCustomer: Optional[GeneralCustomer] = None
    GraphGroupType: None = None
    IncomeItemSearchByCatalogIdAndNameOnly: bool = False
    IsForceFullSearch: bool = False
    IsFromDocumentRequest: bool = True
    IsFromOldSystemRequest: bool = False
    IsRefreshCache: bool = True
    ItemCode: Optional[str] = None
    ItemDescription: Optional[str] = None
    ItemsIncluded: bool = True
    Limit: int = 100
    OldSystemId: Optional[int] = None
    OnlyGeneralClient: bool = False
    PaymentType: Optional[int] = None
    PaymentTypeDeductionOnly: bool = False
    PaymentTypeOtherId: Optional[int] = None
    PaymentsIncluded: bool = True
    ReportType: Optional[str] = None  # ns4:ReportTypes
    ReportTypeInt: Optional[int] = None
    Status: Optional[int] = None
    To: Optional[datetime] = datetime.now()
    ToActualCreationDate: Optional[datetime] = datetime.now()
    ToAmount: Optional[float] = None
    ToNumber: Optional[float] = None
    ToPaymentDueDate: Optional[datetime] = None  # datetime.now()
    TransactionNumber: Optional[str] = None
    Type: None = None  # ns4:DocumentType
    UserCacheType: None = None  # ns4:UserCacheTypes


if __name__ == '__main__':
    i4 = Invoice4U('Test@test.com', '123456')
    req = DocumentsRequest()
    result = i4.service.GetDocuments(asdict(req), i4.token)
    print(result)
