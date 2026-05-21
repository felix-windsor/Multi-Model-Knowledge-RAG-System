# 1995 - gemini - 3. The target IOC computer cards are not to be established until as late as possible, to

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 3. The target IOC computer cards are not to be established until as late as possible, to

3. The target IOC computer cards are not to be established until as late as possible, to
take advantage of technology advances while staying compatible with the development systems. A baseline system is included as part of the ICS work package.

All accesses to the control electronics hardware will be through VME IOC's, using
the EPICS software. No other control interfaces are permitted.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

There are places in the Gemini system where software exists below the IOC level that is
interfaced to IOC software. The standards for this interface is not part of this specification. The use of this software is to be explained and discussed on a case-by-case basis.
In cases where there is a distributed network of target microprocessors involved at this
level, it is appropriate to provide a standard sub-network. This type of Fieldbus is to be
implemented using an ALAN/BRADLEY bus, ProfiBus, or other approved Fieldbus.
In cases where there is a distributed set of commercial equipment to be controlled the recommended method is to use an ALAN/BRADLEY system to control the equipment manually and interface to it using RS-422 or similar connection to an IOC.

All communication hardware must meet the data flow requirements and software protocols defined in this document. The following recommendations are based on currently
available technology. It is entirely appropriate that changes will be made to take advantages of changes to that technology.

A.The control LAN is based on Ethernet IEEE 802.3.
B.The Time distribution systems are described in the Software Design Description..
C.The detector LAN is also based on Ethernet, at least for the development systems. A
solution meeting the performance requirements of the final system is to be decided later.

D.The backbone LAN cannot be Ethernet because of bandwidth requirements. A FDDI
system is recommended for the backbone LAN.

E.Cabling of LANs is shown in Figure 4 - 1. Also shown are cabling requirements to the
base facility. Requirements for cabling are given in the Electronic Design Specification.

F.Interlock connections must be provided for all critical subsystems. The software interface to the interlock system is defined in the Instrument Control System Infrastructure
Work Package Definition.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

FIGURE 4 - 1

Mauna Kea Cabling (Cerro Pachon is similar)

G.Routers, gateways, etc. are defined in the Electronic Design Specification. Their
logical placements are shown in Figure 4 - 1, above.

H.Links to the WAN are defined in the Electronic Design Specification and shown in
Figure 4 - 1, above. There is a requirement of at least one dedicated link of a T1
bandwidth for remote support, development and testing.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS

Wherever possible, Gemini software is to take advantage of existing software. However,
all existing software is to be evaluated in terms of the specifications given here. This
helps reduce life-cycle costs and maintenance efforts.

Life cycle constraints are discussed in the Gemini Software Management Plan.

The Experimental Physics and Industrial Control System (EPICS) toolkit is the foundation
of the Gemini control system. EPICS was originally developed at the Los Alamos and
Argonne National Laboratories for use in large accelerator control and diagnostics systems. It is now an established standard within the international High Energy Physics community and is gaining acceptance amongst astronomical sites.
Within the EPICS community there is understood to be an informal distinction between
two classes of developers, labeled ‘Internals’ and ‘Applications’. Although these definitions are nowhere written down, this understanding serves as the basis for many discussions with the community and for the nature of training classes.

Note: The bulk of this section is taken from the EPICS document ‘EPICS Overview’.
EPICS consists of a set of hardware and software components from which a control system can be created.

• OPI Operator Interface.
This is a UNIX based workstation which can run various EPICS tools.

• IOC Input Output Controller.
This is VME/VXI based chassis containing a Motorola 68xxx processor, various I/O
modules, and VME modules that provide access to other I/O buses such as GPIB.

• LAN Local area network.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
This is the communication network which allows the IOCs and OPIs to communicate. EPICS provides a software component, Channel Access, which provides
network transparent communication between a Channel Access client and an arbitrary number of Channel Access servers.

