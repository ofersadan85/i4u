# coding: windows-1255
import logging
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

import requests
import zeep

from .classes import Invoice4UError, Document, Customer, serialize

logging.getLogger('zeep').setLevel(logging.ERROR)


class Invoice4U(zeep.CachingClient):
    """ Invoice4U documentation: https://invoice4uapi.docs.apiary.io/ """
    def __init__(self, user: str, password: str, timeout=20):
        super().__init__('https://api.invoice4u.co.il/Services/ApiService.svc?singleWsdl')
        self._user = user
        self._password = password
        self.transport.operation_timeout = timeout
        self.transport.load_timeout = timeout

    @property
    @lru_cache(maxsize=1)
    def token(self):
        return self.service.VerifyLogin(self._user, self._password)

    def get_all_customers(self):
        response = self.service.GetCustomersByOrgId(self.token)
        return [serialize(c, Customer()) for c in response.Response.Customer]

    def get_customer(self, cus: Customer) -> Customer:
        if cus.ExtNumber:
            return serialize(self.service.GetCustomerByExternalNumber(cus.ExtNumber, self.token), Customer())
        if cus.Name:
            return serialize(self.service.GetCustomerByName(cus.Name, self.token), Customer())
        raise Invoice4UError('Not enough details to find customer')

    def get_document(self, doc: Document) -> Document:
        if doc.DocumentNumber and doc.DocumentType:
            zeep_doc = self.service.GetDocumentByNumber(doc.DocumentNumber, doc.DocumentType, self.token)
            i4u_doc = Document(zeep_doc.Items, zeep_doc.Payments, zeep_doc.DocumentType)
            return serialize(zeep_doc, i4u_doc)
        raise Invoice4UError('Not enough details to find document')

    @staticmethod
    def document_url(doc: Document) -> str:
        return f'https://newview.invoice4u.co.il/Views/PDF.aspx?docid={doc.UniqueID}'

    def download_document(self, doc: Document, destination: Path = Path.home() / 'Downloads') -> Path:
        url = self.document_url(doc)
        response = requests.get(url)
        if destination.is_dir():
            destination = destination / response.headers['Content-Disposition'][21:]
        destination.write_bytes(response.content)
        return destination

    def create_document(self, doc: Document) -> Document:
        if hasattr(doc, 'NewCustomer') and doc.NewCustomer is not None:
            new_customer = self.create_customer(doc.NewCustomer)
            delattr(doc, 'NewCustomer')
            doc.ClientID = new_customer.ID
        new_doc = self.service.CreateDocument(asdict(doc), self.token)
        if new_doc.Errors:
            raise Invoice4UError(new_doc.Errors)
        return serialize(new_doc, doc)

    def create_customer(self, cus: Customer) -> Customer:
        new_cus = self.service.CreateCustomer(asdict(cus), self.token)
        if new_cus.Errors:
            raise Invoice4UError(new_cus.Errors)
        return serialize(new_cus, cus)

    def update_customer(self, cus: Customer) -> Customer:
        updated = self.service.UpdateCustomer(asdict(cus), self.token)
        if updated.Errors:
            raise Invoice4UError(updated.Errors)
        return serialize(updated, cus)
