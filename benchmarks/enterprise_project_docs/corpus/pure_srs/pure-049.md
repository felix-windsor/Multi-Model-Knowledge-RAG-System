# 1999 - dii - 11 July 1996

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - dii.htm

Section: 11 July 1996

11 July 1996

ACCS-A1-100-006 System Specification for ATCCS, 22 March 1995

ATCCS-A1-302-001A Army Tactical Command and Control
System Common ATCCS Support Software (CASS) Systems/Segment
Specification

CDRL A142 AWIS Software Requirements Specification (ASRD), July 1992

CDRL ML03 AWIS Systems Management Manual (SMM), 31 Oct. 1994

AWIS Support Software Design Document, December 1994

D18664A Standard Theater Army Command and Control System (STACCS) System Design Document Version 1.1/As Built, 1 Oct. 93

AAN-SDA001A Standard Theater Army Command and Control System
(STACCS) System Specification, Version 1.1/As Built, 1 Oct. 93

Standard Theater Army Command and Control System (STACCS) System Software Programmers Manual, Draft.

Global Command and Control System (GCCS) Integration Standard, Version 1.0, October 1994.

Global Command and Control System (GCCS) Common Operating Environment Baseline, DISA, 28 November1994.

User Interface Specifications for Global Command and Control System (GCCS), Version 1.0, October 1994.

Draft Architectural Design Document for the Global Command
and Control System (GCCS) Common Operating Environment (COE),
Version 3, 24 July, 1994.

STANDARDS:

MIL-STD-498 Military Standard - Software Development and Documentation,

DOD, Dec. 1994.

FIPS PUB 127-2 Database Language SQL - Federal Information Processing Standards Publication 127-2, 2 June, 1993.

MIL-STD-6040 Military Standard

ISO/IEC 9070 Formal Public Identifier

NON-GOVERNMENT DOCUMENTS

Petrucci, Steve, "Cross-Platform Power Tools, Application
Developers for the Macintosh, Windows, and Windows NT", Random House
Electronic Publishing, 1993.

Donald Lewine,"POSIX Programmer's Guide", O'Reilly & Associates, Inc. 1991.

W3C Working Draft "Namespaces in XML"

REQUIREMENTS

REQUIRED STATES AND MODES

Environmental Mode: This is the real-time operations that must
react to varying degrees of readiness to full scale wartime operations
such as crisis planning with the use of heterogeneous data types and
sources, transfer capabilities, data management services.

COE Compliance. XML Services shall be segmented. COE sponsors
shall adhere to compliance level requirements described in the
I&RTS.

In the fixed (static) mode of operation (base or data processing
megacenter), the data management services shall have the capability of
being tuned by on-site personnel to adjust for varying workloads and
sizes of associated databases. These workloads and databases are
expected to change more frequently and to a greater extent than for
processing associated with deployed units

In a changing (dynamic) environment, such as with deployed units,
the workload and database sizes may be more predetermined (given a more
precise mission) and require access to fewer data management
administrative capabilities than needed in a fixed environment. The XS
shall have the ability to redefine or reset names of connect descriptors
to database server instances. Connect descriptors are fully qualified
object names and include address (protocol/host/port) and instance name.

In a degraded communications environment, there is a need, for
example, to be able to reset session time-out values if the data
management services are being accessed by users affected by the
communications degradation. At a minimum, the session time-out values
shall be user definable and be able to be reset prior to initialization
of a user session. The goal is to provide the option of dynamically
changing session time values based on current communications performance
identified by capabilities of the network management or DBMS.

End User Mode: Portion of XS services shall be used by various
classes of users: data consumers, data and database managers, network
information infrastructure resource managers. Some of these uses of the
data management services will entail unique requirements that shall be
fulfilled within the capability of XS services.

Maintenance Mode: This mode includes modification and/or addition
of application data segments, user permission, privileges, and
restructuring storage and memory areas. In addition, maintenance also
shall pertain to shutdown, open not-mounted and online/off-line
implementations, modifications, upgrade, or other related actions. The
data management services shall support managing various types of data,
database architectures and platforms that includes hardware and software
at the specified sites.

Training Mode. In support of
training activities
, the data
management services shall provide for the same processing as would be
encountered in a production environment. However, access to the
database may be via a training application access to the DBMS rather
than from the production mission application.

XML SERVICES CAPABILITY REQUIREMENTS

The XS shall deliver inter-related components as shown in figure 3.2-1

Figure 3.2-1

Register Terms and Structures (e.g., tags, DTDs, DCDs)

Producer services
.

A producer is an agent that
contributes metadata for inclusion into an XML Registry for the purposes
of ensuring maximum semantic understanding of a term as it appears in
an XML document. To contribute metadata to a registry, the producer
must be able to receive XML registry forms, submit metadata and the
related information resource artifacts, and notify.

Produce and display submittal forms as part of the
Information Resource Submittal Package from the web containing the
following Information Resource artifacts: XML Tag Specification, XML
Spec (i.e. DTD, DCD etc.), Sample of XML document of the tag to be
submitted. The Package is to be compressed and emailed or sent ftp to an
addressee.

Download Information Resource Submittal Package from the web
containing forms, instructions, and tools for submission to XML
Registry.

Submit prescribed metadata related to information resource type,
information resource association, status code, data types specified and
other related information specified in
Appendix A
within a
combination of forms. These forms are part of the Information Resource
Submittal Package containing the following Information Resource
artifacts: XML Tag Specification, XML Spec (i.e. DTD, DCD etc.), Sample
of XML document of the tag to be submitted. The Package is to be
compressed and emailed or sent ftp to an addressee.