Database
The heart of an IOC is a memory resident database together with various memory
resident structures describing the contents of the database. EPICS supports a large
and extensible set of record types, e.g. ai (Analog Input), ao (Analog Output), etc.
Each record type has a fixed set of fields. Some fields are common to all record types
and others are specific to particular record types. Every record has a record name and
every field has a field name. The first field of every database record holds the record
name, which must be unique across all IOCs attached to the same TCP/IP subnet.
A number of data structures are provided so that the database can be accessed efficiently. Most software components, because they access the database via database
access routines, do not need to be aware of these structures.
Database Access
With the exception of record and device support, all access to the database is via the
channel or database access routines.
Database Scanning
Database scanning is the mechanism for deciding when to process a record. Four
types of scanning are possible: Periodic, Event, I/O Event, and Passive.
Periodic: A request can be made to process a record periodically. A number of time
intervals are supported.
Event: Event scanning is based on the posting of an event by any IOC software
component. The actual subroutine call is: post_event(event_num)
I/O Event: The I/O event scanning system processes records based on external
interrupts. An IOC device driver interrupt routine must be available to accept the
external interrupts.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
Passive: Passive records are processed as a result of linked records being processed or
as a result of external changes such as channel access puts.
Record Support, Device Support, and Device Drivers
In order to remove record specific knowledge from database access, each record type has
an associated record support module. Similarly, in order to remove device specific knowledge from record support, each record type can have a set of device support modules. If
the method of accessing hardware is complicated, a device driver can be provided to
shield the device support modules. Many record types, in particular all types not associated with hardware, do not have device support or drivers.
The IOC software is designed so that the database access layer knows nothing about the
record support layer other than how to call it. The record support layer in turn knows nothing about it’s device support layer other than how to call it. Similarly the only thing a
device support layer knows about it’s associated driver is how to call it. This design allows
a particular installation and even a particular IOC within an installation to choose the set
of record types, device types, and drivers it wishes to use. The remainder of the IOC system software is unaffected.
Every record support module must provide a record processing routine. It is this routine
that is called by the database scanners. Record processing consists of some combination of
a standard set of functions.
Database Monitors
The routines described in this section provide a callback mechanism for database value
changes. This allows the caller to be notified when database values change without constantly polling the database. A mask can be set to specify value changes, alarm state
changes, and/or archive changes.
At the present time only channel access uses database monitors. No other software should
use the database monitors. Because they are of interest only to channel access, the monitor
routines will not be described.

Channel access provides network transparent access to IOC databases. It is based on a client-server model. Each IOC provides a channel access server which is willing to establish
communication with an arbitrary number of clients. Channel access client services are
available on both OPIs and IOCs. A client can communicate with an arbitrary number of
servers.
It should be noted that channel access does not provide access to database records as
records. This is a deliberate design decision. This allows new record types to be added

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
without impacting any software that accesses the database via channel access. A
channel access client can communicate with multiple IOCs having differing sets of
record types.

EPICS provides a number of OPI based tools. These can be divided into two groups
based on whether or not they use channel access. Channel access tools are real time
tools, i.e. they are used to monitor and control IOCs.
Channel Access Tools

• MEDM
Motif version of combined display manager and display editor.

• DM Display Manager.
This tool reads one or more display list files created by EDD, establishes communication with all necessary IOCs, establishes monitors on process variables,
accepts operator control requests, and updates the display to reflect all changes.

• ALH Alarm Handler.
This is a general purpose alarm handler driven by an alarm configuration file.

• AR Archiver.
This is a general purpose tool to acquire and save data from IOCs.

• Sequencer
A tool which runs in an IOC or OPI and emulates a finite state machine.

• Other OPI CA clients
It is possible to interface preexisting software systems to the channel access
library. This has been done for several commercial packages including IDL/
PvWave, Mathematica, and WINGZ to allow access and manipulation of EPICS
process variables by these applications.
Other OPI Tools

• DCT Database Configuration Tool.
This tool is used to create a run time database for an IOC

• CAPFAST and GDCT Graphical Database Configuration Tools
These tools are used to create a run time database for an IOC

• EDD Display Editor.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
This tool is used to create a display list file for the Display Manager. A display list file
contains a list of static, monitor, and control elements. Each monitor and control element has an associated process variable.

• SNC State Notation Compiler.
It generates a C program that represents the states for the IOC or OPI Sequencer tool.

• Build Tools
Tools are available to create the various database components from ASCII definition
files.

• Source/Release
EPICS provides a Source/Release mechanism for managing EPICS.

EPICS consists of a set of core software and a set of optional components. The core software, i.e. the components of EPICS without which EPICS would not function, are:

