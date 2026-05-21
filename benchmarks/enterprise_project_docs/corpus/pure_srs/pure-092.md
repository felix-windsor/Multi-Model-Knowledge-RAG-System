# 2000 - nasa x38 - 12 April 2000

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2000 - nasa x38.doc

Section: 12 April 2000

12 April 2000

Prepared for:

National Aeronautics and Space Administration
Lyndon B. Johnson Space Center
2101 NASA Road 1
Houston, Texas 77058-3696

Prepared by:

The Charles Stark Draper Laboratory, Inc.
555 Technology Square
Cambridge, Massachusetts 02139
Cage Code: 51993

DISTRIBUTION STATEMENT [A]

[Approved for public release; distribution is unlimited]

SOFTWARE REQUIREMENTS SPECIFICATION /
INTERFACE REQUIREMENTS SPECIFICATION

for the

X-38 Fault Tolerant System Services

Approved by:

RECORD OF REVISIONS

Rev
Result of
Pages Affected
Approval/Date
−
ECR 0079A
Initial Release
L.S.A. 5/4/00
A
ECR 0112
Revision due to Updated FTTP Specifications
RR 24 Aug 2000
B
ECR 134
Revision due to Updated FTTP Specifications
RR 22 Dec 2000
C
ECR148
Revision due to NASA Comments and Updated FTPP Requirements Document
RR 14 Mar 2001
D
ECR182
Revision due to NASA Comments and Updated FTPP Requirements Document
RR 2 Jul 2001
E
ECR190
Revision due to NASA Comments
RR 10 Aug 2001
F
ECR0226
Updated Requirements Traceability table, pages 65, 67, 68, 74, 83, 84, 86

