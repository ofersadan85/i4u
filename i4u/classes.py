from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Dict, List

from zeep.helpers import serialize_object as _so


class Invoice4UError(Exception):
    pass


@dataclass
class GeneralCustomer:
    Name: Optional[str] = None


@dataclass
class Customer:
    Name: Optional[str] = None
    ID: Optional[int] = None
    Email: Optional[str] = None
    Cell: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    Zip: Optional[str] = None
    UniqueID: Optional[str] = None  # ת.ז או ח.פ
    PayTerms: int = -1  # מיידי
    Active: bool = True
    ExtNumber: Optional[int] = None  # מספר מזהה במערכת הפנימית
    Errors: None = None

    def __post_init__(self):
        if self.ExtNumber is None:
            self.ExtNumber = self.ID


@dataclass
class Payment:
    Amount: float
    PaymentType: int
    Date: datetime = datetime.now()


@dataclass
class CashPayment(Payment):
    PaymentType: int = 4


@dataclass
class BankTransferPayment(Payment):
    PaymentType: int = 3
    AccountNumber: str = ''
    BankName: str = ''
    BranchName: str = ''


@dataclass
class CheckPayment(BankTransferPayment):
    PaymentType: int = 2
    PaymentNumber: str = ''  # מספר המחאה


@dataclass
class CreditPayment(Payment):
    PaymentType: int = 1
    ExpirationDate: str = ''  # תוקף כרטיס
    NumberOfPayments: int = 1  # מספר תשלומים
    PayerID: str = ''  # מספר ת.ז בעל הכרטיס
    PaymentNumber: str = ''  # 4 ספרות אחרונות כרטיס אשראי


@dataclass
class DocumentItem:
    Price: float
    Name: str
    Quantity: float = 1.0
    TaxPercentage: float = 17.0

    def __post_init__(self):
        self.Price = self.Price / (1 + self.TaxPercentage / 100)


@dataclass
class Document:
    Items: Union[Dict[str, List[DocumentItem]], List[DocumentItem]]  # {'DocumentItem': []}
    Payments: Union[Dict[str, List[Payment]], List[Payment]]  # {'Payment': []}
    DocumentType: int
    Subject: Optional[str] = None
    # Total: float
    BranchID: Optional[int] = None
    ClientID: Optional[int] = None
    Currency: Optional[str] = None
    GeneralCustomer: Optional[GeneralCustomer] = None
    Is2SignDoc: Optional[bool] = None
    IssueDate: datetime = datetime.now()
    Language: int = 1
    MailsAttached: Optional[str] = None  # Comma separated list of emails
    OrganizationID: Optional[int] = None
    # SmsMessages: list
    UniqueID: Optional[str] = None
    DocumentNumber: Optional[str] = None
    Errors: None = None
    Total: Optional[float] = None
    NewCustomer: Optional[Customer] = None

    def __post_init__(self):
        if isinstance(self.Items, list):
            self.Items = {'DocumentItem': self.Items}
        if isinstance(self.Payments, list):
            self.Payments = {'Payment': self.Payments}


@dataclass
class InvoiceReceipt(Document):
    DocumentType: int = 3

    def __post_init__(self):
        super().__post_init__()
        all_items = float(sum(i.Price for i in self.Items['DocumentItem']))
        self.Total = all_items


@dataclass
class InvoiceOrder(Document):
    DocumentType: int = 6
    Payments: None = None
    Is2SignDoc: bool = True
    GeneralCustomer: None = None


@dataclass
class InvoiceQuote(InvoiceOrder):
    DocumentType: int = 7


def serialize(item, i4u_instance):
    """ Helper function to turn wsdl service objects to defined dataclasses """
    obj = _so(item)
    for key, value in obj.items():
        setattr(i4u_instance, key, value)
    return i4u_instance