Submit metadata by an on-line interactive process

Submit metadata by a off-line and interactive batch process

Parse submitted XML Registry specification forms

Populate XML Registry database

Modify of specified terms & definitions of metadata and status of Information Resources.

Associate Information Resources specified in
Appendix A.

Annotate rejected?

Assemble registered information resources to form new components.

Assemble new DTDs from current

Produce DTD as an instantiation (others are database schema, message definition) for modeling environment.

Notify change in Information Resources or authorized producer of tag.

Provide a capability to post planned changes to a registry

Approve and reject submissions

Forward request to different registry

Consumer services
. A consumer examines a registry to
select a tag structure for reuse in one or more applications that will
exchange data according to a pre-defined agreement.

Discovery

View the XML Tags with the following relationships:

Ancestor/ Descendant relationship: Provide the capability to view a Tags origin

Uses/Used by relationship: Provide the capability to view a complex Container Tags parent/child relationship

Data type information: Provide the capability to view a tags data type and related information.

Versioning relationship: Provide the capability to view an Information resources versions

Reference Sets: Provide the capability to view text related to the domain values or the related reference set

Amplifying information: Provide the capability to view other
information resources such as ERwin models, DTDs, documents, etc., which
describe or otherwise provide amplifying information.

View the XML Tags via a tree/hierarchy structure or tabular format.

View the XML Tags by giving the user multiple search options to find a specific Tag.

View the XML tags by giving the user the search option to find all tags of a given subscriber/author.

Each Information Resource will have its own web page to allow the
user to view all pertinent information, according to its information
resource type.

View the Information Resource Submittal Package containing the
following Information Resource artifacts: XML Tag Specification, XML
Spec (i.e. DTD, DCD etc.), Sample of XML document of the tag to be
submitted.

Display an XML Tag Specification form to the author of a
given information resource. This XML Tag Spec will be used for inputting
the requesting information for a specific Information Resource.

Provide capabilities to download the XML Tags or other selected Information Resources.

Catalog entities and attributes within servers to enable browsing, searching, retrieving of data related to XML sources.

Process ANSI standard SQL as specified in FIPS PUB 127-2

Establish rules to ensure maximum semantic understanding of a term as it appears in an XML document

Links to DTDs, DCDs,

Namespace

Provide a capability to subscribe for notification of changes to Communities of Interest (COE) or Information Resources.

Manager services

create and manage usernames, superusers

Establish acceptable naming convention not to be in conflict with
the DOD data standards convention and establish a relationship to other
naming conventions.

Create a naming structure within the COE architecture to express the
context and relationship of the naming convention to other naming
conventions specified in the I&RTS.

Define a set of metadata tags, information attributed to metadata
tags (meta-metadata) and other related terms for the maintenance and
control of XML tags.

Review/approve submission

Monitor changes to data models recorded in Registry

pass request off to (per explicit federation agreements)

Design the schema for an XML document

Structure services

Record structure

Check against standard (e.g., style guide wizard for tags)

Validate

Use and reference existing tags and associated semantic structures

Content services

Use & reference existing tags & associated semantic structures (extracted from Registry)

create new tags & associated semantic structures

interchange w/other design tools & environments

Record semantic structure in JTA-compliant formalism

Generate standard views

Version metadata objects

Generate xml & schema documents

Generate a document that includes (by ref or by value) a schema

Develop scheme to permit dynamic cross-referencing and indexing of XML objects.

Generate language (natural language) and charset values

Check conformance

Well-formed

Validate

Extract views of data

Disassemble document to materialize different query results into different tree structure

Render

Interrogate document

Transmit sufficient metadata to construct alternate, semantically-valid views (e.g., XSL)

Express version

Consume xml & schema documents

Parsers (dom, sax)

Check conformance

Well-formed

Validate

Create validation constraints shall enable a meaningful sharing of XML-based schemas and related information.

Extract semantically-valid views from an XML document (e.g., XSL)

Disassemble hierarchical view to relational representation

Render

REGISTRY SERVICES EXTERNAL INTERFACE REQUIREMENTS

The Registry shall provide standard APIs as specified in
Appendix B
.

DATA ACCESS SERVICES INTERNAL INTERFACE REQUIREMENTS

The XS function shall provide standard APIs as specified in
Appendix C
.

DATA ACCESS SERVICES INTERNAL DATA REQUIREMENTS

The
XS shall internally interface (transparent to the operator) with the
existing data elements of the DBIF, DAC, and COTS RDBMS products.

REGISTRY SERVICES ENVIRONMENT REQUIREMENTS

The Registry software shall be portable and required to execute on COE-compliant platforms.

PERSONNEL-RELATED REQUIREMENTS

Not applicable. Personnel requirements shall be determined by the developers of the system in which the XS module is embedded.

TRAINING-RELATED REQUIREMENTS

Not applicable. Training requirements shall be determined by the developers of the system in which the XS module is embedded.

LOGISTICS-RELATED REQUIREMENTS

The XS developer is responsible for software
maintenance, software support, and software updates. The DISA
Configuration Manager (CM) is responsible for distribution of the XS
product to system developers.

OTHER REQUIREMENTS

None.

PACKAGING REQUIREMENTS

The XS software shall be delivered in accordance with DII COE guidelines.

PRECEDENCE AND CRITICALITY OF REQUIREMENTS

The following table depicts the mapping of the
requirements in Section 3 to their corresponding precedence and
criticality code and to other related requirements within the XS SRS.
The precedence and criticality codes are the following:
