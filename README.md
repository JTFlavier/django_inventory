# Introduction

The following is my submission for the Inventory API based on the use case provided.

# Notes re: Implementation

- DB key and email password were placed in ```django_inventory_api/secrets.py```, which is not in this repo since it is in ```gitignore```. Please provide your own file + credentials when deploying this.
- Please provide your own ```EMAIL_HOST_USER``` and ```DEFAULT_FROM_EMAIL``` in ```django_inventory_api/settings.py```

# Model

I added the following models and fields:

- Item
   - Name: The name of the product (CharField)
   - SKU: A unique identifier for the product (CharField)
   - Price: The price of the product (DecimalField)
   - Description: A description of the product (TextField)
   - Quantity: The quantity of the product in stock (IntegerField)
   - Status: The status of the product (BooleanField) - True if the product is available, False if it is out of stock.
- Customer 
    - Email
    - Name
    - Address
- Order 
    - Order Number
    - Items
    - Customer

# APIs

- GET: ```items/?isAvailable={True/False/other}```
  - By default: returns all items
  - Includes flag ```isAvailable```
    - If ```True```: return all items in stock (aka quantity > 0)
    - If ```False```: return items out of stock (quantity == 0)
- POST: ```items/```
   -  Can be object or array of objects
   -  Inserts the listed objects into the model:
   -  Syntax:
   -  ```
        [
            {
                "sku": "ABCD1234",
                "name": "Vacuum Cleaner 3000",
                "price": 123.45,
                "description": "It sucks",
                "quantity": 50
            },
            {
                "sku": "EFGH5678",
                "name": "Cheeseburger",
                "price": 10.50,
                "description": "Delicious Cheeseburger",
                "quantity": 5
            },
            {
                "sku": "98765432",
                "name": "Empty Lot",
                "price": 25000,
                "description": "Lets you own Kamurocho",
                "quantity": 0
            }
        ]
        ```
 - PUT: ```items/```
   - Updates the given item
   - Syntax:
   - 
   ```
    {
        "sku": "EFGH5678",
        "quantity": 200
    }
   ```
- POST: ```orders/```
  - Given syntax below:
    1. Check if all items exist and are in stock
    2. If all items are in stock: update inventory & send email to email in customer field
    3. Else: return error  
   - Syntax:
   ```
    {
        "order_number": "12345",
        "items": [
            {
                "sku": "ABCD1234",
                "quantity": 2
            },
            {
                "sku": "EFGH5678",
                "quantity": 1
            }
        ],
        "customer": {
            "name": "John Smith",
            "email": "johnsmith@example.com",
            "address": "123 Main St, Anytown USA"
        }
    }
   ```