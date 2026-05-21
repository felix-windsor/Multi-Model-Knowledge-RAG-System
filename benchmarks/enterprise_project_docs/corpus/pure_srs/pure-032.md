# 0000 - inventory - 3. No results are found message is displayed

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - inventory.pdf

Section: 3. No results are found message is displayed

3. No results are found message is displayed
Post conditions
None
Actors
User, Inventory system, Authentication system

24

Included Use Cases
1. Authentication use case
Notes
We suppose that Hosting system and servers support all the operations

Authentication
*

*

«uses»

AUthentication System

Search
*

*

*

*

*
User

Inventory System
«extends»

Advenced
Search

*

SRCH.UC Search Use Case

25

Name: Create Reports Use Case
Identifier: REP.UC
Description
The use case describes the creation of reports that the User can do.
Goal
The User initiates the use case. The use case presents reports that can be created by the
User. Three reports can be created Reports




User Permission Report
Request Report
Assets By Location Report

Preconditions
1. The User is authenticated
