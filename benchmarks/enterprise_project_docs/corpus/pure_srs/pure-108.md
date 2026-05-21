# 2001 - ctc network - 4. Times Commands Accepted

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - ctc network.pdf

Section: 4. Times Commands Accepted

4. Times Commands Accepted

This is used to determine when a
center will accept a command
from a remote user. These are
device type dependent.
This is the response to a
command timeframe request.

Functional

The follow sections detail the functional requirements of the C2C project.
2.2.1

Data Collector Requirements

The Data Collector Requirements define what must be stored on the Data Collector.
requirements are listed in Table 21.

The

Table 21. Data Collector Requirements
Requirement
Number
C2C-DS-01

2.2.2

Requirement Description

Rationale or Comments

The Data Collector shall be designed to support the
storage of TMDD data elements and message set
information.

Data Transmission Requirements

The Data Transmission Requirements define the messaging protocols and message sets to be
used for C2C communications and are listed in Table 22.
Table 22. Data Transmission Requirements
Requirement
Number
C2C-DT-01
C2C-DT-02
C2C-DT-03

Requirement Description

Rationale or Comments

The C2C Project shall utilize the TMDD standard
(including message sets) to transmit information.
DATEX/ASN shall be used to transmit the TMDD
message sets.
TCP/IP shall be used to transmit the DATEX/ASN data. Derived from this requirement is
the necessary TCP/IP connection
management.

SOFTWARE REQUIREMENTS SPECIFICATION

21

2.2.3

Web Map Requirements

The Web Map application generates a map that can be displayed on an Internet WWW server.
The map provides a graphical depiction of the traffic conditions. The requirements for the
WWW map are listed in Table 23.
Table 23. WWW Map Requirements
Requirement
Number
C2C-MP-01
C2C-MP-03

C2C-MP-03
C2C-MP-04
C2C-MP-05

C2C-MP-06
C2C-MP-07
C2C-MP-08

C2C-MP-09

C2C-MP-10

C2C-MP-11

Requirement Description

Rationale or Comments

The map shall display interstates and state highways on
the graphical map.
The basemap data shall be derived from the North
Central Texas Council of Governments (NCTCOG) GeoData warehouse.
The map user shall be able to alter the current
magnification (zoom level) of the map.
The map user shall be able to pan the map in each of the
following directions: North, South, East or West.
Each link displayed on the map shall be color coded to
provide a graphical depiction of speeds. A configuration
file shall be provided to specify specific speed values.
The color coding shall be as follows:
• Green - speeds > TBD MPH
• Yellow - speeds between TBD and TBD MPH
• Red – speeds below TBD MPH
The map shall display the current incidents (as icons)
known to the C2C Project.
The user shall be able to click on an incident icon to
obtain further information about the incident.
All current incidents shall be displayed in tabular format
with the following information contained in the table:
• Location
• Type of incident (e.g., accident, lane closure)
• Severity of incident
• Incident status
• Travel direction
• Effected lanes
The map shall be capable of displaying the following for
a DMS:
