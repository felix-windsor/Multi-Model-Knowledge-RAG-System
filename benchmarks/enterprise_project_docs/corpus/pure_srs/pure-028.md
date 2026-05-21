# 0000 - inventory - 1. The inventory system is updated

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - inventory.pdf

Section: 1. The inventory system is updated

1. The inventory system is updated
Actors
Inventory Admin, Inventory system, Authentication system

16

Included Use Cases
1. Authentication use case
Notes
We suppose that Hosting system and servers support all the operations
Authentication
*

*

«uses»

AUthentication System

return item
*
Inventory Admin

*

*

*
«uses»

Inventory System
change item status

RTI.UC: Returning Asset

17

Name: Approving Request
Identifier: APR.UC
Description
The use case describes the approving of requests that an Inventory Admin can do.
Goal
The Inventory Admin initiates the use case. The use case presents all the approval or
denial of a user request that can be done by an Inventory Admin.
Preconditions
1. The Inventory Admin is authenticated
