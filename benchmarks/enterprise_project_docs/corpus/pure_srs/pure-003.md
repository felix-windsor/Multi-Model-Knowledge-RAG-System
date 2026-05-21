# 0000 - cctns - 5. FUNCTIONAL ARCHITECTURE RECOMMENDATIONS

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 0000 - cctns.pdf

Section: 5. FUNCTIONAL ARCHITECTURE RECOMMENDATIONS

5. FUNCTIONAL ARCHITECTURE RECOMMENDATIONS
The proposed functional architecture is modeled around centralized deployment to facilitate
ease of maintenance and leverage advancement in open standards and web technologies.
The 3 C’s (Core-Configuration-Customization) forms the guiding principle for the
architecture. The functional architecture of the CCTNS solution is given in the figure below.
The functional architecture is composed of 4 major components based on SOA principles.
Each of the components contains multiple services as defined by Service Definition. The
core services, support layer and security and access control components can be deployed as
standard components with necessary configuration changes. The customization layer can
override and add to the core services based on the specific state requirements and can be
plugged with the core services.

CCTNS Functional Architecture Overview

Ministry of Home Affairs

Draft Core Scope Document

Page 16 of 19

E-Governance Mission Mode Project: Crime & Criminals Tracking Network and Systems

The deployment of the application will be at state level and will be configured and
customized as per the state specific extensions.
The systems should be designed with the following broad guidelines:
System Functionality
1)
2)
3)
4)

5)
6)
7)

The system should support multilingual interface
The system should be designed in manner that operational data is not lost in case of any
failure of equipment or communication network.
The system should work even in an offline mode with the critical functionality
The system should be designed to have satisfactory performance even in Police Stations
connected on low-bandwidth
The system should be implemented using Service Oriented Architecture (SOA) and have a
modular design
The system should be developed on Open Standards
The system should be built on a common User Access and Authentication Service to
ensure Single-Sign on for the end-user

8)

The system should be developed for a centralized deployment and maintenance

9)

The system should be developed to be deployed in a 3-tier datacenter architecture

10)

11)
12)
13)
14)
15)
16)

The system should be designed to have a n-tier architecture with the presentation logic
separated from the business logic that is again separated from the data-access logic
The system should be extensible to provide access to the interfaces through PDA’s and
mobile data terminals
The system should adopt standardized formats and common metadata elements
The system should be designed for access through browser-based systems and must
impose minimal requirements on the client device
The system must support multiple types of communication services for remote access
The system should have capability to support public access to a subset of data and
functionality
The system should support multi-tier authentication where required

Ministry of Home Affairs

Draft Core Scope Document

Page 17 of 19

E-Governance Mission Mode Project: Crime & Criminals Tracking Network and Systems

17)

The system should support SSL encrypted connections

18)

The system should support secure virtual private network connections

19)

The system should use HTTPS as the communication protocol, i.e., HTTP over an
encrypted secure socket layer (SSL)

20)

The system should run on multiple browsers

21)

The system should support selective encryption of the stored data

22)

The system should ensure secure transmission of data over the network and utilize SSL
and 2-way digital signatures
The system should ensure high standards of security and access control through:
a) Prevent cross-site scripting
b) Validate the incoming data / user request
c) Encode the incoming data / user request

23)

d) Prevent SQL Injection
e) Utilize parameterized queries
f) Sanitize the user-inputs
g) Validate the data both at the client and server
h) Do not allow hard delete and perform only soft tagging the row for deletion
The system should ensure high scalability and performance through:
a) Use of cache for storing frequent data
b) Use of AJAX based technology to improve user experience. Aggressive page loading to
be considered based on the screen and estimate usage pattern
c) Leverage Asynchronous HTTP socket capabilities of web server for scalability and
performance

24)

d) Host all the static content (documents, images) on the web server
e) The search results should be fetched from the database in batches of 10 or 20 maximum
as configured within the application
f) Display of records on the screen in batches/paged manner
g) The search should fetch only the fields that need to be displayed to the user. Only when
the user clicks on a particular record to view its further details should a query be fired to
fetch the additional details for this particular record only
h) A hierarchical cache should be configured and used for caching of results of most

Ministry of Home Affairs

Draft Core Scope Document

Page 18 of 19

E-Governance Mission Mode Project: Crime & Criminals Tracking Network and Systems

frequently used searches
i) Database Indexes should be applied on the key columns used for searching

Ministry of Home Affairs

Draft Core Scope Document

Page 19 of 19