TOC \o "1-5" \f 1. SCOPE PAGEREF _TOC518715562 \H 1
1.1 Identification PAGEREF _Toc518715563 \h 1
1.2 System Overview PAGEREF _Toc518715564 \h 1
1.3 Document Overview PAGEREF _Toc518715565 \h 4
2. REFERENCED DOCUMENTS PAGEREF _TOC518715566 \H 6
2.1 Government Documents PAGEREF _Toc518715567 \h 6
2.2 Non-Government Documents PAGEREF _Toc518715568 \h 6
3. REQUIREMENTS PAGEREF _TOC518715569 \H 7
3.1 Required States and Modes PAGEREF _Toc518715570 \h 7
3.2 CSCI Capability Requirements PAGEREF _Toc518715571 \h 8
3.2.1 System Initialization PAGEREF _Toc518715572 \h 8
3.2.2 Scheduling Services PAGEREF _Toc518715573 \h 9
3.2.2.1 Scheduling Execution PAGEREF _Toc518715574 \h 9
3.2.2.2 Task and Rate Group Execution PAGEREF _Toc518715575 \h 11
3.2.2.3 Exception Handling PAGEREF _Toc518715576 \h 12
3.2.3 Memory Management Services PAGEREF _Toc518715577 \h 13
3.2.3.1 Memory Protection PAGEREF _Toc518715578 \h 13
3.2.4 Communication Services PAGEREF _Toc518715579 \h 13
3.2.4.1 Sockets PAGEREF _Toc518715580 \h 14
3.2.4.1.1 Message Queue Sockets PAGEREF _Toc518715581 \h 15
3.2.4.1.2 Pipe Sockets PAGEREF _Toc518715582 \h 16
3.2.5 Fault Detection and Isolation PAGEREF _Toc518715583 \h 17
3.2.5.1 Initial BIT PAGEREF _Toc518715584 \h 17
3.2.5.2 Continuous BIT PAGEREF _Toc518715585 \h 20
3.2.5.3 RAM Scrub PAGEREF _Toc518715586 \h 21
3.2.6 Redundancy Management PAGEREF _Toc518715587 \h 21
3.2.6.1 Virtual Group Configuration PAGEREF _Toc518715588 \h 22
3.2.6.2 Recovery PAGEREF _Toc518715589 \h 22
3.2.6.2.1 Recovery from Processor Failure PAGEREF _Toc518715590 \h 26
3.2.6.2.2 Recovery from Link Failure PAGEREF _Toc518715591 \h 28
3.2.6.2.3 Recovery from Network Element Failure PAGEREF _Toc518715592 \h 28
3.2.7 Time Services PAGEREF _Toc518715593 \h 28
3.2.8 System Support Services PAGEREF _Toc518715594 \h 29
3.2.8.1 CTC Requirements PAGEREF _Toc518715595 \h 29
3.2.8.1.1 Telemetry Requirements PAGEREF _Toc518715596 \h 30
3.2.8.1.2 Command Read Requirements PAGEREF _Toc518715597 \h 30
3.2.9 Power Down Services PAGEREF _Toc518715598 \h 30
3.3 CSCI External Interface Requirements PAGEREF _Toc518715599 \h 30
3.3.1 Interface Identification and Diagram PAGEREF _Toc518715600 \h 30
3.3.2 IRIG-B/FTSS Interfaces PAGEREF _Toc518715601 \h 31
3.3.3 API/FTSS Interfaces PAGEREF _Toc518715602 \h 31
3.3.4 Network Element/FTSS Interfaces PAGEREF _Toc518715603 \h 32
3.3.5 Radstone/FTSS Interfaces PAGEREF _Toc518715604 \h 36
3.3.6 VxWorks/FTSS Interfaces PAGEREF _Toc518715605 \h 36
3.3.7 Multi-Protocol Communications Controller (MPCC)/FTSS Interfaces PAGEREF _Toc518715606 \h 36
3.3.8 FCP-ICP/FTSS Interfaces PAGEREF _Toc518715607 \h 37
3.4 CSCI Internal Interface Requirements PAGEREF _Toc518715608 \h 38
3.5 CSCI Internal Data Requirements PAGEREF _Toc518715609 \h 38
3.6 Adaptation Requirements PAGEREF _Toc518715610 \h 38
3.7 Safety Requirements PAGEREF _Toc518715611 \h 38
3.8 Security and Privacy Requirements PAGEREF _Toc518715612 \h 38
3.9 CSCI Environment Requirements PAGEREF _Toc518715613 \h 38
3.10 Computer Resource Requirements PAGEREF _Toc518715614 \h 39
3.10.1 Computer Hardware Requirements PAGEREF _Toc518715615 \h 39
3.10.2 Computer Hardware Resource Utilization Requirements PAGEREF _Toc518715616 \h 39
3.10.3 Computer Software Requirements PAGEREF _Toc518715617 \h 40
3.10.4 Computer Communications Requirements PAGEREF _Toc518715618 \h 40
3.11 Software Quality Factors PAGEREF _Toc518715619 \h 40
3.12 Design and Implementation Constraints PAGEREF _Toc518715620 \h 40
3.13 Personnel-related Requirements PAGEREF _Toc518715621 \h 40
3.14 Training-related Requirements PAGEREF _Toc518715622 \h 40
3.15 Logistics-related Requirements PAGEREF _Toc518715623 \h 40
3.16 Other Requirements PAGEREF _Toc518715624 \h 40
3.16.1 ICP Services PAGEREF _Toc518715625 \h 41
3.17 Packaging Requirements PAGEREF _Toc518715626 \h 42
3.18 Precedence and Criticality of Requirements PAGEREF _Toc518715627 \h 42
4. QUALIFICATION PROVISIONS PAGEREF _TOC518715628 \H 43
5. REQUIREMENTS TRACEABILITY PAGEREF _TOC518715629 \H 44
6. NOTES PAGEREF _TOC518715630 \H 91
6.1 List of Acronyms PAGEREF _Toc518715631 \h 91
6.2 Glossary PAGEREF _Toc518715632 \h 92

Figure Page

TOC \t "Figure Title,8" \c "Figure" Figure 1‑1 FCC Virtual Architecture. PAGEREF _Toc518707438 \h 2
Figure 1‑2. FCC Software Architecture. PAGEREF _Toc518707439 \h 3
Figure 3‑1. Fault Tolerant System Services States. PAGEREF _Toc518707440 \h 7
Figure 3‑2 Fault-down Map PAGEREF _Toc518707441 \h 23
Figure 3‑3 Fault Tolerant System Services CSCI External Interfaces. PAGEREF _Toc518707442 \h 31
Figure 3‑4. Network Element Interfaces to FTSS CSCI. PAGEREF _Toc518707443 \h 32

LIST OF TABLES

Table Page

TOC \t "table caption" \c Table 3.2-1. Software Exception Mapping Table. PAGEREF _Toc518707779 \h 12
Table 3.2-2. FCP IBIT Table. PAGEREF _Toc518707780 \h 18
Table 3.2-3 ICP IBIT Table PAGEREF _Toc518707781 \h 19
Table 3.2-4. ICP/PMC1553 IBIT Test Configuration. PAGEREF _Toc518707782 \h 20
Table 3.2-5. MPCC IBIT Test Configuration. PAGEREF _Toc518707783 \h 20
Table 3.3-1. Network Element Descriptor Block Interface. PAGEREF _Toc518707784 \h 33
Table 3.3-2. Network Element Data Block Interface. PAGEREF _Toc518707785 \h 34
Table 3.3-3. Data Element Definition Table for Radstone/FTSS Interfaces. PAGEREF _Toc518707786 \h 36
Table 3.3-4. Data Element Definition Table for FTSS Scheduler Interface. PAGEREF _Toc518707787 \h 38
Table 5-1. FTPP to SRS Trace Table. PAGEREF _Toc518707788 \h 44

