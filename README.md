# i4u
![](https://img.shields.io/github/v/release/ofersadan85/i4u)
![](https://img.shields.io/pypi/v/i4u)
![](https://img.shields.io/github/license/ofersadan85/i4u)
![](https://img.shields.io/github/workflow/status/ofersadan85/i4u/Python%20package%20tests?label=Tests)

Python package to interact with [Invoice4U](https://www.invoice4u.co.il) API

Invoice4U API natively uses wsdl soap, so to interact with it this package is built based on [zeep](https://github.com/mvantellingen/python-zeep) with additional data structures that allow easier interaction

## Installation
![](https://img.shields.io/pypi/v/i4u)
![](https://img.shields.io/pypi/wheel/i4u)

    pip install i4u

## Requirements
![](https://img.shields.io/pypi/pyversions/i4u)

As this package is currently in initial development, it was only tested using python 3.7, 3.8 and 3.9 and only on Windows and on Linux Ubuntu 20.04

It **_might_** work on python 3.6 if you backport the missing [dataclasses](https://pypi.org/project/dataclasses/) (`pip install dataclasses`), and I can't see any reason it would not work on other operating systems (but did not test that)

If you wish to create a pull request to add tests / modifications that enable it to work on other python versions or operating systems, see the [Contributing]() section below

## Usage Examples
To connect and authenticate you must first create an `Invoice4U` instance with your username and password provided (this assumes you have an account set up on [Invoice4U](https://www.invoice4u.co.il))

    from i4u import Invoice4U
    i4u_api = Invoice4U('your_user', 'your_password')

If you don't have API access yet, or you just want to test out the code, you may test the API usage with these test credentials

    from i4u import Invoice4U
    i4u_api = Invoice4U('Test@test.com', '123456')

To verify that you're logged in correctly, check that you received a `token`

    if i4u_api.token is None:
        print('Username or password are incorrect')
    else:
        print('Login success')

To get a list of **_all_** customers belonging to your organisation:

    customers = i4u_api.get_all_customers()

You can edit and save customer details:

    customers = i4u_api.customers()
    c = customers[6]
    c.Email = 'some_other_email@mail.com'
    c.Fax = '1800123456789'
    i4u_api.update_customer(c)

You can also create a new customer:

    from i4u.classes import Customer

    new_customer = Customer('Elon Musk', City='Jerusalem')
    created = i4u_api.create_customer(new_customer)
    print(created.ID)  # Check the system generated ID of the new customer if needed

Similarly, you can create new documents along with new customers in the same call:

    from i4u.classes import InvoiceOrder, DocumentItem, Customer

    customer = Customer('Joe Smith')  # Create a new client while creating the document
    products = [
        DocumentItem(Price=30, Name='Chair', Qunatity=2),
        DocumentItem(Price=50, Name='Table', Qunatity=1),
    ]
    new_invoice_order = InvoiceOrder(Subject='Furniture', Items=products, NewCustomer=customer)
    created_doc = i4u_api.create_document(new_invoice_order)
    print(created_doc.Total)  # Will print 110 (30 * 2 + 50)

Alternatively, create the same document for an existing customer:

    new_invoice_order = InvoiceOrder(Subject='Furniture', Items=products, ClientID=customer.ID)
    created_doc = i4u_api.create_document(new_invoice_order)

You can also download the document:

    i4u_api.download_document(doc=created_doc, destination='/some/folder')

More examples of document types you can create will be added here soon!

## Contributing

If you would like to contribute to this project, you are welcome to submit a pull request

For bugs / feature requests please submit [issues](https://github.com/ofersadan85/i4u/issues)

In order to add features not yet available in this package but that are possible with Invoice4U API in principle, please
refer to [Invoice4U API documentation](https://invoice4uapi.docs.apiary.io/)

## Warranty / Liability / Official support

This project is being developed independently of Invoice4U and not supported officially by them, we provide the
package "as-is" without any implied warranty or liability, usage is your own responsibility
