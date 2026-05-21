# 1999 - dii - 2 for Desirable (D)

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - dii.htm

Section: 2 for Desirable (D)

2 for Desirable (D)

3 for Optional (O).

Requirement/ Paragraph Number

Requirement Description

Prec

Related Requirement

Within XS SRS

TBD

QUALIFICATION PROVISIONS

COE Software will be qualified through formal validation tests
of the SRS level requirements. The Qualification Methods applied to
the software shall include test, demonstration, analysis, and inspection
(T, D, A, I).

TEST

A qualification method that is carried out by operation of the
item/component/I/F (or some part of the computer S/W configuration
item, etc.) and that relies on the collection and subsequent examination
of data.

DEMONSTRATION

A qualification method that is carried out by operation of the
item/component/I/F (or some part of the computer S/W configuration
item, etc.), and that relies on observable functional operation not
requiring the use of elaborate instrumentation or special test
equipment.

ANALYSIS

A qualification method that is carried out by the processing
of accumulated data. An example of accumulated data is the compilation
of data obtained from other qualification methods. Examples of the
processing of accumulated data are interpretations or extrapolations
made from the data.

INSPECTION

A qualification method that is carried out by visual
examination, physical manipulation, or measurement to verify that the
requirements have been satisfied.

REQUIREMENTS TRACEABILITY

Provided under separate document.

NOTES

ACRONYMS & ABBREVIATIONS

ACCS Army Command and Control Systems

GCCS-AAGCCS Army Global Command and Control System- Army

ANSI American National Standards Institute

API Application Programming Interface

ASCII American Standard Code Information Interchange

ASCII RTF American Standard Code Information Interchange Rich Text Format

ASRD AWIS Software Requirements Specification Document

ATCCS Army Tactical Command and Control Systems

AWIS Army WWMCCS Information System

CASS Common ACCS Support Software

CLI

Client Library Interface

CM Configuration Manager

COE Common Operating Environment

COTS Commercial Off-The-Shelf

X-DA Data Access

DAC Discretionary Access Control

XS Data Access Service

DBIF Database Interface

DBMS Database Management System

DBs Databases

DATATWG Data Access Services Technical Working Group

DCE Distributing Computing Environment

DDL Data Definition Language

DDS Data Distribution System

DES Data Encryption Standard

DID Data Item Description

DII Defense Information Infrastructure

DISA Defense Information Systems Agency

DML Data Manipulation Language

DoD Department of Defense

DTG Date-Time-Group

FIPS PUB Federal Information Processing Standards Publication

FMWG File Management Working Group

GCCS Global Command and Control Systems

GOTS Government Off-The-Shelf

GUI Graphical User Interface

HP Hewlett-Packard

IAW in accordance with

ID Identification

I/F Interface

IF Intell Fusion

I/O Input/Output

JMCIS Joint Maritime Command Information System

JOBES Joint Operation Planning and Execution System

MAC Mandatory Access Control

Mbs Megabytes

MCG&I Mapping, Charting, Geodesy and Imagery

MIL-STD Military Standard

MSB Most Significant Bit

OS Operating System

PM Project Manager

POSIX Portable Operating System Interface for Computing Environments

RAID Redundant Array of Inexpensive Disks

RDA Remote Database Access

RDBMS Relational Database Management System

RISC Reduced Instruction Set Computer

RTF Rich Text Format

SECTWG Security Services Technical Working Group

SMM Systems Management Manual

SQL Structured Query Language

SRI Standing Request for Information

SRS Software Requirements Specification

SSDD Support Software Design Document

STACCS Standard Theater Army Command And Control System

S/W Software

TBD To Be Determined

WWMCCS World-Wide Military Command and Control System

GLOSSARY OF TERMS

Automatically: Indicates
processing initiated during execution of other processes, but dependent
on information and/or parameters to be generated or supplied to these
other processes. The information / parameters may be data dependent, or
application dependent, or dependent on a manual process/human
intervention. It will include controls qualifying the processing
involved.

