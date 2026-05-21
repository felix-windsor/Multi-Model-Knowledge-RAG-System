# 1995 - gemini - 4. develop procedures and training

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 4. develop procedures and training

4. develop procedures and training

The general safety requirements are:

A.eliminate hazards through design, including material selection
B.isolate hazardous substances from people

A TTRIBUTES

C.minimize hazard to people during operation and maintenance from high voltage, electromagnetic radiation, sharp edges, hot surfaces, chemicals, etc.

D.minimize risks due to environmental conditions, such as temperature, noise, vibration,
etc.

E.minimize risks created by human error
F.use interlocks and other protective devices when hazards cannot be eliminated
G.provide distinctive markings and warnings to protect people

A Controls Test Plan is part of the Gemini Control System. This plan will address all areas
of testing from design, acceptance, commissioning through to hand-over. The objectives
and requirements of this plan are detailed below.
MIL-STD-1309C, Definitions of terms for Test, Measurement and Diagnostic Equipment,
has these definitions:
Testability: A design characteristic which allows the status of a unit to be confidently
determined in a timely fashion.
Built-in-test: An integral capability of the mission equipment which provides an onboard,
automated test capability to detect, diagnose, or isolate system failures. The fault detection
and, possibly, isolation capability is used for periodic or continuous monitoring of a system’s operational health, and for observation and, possibly, diagnosis as a prelude to maintenance action.

The major objectives are:

• test effectively with minimum effort and cost
• reduce maintenance induced problems
• reduce the cost of test equipment and programming
• reduce cost of documentation

A TTRIBUTES

• testability requirements
TABLE 1. Goals for Testability Values
Item

Organizational
% Capacity

Intermediate
% Capability

Depot
% Capability

Fault Detection (all means)

90

100

100

Fault Detection (BIT)

90

95

95

Eight or less modules

95

95

95

Three or less modules

90

90

90

One module

80

80

80

Fault Isolation

The interpretation of this table is that we should discover the failure of a subsystem
90% of the time before the failure impacts observing.

Since the Gemini software will be developed in stages over a period of years, and
since computer technology is expected to evolve rapidly over this same period, the
software is to be designed to be easily extended and upgraded with modifications to
non-changing components. The software itself, its installation process, and its documentation must be developed with this expandability in mind, using general industry
standards.

All software is to be developed using typical modularization and standardization
techniques. In particular, each module’s environment is strictly defined by its interface to other components. No module can rely upon information outside of this interface. Module selection should be done in logical fashion to minimize the size of the
interfaces between modules.
The on-line databases can be considered part of this interface, but are only accessible
through their defined interfaces.
The software must be strictly modular, i.e. the functionality of a subsystem should
correspond to that which belongs to that subsystem and only to that, so that software
for different subsystems can be installed and maintained independently of all the rest.

L IFE C YCLE A SPECTS
This is needed in particular for multi-instrument operation, for example, as instruments
share the same subsystems on the telescope.
At the same time, the possibility must exist to acquire information about other parts of the
system (for example, telescope coordinates) (as mentioned in the control flow requirements in Section 3.1.1).
It also important that there are no undesired interactions between subsystems. This may be
enforced either at the client/server interface or at the message system level.

A. Fault tolerance. The security and safety of the system should be guaranteed even in the
event of failure of any component, including the higher-level software.
B. Redundancy. Hardware redundancy is a not requirement of the Gemini systems. However, the ability to reconfigure the software if one actuator fails is desirable. Data redundancy is also a requirement, to prevent a single failure from causing the loss of collected
data. The goal is to minimize the effects of single-point errors throughout the system.

As much as possible, the system is to take advantage of parallel operation to improve efficiency. The Telescope Control System should be capable of detecting and invoking parallel operation as it is responsible for control of all of the telescope and enclosure
subsystems.

The Gemini 8m Telescopes software has to be developed according to a structured and
formally defined development model. The purpose of this is to:

• make the development process visible (for quality and maintenance reasons)
• avoid incomplete specifications
• discover errors early (via review and audit procedures)
• secure structured, maintainable software
• guarantee software quality
• improve and ease cooperation.
This has to be defined in [SMP] and [SCP] (see Applicable Documents, Section 1.3),
which will cover:

D EVELOPMENT ENVIRONMENT

• Development methods
• Formal approval, review and audit procedures
• Documentation
• Coding and debugging
• Simulation
• Component and integration-verification and testing
• Configuration and version management.

The development environment for the Gemini 8m Telescopes software consists of the
computer hardware and system software (operating system, languages and tools) chosen optimally to support the development model presented in the previous section on
life-cycle aspects.
The choice of such an environment has to be defined, together with the choice of all
the Gemini 8m Telescopes standards, but excluding the target computer hardware, in
Section 4.2.5 on page 4- 7.
The following criteria for later selection shall be kept in mind:

•Emphasis on development and productivity requirements, including cross support
tools

•Portability of software (target hardware independence)
•Hardware and vendor independence
•Use of industrial and defacto standards.

