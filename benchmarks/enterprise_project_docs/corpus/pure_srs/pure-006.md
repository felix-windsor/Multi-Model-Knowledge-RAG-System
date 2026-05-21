# 0000 - gamma j - 3. System Features

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 3. System Features

3. System Features
3.1 Customer Accounts
3.1.1 Description And Priority
Customers will be able to create accounts to store their profiles, contact information,
purchase history, and confirm orders. This is a high priority system feature. Security
methods will ensure that customer accounts remain confidential and resistant to
tampering.
3.1.2 Stimulus/Response Sequences
•
Web Browser initiates request to Web Server via HTTPS
•
Web Server parses request
•
Web Server submits request to Service
•
Service picks up request
•
Service runs task
•
Service returns results
•
Web Server checks for completion
•
Web Server returns results to Web Browser
•
Web Browser displays results
3.1.3 Functional Requirements
Customers will be able to create accounts to store their customer profiles, configure
contact information, view their purchase history, and confirm orders. Customers will be
able to register, log in, and log out of their accounts. Furthermore, Customer profiles will
also include payment information, such as the ability to store credit card information,
and address information.
3.2 Inventory Management
3.2.1 Description And Priority
Inventory management will allow for the placement of products into multi-tiered
categories. This is a medium priority system feature.
3.2.2 Stimulus/Response Sequences
Same as 3.1.2
3.2.3 Functional Requirements
Products will be stored in multi-tiered categories; a category can contain sub categories
or products. The inventory management will allow for administrators to update the
categories, the products placed in categories, and the specific product details.
3.3 Shopping Cart
3.3.1 Description And Priority
Customers will be able to add and store products for purchase within the shopping cart.
This feature is a medium priority system feature.

GAMMA-J Web Store

7

3.3.2 Stimulus/Response Sequences
Same as 3.1.2
3.3.3 Functional Requirements
Customers will also be able to add products into the shopping cart. The shopping cart
will clearly display the number of items in the cart, along with the total cost. The customer
will also be able to add to or remove products from the shopping cart prior to checkout
and order confirmation.
3.4 Order Confirmation
3.4.1 Description And Priority
Order confirmation will allow the customer to review their order after checkout prior to
confirmation. This is a medium priority system feature.
3.4.2 Stimulus/Response Sequences
Same as 3.1.2
3.4.3 Functional Requirements
Customers will be able to confirm the order after checkout. If the order is incorrect, the
customer will be able to revise and update their order. The customer will then receive a
confirmation email with the specific order details.
3.5 Interface
3.5.1 Description And Priority
The interface will be presented to the customer in a web browser. The interface must
remain consistent among various web browsers and be intuitive to the customer. This is a
medium priority system feature.
3.5.2 Stimulus/Response Sequences
Same as 3.1.2
3.5.3 Functional Requirements
Customers will be presented with an unambiguous interface to assist in browsing the
categories and products. Customers will be able to search for products matching their
search criteria. The interface will be compatible with all major web browsers such as
Internet Explorer, Mozilla Navigator, Mozilla Firefox, Opera, and Safari.
3.6 Plug-in API
3.6.1 Description And Priority
The system will feature an API to allow customers to build custom plug-ins to be able to
meet their needs. This is a high priority system feature as it ensures the flexibility of the
system to be tailored to specific needs.
3.6.2 Stimulus/Response Sequences
•
Web Browser initiates request to Web Server via HTTPS
•
Web Server parses request
•
Web Server submits request to API Service
•
API Service picks up request
•
API Service submits request to Plug-in
•
Plug-in picks up request
•
Plug-in runs tasks

GAMMA-J Web Store

8

•
•
•
•
•
•

Plug-in returns results
API Service validates results
API Service returns results
Web Server checks for completion
Web Server returns results to Web Browser
Web Browser displays results

3.6.3 Functional Requirements
The system will implement an Application Interface to allow for various plug-ins to interact
with the system. The plug-in API will be well documented and specifications will be
provided to plug-in developers.
