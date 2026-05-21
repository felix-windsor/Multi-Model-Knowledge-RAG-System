# 0000 - gamma j - 5. System displays account home page to Customer

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 5. System displays account home page to Customer

5. System displays account home page to Customer
Alternative Scenario:
A1. System recognizes Customer's cookie
A2. Go to Step 5 (Basic Scenario).
B1. Customer enters incorrect login information.
B2. System prompts Customer to resend login details to email account.
B3. Customer confirms.
B4. System sends email to registered email address.
B5. Go to Step 1 (Basic Scenario).
Postconditions:
The Customer is logged into the system.
Edit Customer Details
Goal:
Edit the customer account details.
Actors:
Customer
Weborder System
Preconditions:
Customer must be logged-in on the system.
Triggers:
Customer clicks button or link to "Edit Account"
Basic Scenario:
1. Customer clicks button or link to initiate the process to edit the account.
2. System displays account home page to Customer.
3. Customer clicks button or link to edit the account details.
4. System verifies the changes.
5. System stores new account information.
Alternative Scenario:
None
Postcoditions:
The Customer has changed the account details.
Logout Customer
Goal:
Logout the customer account on the system.
Actors:
Customer

GAMMA-J Web Store

38

Weborder System
Preconditions:
Customer must be logged-in on the system.
Triggers:
Customer clicks button or link to "Logout"
Basic Scenario:
1. Customer clicks button or link to initiate logout process.
2. System terminates the session cookie.
3. System displays home page.
Alternative Scenario:
None
Postconditions:
The Customer is logged out of the system.
Add Item To Cart
Goal:
Customer adds item(s) in the cart
Actors:
Customer
System
Preconditions:
The customer must be logged-in on the system.
Triggers:
Customer clicks button or link to "Add To Cart".
Basic Scenario:
1. Customer clicks the button or link to add to the cart with specified quantity.
2. System adds the item(s) to the cart.
3. System prompt Customer to edit quantity or remove item from cart.
4. Customer confirms items in cart.
5. System stores cookie with cart details.
6. Customer returns to product listings.
Alternative Scenario:
A1. Customer terminates the web browser window after adding item(s) to cart.
A2. Customer returns to weborder interface.
A3. System recognizes cookie and goes to step 6 (Basic Scenario) with existing items in
cart.
Postconditions:
The Customer has added item(s) to the shopping cart.

Checkout An Order

GAMMA-J Web Store

39

Goal:
Customer places and confirms an order for the checkout process.
Actors:
Customer
Weborder System
Preconditions:
1. Customer must be logged-in on the system.
2. Customer must have item(s) in the shopping cart.
Triggers:
Customer clicks button or link to "Ckeckout"
Basic Scenario:
1. Customer clicks the button or link to initiate the checkout process.
2. System calculates order of items in the shopping cart.
3. System appends cookie with flag for checkout process.
4. System presents customer with account details and payment methods.
5. Customer confirms account details and payment methods.
6. Customer confirms order.
7. System stores order confirmation and order details.
8. System sends email confirmation to the Customer.
9. System appends cookie with flag for completed checkout process.
Alternative Scenario:
A1. Customer terminates order web browser during order the checkout process.
A2. Customer returns to weborder interface.
A3. System recognizes cookie and goes to step 4 (Basic Scenario).
Postconditions:
The Customer has placed and confirmed an order.

GAMMA-J Web Store

40

Appendix C: Analysis Models

GAMMA-J Web Store

41

Appendix D: Issues List
1.
Currently, telephonic orders are a significant source of business at Gamma-J
which is both expensive and labor extensive. The organization has to figure out a way to
have a smooth transition of orders coming in through telephones to the new online
ordering system without loosing business to the competitor.
2.
Gamma-J depends mainly on Fed-Ex for its tracking number and transportation
needs to ship the orders. A separate module to generate the tracking numbers and
having a transportation system will be considered in the future.

3.

GAMMA-J Web Store

System does not support customer order analysis.

42

Appendix E: Data Dictionary
User ID = * User ID of the employee /customer of Tool Co Company; minimum 4 to
maximum 10 characters (alphabetic or alphanumeric)*
Password = * Password of the employee /customer of Tool Co Company; minimum 4 to
maximum 10 characters (alphabetic or alphanumeric)*
Item name = * Name of the selected item; maximum 50 character alphabetic string *
Item ID = * ID that uniquely identified the selected item; a 7-digit system generated
alphanumeric character*
Price = * Cost of a single unit of the selected item; in dollars and cents.*
Text description = * special description of the selected item; maximum 100 alphabetic
characters *
Shipping price = * Cost for shipping the item to its destination; in dollars and cents *
Quantity = * the number of units of each selected item that the customer is ordering;
default = 1; maximum = quantity presently in inventory *
Total = * Cost of a single unit of the selected item * Number of units of that item selected;
in dollars and cents *

Name = * Name of the customer; maximum 100 alphabetic characters *
Address = * Location of the customer *
City = * Name of the city for the above address; maximum 20 characters alphabetic
string*
State = * Name of the state for the above city; maximum 20 characters alphabetic
string*
Zip code = * The postal code of the above address; 5 digit numeric string *
E-mail ID = * E-mail address of the customer who is using the Web order system; 50
characters alphanumeric *
Credit Card No. = * Credit card number of the customer; 16 digit numeric string *
Shipping address = * Address where the item has to be shipped *
Credit card expiry date = * The date on the credit card when it will get expired; format
MM/YY *
Order No = * Unique confirmation number of the order to the customer; 9 characters
alphanumeric *
Tracking No. = * Number to track the order; 20 characters alphanumeric*

GAMMA-J Web Store

43

Shipping date = * Date when the specified order is shipped; format MM/DD/YYYY*

Location = * Place where the item is kept in the warehouse in the form of (aisle, column,
shelf)*

GAMMA-J Web Store

44
