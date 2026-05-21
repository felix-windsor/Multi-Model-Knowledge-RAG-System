# 2001 - elsfork - 2 Scope and Outline of the Document

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 2 Scope and Outline of the Document

2 Scope and Outline of the Document
The scope of this specification is communication systems supporting functions mainly for
remote operation and supervision of wind power plants. Apart from the functions needed by
the operator the system shall support also functions needed by other parties. The functions are
further described in Section 4 System.
This chapter explains the different parts of the operational system and how they are defined.
The structure of the document is described by Figure 1, where the different subsections correspond with the disposition of the document.
SYSTEM

(operational functions)

COMMUNICATION

Users

Wind farm

(services,functions)

COMMUNICATION

WFMC

SCADA

SWPU

CU
SWPU

SWPU

CU

CU
SWPU

CU
DATA

DATA

WFMC: Wind Farm Main Controller
CU:
Control Unit
SWPU: Single Wind Power Unit

Figure 1: System overview for wind power communication
2.1 System description
On the highest level the system is described from an operational point of view, i.e. the functions needed for remote operation and supervision of wind power plants. The functions are
described from a communication point of view. The affected actors and functions are described in Section 4 System.
As depicted in Figure 1, there are both wind farms and single wind turbines. In the case of
bigger plants there is usually a wind farm main controller (WFMC) and an internal communication system, which connects all the turbines to the WFMC for further external communication.
2.2 Communication System
In this Specification “communication system” shall be understood as a system for:
• Transfer of data from a process/plant level to a level, where data are accessible for an application in a standardised format
• Transfer of data to a process/plant level for distribution of commands, operational settings
etc.
The requirements on the communication system are specified in Section 5 Communication.
Page 7

ELFORSK

Data may also be understood as verbal communication, as in telephone communication, as
well as visual communication, as in video communication. The different kinds of data communication need to be able to coexist on the same transmission network.
2.3 Wind Power Plant Data
The different operational functions need access to data in the power plant and the sending and
receiving parts must be able to interpret and handle the data. Therefore, the data structure
must be defined together with the data types and other characteristics. This is done in Section 6 Plant Data.

Page 8

ELFORSK