• Channel Access - Client and Server software
• Database
• Scanners
• Monitors
• DCT
• Build Tools
• Source/Release
All other software components are optional. Of course any application developer would
be crazy to ignore tools such as MEDM (or EDD/DM). Likewise an application developer
would not start from scratch developing record and device support. Most OPI tools do not,
however, have to be used. Likewise any given record support module, device support
module, or driver could be deleted from a particular IOC and EPICS will still function.

Each of the Gemini Controls work packages will be involved with some aspect of EPICS
development ranging from creation of new device drivers to database creation and the
design of new CA clients.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
The details of the EPICS work required can be broken down into several broad categories which reflect the nature of the various work packages. This breakdown is
given in the following subsections:

• Channel Access - Client and Server Software, Scanners, Monitors
Gemini will not modify the heart of EPICS. We leave this to Los Alamos.

• Host-based Development Tools (CAPFAST, EDD, etc.)
Neither will Gemini plan on creating new development tools.

• Record Support, Device Support, and Device Drivers
For Gemini this entails support for new devices:
PMAC, VMIC5578, BANCOMM

• Other OPI CA Clients
The OCS may need a CA client that implements the OCS Attribute/Value protocol.
The DHS may need a CA client that gathers logging information. This could be an
EPICS AR (or AR_cmd) task.

• IOC Database
• IOC SNC programs
• Files associated with OPI Channel Access Tools
These would include MEDM .adl display definition files, PvWave/IDL scripts,
AR request files, ALH alarm configuration files, and the like.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS

For the purposes of work performed for the Gemini 8-m Telescopes Project the following
definitions will be used to differentiate between the two flavors of EPICS development
work:
Internals work would include any of the following:

• Channel Access - Client and Server Software, Scanners, Monitors
• Record Support, Device Support, and Device Drivers
• Host-based Development Tools (CAPFAST, EDD, etc.)
• Other OPI CA Clients
The first two items would be suitable topics for an advanced EPICS course on EPICS
System Development. The latter two items would be covered under Advanced Application Development and a case can probably be made that they constitute a category unto
themselves which should be labeled something like ‘Internals - Tools’
Applications work would then include any of:

• IOC Database
• IOC or OPI SNC programs
• Files associated with OPI Channel Access Tools
These are all topics that would be covered in an EPICS Basics, Building and Using
Applications course.

For each class of developer a specific set of skills is required. The following sections list
those that would be commonly used.

• Knowledge of VME and other I/O electronics
• EPICS Database design techniques
• SNC programming
• Use of standard EPICS OPI tools
• Basic knowledge of UNIX and VxWorks as development environments

U SER R EQUIREMENTS FOR EPICS D EVELOPERS

• Advanced C/C++ programming techniques
• UNIX internals
• VxWorks internals
• Real-time programming techniques
• Motif application development skills
• Networking skills: TCP/P and UDP/IP sockets

The experience of the High Energy Physics community is that only a core group of
Internals developers is required for maintenance and enhancement of EPICS IOC
software and of the standard development and CA client tool set. Specifically, the
IOC core software is almost exclusively in the domain of the Los Alamos AOT-8
office.
Two major flavors of development tools are in use with support coming from key
groups within Los Alamos and Argonne.
Many sites contribute custom CA client tools as this generally involves C or C++
programming under a UNIX O/S to interface to the standard CA library.
In addition, many sites create their own database record types and new device support
and driver layers.
Although there is presently a large amount of activity in the enhancement of EPICS
Internals software especially in the fields of non-IOC core software, this is an order of
magnitude less than the amount of Applications work under way at over 20 distinct
programs.

Another large group of predominately Applications developers that are starting work
are the Collaborative Access Teams (CATS) at Argonne’s Advanced Photon Source
(APS).

U SER R EQUIREMENTS FOR EPICS D EVELOPERS
The APS is a facility to produce high brilliance X-rays for a variety of experiments and
includes 36 experimental halls with 2 lines each. As of March 1994, there were 15 CATS
at the APS with most CATS responsible for a single sector (2 beamlines). Each CAT has
its own funding for designing/building/operating the physical beamline, instrumentation,
controls, and data acquisition systems.
Because the experimental areas must be coordinated with the main facility control system
and since 25% of the beamtime must be made available to independent investigators it
was strongly recommended that EPICS be used as the toolkit for all CATS development
work. Not only would this simplify the integration with the central control system but
would also provide a common environment for facility visitors.
Typically, each CAT has 1 or 2 developers, and the major focus is not on the IOC software
although some new records, like the Multichannel Analyser, have been created, but rather
on the OPI CA client applications. Heavy use is being made of both Tcl/TK and IDL to
support high-level sequencing and data reduction. This is similar to the Gemini architecture as the bulk of the control system intelligence is contained within OPI CA client tasks.
Other items of concern are:

