# 0000 - gamma j - 2. System prompts the Administrator to fill out first name, last name, username, email

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 2. System prompts the Administrator to fill out first name, last name, username, email

2. System prompts the Administrator to fill out first name, last name, username, email
address, password, and privileges of the user.
3. System validates new user information.
4. System creates a new account for the new user with desired privileges.
5. System displays account home page to Administrator.
Postconditions:
A new customer account is created within the system.
Remove User
Goal:
Remove a user from the system.
Actors:
Administrator
Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks button or link to “Remove User"
Basic Scenario:
1. Administrator clicks button or link to initiate the remove user process.
2. System prompts the Administrator to select a user by searching or viewing a list of users.
3. System displays user information.
4. System confirms deletion of selected user.
5. System displays account home page to Administrator.
Postconditions:
An account has been deleted within the system.
Change User Properties
Goal:
Alter properties such as passwords and privileges of the user.
Actors:
Administrator

GAMMA-J Web Store

31

Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks button or link to “Change User Properties"
Basic Scenario:
1. Administrator clicks the button or link to initiate change user properties process.
2. System prompts the Administrator to select a user by searching or viewing a list of users.
3. System displays the user information.
4. System alters the user properties.
5. System displays the account home page to Administrator.
Postconditions:
An account has been altered within the system.
Install Plug-ins
Goal:
Install a new plug-in to the application.
Actors:
Administrator
Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks the button or link to "Install Plug-ins "
Basic Scenario:
1. Administrator clicks the button or link to initiate Plug-in installation process.
2. System prompts the Administrator to upload the Plug-in module.
3. System installs plug-in and validates changes.
4. System displays plug-in options to the Administrator.

Postconditions:
A new plug-in is installed in the application.
Remove Plug-ins
Goal:
Remove a plug-in from the application.
Actors:
Administrator
Weborder System

GAMMA-J Web Store

32

Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks the button or link to "Install Plug-ins "
Basic Scenario:
1. Administrator clicks the button or link to initiate Plug-in deletion process.
2. System prompts the Administrator to select the desired Plug-in module.
3. System removes the plug-in and validates changes.

Postconditions:
A plug-in is removed from the application.
Manage Plug-in Options
Goal:
Make changes to an installed plug-in.
Actors:
Administrator
Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.
Triggers:
Administrator clicks button or link to "Manage Plug-ins "
Basic Scenario:
1. Administrator clicks the button or link to initiate Plug-in Options process.
2. System prompts the Administrator to select the desired Plug-in module.
3. System displays all plug-in options to the Administrator.
4. System confirms changes with the Administrator.

Postconditions:
A plug-in’s options have successfully been changed.

Install patch process
Goal:
Install patches or software updates to the web store.
Actors:
Administrator
Weborder System
Preconditions:
Administrator must be able to access the weborder system via a web browser with HTTPS.

GAMMA-J Web Store

33

Triggers:
Administrator clicks the button or link to "Install Patch"
Basic Scenario:
1. Administrator clicks the button or link to initiate Patching process.
2. System prompts the Administrator to upload the patch.
3. System automatically installs patches and reinitializes software.
4. System confirms that patch has been successfully installed.

Postconditions:
The web store was successfully updated.

Sales Person Use Cases
Login Sales Person
Goal:
Login to an account with the system.
Actors:
Sales Person
Weborder System
Preconditions:
Sales Person account must already be registered.
Triggers:
Sales Person clicks button or link to "Login"
Basic Scenario:
1. Sales Person clicks the button or link to initiate login process.
2. System prompts the Sales Person for email and password.
3. System verifies the information.
4. System creates session cookie.
