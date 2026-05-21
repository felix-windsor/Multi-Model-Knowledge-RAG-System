# 0000 - gamma j - 2. System prompts the customer to fill out his/her first name, last name, billing address,

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 2. System prompts the customer to fill out his/her first name, last name, billing address,

2. System prompts the customer to fill out his/her first name, last name, billing address,
shipping address, email address, and their password.
3. Customer enters fields.
4. System validates the customer's information.
5. System creates a new account for the Customer.
6. System creates a session cookie.
7. System displays an account home page to Customer.
Alternative Scenario:
A1. System recognizes Customer's cookie.
A2. Go to Step 7 (Basic Scenario).
Postconditions:
The Customer registers and creates a new customer account with the system.
Login Customer
Goal:
Login to a customer account with the system.
Actors:
Customer
Weborder System
Preconditions:
Customer account must already be registered.
Triggers:
Customer clicks button or link to "Login"
Basic Scenario:

GAMMA-J Web Store

26

1. Customer clicks on the button or link to initiate the login process.
2. System prompts the customer for his/her email and password.
3. System verifies the information.
4. System creates session cookie.
