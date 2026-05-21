# 0000 - gamma j - 5. System displays account home page to Administrator

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 5. System displays account home page to Administrator

5. System displays account home page to Administrator
Alternative Scenario:
A1. System recognizes Administrator 's cookie
A2. Go to Step 5 (Basic Scenario).
B1. Administrator enters incorrect login information.
B2. System prompts Administrator to resend login details to email account.
B3. Administrator confirms.
B4. System sends email to registered email address.
B5. Go to Step 1 (Basic Scenario).
Postconditions:
The Administrator is logged into the system.
Logout Administrator
Goal:
Logout the Administrator account on the system.
Actors:
Administrator
Weborder System
Preconditions:
Administrator must be logged-in on the system.
Triggers:
Administrator clicks button or link to "Logout"
Basic Scenario:
1. Administrator clicks button or link to initiate logout process.
2. System terminates the session cookie.
3. System displays home page.
Alternative Scenario:
None
Postconditions:
The Administrator is logged out of the system.
Add User
Goal:
Register a new customer, sales person, or administrator account with the system.
Actors:

GAMMA-J Web Store

30

Administrator
Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks button or link to "Add Users"
Basic Scenario:
1. Administrator clicks the button or link to initiate Add user process.