SCOPE
Identification
This Software Requirements Specification/Interface Requirements Specification (SRS/IRS), Draper document number 297749, defines the software requirements and the external interface requirements for the Fault Tolerant System Services (FTSS) Computer Software Configuration Item (CSCI).
System Overview
The central part of the avionics architecture of NASA's X-38 Crew Return Vehicle is a quad-redundant Flight Critical Computer (FCC) which is based on Draper's Fault Tolerant Parallel Processor (FTPP) architecture. The FCC consists of four Flight Critical Processors (FCPs) operating as a quad-redundant Virtual Group (VG), five simplex Instrument Control Processors (ICPs) running as five separate VGs, five Draper Network Elements (NEs), four Multi-protocol/RS-422-cards, sixteen Digital I/O (DIO) cards, four Analog I/O cards, and four Decomm cards.
The FCPs, operating as a single, quad-redundant set, function as the main application processor. A complete suite of Fault Tolerant System Services (FTSS) software will be loaded onto the FCPs and provide an Application Programming Interface (API) between NASA's application code and the underlying hardware (Motorola Power PCs) and a COTS operating system (VxWorks). The FTSS software provides Scheduling Services, Communication Services, Time Services, Memory Management Services, Fault Detection and Isolation, Redundancy Management, System Support Services, and a Mission Management template. A reduced set of FTSS Communications Services will be loaded onto each ICP and will provide an API between the I/O software running on the ICPs and the NEs.
REF _Ref427650716 \* MERGEFORMAT Figure 1-1 is a high-level block diagram of the FCC virtual hardware configuration.
REF _Ref427650790 \* MERGEFORMAT Figure 1-2 is a high-level block diagram of the FCC software architecture.

Figure STYLEREF 1 \s 1‑ SEQ Figure \* ARABIC \s 1 1 FCC Virtual Architecture.

Figure STYLEREF 1 \s 1‑ SEQ Figure \* ARABIC \s 1 2. FCC Software Architecture.

Document Overview
This specification defines the software requirements and the interface requirements for the FTSS CSCI. It has been prepared using MIL-STD-498 and DI-IPSC-81433 and DI-IPSC-81434 for guidance. This SRS/IRS is organized as follows:
Section 1 - Scope: identifies the CSCI that this specification pertains to, provides an overview of FTSS, and provides an overview of this specification.
Section 2 - Referenced Documents: provides a list of documents referenced in this specification.
Section 3 - Requirements: specifies the engineering requirements for the FTSS CSCI
Section 3.1 describes the CSCI required states and modes.
Section 3.2 specifies the CSCI software requirements for each capability as follows:
3.2.1 System Initialization
3.2.2 Scheduling Services
3.2.3 Memory Management Services
3.2.4 Communication Services
3.2.5 Fault Detection and Isolation
3.2.6 Redundancy Management
3.2.7 Time Services
3.2.8 System Support Services
Section 3.3 describes the CSCI external interface requirements.
Section 3.4 identifies internal interface requirements.
Section 3.5 identifies internal data requirements.
Section 3.6 identifies the adaptation requirements.
Section 3.7 presents safety requirements.
Section 3.8 presents security and privacy requirements.
Section 3.9 discusses environment requirements.
Section 3.10 identifies computer resource requirements.
Section 3.11 describes software quality factors.
Section 3.12 identifies design and implementation constraints.
Section 3.13 identifies personnel requirements.
Section 3.14 identifies training-related requirements.
Section 3.15 identifies logistics-related requirements.
Section 3.16 identifies other requirements.
Section 3.17 presents packaging requirements.
Section 3.18 identifies precedence and criticality requirements.
Section 4 - Qualification provisions: defines a set of qualification methods and specifies for each requirement in Section 3 the method(s) to be used to ensure that the requirement has been met.
Section 5 - Requirements Traceability: provides a summary of traceability between system requirements expressed in the X-38 Fault Tolerant Parallel Processor Requirements document and the requirements elaborated in Section 3 of this document.
Section 6 - Notes: provides a list of acronyms and a glossary of terms used throughout this document.

REFERENCED DOCUMENTS
The following documents of the exact issue shown, or current issue if not shown, form a part of this specification to the extent specified herein. This document is directly traceable to the X-38 Fault Tolerant Parallel Processor Requirements document. In the event of conflict between that document and the contents of this specification, Draper will propose resolution of the conflict to NASA for approval.
Government Documents
Document No.
Date
Title
MIL-STD-498
