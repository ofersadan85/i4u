import random
import string
import tempfile
import unittest
from pathlib import Path

from i4u import Invoice4U, Customer, Invoice4UError
from i4u.classes import InvoiceReceipt, GeneralCustomer, DocumentItem, CashPayment, InvoiceQuote, InvoiceOrder


class Invoice4UFull(unittest.TestCase):
    i4u = None

    @classmethod
    def setUpClass(cls):
        cls.i4u = Invoice4U('Test@test.com', '123456')

    def test_dev_login(self):
        self.assertIsNotNone(self.i4u.token)

    def test_existing_customer_creation(self):
        customer = Customer('test customer', Email='test@test.com')
        self.assertRaises(Invoice4UError, self.i4u.create_customer, customer)

    def test_good_customer_creation(self):
        created = self.i4u.create_customer(Customer(random_word(), Email='test@test.com'))
        self.assertIsInstance(created.ID, int)
        self.assertGreater(created.ID, 0)

    def test_get_customer(self):
        customer = Customer('test customer', Email='test@test.com')
        new_customer = self.i4u.get_customer(customer)
        self.assertEqual(new_customer.Name, customer.Name)
        self.assertEqual(new_customer.Email, customer.Email)
        self.assertEqual(new_customer.ExtNumber, new_customer.ID)

    def test_bad_invoice_receipt_1(self):
        empty = InvoiceReceipt(Subject=random_word(), Items=[], Payments=[], GeneralCustomer=GeneralCustomer('test'))
        self.assertRaises(Invoice4UError, self.i4u.create_document, empty)

    def test_bad_invoice_receipt_2(self):
        gc = GeneralCustomer('test')
        items = [DocumentItem(33, 'test')]
        unmatched = InvoiceReceipt(Subject=random_word(), Items=items, Payments=[CashPayment(22)], GeneralCustomer=gc)
        self.assertRaises(Invoice4UError, self.i4u.create_document, unmatched)

    def test_gc_invoice_receipt(self):
        total = random.randint(100, 100000)
        good_with_gc = InvoiceReceipt(
            Subject='sbj',
            Items=[DocumentItem(total, random_word())],
            Payments=[CashPayment(total)],
            GeneralCustomer=GeneralCustomer('test'),
            BranchID=0,
        )
        new_doc = self.i4u.create_document(good_with_gc)
        self.assertIsNone(new_doc.Errors)
        self.assertNotEqual(new_doc.UniqueID, '00000000-0000-0000-0000-000000000000')
        self.assertEqual(new_doc.Subject, good_with_gc.Subject)
        self.assertEqual(new_doc.Total, total)
        self.assertEqual(new_doc.DocumentType, 3)

    def test_client_id_invoice_receipt(self):
        customer = self.i4u.get_customer(Customer('test customer'))
        total = random.randint(100, 100000)
        new_doc = self.i4u.create_document(InvoiceReceipt(
            Subject='sbj',
            Items=[DocumentItem(total / 3, '1third'), DocumentItem(total / 3 * 2, '2thirds')],
            Payments=[CashPayment(total)],
            ClientID=customer.ID,
            BranchID=0,
        ))
        self.assertIsNone(new_doc.Errors)
        self.assertEqual(new_doc.ClientID, customer.ID)

    def test_new_client_invoice_receipt(self):
        customer = Customer(random_word())
        new_doc = self.i4u.create_document(InvoiceReceipt(
            Subject='sbj',
            Items=[DocumentItem(33, 'test33'), DocumentItem(11, 'test11')],
            Payments=[CashPayment(44)],
            NewCustomer=customer,
            BranchID=0,
        ))
        self.assertIsNone(new_doc.Errors)
        new_customer = self.i4u.get_customer(customer)
        self.assertEqual(new_doc.ClientID, new_customer.ID)
        self.assertEqual(customer.Name, new_customer.Name)

    def test_get_document_and_download(self):
        new_doc = self.i4u.create_document(InvoiceQuote(
            Subject=random_word(),
            Items=[DocumentItem(100, random_word())],
            NewCustomer=Customer(random_word())
        ))
        fetched_doc = self.i4u.get_document(new_doc)
        print(fetched_doc)
        self.assertEqual(new_doc.UniqueID, fetched_doc.UniqueID)
        temp_dir = Path(tempfile.gettempdir())
        temp_file = self.i4u.download_document(new_doc, temp_dir)
        self.assertTrue(temp_file.is_file())
        self.assertGreater(temp_file.stat().st_size, 0)
        temp_file.unlink()

    def test_get_empty_document(self):
        self.assertRaises(Invoice4UError, self.i4u.get_document, InvoiceOrder(Items=[]))

    def test_get_empty_customer(self):
        self.assertRaises(Invoice4UError, self.i4u.get_customer, Customer())

    def test_update_customer(self):
        customer = self.i4u.get_customer(Customer('test customer'))
        old_address = customer.Address
        new_address = random_word()
        self.assertNotEqual(old_address, new_address)
        customer.Address = new_address
        self.i4u.update_customer(customer)
        updated_customer = self.i4u.get_customer(Customer('test customer'))
        self.assertEqual(updated_customer.Address, new_address)

    def test_update_bad_customer(self):
        self.assertRaises(Invoice4UError, self.i4u.update_customer, Customer())

    @classmethod
    def tearDownClass(cls):
        del cls.i4u


class Invoice4UBadLogin(unittest.TestCase):
    i4u = None

    @classmethod
    def setUpClass(cls):
        cls.i4u = Invoice4U('wrong_user', 'wrong_pass')

    def test_wrong_login(self):
        self.assertIsNone(self.i4u.token)

    def test_customers(self):
        customers = self.i4u.get_all_customers()
        self.assertListEqual(customers, [])

    @classmethod
    def tearDownClass(cls):
        del cls.i4u


def random_word(length: int = 16):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
