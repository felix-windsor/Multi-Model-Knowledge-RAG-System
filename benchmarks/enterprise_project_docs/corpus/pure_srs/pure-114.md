# 2001 - elsfork - 5 Communication

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 5 Communication

5 Communication
In this section the requirements on the communication between the different units in the system are specified.

COMMUNICATION
(services,functions)
COMMUNICATION

WFMC

SCADA

SWPU

CU
SWPU

SWPU

CU
DATA

CU
SWPU

CU
DATA

WFMC: Wind Farm Main Controller
CU:
Control Unit
SWPU: Single Wind Power Unit

Figure 2: Communication between control units and SCADA
In wind farms a local communication system might be the link between overall control units
and the individual wind turbine controller. An overall control unit may be a “wind farm main
controller” conducting an overall governing of the plant output and the grid compatibility.
5.1 Basic Services
As stated in Section 2.2 the main objective for the communication system is to transfer data to
and from the process/plant level. The overall purpose is to support the functions described in
Section 4. In order to accomplish this the basic services of the communication system shall
include the following:
• Connection establishment and release
• Authentication
• Identification of functional object and devices
• Data access and transfer
• Reliable communication over a network
5.2 Data Transfer Principles
Data can be transferred according to one of the following principles:
A. Periodic data transfer (all data or only data that has changed since last transfer)
B. Data transfer on demand
C. Event driven (spontaneuos) data transfer
D. Command transfer
E. Set point transfer

Page 14

ELFORSK

5.3 Different kinds of data
The following kinds of data need to be supported:
I.
Measurements/analogue data (signals) from the wind power plant
II.

Set points sent to the wind power plant

III.
Binary Signals/Status data from the wind power plant.
IV.
Binary control commands to the wind power plant
V.
Alarms
VI.
Events
VII. Counters
VIII. Timers
IX.
Data structures
X.
Time series data
XI.
Short text messages
XII. Flat files
A specific kind of data put specific requirements on the communication system. Alarms, for
example, need to reach the remote control centre much faster than events. And the latter is
often grouped with other events before transmission. The mapping between the different
kinds of data, the data transfer principles and the operational functions are described in section 5.4.
The different kinds of data can be grouped and named real time/on-line data, historical data or
forecasts/schedules. On-line data include measurements/analogue data, binary signals/status
data (but might also include counters). Historical data include measurement data (calculated
values), counters and timers. Schedules could be start/stop schedules for individual wind turbines.
The different kinds of data for wind power applications is further described, in more detail, in
Section 6 Plant Data.
5.4 Mapping between functions and ways of communication
Data are either polled at the node (the wind turbine) or periodic and automatic sent out from
the node (periodic broadcast and event driven transfer). The important requirement is the
‘scanning rate’ (maximum delay).
Historical data, counter’s and log’s are transferred on demand (a request is sent to the wind
turbine and the information is send back).
Alarm data shall be sent from the wind turbine on occurrence.
Setting data in the wind turbine and giving orders to the wind turbine are sent to the wind
turbine when needed.

Page 15

ELFORSK

Functions

Data kinds

Transfer principles

(see Section 4.2)

(see Section 5.3)

(see Section 5.2)

Access security management
Supervision
Control
Parameter changes

XI
I, III
II, IV
II

B, D
A, B, C
D, E
B, D, E

Alarm management
Event and Log management

V, XI, XII
VI, XI, XII

C
A, B, C

Data retrieval of configuration data and
settings
Disturbance /
fault record retrieval
System Management Functions
System support
System Configuration and Maintenance

VII, VIII, IX,
X, XII
IX, X, XII

A, B
B

Most
IX, XII

Most
B, E

Comments

Operational Functions
Encrypted?

E.g. historical data

Network mgmt, time synch..
Mgmt, settings..

Table 2: Possible mapping between functions and ways of communication
5.5 General Requirements for All Data Kinds
1. It should be possible to time stamp all data. Time stamped data shall be stamped with ‘last
updated date + time’ (UTC time). The accuracy and resolution of the timestamp should be
at least 10 ms.
2. All analogue measured values should have readable properties like ‘signal quality’ and
‘scanning rate’. This information does not have to be included with every data transfer.
The averaging time and the measuring and averaging method should be documented for all
data.