Business Rule: A narrative
description of policies, procedures, or principles within an
organization. Business rules can be divided in to four categories:
definitions, facts, constraints, and derivations.

Definitions are business rules that define entities and attributes.

Facts are either links (relationships) between entities or associations

between an entity and attributes

Constraints are conditions about the data
that must always be true. They are the integrity rules that protect
the data in the eventual database.

Derivations are business
rules that materialize a new piece of information (often attribute
values) from other pieces of information. For example, a mathematical
derivation might specify that you can obtain a person's age by
subtracting his or her birth date from the current date.

Commit/Rollback: An
individual transaction is processed (commit) or discarded (rollback) by
the proponent maintainer of the data items involved.

Discretionary Access Controls
(DAC): A means of restricting access to objects based on the identity
of subjects or groups to which they belong. The controls are
discretionary in the sense that a subject with a certain access
permission is capable of passing that permission on to any other
subject.

Dynamically Generated
Processing: Indicates processing initiated during execution of other
processes, but dependent upon information and/or parameters to be
generated or supplied to these other processes. The
information/parameters may be data dependent, or application dependent,
or dependent on a manual process/human intervention. It will include
controls qualifying the processing involved.

Location Transparency:
occurs when the physical location of data is transparent to the
applications and users of the database system. For example, a view that
joins table data from several databases provides location transparency
because the user of the view does not need to know where the data
originates from.

Mandatory Access Control
(MAC): mediates access to an object based on the clearance level of the
subject (user) and the sensitivity label of the object. (These
controls are always enforced above any discretionary control implemented
by users).

Mirrored Databases:
Replication and maintenance of a database on a transaction basis for the
purpose of rapid error or failure recovery as supported by the resident
COTS RDBMS own system utilities and operating system.

Object: A passive entity that
contains or receives information. Access to an object potentially
implies access to the information it contains. Examples of objects are
records, blocks, pages, segments, files, directories, directory trees,
and programs, as well as bits, bytes, words, fields, processors, video
displays, keyboards, clocks, printers, and network nodes.

Proponent Scheme: Describes
the sites at which databases are replicated and also who owns and has
update authority with respect to the data at each site. It refers to
proponency at the source and record level.

Redundant Array of
Inexpensive Disks (RAID): A RAID system appears as one very large,
reliable disk to the CPU. The main reason for using RAID storage is its
reliability. RAID has the same advantages as shadowing and striping at
a lower cost. There are several types/levels of RAID implementations,
including: RAID 0 (known as disk striping), RAID 1 (known as disk
shadowing), RAID 3 (in which data is distributed in small increments
across all data disks and adds a parity value to a separate disk for
recovery if any disk fails, RAID 4 (in which data is distributed in
large chunks across all data disks and also has a single parity disk.
RAID 4 intended to overcome performance penalties of RAID 3 for small
transfers. RAID 5 (in which parity over RAID 3 or RAID 4
implementations), and RAID 6 ( in which two parity disks in addition to
data disks are used in an attempt to further improve performance). In a
RAID 5 implementation, the data is stored as are check sums and other
information about the contents of each disk in the array. If one disk
is lost, the others can use the check sums and other stored information
to recreate the lost data. Storage system vendors may provide
additional enhancements to RAID level implementations to improve
performance and reliability.

Remote Data Access (RDA): is
an ISO (9579) application layer interoperability standard (protocol and
formats) to support access by an application to a (remote) DBMSs over an
OSI network. The goal of RDA is to allow interoperability between
applications (clients) and databases (servers) of different
manufacturers so that an application is able to read and update data in
remote databases via well defined standards. RDA defines a set of client
and server standards and a mapping of SQL commands to these services.
RDA also defines an interface to ISO (transaction processing) two phase
commit TP services in the case where updates to multiple remote
databases need to be coordinated. RDA does not yet define
interoperability between server databases (i.e. it is not yet a standard
for distributed database management).

Replication Scheme:
Information that precisely identifies DBs, or partitions of DBs, to be
copied and/or distributed, replication schedules, and master/remote
sites that are to receive the copies.

Spatial DBMS: Geographic
information system that organizes and maintains spatial data (i.e. data
with graphical attributes) in terms of type, scale, location(s), extent,
topology and geometry. Supports queries of spatial data where the
selection criteria are defined by spatial attributes.

SRI: A Standing Request For
Information (SRI) is a capability in which CASS monitors for the
occurrence of conditions established by an application program, and
notifies the calling or establishing application program when the
conditions are satisfied. An SRI may be one of three types:
timer-based, data-based, or message-based.

Subject: An active entity,
generally in the form of a person, process, or device that causes
information to flow among objects or changes the system state.
Technically, a process/domain pair.

Transaction Journalling:
Individual messages or database transactions are stored in a journal
file, which may be a linear log file or a circular file.

APPENDIX A

The metadata and procedures are described for the current Information Resource Submittal Package .

Metadata and Related Information

An XML tag may be described as any object and is easily created by
anyone using a text editor. Although XML is a relatively new technology,
many developers are already using XML in operational COE systems and
have already created tags and specifications, many of which may be
inconsistent with tags used in other systems. So far, the burgeoning
sets of XML tags have created redundancy and irrelevancy, and they lack
validity.

XML Registry.

To ensure interoperability, this registry provides a baseline set of
tags developed through coordination and approval among the Community.
The Registry allows a user to browse, search, and retrieve data that
satisfy your requirements. The Registry has a substring search
capability so that the user may easily find information resources that
meet the criteria. The user may specify whether to search for the term
within the name of the information resource or the definition or both.

Developer's Role
.

Developers are urged to review the baseline tags, adopt them where
possible, and subscribe to future notifications about the tags. If,
after reviewing the tags in the Registry, you cannot reuse an existing
specification (a.k.a. Document Type Definition (DTD)) or existing tags,
you may submit your proposed tag to a Community of Interest (COI) and
provide amplifying information for all to understand the semantics for
its proper use.

COE Chief Engineer's Role.

The COE Chief Engineer will approve a single Point of Contact (POC) for a
COI to manage the tags within that COI. The COE Chief Engineer will
reserve ultimate authority to mediate any unresolved disputes within all
COIs.

The COE Data Engineering Team's Role
.

Tags and semantics will be analyzed to identify opportunities to
consolidate tags towards a single or a minimal number of
representations. A "market forces" model can also guide COE Data
Engineering in identifying the weak candidates from the strong.

The Community of Interest's POC's Role
.

(The information in the following section is current as of 17 May, 1999.
Please consult the Registry for the most authoritative list of
information resources types.) The POC responsibilities will include the
transitioning of information resources from one status to another. Table
1 lists the valid types of information resources. The status levels are
developmental, candidate, approved, rejected, and retired.

Table 1 Information Resource Types

Information Resource

Description

XML_Element

tag, either complex or terminal node

XML_Attribute

characteristic of an element, may be constrained by enumeration

Model

a representation using a formalism such as IDEF1x or Object Modeling

XML_Spec

a DTD or DCD; the schema for an XML document

Domain

the valid values for an element or attribute; expressed as a valid
SQL expression or by reference to a separately available set (e.g., XML
doc of current CTRY values)

XML_Namespace

the reference for uniqueness within the Registry

Catalog

a Registry which conforms to some explicit rules of engagement

Document

any other amplifying information that is available (e.g., readme.txt)

Table 2 - Information Resource Association Types

Forward term

Reverse term

uses

used_by

describes

described_by

is_XML_spec_for

defined_by_XML_spec

is_newer_version_of

is_older_version_of

is_constrained_by_domain

is_domain_for

belongs_to_namespace

is_namespace_for

element_may_be_qualified_by_attribute

attribute_may_qualify_element

is_model_for

is_modeled_by

Procedures

For Developers may submit and use information resources within
the Registry constitutes guidance in the generation and use of XML as an
authoritative source for approved XML data and metadata components.

Review Tags in Registry and decide what additions/modifications to submit (if any)

Fill out one XML submission document to package multiple Tags

Specify relationships among Tags, provide valid values, and add to submission package

Include amplifying info associated with specific Tag(s)

Zip and attach submission package to e-mail message to: ____________________

Rules and Convensions.

Establishing a new Information Resource. Follow these conventions for creating new information resources for the Registry

Use "XML_Attributes" sparingly

If the term is well recognized outside its container term, designate it
as an element. Example: CTRY_CD, CTRY_NM, CTRY_ABBRD_NM, CTRY_OFF_NM,
CTRY_SCP_NT_TX, and CTRY_PSTL_NM are all characteristics (ER-attributes)
for the entity CTRY. In the relational world, they are columns within
the table ctry, attributes of the entity ctry in er-modeling, and member
attributes in object modeling. It would be expected that a submitter
would identify them as attributes rather than elements. But if they were
identified as attributes of the element ctry, then the additional
baggage (other attributes) must be carried, or submitted as separate
elements. We wish to limit the proliferation of tags, so we strongly
urge folks to use XML_Attributes sparingly.

Include descriptive definitions AND synonyms for the Information Resource Definition.

Initially, the Registry will not have keyword, thesaurus, or ontology
support but it will have a substring search for a number of fields,
including definition. Therefore, we urge submitters to include enough
expressive terms so that COE developers would easily find the term they
might consider "natural" in the definition and find the desirable tag
for expressing that concept. Example: If the registered tag is ORG_ID,
the description that includes references

APPENDIX
B

EXTERNAL PROGRAMMING INTERFACES

The External Interfaces for the XS SRS are defined as
interfaces to non-COE components. Detailed information (as specified in
paragraph 3.3 of the Data Item Description DI-IPSC-81433) defining
these interfaces will be specified during the design phase of the COE XS
architecture. At this time such detailed information is unavailable.

APPENDIX
C

INTERNAL PROGRAMMING INTERFACES

The Internal Interfaces for the XS SRS are defined as
interfaces to COE components. Detailed information (as specified in
paragraph 3.4 of the Data Item Description DI-IPSC-81433) defining these
interfaces will be specified during the design phase of the COE XS
architecture. At this time such detailed information is unavailable.

The COE components identified to-date are listed below.

MANAGEMENT SERVICES API

It incorporates other interfaces to:

Network Administration

System Administration

Security Administration

DISTRIBUTED SYSTEM SERVICES

COMMUNICATIONS SERVICES API

It incorporates other interfaces to:

Communications

Network Services

DISTRIBUTION AND OBJECT MANAGEMENT SERVICES

It incorporates other interfaces to:

Distributed Computing Services

Data Interchange Services

APPLICATION SUPPORT SERVICES

PRESENTATION SERVICES

It incorporates other interfaces to:

Executive Manager

Multi-Media Support

COMMON SUPPORT APPLICATIONS

It incorporates other interfaces to:

Office Automation

Message Processing

Correlation

MCG&I

Alerts

On-line Help

SOFTWARE DEVELOPMENT SERVICES

It incorporates other interfaces to:

Developers Toolkit

APPENDIX C

INTERFACES TO COMMERCIAL PRODUCTS

The Interfaces to Commercial Products for the XS SRS
are identified below. Detailed information (as specified in paragraph
3.3 of the Data Item Description DI-IPSC-81433) defining these
interfaces will be specified during the design phase of the COE XS
architecture. At this time such detailed information is unavailable.

The three commercial products or environments identified for the COE are the following Relational Database engines:

Sybase

Oracle

Informix.
