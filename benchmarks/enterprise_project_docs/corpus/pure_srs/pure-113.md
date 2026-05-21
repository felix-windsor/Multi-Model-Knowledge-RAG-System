# 2001 - elsfork - 4 System

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 4 System

4 System
This section describes the parties’ functional requirements.
4.1 General
Basically the communication system must assist the operators, users and other interested parties in performing their tasks by provision of services. The system must be flexible in supporting future requirements and future developments. The system must be open in the sense that
“anyone shall be able to get information on anything from anywhere”, once they have authorisation to the system. The system thus shall be adapted to individual users and services
provided accordingly by means of configurations, set-ups etc.
The communication system shall be based on open and widely accepted methods with a high
degree of interface possibilities. The system shall be robust and reliable, but the system shall
not be used for the safe and secure operation of the plant. Faults in the communication system
shall not cause malfunction of an individual wind turbine. The system shall be designed in a
way that faults of a sub-system interferes as little as possible with functions of the communication system as a whole.
In designing the system it shall be taken into account, that the physical environment at the
plant typically has a wide span of temperature, moisture, salinity and vibration levels.

4.1.1 Data interchange for secondary systems
Secondary systems may be for example Beacons (sea and air), Fire protection, Emergency
alarm, Intruder alarm, Power supplies and emergency power systems, Meteorological stations, Safety systems for personnel, Data logger systems and Condition monitoring. Condition
monitoring will be very important for offshore wind farms and it will be a standard function
in all larger wind turbines.
The condition monitoring system provides status and analysis reports for components. The
analysis may be in the form of spectres, trends, statistic figures, time tracking etc.
The values shall be available for display on operator HMI as well as for storage (databases).
Updating of values shall be selectable down to an interval of 1 sec. All data must be stored in
the plant controller for transmission on demand. Transfer of data from the buffers may be
carried out off-line without synchronism with real-time.
4.2 Functions
The basic functions of the system can be grouped in two main categories, Operational or control functions and System management functions.
A third group is Process automation functions, which involve functions that operate with process data directly without the involvement of an operator. However this group is not within
the scope of this specification and is not further treated.

4.2.1 Operational functions
The operational functions are needed for the normal daily operation of the wind power plant.
In these functions an HMI, either local or remote, is included. The operational functions are
used to present process or system information to an operator or to provide him the control e.g.
by commands. The operational functions include the following:
• Access security management
Access to operational functions has to be controlled by a set of rules. Access control is to
Page 11

ELFORSK

•
•

•
•

•

•

•

allow the capability to restrict an authenticated client to a pre-determined set of services
and objects.
Supervision (Wind power plant operation and Network operation)
Local or remote monitoring of the status and changes of states (indications) for operational devices.
Control
Control function allows an operator or an automatic function to operate equipment like
switchgear or transformer, a protection, etc. Control is subject to miscellaneous filters that
check that there will be no damage if the control is issued.
Parameter changes (parameter set switching, subset of setting, or single parameter)
In addition to single parameters, an application may have several possible pre-defined parameter sets (but only one active set).
Alarm management
Alarm is generated when a data of the system takes a value that shall be specially considered by the operator, i.e. there is a need for attracting attention to some abnormal state.
Alarm management functions allow an operator to visualise, acknowledge and clear
alarms.
Event and Log management
Functions for continuous scanning of devices for alarms, operator control actions and
changes in state, and for recording the events chronologically with date and time information.
Data retrieval of configuration data and settings
Functions for a follow-up of parameter settings should include services to retrieve all parameters (names, values and units for all setpoints) or to retrieve only those that differ
from the default values.
Disturbance / fault record retrieval
Data retrieval for the purpose if display and bulk data storage of fault data.

4.2.2 System management functions
System management functions include both functions for system support and for system configuration and maintenance. System support functions are used to manage the system itself
(e.g. Network management, Time synchronisation, and Self-checking of communication
equipment). The functions support the total system and have no direct impact on the process.
System configuration or maintenance functions are used to set-up or evolve (maintain) the
system. The system configuration and maintenance functions include the setting and changing
of configuration data and the retrieval of configuration information from the system. The most
important examples of System Management functions are:
System Support
• Network management
Functions needed to configure and maintain the communication network. The basic task is
the identification of communication objects/devices.
• Time synchronisation
Synchronisation of devices within a communication system.
• Self-checking
The self-check detects if an object or device is fully operational, partially operational or
not operational.

Page 12

ELFORSK

System Configuration and Maintenance
• Software management
The software management include version control, download, activation and retrieval of
software.
• Configuration management
The function is used to download, activate and retrieve configuration data
• Operative mode control
Allows an authorised operator to start and stop functions or objects within the system, including manual activation or reset of subsystems.
• Setting (parameter set)
The setting function allows an operator read and to change on or more parameters affecting the behaviour of the object/device.
• Test mode
Possibility to check a function but avoiding impact on the process (blocking of process
outputs).
• System security management
Function to allow control and supervision of the security of the system against unauthorised access or loss of activity.
4.3 Other functions, out of scope
The functions here described are not within the scope of this Specification, that is communication for remote operation. However, from an overall communication system point of view,
it can be desired that all communication have to be able to coexist on the same transmission
media.

4.3.1 Local functionality
Local system functionality for hook-up for temporary data transmission is not within the
scope of this specification. Thus the communication system for remote operation do not need
to support functions such as hook-up of portable PC at the plant for Internet access, WEBcam connection, E-mail service, Program execution, Plant information and Service instructions.

4.3.2 Voice and visual communication
A verbal dialogue system (e.g. telephone) is essential for contacts between operation and
maintenance personnel in the wind power plant and the control centre operator. Video communication may also facilitate the co-operation between field personnel and control centre
personnel. Video may also be used for supervision of equipment. However these function is
not within the scope of this specification.

4.3.3 Actor specific functions
Functions that are of no relevance to the wind power plant or wind turbine operators, the most
important actors, are considered to be out of scope. Energy accounting for the network operator is one example.

Page 13

ELFORSK
