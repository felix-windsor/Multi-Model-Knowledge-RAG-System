# 1998 - themas - 2.0 General Description

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1998 - themas.pdf

Section: 2.0 General Description

2.0 General Description
This section of this SRS describes the general factors that
effect the THEMAS system and its requirements. This section does
not state specific requirements, it only makes these requirements
easier understood.
2.1 Product Perspective
The THEMAS system is a system that operates independent of any
other system, or any components of the heating and cooling system
to which it is attached. The THEMAS system, however, is composed
mainly of a hardware and software portion. This SRS only
specifies the requirements dealing with the software portion of
the system. If assumptions or dependencies about the hardware
were made, they are stated in this section of the SRS.
2.2 Product Functions
The THEMAS system is divided into four major sections: Monitor
Temperature, Determine Utilization, Initialize System, and System
Reports. All four sections have an associated software
configuration item; all except the System Reports have an
associated hardware configuration item. The hardware
requirements are contained in the system specification. The
functions of the software for the system are contained in the
following paragraphs.
2.2.1 Monitor Temperature
The monitor temperature function receives the valid temperature
and system parameters. The function then goes through the
process of determining temperature status. After this process is
done, either temperature limit is exceeded or the temperature
change is requested. If the temperature change is requested,
then the determine heating /cooling mode process is activated and
makes a heating/cooling request. Some other processes that help
the monitor temperature function are: validate temperature,
change thermostat setting, generate alarm, and system
initialization.
2.2.2 Determine Utilization
The determine utilization function receives the heating/cooling
request and utilization parameters. The function then processes
the status of all heating/cooling units and sends out either unit
unavailable or heating/cooling unit needed. The fun ction
generates either a unit unavailable event which goes into the
System Reports function or it generates a heating/cooling signal
to turn on/off the units. The Monitor Temperature and Initialize
2 - 1

D_THEMAS_SRS_001
System functions help the determine utilization to do its
processes.
2.2.3 Initialize System
The initialize system function receives the initialization data
for the THEMAS system. The processes that are associated with it
are: load heating/cooling unit definitions, turn off all
heating/cooling units, load th ermostat definitions, load
utilization parameters, set trigger values, set overtemperature
values, and establish valid temperature range. The outgoing
information that starts the entire THEMAS system is: clear all
heating/cooling signals, send thermostat definitions, send
utilization parameters, send trigger values, send overtemperature
values, and send valid temperature range.
2.2.4 System Reports
The system reports function receives event data from the THEMAS
system. This function is a database that stores all the events
in the THEMAS system. This function is mainly for the use of
the supervisor of the THEMAS system to maintain an efficient
heating and cooling system. The only process that interacts with
the system reports function is the generate event data process.
2.3 User Characteristics
This system is intended to be used by people that maintain the
heating and cooling systems in a building. The system should not
need intervention from outside users other than the supervisor to
maintain operation of THEMAS. The system should provide warnings
to the supervisor about faulty temperatures. The displaying of
the current status of the system to the supervisor should not
contain excessive information which could confuse the supervisor.
The system should provide information in the form of reports to
the supervisor so that the system can be run efficiently.
2.4 General Constraints
The general constraints of the THEMAS system focus on the
functionality provided by the external devices connected to i t.
The thermostats shall only provide temperature values and
temperature settings. The heating and cooling units provide no
feedback to the THEMAS system. When a signal is sent to a
heating or cooling unit, no signal shall be available to allow
the THEMAS system to determine if the signal sent to the unit was
realized by the unit.
2.5 Assumptions and Dependencies

2 - 2

D_THEMAS_SRS_001
In developing the requirements for the THEMAS system, several
assumptions have been made about the thermostat hardware and the
heating/cooling hardware. These assumptions are stated in the
following paragraphs.
2.5.1 Operating System Assumptions
The THEMAS system shall be designed to run on the Microsoft ®
Windows NT™ operating system. All the internal process
communications shall be designed to operate on this operating
system. Any communication with the thermostats and heating and
cooling units shall be done through the interface to these units.
These interfaces shall run on this operating system as well.
2.5.2 Thermostat Hardware Assump tions
It is assumed that the thermostat is capable of returning the
current temperature and the current desired temperature setting
to the THEMAS system. The thermostat is constantly returning
these values with no real time delay in between the thermostat
and the THEMAS system. The thermostat also has the capability of
being set and controlled by a user of the THEMAS system.
All data sent by the thermostat is in the correct format for the
THEMAS system to use.
2.5.3 Heating/Cooling Hardware Assumptions
It is assumed that the heating/cooling unit is incapable of
returning its current off/on status to the THEMAS system. The
heating/cooling unit has no real time delay when sending these
statuses to the THEMAS system. The heating/cooling unit shall
have the capability of being turned off and on by the supervisor
of the THEMAS system.

2 - 3

D_THEMAS_SRS_001
