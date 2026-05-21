# 0000 - gamma j - 5. System displays account home page to the Customer

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 5. System displays account home page to the Customer

5. System displays account home page to the Customer
Alternative Scenario:
A1. System recognizes the Customer's cookie
A2. Go to Step 5 (Basic Scenario).
B1. Customer enters incorrect login information.
B2. System prompts the Customer to resend login details to the email account.
B3. Customer confirms.
B4. System sends an email to the registered email address.
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
Customer clicks on the button or link to "Edit Account"
Basic Scenario:
1. Customer clicks the button or link to initiate the process to edit the account.
2. System displays the account home page to the Customer.
3. Customer clicks the button or link in order to edit the account details.
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

GAMMA-J Web Store

27

Customer
Weborder System
Preconditions:
Customer must be logged-in on the system.
Triggers:
Customer clicks on the button or link to "Logout"
Basic Scenario:
1. Customer clicks the button or link in order to initiate logout process.
2. System terminates the session cookie.
3. System displays the home page.
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
Customer clicks the button or link to "Add To Cart".
Basic Scenario:
1. Customer clicks the button or link in order to add to the cart with specified quantity.
2. System adds the item(s) to the cart.
3. System prompts the Customer to edit the quantity or remove the item from cart.
4. Customer confirms the items in the cart.
5. System stores cookie with cart details.
6. Customer returns to product listings.
Alternative Scenario:
A1. Customer terminates the web browser window after adding item(s) to cart.
A2. Customer returns to weborder interface.
A3. System recognizes cookie and goes to step 6 (Basic Scenario) with existing items in
cart.
Postconditions:
The Customer has added item(s) to the shopping cart.

GAMMA-J Web Store

28

Checkout An Order
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
4. System presents the customer with the account details and payment methods.
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

Administrator Use Cases
Login Administrator
Goal:
Login to an Administrator account with the system.
Actors:
Administrator
Weborder System
Preconditions:
Administrator account must already be registered.
Triggers:
Administrator clicks button or link to "Login"

GAMMA-J Web Store

29

Basic Scenario:
1. Administrator clicks button or link to initiate login process.
2. System prompts the Administrator for email and password.
3. System verifies information.
4. System creates session cookie.
