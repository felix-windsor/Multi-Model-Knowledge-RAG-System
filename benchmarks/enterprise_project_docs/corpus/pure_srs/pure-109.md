# 2001 - ctc network - 2. Status

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - ctc network.pdf

Section: 2. Status

2. Status

SOFTWARE REQUIREMENTS SPECIFICATION

22

2.2.4

Incident GUI Requirements

The Incident GUI must provide data to the C2C Infrastructure. The GUI requirements are listed
in Table 24.
Table 24. Incident GUI Requirements
Requirement
Number
C2C-GI-01
C2C-GI-02

C2C-GI-03

C2C-GI-04
C2C-GI-05
C2C-GI-06
C2C-GI-07
C2C-GI-08
C2C-GI-09

2.2.5

Requirement Description

Rationale or
Comments

The Incident GUI shall allow the user to enter incident or lane closure
information without the use of an Center.
The Incident GUI shall allow the user to input the following
information for each incident:
•
Location (latitude/longitude)
•
Description
•
Status
•
Effected lanes
•
Detection time
•
Response time
•
Estimated time to clear queue
•
Queue length
The Incident GUI shall allow the user to input the following
information for each lane closure:
•
Location (latitude/longitude)
•
Description
•
Effected lanes
•
Date
•
Start time
•
End time
The GUI shall provide a list of previously entered incidents.
The GUI shall allow the data about an incident to be modified.
The GUI shall allow a user to delete a previously entered incident.
The GUI shall provide a list of previously entered lane closures.
The GUI shall allow a user to delete a previously entered lane closure.
The GUI shall allow a user to delete a previously entered lane closure.

Remote Control GUI

Table 25 contains the requirements for the Remote Control GUI.

SOFTWARE REQUIREMENTS SPECIFICATION

23

Table 25. Remote Control GUI
Requirement
Number

Requirement Description

Rationale or Comments

The remote Center Control GUI shall be designed to
execute on a public network (e.g., Internet) and transmit
equipment requests to the C-2-C software system.

The Remote Control GUI will
execute as a local application on
a PC. The application will
generate TMDD device control
messages that will be sent to a
Center for processing.
Connectivity through the various
firewalls and gateways is not
addressed by this requirement.

C2C-CG-01

C2C-CG-02

C2C-CG-03

C2C-CG-04

C2C-CG-05

C2C-CG-06

C2C-CG-07

C2C-CG-08

C2C-CG-09

C2C-CG-10

C2C-CG-11

When the GUI application is initiated, the user shall be
prompted for the following information:
• User name
• Password
The user shall be provided with the capability to select a
network identifier for a device command/control request.
Once an Center is selected, the user shall be able to select
a DMS from a list and provide the following information:
• Target DMS
• Message to be displayed
• Beacons On/Off
Once an Center is selected, the user shall be able to select
a LCS from a list and provide the following information:
• Target LCS
• Assignment of lane arrows
Once an Center is selected, the user shall be able to issue
a CCTV switching command:
• Source (input)
• Destination port (output)
Once an Center is selected, the user shall be able to select
a CCTV from a list and provide the following
information:
• Target CCTV
• Device control including:
• Pan
• Tilt
• Zoom
Once an Center is selected, the user shall be able to select
a Ramp Meter from a list and provide the following
information:
• Target Ramp Meter
• Plan
Once an Center is selected, the user shall be able to select
a HAR from a list and provide the following information:
• Target HAR
• Text to be sent to the HAR
Once an Center is selected, the user shall be able to select
a Traffic Signal from a list and provide the following
information:
• Target Traffic Signal
• Plan
Once an Center is selected, the user shall be able to select

SOFTWARE REQUIREMENTS SPECIFICATION

24

Requirement
Number

C2C-CG-12

C2C-CG-13

C2C-CG-14

C2C-CG-15

2.3

Requirement Description

Rationale or Comments

a HOV from a list and provide the following information:
• Target HOV
• Plan
Once an Center is selected, the user shall be able to select
a School Zone from a list and provide the following
information:
• Target School Zone
• Plan
Once an Center is selected, the user shall be able to select
a Reversible Lane from a list and provide the following
information:
• Target Reversible Lane
• Plan
Once an Center is selected, the user shall be able to select
a Dynamic Lane from a list and provide the following
information:
• Target Dynamic Lane
• Plan
For each device command/control status request sent by
the Remote GUI, the status returned from the network
identifier will be displayed in a scrollable list on the GUI.

Design and Construction Standards

The computer resource requirements are listed in Table 26.
Table 26. Computer Resource Requirements
Requirement
Number
C2C-DC-01
C2C-DC-02
C2C-DC-03

Requirement Description

Rationale or Comments

The C2C Server shall execute in a Microsoft Windows
NT environment.
A DATEX/ASN runtime library shall be available on any
computer communicating to the C2C project.
The web server application shall use ESRI's ARC
Internet Map Server (ARC IMS) product for creating of
map images.

The Design and implementation requirements are listed in the in Table 27.

SOFTWARE REQUIREMENTS SPECIFICATION

25

Table 27. Design and Implementation Requirements
Requirement
Number
C2C-DC-04
C2C-DC-05
C2C-DC-06
C2C-DC-07
C2C-DC-08

2.4

Requirement Description

Rationale or Comments

The C2C shall execute in a Microsoft Windows NT
environment.
The C2C shall be implemented in the C/C++
programming language.
The C2C web interface shall be implemented using
C/C++ and ESRI ARC IMS.
The Incident GUI shall be implemented using C/C++ and
ESRI Map Objects.
The Remote Control GUI shall be implemented using
C/C++ and ESRI Map Objects.

Operational

The C2C Project shall be capable of operating in one of two modes: normal mode for normal
operations or in test mode for development and testing. The requirements for these modes are
listed in Table 28.
Table 28. Required States and Modes Requirements
Requirement
Number
C2C-OP-01

C2C-OP-02

Requirement Description

Rationale or Comments

The C2C shall be able to operate in normal mode. In this
mode the C2C receives data from all connected systems,
including the Incident GUI, and combines the data into a
single data store (database).
The C2C shall be able to operate in test mode. In this
To provide additional
mode, the C2C performs normal mode operations and
information for development and
also logs activities.
testing.

SOFTWARE REQUIREMENTS SPECIFICATION

26

APPENDIX A
ACRONYMS

SOFTWARE REQUIREMENTS SPECIFICATION

ACRONYMS
ASN.1
ATIS

Abstract Syntax Notation One
Advance Traveler Information System

ATMS

Advanced Traffic Management System

CCTV

Closed Circuit Television

DATEX/ASN

DATEX/Abstract Syntax Notation

DFW
DMS

Dallas/Ft. Worth
Dynamic Message Sign

DT

Data Transmission

ESS

Environmental Sensor Stations

GI

Incident GUI

GUI
HAR

Graphical User Interface
Highway Advisory Radio

HOV

High Occupancy Vehicle

ICD

Interface Control Document

IMS

Internet Map Server

ISP
ITS

Information System Provider
Intelligent Transportation Systems

LCS

Lane Control Signal

MPH

Miles Per Hour

MULTI

Mark-Up Language for Transportation Information

NCTCOG
NTCIP

North Central Texas Council of Governments
National Transportation Communications for ITS Protocol

SRS

Software Requirements Specification

TBD

To Be Determined

TCP/IP

Transmission Control Protocol/Internet Protocol

TMC
TMDD

Traffic Management Center
Traffic Management Data Dictionary

TxDOT

Texas Department of Transportation

WWW

World Wide Web

SOFTWARE REQUIREMENTS SPECIFICATION

A-1