• Different science programs in use at each CAT which have complex associated data
acquisition and reduction routines.

• The creation of large data sets.
• Simultaneous local and remote monitoring and intervention.
• Ease of use for one-time users.
• Data export to home institutions.

The Standard Instrument Controller work package is tasked with laying the Internals
ground work for all other Gemini control system work packages. In this project, the only
required IOC-based Internals work is the creation of record, device, and driver support for
three VME I/O cards. It is anticipated that all other IOC-related work packages will be
performing exclusively Applications work.
In the advent of future work packages requiring Internals work it is planned the RGO SIC
development staff will be made available. In this way the number of Internals staff is kept
at a minimum.

U SER R EQUIREMENTS FOR EPICS D EVELOPERS

5

There are several means of transmitting commands and data across the Gemini system:

A.Direct: A command source may directly specify the target subsystem. This is the most
common means of command transfer from the Observatory Control System to the subsystems.

B.Channel: Commands and data may be routed through a channel. This mechanism
requires that some (unknown to the source) target subsystem has been attached to the
channel as the target. It is possible that the channel is 'intelligent', in the sense that data
may be converted from one form to another during transmission. This might be implemented by connecting two channels with a conversion module. An example of a channel
connection might be the data stream between the A&G system and the Primary Mirror
Control System. The A&G might be transmitting Zernickes to the PMCS, which is receiving Shack-Hartmann data. The intelligent channel would be responsible for the conversion. It is possible that a channel have multiple sources, multiple targets, or both! Finally,
a channel might use a separate physical route, to prevent large data transmissions (say)
from interfering with the 'normal' command streams.

C.Broadcast: Some commands and data signals are simply broadcast across the control system. Any subsystem may examine these communications and respond or ignore as appropriate. For example, the OCS might broadcast a RunTest command, causing all
subsystems to perform self-testing. As another example, a critical system failure might
cause a ShutDown command to be broadcast.

C OMMAND S TRUCTURE

All commands contain the same general structure:

Identification:
Command_ID
Source
Target
The Command_ID is an identification that is unique to that specific instance of each
command. A portion of the ID is monotonically increasing and functions as a timestamp for journalling and tracing. This is to be implemented using a technique analogous to the CFHT odometer.
The Source and Target fields indicate the originator and the recipient for the command, as expected. The Target may be a specific recipient, a Channel, or simply a
Broadcast, but the Source is always the origination point of the command.

Instruction:
Opcode
Parameter set
The remainder of the command provides the body of the command. The Parameter
list structure is dependent on the Opcode.

This section presents the “generic” commands that all Gemini systems must respond
to. There are also “Control Commands” common to all Gemini systems to provide
specific functionality during observing. These control commands are presented in the
Gemini Software Design Description. Specific commands are presented in the Software Design Descriptions for the individual subsystems.

The following commands are “status” queries used to obtain information about the
state of the subsystem.
GetVersion The subsystem returns its version identification as a string value.
GetStatus The subsystem reports its current status as one of:

G ENERAL P URPOSE C OMMANDS

•DOWN - the subsystem is not operational
•BOOTED - the subsystem has been booted, but not yet configured
•CONFIGURING - the system is in the process of configuring (Steven).
•CONFIGURED - the subsystem is configured, but not yet initialized
•INITIALIZING - the subsystem is doing initialization actions
•RUNNING - the subsystem is running at observing level
•MAINTENANCE - the subsystem is running at maintenance level
•SIMULATION - the subsystem is running in simulation mode
•DISABLED - the subsystem is functional, but has been commanded to ignore control
commands

•SHUTDOWN - the subsystem is in the process of shutting down
•LOCKED - an interlock exists on this subsystem.
GetState The internal state of the subsystem is returned as one of:

•READY - the subsystem is fully operational, but currently idle.
•BUSY_ON command - the subsystem is working, and currently processing the indicated
command.