Test procedure methods have to be defined in the Software Test Plan (STP), while test
plans shall be written for all individual software packages and modules comprising
the Gemini 8m Telescopes software.
Apart from the component and integration test procedures, a formal release system
should exist at package and module level, which should be checkable on-line by the
operational procedures for consistency. Every system must thus be able to supply its
current version upon request.
The test operation level has already been discussed in Section 3.2.1 on page 3- 3.

I NSTALLATION A SPECTS
The phasing of the various parts of the project is given in the [SMP].

I NSTALLATION A SPECTS

4

This section presents the specific attributes and requirements for Gemini software.
Only the high-level requirements for Gemini software are presented here. Detailed specifications for the subsystems are found in the individual chapters of the Software Design
Description.

Regardless of application, the Gemini software exhibits numerous common attributes.
These attributes are described in this section.

The Gemini system maintenance philosophy is described in the Software Management
Plan (SMP).
Preventative maintenance is scheduled as specified in the Gemini Design Requirements
Specification.

All software is to be developed using typical modularization and standardization techniques. In particular, each module's environment is strictly defined by its interface to
other components. No module can rely upon information outside of this interface. Mod-

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS
ule selection should be done in logical fashion to minimize the size of the interfaces
between modules.
The on-line databases can be considered part of this interface, but are only accessible
Reliability and availability
A measure of fault rates should be done during commissioning to establish baseline
rates for system reliability monitoring.
There are to be recovery procedures to restart after error failure. See section
Section 3.2.5 on page 3 - 5.
During science planning, there should be validity and feasibility checks to help
ensure effective and efficient use of the telescope. Where appropriate, these checks
should also be performed during operation.
The system should be constantly monitoring active subsystems to be sure they are
operating correctly before sending commands to each subsystem. This monitoring
should continue on inactive subsystems.

All telescope and instrument parameters are kept in an on line database to permit easy
implementation of table-driven applications. The interface between software control
packages is normally done via interface calls to the on-line database.
The requirements for this database package are:

A.All telescope, instrument, and detector control information is to be available at any
operation level.

B.Access times to the database are to be in the range of 2-3 msec per access.
C.Asynchronous writes are to be supported, allowing for concurrent operation.
D.Time-access critical information is available in memory.
E.There is to be a consistent and logical (i.e. name based) access method.
F.The database must support both remote access and distributed data.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS
The internal (within the IOC) implementation of this database is to be based on EPICS.
The implementation within the host workstation is TBD.

A fundamental criteria of Gemini telescope operation is that it support a full implementation of remote operations. This includes remote observing, remote control of telescope,
enclosure, and instruments, multipoint monitoring, remote monitoring, remote access for
testing, development, diagnostics, and maintenance,
It is expected that all operational capability found in on site operations is extended to
remote operations, with some degradation in performance resulting from WAN bandwidth
considerations. This means the video data signals must be encoded digitally and transferred via the WAN to remote sites.
There must be some form of security to control access to system features, possibly
restricting some operations to specific remote sites (e.g. Hale Pohaku or Hilo in Hawaii,
Cerro Tololo in Chile, etc.)

The various types of data were presented earlier. This section examines the input, output,
and interrelationships of the various data types.

Final storage locations for the data types is presented here, along with a description of the
different databases that are available.

A.The on-line data store holds astronomical data for the current observation.
B.Astronomical data are automatically stored onto the Archive medium (external software).
C.Star catalogs are available in Astronomical object catalogs (external software).
D.Telescope and instrument parameters are distributed in databases across the IOCs for
those systems. There is also a central repository maintained by the OCS that holds these
databases for down-loading to the IOCs. (developed software)

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

E.All additional data that is not required on line (configuration information, detailed
documentation, operation logs, etc.) are stored in a relational DBMS. (supported
software).

Input data are all data that are predefined at operation start. This includes catalogs,
calibrations and flat fields available in archives, etc.
Observing commands (whether entered interactively or via the Sequencer) are input
data that provide information on the course of operation and trigger events.

Replies to commands, including status information, updates to parameters, video and
astronomical information are considered data outputs.
These data end up in the different databases.
Operational information, such as logging messages, alarms, and errors are special
forms of output data, since they are made available for later inspection and debugging.

One criteria is that sufficient information be recorded during an observation to recreate the sequence of events that occurred during the observation. This requires that
all input and output data be logged appropriately.
Given an initial set of configuration parameters, the Gemini system operates via a
sequence of commands. This operation is complemented by using previously stored
data, calibrations, and star catalogs

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

A.Automatic operation. This is the normal mode of operation. The observation is performed through a preplanned program requiring little or no interaction with the observer.

B.Interactive operation. Science planning and program changes are accomplished through
interactive operation. Is is possible to enter interactive operation from automatic operation
to handle exceptional conditions.
This is the normal mode of operation at maintenance and test levels.

C.Modes and control. Normal operation is possible at all operation levels (observing,
maintenance, and test) and applies to the following conditions (where appropriate) on any
subsystem:
