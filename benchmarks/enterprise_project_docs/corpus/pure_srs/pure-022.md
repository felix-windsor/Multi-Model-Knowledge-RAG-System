# 0000 - inventory - 5. Functional requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - inventory.pdf

Section: 5. Functional requirements

5. Functional requirements
5.1. Transferring Assets
5.1.1. Within the same department: data base can be updated directly without
any request
5.1.2. Inter departments: request must be approved by a DA group member and
faculty group member unless it came from a higher level group
5.1.3. Inter faculties transfer: request can be made by any authorised user and
approved by faculty group or higher level
5.1.4. Transfer outside university should be approved by the university group
5.2. Editing Assets
5.2.1. Any administrative level user or inventory user can edit an asset that
belongs to its department; same thing for faculty user, or university user; in
order to make modification if he is authorised to do it.
5.3. Modifying assets
5.3.1. all fields of an edited asset can be modified except Ids
5.3.2. a bulk entry file can be used
5.4. Adding inventory assets
5.4.1. Any DA group member or authorised inventory group member asset is
owned by the department
5.4.2. Any faculty member can add all related departments inventory
5.4.3. Any university group member can add all assets in the inventory
5.4.4. A bulk entry can be used to add many assets
5.5. Creating request to borrow an asset or a reserve a location
5.5.1. request can be made by any authorised user
5.5.2. After creation a request still pending waiting to be approved by an
administrative level user according to that have this authority
5.6. Retuning assets
5.6.1. An inventory user should check returned asset and update inventory
5.7. Creating a new location
5.7.1. IT group members can create a new space and modify floor structure when
they receive an exception request from any administrative level
5.8. Approving requests
5.8.1. Any administration level or authorised inventory group member can
display all pending requests waiting for approval from this level and approve
those requests
5.8.2. When request is treated user is notified by email
5.8.3. Request is added to the waiting for execution list
5.8.4. Inventory is updated when user receive requested asset
6

5.9. Authentication
5.9.1. Authentication is made by user name and a password for all users
5.9.2. administrative level working on administration computer
5.10.
Changing permission
5.10.1. Any administrative level user can delegate another user to execute some or
all his authorized actions. And this user acquires the role of inventory
administrator
5.11.
Output reports
5.11.1. Asset report by location
5.11.2. Request report
5.11.3. User permission user
