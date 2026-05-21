# 0000 - inventory - 3. Authentication use case

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - inventory.pdf

Section: 3. Authentication use case

3. Authentication use case
Notes
We suppose that Hosting system and servers support all the operations

Authentication
*

*

«uses»

AUthentication System

Modify Item
*

*

*

*
«uses»

*

Inventory Admin

Inventory System
«uses»

Edit Item

Search

*

MOD.UC Modify Use Case

9

Name: Edit Use Case
Identifier: EDT.UC
Description
The use case describes the edit operation that the Inventory Admin can do.
Goal
The Inventory Admin initiates the use case. The use case presents the edit done by the
Inventory Admin.
Preconditions
1. The Inventory Admin is authenticated
Assumptions
1. We assume that use Knows the results of each operation there is no go back
actions
Basic Course
1. Use case begins when Inventory Admin start searching for an asset
2. Inventory Admin Edit the asset
Alternate Course A:
Condition: administrator or authorised inventory user is working on waiting for approval
list or waiting for execution list
1. Inventory user or Admin Edit the asset
Exceptional Course :
1.
1. Inventory Admin search for asset
2. Inventory Admin edit asset
3. Inventory Admin does not have sufficient privileges to edit asset
4. Message error is displayed
2.
1. Inventory Admin search for asset
2. no asset found
3. Message error is displayed
Post conditions
1. The system state change according to modification
Actors
Inventory Admin, Inventory system, Authentication system

10

Included Use Cases
1. Search use case
