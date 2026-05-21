# 1995 - gemini - 2. For mosaicked, large optical detectors, a full readout of the detector must be done in

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 2. For mosaicked, large optical detectors, a full readout of the detector must be done in

2. For mosaicked, large optical detectors, a full readout of the detector must be done in
about 2 or 3 minutes.

B.Concurrent data access and display. Since the Gemini system supports monitoring
of operation, there must be the capability of providing multiple, simultaneous access
to data. Data transfer between the virtual telescope system and attached workstations
therefore imposes significant transfer requirements on the LAN. The LAN must support a transfer rate of 20-40 Mbits/second.

C.Data acquisition format. Data is normally acquired as uncompressed data, but may
be compressed using a loss-less compression technique for transmission from the
Gemini system or across the system LAN. The goal of compression is to minimize
bandwidth impact on the LAN and WAN and to save space on removable media.
For data that requires preprocessing, such as infrared detector data, only the preprocessed data is stored.

D.Storage of data. Data from all instruments and detectors is stored as compressed
data, using a standard format. There is a first level of storage within IOCs, to secure
data in the event of link failures.
A second level of storage is on the Gemini system data disk(s), possibly also on
removable media. Quick-look data quality assessment is done using this level.

O PERATION P RIVILEGES , P ROTECTIONS , AND P ROCEDURES
Archiving of data is automatically done while in observing and maintenance level operation to the Gemini Archive subsystem. Shipping of data to a central archive follows later.

E.Data transmission format. Data is transmitted between Gemini and home Institutes using
a FITS format and contains all header information provided with the data.

F.System-wide data capacity. The data capacity of the system is limited by transfer methods and technology, as well as archiving capacity on site. The system data capacity is
capable of retaining 7 days of data produced by the largest instrument, the last 3 days
of which must be available interactively from hard disk or similar medium.

Video information originates from target acquisition, guiding, and site monitoring cameras. The requirements for transferring video data are:

A.The system must allow for fast transmission of rough images every 0.5 sec. This may be
assisted through the use of data-loss compression techniques (e.g. JPEG, MPEG, etc).

B.In addition, there is the need for transmission of images matching the original resolution.
This high-quality transmission must require less than 20 sec, and can only be assisted with
loss-less compression.

To preserve the integrity of the system, there must be a system of privileges established at
each operating level of the system. These privileges should be determined in a simple
manner during logging into the system.
Protection against accidental interference is to be implemented using an Access Mode
Allocation system that dynamically identifies and assigns resources as needed. Critical
resources (those that can support only a restricted number of simultaneous uses) are
assigned solely through this allocation system. The allocation system must ensure that the
system cannot remain deadlocked with respect to this resource allocation.
Finally, procedures must be implemented for convenience and system integrity, to simplify and codify common tasks. The tasks that require such procedures include:

•Telescope start-up and shutdown.
•Telescope system self-testing.
•Instrument start-up and shut-down. This is not permitted to interfere with telescope
operation.

•Instrument self-testing and self-diagnosis This is not permitted to interfere with telescope operation.

G ENERAL PERFORMANCE AND RELIABILITY REQUIREMENTS

•Configuration and reconfiguration.
•Dynamic reconfiguration of observing configuration (beam switching without
restarting instruments and telescope).

•The control software should know what subsystems are installed and their status at
all times.

The Gemini software should have no hard restrictions on the number of simultaneous
users, but should allow for policy decisions that do restrict the amount of simultaneous access.

The response time requirements vary with the function. The appropriate limits are:

A.Every command must be accepted/rejected within 2 sec and before the corresponding action occurs. (This is different than the ACK/NAK response of the communications protocol - here, the target system must have examined the command and
verified its validity.

B.Status display update must be within 4 sec at the local stations (certain functions,
such as telescope position, may have tighter constraints). Remote station update
response is given in the Requirements for Remote Operations section.

C.Requests of subsystems for status information must be answered within 5 sec and be
possible in maintenance level operation.

D.Requirements for response times within the user interfaces are given in the User
Interface requirements section.

All software bugs should be logged and then fixed as soon as possible after detection.
The goal is to have restart conditions occur only on hardware failure.
Fault recovery, exception handling, fail-safe checks, etc. should be used to improve
reliability.

T EST AND CHECKOUT REQUIREMENTS

The telescope and instrument software shall contain built-in test (BIT) facilities to verify
Gemini 8m Telescopes system and Gemini 8m Telescopes software performances.
Every Gemini 8m Telescopes software module shall have corresponding test specifications to check normal operation of releases, to be used both for acceptance tests and as an
on-line test procedure.
The Gemini 8m Telescopes control software shall also provide for execution of self-test
sequences of the Gemini 8m Telescopes system and subsystems. These shall automatically exercise all subsystems present in a given operational configuration.
Regression tests should be a part of every Gemini 8m Telescopes software package.

Subsystems must notify the user when faults occur. This notification must be specific as to
origin and problem. The notification must also be capable of being electronically logged.
It may also prove useful to have multiple levels of fault notification such as detailed, verbose, short, etc. to aid in tracking down problems.

Should a subsystem fail (e.g. one detector, one instrument) predefined procedures must
exist to redefine the environment in such a way that operation can restart with the remaining equipment.
In case of computer hardware failure concerning the user station equipment, it shall be
possible to transfer control from one user station to another via a simple software reconfiguration procedure.
In the case of IOC failure, no transfer of control to another IOC will be possible, due to the
local connections and interfaces to the control electronics. In this case there shall be a procedure to replace faulty cards and/or assemblies. If it is possible to observe with that particular IOC in a failed state (in general, this is limited to IOCs that are associated with
individual scientific instruments) then it must be possible to reconfigure the system to do
so.

C ONSTRAINTS

Full redundancy is not a requirement of the Gemini 8m Telescopes and it will be
acceptable to have to replace units in case of failure.
There are subsystems which are relatively inexpensive to support as redundant systems, such as telescope control computers. For each area where redundancy is
decided to be cost effective, procedures for switching to the backup system will be
established. There is no requirement for automatic switching to the backup system.
All communication shall be based on the use of standard communication protocols,
where retry procedures are applied (a form of software redundancy) as part of the
protocol.
Certain network concepts may be preferable as they offer intrinsic redundancy (e.g.
double loops) and re-routing possibilities in case of node failures (single point failure
protection).

The Gemini system software is designed under the following constraints.

A.There should be no restrictions imposed by the software on users. Only policy decisions (permissions, access privileges, etc.) should prevent any user from accessing
any part of the Gemini system from any local or remote station.

B.Similar functionality should be presented to the users using similar user interfaces.
However, user interfaces should clearly reflect access modes and operating levels.

Hardware constraints are covered in the individual chapters the Software Design
Description.

There are a number of general constraints placed on the Gemini Software. These are:

A.Commercial packages, off-the-shelf public domain software, and standards are to be
used whenever feasible.

C ONSTRAINTS

B..Existing external software will be integrated with the Gemini software. The interfaces
involved in this integration are considered part of the Gemini software system.

C.All Gemini software is to be developed using standard methodologies and development
environments. One of the goals of Gemini software is that all components be easily (preferably automatically) combined into an integrated system.

D.Gemini software developers should maintain accurate change logs showing software
modifications as they are applied to the system software.

E.Gemini software developers should adhere to a standard method for the reporting and
recording of errors from both internal and external sources.

F.Gemini software should be developed in evolutionary fashion, using the CVS version
control system.

G.All Gemini subsystem packages should include as part of the software both a simulator
module for inclusion in the virtual telescope (see Design constraints, below), and user
interface modules for the user interface environments that the subsystem will be operating
in. The interfaces required of these user interface modules are described in Section 3.3 on
page 3-6.

H.All Gemini software is to be fully documented, internally with appropriate comments,
and external documentation. External documentation must include Unix-style man pages.

I.All Gemini subsystem packages must provide modules for the testing and diagnosis of
the subsystem.

J.All instrumentation control software must provide full access to all instrument functionality. It is likely that different user interface modules (see above) would present different
portions of this functionality to the user. The information required of each interface module is found in the Functional Requirements specifications for each instrument.

K.All Gemini software must be version labeled, both in source and binary form. The version information is to be retrievable from executing software via control commands.

A.There are different requirements for software running on different layers. For example,
strict real-time control is restricted to the IOC layer.

B.Also, the use of a virtual-telescope model in the Gemini system means that the integrated
system can be tested and developed independently of the target hardware. This is useful
not only in the use of the telescope simulator during science planning, but in maintenance
and testing as well. Therefore all hardware subsystems must provide a software simulation
module (as stated earlier) that responds in reasonable fashion to commands directed at that
hardware. This simulation may require a standard environment, such as VxWorks, EPICS,
and VME crate/cpu, but it cannot require any hardware specific to the application.

C ONSTRAINTS

C.Gemini subsystem should be as self-contained and autonomous as possible, thereby
decreasing the functional width of the interface to the rest of the Gemini system.

D.No subsystem package should make any assumptions about the surrounding environment beyond that provided in the interface specifications.

3

The final purpose of the Gemini 8m Telescopes software is the acquisition of astronomical
data in digital form in the most efficient way.
To achieve this, many other data concerning the telescope and instruments (parameters)
and control commands will have to be exchanged between different processing units in
order to setup and control telescope and instruments. Additionally, video and voice data
are also necessary (for example, field monitors).

Control information must be transferred, typically in the form of commands and replies
from users, to telescope and instruments. Replies might contain status information and, in
general, data concerning instruments and telescopes, to be stored together with the astronomical data.
Control information on all controlled variables must be provided by all subsystems on
request. No request for information shall produce a delay of control activities or locking,
even if the corresponding equipment is not available or faulty.
Delay times for the exchange of control information must stay within precise time limits
to be defined in “General Description” in Chapter 2. One can afford to retransmit commands in case of transmission error or collision, but the protocol has to be predictable in
that commands cannot get lost and replies have to come back reliably.

D ATA S PECIFICATIONS
In a number of cases, synchronization with the Time Reference System at the Gemini
8m Telescopes site is also necessary.
Access to control parameters, telescope and instrument information for monitoring or
other use makes a significant contribution to the control flow, and may be logged at
quite high rates for short periods (i.e. up to 200 Hz for some information).
It is explicitly required that all such information is available to the Gemini 8m Telescopes software and is capable of being available to all users of the Gemini 8m Telescopes, subject only to restrictions with respect to updating. It must also be possible
to restrict user access to such information.
In particular also, the meteorological information coming from a weather station
should be available centrally.

Detector data must be acquired and stored in the most effective way technology will
allow; effectiveness should be evaluated in terms of cost, space requirements, longevity, and speed. This shall lead to the definition of a Gemini 8m Telescopes standard, used on all instruments. In general, operational overheads must be kept as low
as possible, to maximize actual observing times.
Intermediate storage of raw data in memory on different nodes and in different formats should be kept to a minimum. However, there must be at least two copies - one
to secure data as acquired and one to do assessment of data quality on-line (this last
copy preferably on removable media).
The link chosen to transfer data should represent as small a bottleneck as possible for
data acquisition.

Normally, raw data will be acquired and stored as such for quick look evaluations.
There might, however, be cases (for example, infrared detectors) where fast preprocessing is needed and where, therefore, raw data will not be stored as such, but in a
preprocessed format.

O PERATION

Astronomical data will have to be transported between GEMINI and the home institutes of
visiting astronomers in FITS format (as defined by NOST 100-1.0, “Definition of the Flexible Image Transport System (FITS)”, NASA Science Office of Standards and Technology).

TV data concerning site monitoring and voice need to be capable of being available at all
operations facilities. It will be a question of interfacing and bandwidth costs whether such
information is actually available at a specific location. It is not a requirement that point to
point video be available between Gemini 8m Telescopes operations facilities. It is a
requirement that voice connectivity, perhaps point to point, be available on a permanent
connection.
Other astronomical information such as that coming from sky field monitors, autoguider
cameras and sky monitoring devices such as cloud and seeing monitors shall also be capable of being available.

Operation of telescope, instruments and subsystems can be carried out at three different
levels. There will be parameters associated with each level of operation which define the
status of the system and / or control the system. The specific access by different types of
users to particular parameters of the different levels are given in Section 2.5.8 on page 25.

This is the normal operational mode. It allows a certain number of embedded tests, normally at a fairly high level. Monitoring is also done at this level.
It is anticipated that all user categories have access to this level.

This allows maintenance tables (for example, with instrument parameters) to be updated.

O PERATION
It is anticipated that the majority of parameters at this level will be accessed by operations and development staff.

This allows the installation and testing of new packages or new releases. Any low
level test can be performed in this mode.
It shall be possible to update all non-protected parameter values, i.e. those not used
by operations at observing level.
Access to this level will be extremely limited.

Privileges and protections are also important parameters to define user operations.

A further subdivision within the levels can be achieved by implementing privileges
associated with categories of users or with the location of the user station (local or
remote). For example some users might only be allowed monitoring, as a subsystem
is in use by someone else.

Protections must also be enforced (see also Security in Section 3.5.6 on page 3- 20)
among users and the operational software should indicate clearly to users the current
operation level and check the compatibility between subsystems in different modes.

The capacity of the system can be expressed in terms of nodes, which is defined as
the number of workstations, or in terms of users, which is defined as the sum total of
users at all the nodes. The capacity requirements will be expressed in terms of nodes.
Each node will have the capability to run at all operation levels.
When the Gemini 8m Telescopes telescope is used in its normal observing mode,
there will be a single operator node for the telescope and two data acquisition and
instrument control nodes.

O PERATION
Some tests might be run in parallel on instruments that do not have the light beam at that
moment, so in principle additional nodes might be working at the same time. The system
will provide for one auxiliary data acquisition and instrument control nodes.
In addition, the system must support off-site observing modes. The system will provide
for a single off-site data acquisition and instrument control node - to be located at either
the Gemini 8m Telescopes Site Support or Base Facility.
One supervisor will monitor the system, and other users might need to monitor the running of observing programs, locally or remotely. The system will provide for a single local
monitoring node and a single remote monitoring node.
As a conclusion, the Gemini 8m Telescopes control software shall allow simultaneous
operation of up to six active control nodes and up to two more monitoring nodes (one
local and one remote) without appreciable degradation of performance.
In practice the operation and facilities foreseen so far for the Gemini 8m Telescopes will
limit this number to a maximum in the order of three active nodes, but the Gemini 8m
Telescopes computers and software shall be capable of coping with the load of 10 active
nodes, should the case arise.

This section is intentionally kept at the level of performance criteria rather than response
times (found in Section 2.11.2 on page 2- 22). Every command must be acknowledged in
a positive or negative way before the occurrence of the corresponding action within given
response times.

There must be automatic procedures to implement startup and shutdown of the telescope
and instruments. These must allow startup and shutdown of instruments independently of
the telescope and without affecting the telescope operation.
Reconfiguration procedures must exist, to change the observing environment.
The definition of the observing environments must be dynamic, i.e. feasible during operations without the need to restart everything. The same applies to the related light path.
Operations staff have privileges to change the environment, meaning selecting a suitable
combination of instruments.

E XTERNAL I NTERFACE R EQUIREMENTS
The operational software should know which subsystems are installed and operational at any given time.

The user interface defines the way users see the Gemini 8m Telescopes system. Given
the large number of instruments, there can be many different stations which are active
at the same time. It is essential for operational and maintenance reasons that, in spite
of the obvious differences of the setups and commands available, the same philosophy is applied throughout. This calls for a homogeneous user interface, which can be
achieved only by applying the same user interface tools to the whole project, providing the Gemini 8m Telescopes user interface's ‘look and feel’.
The user interface should not be seen as a package linked to a specific computer.
Given the requirement to be able to access the Gemini 8m Telescopes from several
points, the user interface should rather be seen as a package to be callable from a
large number of stations, depending on where a user is. It should also be network
transparent so that it does not matter where it is being run.
The user interface tools shall be based on standards, defined in Section 4.2.5 on page
4- 7, which will be portable across different computer hardware platforms (Portable
User Interface Toolkit). The intent of a portability requirement is to facilitate migrating existing and future Gemini systems to different hardware as the need arises. It is
the current intent to limit the selection of computer hardware platforms to as few as is
practical.

Main processor computer hardware requirements will be defined in the Hardware
constraints (see Section 3.4.2 on page 3- 12).
This section deals instead with external hardware interfaces, namely the ones from
the microprocessors to the control electronics. The definition of these terms is as follows:

•main processors - these are the computers with which the user interacts
•control electronics - these are the computers controlling the instruments

E XTERNAL I NTERFACE R EQUIREMENTS

•microprocessors - these are computers embedded in the instrument (for instance a DSP
or transputer required for array control functions, or special purpose controllers for
the primary mirror support actuators).
Standard interfaces to the control electronics shall be available, in the form of:

•standard bus systems
•a standard set of interface cards to be used on all the subsystems and instruments
•a standard software skeleton running on the control electronics
The existence of hardware standards is clearly essential for maintenance and repairs. It is
also essential to avoid software duplication, and to simplify the Gemini 8m Telescopes
software. Microprocessor software in particular tends to contain hardware specific software, though one should try to keep it as hardware independent as possible, isolating different software layers.
The standard software must be adequate for the real-time requirements and must offer
drivers to the standard electronics to be used on all the Gemini 8m Telescopes software
subsystems and instruments.
Links between electronics interfaces and main processors must meet the requirements
imposed by the data specifications (see Section 3.1 on page 3- 1).

The Gemini 8m Telescopes software covers all aspects of control and data acquisition
related to the telescope, instruments, and auxiliary instrumentation.
It also covers all the operational aspects of the Gemini 8m Telescopes, including on-line
scheduling and rescheduling.
There is also software which, although it will be interfaced to the Gemini 8m Telescopes,
is referred to as external. The external software consists of:

•commercial software integrated into the Gemini 8m Telescopes software (e.g. DBMS)
•preexisting software used in the Gemini 8m Telescopes (e.g. image processing systems,
star catalogues)

•software associated with visitor instrumentation
•embedded software dedicated to hardware control, but not communicating on-line with
the other Gemini 8m Telescopes software (in general this would be microprocessor
code)

E XTERNAL I NTERFACE R EQUIREMENTS
The Gemini 8m Telescopes software must interface to the external software and
clearly the interfaces are fully part of the Gemini 8m Telescopes software.

In order to make efficient use of the telescope, to support different observing modes,
and to support the versatility requirements, some form of on-line image (or pixel)
quick-look analysis is required. The following statements are proposed:
“It shall be possible to monitor the quality (image quality, spectral resolution, signal
to noise, etc.) of the astronomical data as it comes in.
Standard reduction procedures should be available for basic on-line calibrations of
the observed data. Ultimately, one would like to have fully reduced and calibrated
data at the end of the observations. Advanced pipeline procedures might make this
feasible, at least for observations of a standard nature.”
The above statements define the goal of quick-look analysis for the Gemini 8m Telescopes.
Quick-look data processing should be provided on the Gemini 8m Telescopes, with
procedures suitable for fast on-line data preprocessing. A prerequisite for this is that
acquired data are made available as directly as possible in a common format, and that
all additional data related to an exposure and logging information are made available
on-line at the same time.
Quick-look should be usable within exposure sequences to provide results and feedback parameters to the control software in a programmed way, without the need for
manual intervention. This document does not try to be specific about the requirements for Quick-look other than that it should be synchronous.
Near-line processing should be available for simple data reductions required for data
integrity validation (i.e. remove instrument and observatory effects so the observer
can make decisions about further observing actions). This data reduction proceeds
sequentially through requests, but asynchronously from data acquistion. In particular,
data acquisition takes precedence over near-line data reduction.
Off-line pixel processing for full data reduction should also exist at the Gemini 8m
Telescopes site, but does not have any interface to the Gemini 8m Telescopes software. The Astronomical communities have made considerable investments in image
processing software, and therefore, compatibility with and adaptations to these packages must be sought.

E XTERNAL I NTERFACE R EQUIREMENTS
It should also be noted that some Gemini 8m Telescopes subsystems, such as adaptive
optics, may require their own special on-line pixel processing software, which is better
defined in the requirements for those subsystems. This is largely due to the difficulty of
applying on-line the same algorithms used for full off-line reductions — in general due to
the time critical nature of the image processing needs.
The same situation might also occur with other instruments, where specific observer support software has to be foreseen for on-line use.
In all these cases the specific on-line (quick-look) software development shall be seen as a
subset of the development for the off-line data reduction system, to avoid as far as possible duplication of development effort.

The output format of the Gemini 8m Telescopes data must be compatible with the GEMINI archive requirements.
As comparisons with previous data might be of great value and affect the actual observing
program, on-line interactive access to the data archiving system should exist, so that
access to this database is possible for Gemini 8m Telescopes users.
The specific types of data available; flat fields, calibrations, science exposures, etc.; the
amount of a specific exposure available; header only, averaged exposure, complete raw
data set; and the time frame within which such data will be made available; same night,
weekly, after proprietary period; will be established by the Gemini Archiving Requirements.
Computer access to star catalogues is also required, so that an automatic selection of candidate guide and standard stars can be made.

The Gemini 8m Telescopes software must be able to interface with all commercial software packages available on the Gemini 8m Telescopes and integrated into the Gemini 8m
Telescopes operation.
A relevant example of such a package is a general database management system (DBMS),
where operational information such as schedules, logs, problem reports and maintenance
information related to various pieces of equipment should be kept.

E XTERNAL I NTERFACE R EQUIREMENTS

Being in itself a distributed telescope system and having a large number of instruments, the Gemini 8m Telescopes system has internal communication needs.

The LAN shall support the majority of the Gemini 8m Telescopes system internal
communication needs. This LAN must be capable of dealing both with the data bandwidths required (at peak and on average) and with the required response times and
synchronization needs. This LAN shall be supplemented with a Local Time Bus, for
distribution of absolute and relative time signals, and both a digital reflective memory
bus and an analog event-based bus, for distribution of signals with requirements not
satisfied by a LAN.
Independently of the physical layout of such a network, its functional requirements
can be split into several categories:

•Local coordination and synchronization needs within a subsystem (for example,
coordination of active support system for primary mirror, bi-directional traffic of
commands/replies). This layer could be considered as internal to a given subsystem or instrument, but as more than one subsystem might need it, one should
aim for a unique solution at the hardware and software level.

•Global synchronization needs, such as the universal time synchronization requirement. The required accuracy will be defined in Section 2.9 on page 2- 19.

•Exchange of control information, in the form of commands and status information.
(Bi-directional traffic) (see also Section 3.1.1 on page 3- 1).

•Collection and transfer (for archiving or remote access) of raw astronomical data.
The capacity will be defined in Section 2.9 on page 2- 19(see also Section 3.1.2
on page 3- 2).

•Access from Wide Area Network (WAN) for remote diagnostics and monitoring
from operations facilities (Bi-directional traffic).
No distinction is made here between WAN and point to point links as there shall be
no difference in the software between the two cases. However the system architecture
will be designed so as to minimize the communication load placed on peer and higher
level networks.
Control data and astronomical data have already been defined in the Data specifications (see Section 3.1 on page 3- 1). The reason for repeating them here is to have a
complete view of the required network functionality.

G ENERAL C ONSTRAINTS
To eliminate conceptual access problems, while coping with different bandwidths, LAN
and WAN interfaces shall be homogeneous and shall be based on standards which allow
migration on different media, should they become required during the Gemini 8m Telescopes project life.
For maintenance reasons and hardware independence, a clear hierarchical model must be
implemented, supporting separation of logical and physical layers, e.g. ISO/OSI model. It
is recognized that this hierarchy may need to be violated for (in general) performance reasons. This results in point-to-point connections between peer systems or direct connections bypassing the hierarchy.
Network redundancy should also be considered in the design phase as a way to increase
reliability and security, in particular for control information.
Due to the uncertain future of the Internet, only non-essential tasks may employ it. All
essential tasks, not including remote observing, must take place on resources controlled by
the project (such as leased lines).
Violation of the hierarchical nature of the system can lead to testing and maintenance
problems. The use of these features must be limited and constrained by the following
guidelines:
