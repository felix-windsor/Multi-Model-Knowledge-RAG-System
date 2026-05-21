# 0000 - gamma j - 2. Overall Description

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - gamma j.pdf

Section: 2. Overall Description

2. Overall Description
2.1 Product Perspective
Web Store is a new system designed for users new to the online E-commerce. This will be
a plug and play device with its own CPU and operating system. The Web Store will be a
quick and easy means to setup and operate an online Web Store. The Figure 2.1 is a
context diagram showing external system interfaces.

2.2 Product Features
Account Management (AM) (High Priority): AM allows users to create, edit, and view
accounts information. It also allows the user to login/out of the system.
Search Engine (SE) (Medium Priority): SE is the tool that assists the user in finding a specific
item in the database. It can receive search criteria, find search criteria, and return the
results of the search.
Product Management (PM) (High Priority): PM allows sales personnel to manage the
product line shown on the web site.

GAMMA-J Web Store

5

Shopping Cart (SC) (Medium Priority): SC is temporary storage for customers shopping on
the web. Items from the inventory can be reserved in a virtual cart until the customer
decides to purchase them.
Purchasing and Payment (PP) (High Priority): PP is used to approve and transfer payment
from buyers when purchasing items in the cart.
2.3 User Classes
System Administrator: Is generally the owner that takes care of maintenance for the
Web Store system. The administrator will be in charge of assigning privileges of accounts.
Suggested more than one individual can have administrator privilege to ensure
advisability. Full documentation will be provided to the Administrator to assist with this
process.
Sales Personnel: Is generally the owner of the Web Store tasked with updating inventory
and product line descriptions. Once added, sales personnel can add, delete and
change descriptions, pictures, prices, and when ready flag items for customers to buy.
Customer: A customer is an individual wishing to purchase inventory from GAMMA-J’s
Web Store. The Web store will have a variety of clientele depending upon the inventory
loaded on the Key. When creating a new account on Web Store it will default as a
customer account. Later if the account needs to be upgraded the administrator can
accomplish this via the administrator interface.
2.4 Operating Environment
OE-1: Web Store shall operate with the following internet browsers: Microsoft Internet
Explorer version 6 and 7, Netscape Communicator Version 4 and 5.
OE-2: Web Store shall operate on an Intel based system with Slackware Linux 2.6 and
Apache Web Server. The operating system is designed by the Yoggie Corporation.
Although maintenance documentation will be supplied and the operating system will be
tested, the developers of this Web Store are not responsible for the functionality of the
operating system.
OE-3: The system shall use SQL based database to store inventory information.
OE-4: USB interface and divers are provided by Yoggie Corporation.
2.5 Design and Implementation Constraints
CO-1: Must use a SQL based database. SQL standard is the most widely used database
format. Restricting to SQL allows easy of use and compatibility for Web Store.
CO-2: Compatibility is only tested and verified for Microsoft Internet Explorer version 6 and
7, Netscape Communicator Version 4 and 5. Other versions may not be 100%
compatible. Also other browsers such as Mozilla or Firefox may not be 100% compatible.
2.6 User Documentation
UD-1: Shall install online help for users via the web interface
UD-2: Shall deliver Operations and Maintenance manual, Users Guide book, and
Installation Instructions for the Administrator.
2.7 Assumptions and Dependencies

GAMMA-J Web Store

6

AD-1: Assume the delivery of development, test and evaluate samples of the USB system
from Yoggie.
AD-2: Assume Yoggie will freeze the baseline of the USB system after delivery.
