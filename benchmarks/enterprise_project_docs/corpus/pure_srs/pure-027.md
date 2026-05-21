# 0000 - inventory - 3. Error Message is displayed

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - inventory.pdf

Section: 3. Error Message is displayed

3. Error Message is displayed
14

Post conditions
A new request is pending waiting approval
Actors
Inventory Admin, Inventory system, Authentication system
Included Use Cases
1. Search use case
2. Authentication use case
Notes
We suppose that Hosting system and servers support all the operations

Authentication
*

*

AUthentication System
«uses»

fill basic form
*
Create a new
request
*
Inventory Admin

*

*

*

fill advenced form

{OR}

*
*

*

*

*
*

«extends»

fill exceptions
form

*

Search

*
*

*

CRQ.UC: Create request Use Case

15

Inventory System
*

Name: Returning Asset
Identifier: RTI.UC
Description
The use case describes the returning asset update that the Inventory Admin can do.
Goal
The Inventory Admin initiates the use case. The use case presents all the updates to the
inventory that can be done by the Inventory Admin.
Preconditions
1. The Inventory Admin is authenticated
Assumptions
1. We assume that use Knows the results of each operation there is no go back
actions
Basic Course
