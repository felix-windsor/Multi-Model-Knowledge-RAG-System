# 2001 - ctc network - 1.0 SCOPE

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - ctc network.pdf

Section: 1.0 SCOPE

1.0 SCOPE
This Software Requirements Specification (SRS) provides the requirements for the Center-toCenter Communications (C2C) Communications project.
1.1

Identification
Project Title:

1.2

Project Number:

Center-To-Center Communications
04594, EO 17
04594, EO 22

Abbreviation:
Version Number:
Release Number:

C2C
3.0
1

System Overview

This document describes the requirements for the Dallas/Ft. Worth (DFW) Regional “Center-toCenter (C2C) Communications Network” that is based on a Texas Department of Transportation
(TxDOT) C2C project. The TxDOT C2c project initially connected the DFW TxDOT Traffic
Management Centers (TMCs). This C2C infrastructure implements a repository for traffic data
and provides a mechanism to exchange device control information between TMCs.
The C2C project will be implemented using the evolving ITS Traffic Management Data
Dictionary (TMDD) standard, the message sets associated with TMDD, other ITS Data Elements
and Message Sets. The use of ITS standards will create a system that is reusable for other ITS
application areas and will provide the State of Texas with a baseline system that can be cost
effectively extended in the future.
1.3

Operational Concept

The C2C infrastructure must interconnect several dissimilar traffic management systems. In
order to create the C2C infrastructure, interfaces to the existing systems will be created. The
data from these interfaces will communicate with the existing system in a “system specific”
format. The data being deposited into the C2C infrastructure will be converted to a standard
format (based on the ITS standards). The C2C infrastructure is being created using a series of
building blocks. These building blocks allow the software to be utilized in a number of
configurations (by simply altering the configuration parameters of the software).
In a region such as Dallas/Ft. Worth, multiple instances of the building blocks will be utilized.
The software is being designed so that multiple instances of a building block can be deployed by
simply “configuring” the building block of operation within a specific agency. Conceptually, the
C2C infrastructure would be deployed as depicted in the following diagram:

SOFTWARE REQUIREMENTS SPECIFICATION

1

Any data that is passed into the “cloud” in the above figure will be based on the ITS standards.
Systems will interface to the “cloud” using a project defined protocol. New systems that are
deployed (based on the ITS standards) will not utilize the project defined protocol but will be
moved “into” the cloud (because they themselves would be based on the ITS standards.
1.4

Goals and Objectives

The C2C project has the following goals:
•

To provide a common repository for traffic information for the DFW Metroplex.

•

To provide a World Wide Web based graphical map to display traffic conditions in the
DFW Metroplex.

•

To provide a Microsoft Windows application that will allow agencies without a formal
Traffic Management Center (TMC) to participate in the C2C infrastructure and
information sharing.

•

To provide a system which supports ITS center-to-center communications for
command/control/status of various ITS field devices including: Dynamic Message
Signs, Lane Control Signals and Closed Circuit Television Cameras (CCTVs), Ramp
Meters, and Highway Advisory Radios (HARs).

•

To utilize National ITS standards to implement the project.

•

To provide a software system that is extensible all local or regional partners. This
would allow a “local” common repository to be created by “linking” individual
partners, a “regional” common repository to be created by “linking” local common
repositories and a “statewide” common repository to be created by “linking” regional
common repositories.

SOFTWARE REQUIREMENTS SPECIFICATION

2

1.5

Constraints

None.
1.6

Document Overview

Section 2 defines the requirements of the system. Acronyms are defined in Appendix A.
1.7

Related Documents

•

Concept Of Operations Framework For The Dallas/Ft. Worth Regional Center-to-Center
Communications Network, Version 1.0, Southwest Research Institute, November 2001.

SOFTWARE REQUIREMENTS SPECIFICATION

3
