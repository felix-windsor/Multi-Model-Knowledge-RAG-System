# 0000 - gamma j - 5. Quality Attribute Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 5. Quality Attribute Requirements

5. Quality Attribute Requirements
5.1 Performance Requirements
•

Upon the USB being plugged in the system shall be able to be deployed and
operational in less than 1 minute.

•

The system shall be able to handle 1000 customers logged in concurrently at the
same time.

•

The system shall be able to retrieve 200 products per second.

•

The system shall be able to add product to shopping cart in less than 2ms.

•

The system shall be able to search for a specified product in less than 1 second.

•

The system shall be able to email customer and vendor in less than 1 second.

•

The system shall be able to validate credit card in less than 2 seconds.

•

The system shall be able to acquire shipping charges in less than 2 seconds.

•

The system shall be able to restore 1000 records per second.

5.2 Safety Requirements
•

The system will do periodic backups through a live internet connection.

5.3 Security Requirements
• The system shall validate credit cards against fraud.
•

The system shall encrypt all sensitive information via https.

•

The system shall encrypt all customer data in database.

•

The system shall auto detect IP DOS attacks and block IP automatically.

•

The system shall detect consecutive failed login attempts.

•

The system shall be protected by open source firewall called Firestarter.
http://www.fs-security.com/

5.4 Availability Requirements
•

The system shall have an availability of 99.99%.

5.5 Efficiency Requirements
•

The system shall perform searches via Dijkstra's shortest path algorithm.

•

For returning customers, the system shall validate 'existing' credit card in system
after each log in.

•

The system shall automatically compress image files that are too large in size.

•

The system will employ on demand asynchronous loading for faster execution of
pages.

•

The system shall validate email address existence.

5.6 Usability Requirements

GAMMA-J Web Store

21

•

The system shall be easy to use

•

The system shall be easy to learn

•

The system shall utilize help bubbles to assist managers, customers, and
administrators

•

The system shall employ easy to locate buttons

•

The system shall prompt customer with friend easy to read error messages.

•

The system shall utilize consistent symbols and colors for clear notifications.

5.7 Maintainability Requirements
•

The system shall utilize interchangeable plugins.

•

The system shall be easily updatable for fixes and patches.

•

The system shall create logs of all changes, updates, or fixes that are done to the
site.

•

The system shall be easy to upgrade.

5.8 Portability Requirements
• The system shall be extremely portable via the usb drive.
•

The system shall be easy to migrate or backed up via another usb drive.

5.9 Testability Requirements
• The system should be able to run under debug mode.
•

The system should be able to run test credit card transactions.

•

The system should be able to run test shipping orders.

•

The system should be able to create test environment of weborder system.
