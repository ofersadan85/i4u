# i4u-py
Python package to interact with [Invoice4U](https://www.invoice4u.co.il) API

Invoice4U API natively uses wsdl soap, so to interact with it this package is built based on [zeep](https://github.com/mvantellingen/python-zeep) with additional data structures that allow easier interaction

## Installation & Requirements
To install with pip:

    pip install i4u-py

As this package is currently in initial development, it was only tested using python 3.8, if you wish to create a pull request to add tests / modifications that enable it to work on other python versions, see the [Contributing]() section below

## Usage Examples
To connect and authenticate you must first create an `Invoice4U` instance with your username and password provided (this assumes you have an account set up on [Invoice4U](https://www.invoice4u.co.il))

    from i4u-py import Invoice4U
    i4u = Invoice4U('your_user', 'your_password')

If you don't have API access yet, or you just want to test out the code, you may test the API usage with these test credentials

    from i4u-py import Invoice4U
    i4u = Invoice4U('Test@test.com', '123456')

To verify that you're logged in correctly, check that you received a `token`

    if i4u.token is None:
        print('Username or password are incorrect')
    else:
        print('Login success')

To get a list of **_all_** customers belonging to your organisation:

    customers = i4u.customers()

This will output a list of customers, each one is returned as in the following example form:
    
    {
        'Errors': None,
        'Info': None,
        'OpenInfo': None,
        'AccountNumber': None,
        'Active': False,
        'AddToMailChimp': None,
        'Address': None,
        'BankName': None,
        'BranchName': None,
        'Cell': None,
        'City': None,
        'ClientCode': 0,
        'ContactEmail': None,
        'ContactFirstName': None,
        'ContactLastName': None,
        'ContactName': None,
        'Country': None,
        'CountryId': None,
        'CreditCardNumber': None,
        'CreditCardType': None,
        'CustomerEmails': {
            'AssociatedEmail': []
        },
        'DateCreated': datetime.datetime(2012, 11, 20, 10, 8, 45),
        'Email': 'mail@mail.com',
        'EmailAccounting': None,
        'ExtNumber': 100,
        'Fax': None,
        'FreeBalance': 0.0,
        'FreeUniqueID': None,
        'FreeZip': None,
        'Guid': None,
        'HasBeenExported': False,
        'ID': 76747,
        'IdNewAndOldSystem': None,
        'InternalNote': None,
        'IsAutomaicInvoices': None,
        'IsFromLead': False,
        'IsNonUniqueNameCreation': False,
        'LeadId': 0,
        'Name': 'vvvvvv',
        'NameAccounting': None,
        'OrgID': 50,
        'PayTerms': 0,
        'Phone': None,
        'PhoneAccounting': None,
        'Retainer': False,
        'RetainerAmount': 0.0,
        'RetainerTitle': None,
        'Token': None,
        'Ucan2ClientID': 1968083,
        'UniqueID': None,
        'Website': None,
        'Zip': None
    }

You can edit and save customer details:

    customers = i4u.customers()
    c = customers[6]
    c.Email = 'some_other_email@mail.com'
    c.Fax = '1800123456789'
    i4u.update_customer(c)

You can also create a new customer:

    from i4u-py import Customer

    new_customer = Customer('Elon Musk', City='Jerusalem')
    created = i4u.create_customer(new_customer)
    print(created.ID)  # Check the system generated ID of the new customer if needed

Similarly, you can create new documents along with new customers in the same call:

    from i4u-py import InvoiceOrder, DocumentItem, Customer

    customer = Customer('Joe Smith')  # Create a new client while creating the document
    products = [
        DocumentItem(Price=30, Name='Chair', Qunatity=2),
        DocumentItem(Price=50, Name='Table', Qunatity=1),
    ]
    new_invoice_order = InvoiceOrder(Subject='Furniture', Items=products, NewCustomer=customer)
    created_doc = i4u.create_document(new_invoice_order)
    print(created_doc.Total)  # Will print 110 (30 * 2 + 50)

Alternatively, create the same document for an existing customer:

    new_invoice_order = InvoiceOrder(Subject='Furniture', Items=products, ClientID=customer.ID)
    created_doc = i4u.create_document(new_invoice_order)

You can also download the documents:

    i4u.download_document(doc=created_doc, destination='/some/folder')

More examples of document types you can create will be added here soon!
    

## Contributing

If you would like to contribute to this project, you are welcome to submit a pull request. For bugs / feature requests please submit issues

In order to add features not yet available in this package but that are possible with Invoice4U API in principle, please refer to [Invoice4U API documentation](https://invoice4uapi.docs.apiary.io/)