•NOT_READY - the subsystem is not responding to commands at this time. A GetStatus
command can be used to determine the current status.
GetID The subsystem reports its unique identification tag.
GetConfiguration Detailed configuration information is provided. This configuration
information includes details of any settings internal configurations (filters, positions, etc.)
and, if requested, the detailed results of any self-tests.

The following commands affect the behavior of a subsystem independently of the specific
task of that subsystem.
SetStatus The target subsystem is to enter the state associated with the specified status
argument. For example, SetStatus SIMULATION causes the targeted subsystem(s) to
enter simulation mode. Setting the status to SHUTDOWN disables a subsystem. Not all
status levels are reachable through SetStatus.

D ATA C OMMUNICATIONS
SetConfiguration This command directs the downloading of a configuration from
the host to the target subsystem. It is important that care be taken to avoid configuration values that would result in motion, etc. This command can operate with the GetConfiguration command given above to provide 'sequencing points' for subsystem
restarts or roll backs.
RunTest The subsystem runs a self-test and reports the result as one of:

•OK - the subsystem has detected no problems, it is running within specifications
•BAD - the subsystem has detected problems that prevent its successful operation
•WARNING - the subsystem has detected a problem that may prevent it from operating to full specification, but does not prevent it from functioning at this time
There may be an argument describing a particular self-test to run. The individual selftests are specific to the subsystem and are given in the appropriate Work Package
Description. Detailed results of self-tests are available through the GetConfiguration
command.
SetLogging Logging by the indicated subsystem is set to occur at the specified level.

Communication of information is similar across all systems in the Gemini controls
network. Instances of this communication is via routes, which may be direct channels, intelligent channels, or broadcasts. Communication via a route is typically asynchronous, with commands available to establish synchronization as needed.
OpenRoute A route of the indicated class is being established for some item. The
command includes sufficient information on the route to permit the IOC to communicate through the route. The 'route' may be a specific subsystem, channel, or broadcast.
CloseRoute A previously-opened route is being closed. Modules at either end of the
channel are notified and take appropriate action.
ResetRoute The route is to be reinitialized. Modules receiving this command are to
flush buffers associated with this route and reset operating parameters to initial conditions.
TestRoute A test message is transmitted across the route. All receivers on the route
are to respond with an identification.

IOC C OMMANDS
AwaitItem The module sending this command is blocked until information is received via
the indicated route, or a timeout occurs.
SetCallback A callback is established to process data across the indicated route.
ClearCallback A previously established callback is removed.

The following commands are common to all IOC-based subsystems. (Most control subsystems are IOC-based.) These commands are processed by the IOC subsystem.

IOC crates in the Gemini system have local databases. Under the Gemini control system,
it is expected that the majority of subsystem control is accomplished through these databases. The following commands provide access to those databases.
LocateItem If the IOC local database contains the requested item, it responds with an
identification sufficient for establishing a route to that item. The LocateItem may be
broadcast through the IOC network.
GetValue The value of the specified item is obtained.
PutValue A value is transmitted for the specified item.
StartStream A stream of data is transmitted through the indicated route. The IOC system
continues to transmit data values until a StopStream command is received.
StopStream The indicated data stream is terminated.
SetEvent An event is established as a monitor of some database entry. Appropriate
changes to that entry are to result in the indicated event being transmitted.
ClearEvent A previously set event is terminated.

Time synchronization is commonly required among control subsystems. These commands
are to permit appropriate time synchronizations. Times will be provided in IRIG-B format
as UTC.

TBD

C OMMAND I MPLEMENTATION

Some subsystems may need to obtain information from other systems within the
Gemini control system. This access is accomplished using the same communication
and database access commands as given above.

Within the OCS, all commands are represented as ASCII strings. Fields within the
command are labelled and nesting is permitted using braces ({ , }). For example, a
typical command might be:

Ident={ID=314159 Source=Operator_Console
Target=BROADCAST} Instruction=ShutDown
Details of the implementation are the province of the OCS work package developers,
who are responsible for providing procedures for constructing/deconstructing/routing
command strings. The mappings of specific IOC commands between ASCII strings
and EPICS channel access calls are determined by the individual IOC subsystem
developers. Work Package Descriptions include baseline command descriptions that
need to be implemented for that specific work package.
