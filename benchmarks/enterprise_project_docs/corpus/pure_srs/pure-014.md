# 0000 - gamma j - 5. System displays the account home page to Sales Person

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 5. System displays the account home page to Sales Person

5. System displays the account home page to Sales Person
Alternative Scenario:
A1. System recognizes Sales Person's cookie
A2. Go to Step 5 (Basic Scenario).
B1. Sales Person enters incorrect login information.
B2. System prompts the Sales Person to resend login details to email account.
B3. Sales Person confirms.
B4. System sends email to registered email address.
B5. Go to Step 1 (Basic Scenario).
Postconditions:
The Sales Person is logged into the system.
Logout Sales Person

GAMMA-J Web Store

34

Goal:
Logout the Sales Person account on the system.
Actors:
Sales Person
Weborder System
Preconditions:
Sales Person must be logged-in on the system.
Triggers:
Sales Person clicks the button or link to "Logout"
Basic Scenario:
1. Sales Person clicks the button or link to initiate logout process.
2. System terminates the session cookie.
3. System displays home page.
Alternative Scenario:
None
Postconditions:
The Sales Person is logged out of the system.
Add Product
Goal:
Add a product to the system.
Actors:
Sales Person
Weborder System
Preconditions:
Sales Person must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Sales Person clicks the button or link to "Add Product"
Basic Scenario:
1. Sales Person clicks the button or link to initiate Add Product process.
