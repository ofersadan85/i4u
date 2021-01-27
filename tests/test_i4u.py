import unittest
from i4u import Invoice4U, Customer, InvoiceReceipt, GeneralCustomer, DocumentItem, CashPayment, Invoice4UError


class Invoice4UFull(unittest.TestCase):
    i4u = None

    @classmethod
    def setUpClass(cls):
        cls.i4u = Invoice4U('Test@test.com', '123456')

    def test_dev_login(self):
        self.assertIsNotNone(self.i4u.token)

    def test_customer_creation(self):
        customer = Customer('test customer', Email='test@test.com')
        self.assertRaises(Invoice4UError, self.i4u.create_customer, customer)

    def get_test_customer(self):
        customer = Customer('test customer', Email='test@test.com')
        new_customer = self.i4u.get_customer(customer)
        self.assertEqual(new_customer.Name, customer.Name)
        self.assertEqual(new_customer.Email, customer.Email)
        self.assertEqual(new_customer.ExtNumber, new_customer.ID)

    def test_bad_invoice_receipt_1(self):
        self.assertRaises(ValueError, InvoiceReceipt, Subject='some subject', Items=[], Payments=[])

    def test_bad_invoice_receipt_2(self):
        empty = InvoiceReceipt(Subject='some subject', Items=[], Payments=[], GeneralCustomer=GeneralCustomer('test'))
        self.assertRaises(Invoice4UError, self.i4u.create_document, empty)

    def test_bad_invoice_receipt_3(self):
        gc = GeneralCustomer('test')
        items = [DocumentItem(33, 'test')]
        unmatched = InvoiceReceipt(Subject='sbj', Items=items, Payments=[CashPayment(22)], GeneralCustomer=gc)
        self.assertRaises(Invoice4UError, self.i4u.create_document, unmatched)

    def test_good_invoice_receipt(self):
        gc = GeneralCustomer('test')
        good_with_gc = InvoiceReceipt(
            Subject='sbj',
            Items=[DocumentItem(33, 'test33'), DocumentItem(11, 'test11')],
            Payments=[CashPayment(44)],
            GeneralCustomer=gc,
            BranchID=0,
        )
        new_doc = self.i4u.create_document(good_with_gc)
        self.assertIsNone(new_doc.Errors)
        self.assertNotEqual(new_doc.UniqueID, '00000000-0000-0000-0000-000000000000')
        self.assertEqual(new_doc.Subject, good_with_gc.Subject)
        self.assertEqual(new_doc.Total, 44)
        self.assertEqual(new_doc.DocumentType, 3)

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
