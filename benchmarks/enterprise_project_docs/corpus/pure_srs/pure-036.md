# 1995 - gemini - 2. Bypassing the hierarchy (connected between grandmother and granddaughter with no path

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 2. Bypassing the hierarchy (connected between grandmother and granddaughter with no path

2. Bypassing the hierarchy (connected between grandmother and granddaughter with no path

through the mother) should only be used for transmission of status information or bulk
data, not control flow.

It is envisaged that observing astronomers who have travelled to the Gemini 8m Telescopes site will make use of the Gemini 8m Telescopes control room facilities. This will
allow centralized support and coordination of their operations, providing both operations
support for individual instruments and supervision for all of them.
However, even at the Gemini 8m Telescopes site there will be users (e.g. software development and maintenance staff) installing or enhancing other parts of the system, possibly
working directly at the telescope.
Finally, in the case of remote operations, other users (e.g. support staff) might be on Cerro
Tololo or in Hilo.

G ENERAL C ONSTRAINTS
To allow coordination both locally at the Gemini 8m Telescopes site between the various users and with remote users, the software shall support access to the system from
any user station. It will then be an operational decision, implying privileges and priorities for the various categories of users, and definition of what a given user can
actually do.
Access from any user station will make user stations in principle identical and software configurable as the user station of this or that subsystem. This should greatly
simplify the coordination problem posed by the large number of simultaneous users
(as already described in the Capacity requirements, Section 3.2.2).

There are a number of constraints for the Gemini 8m Telescopes computer hardware.
Although some of these constraints may appear redundant the project recognizes that:

•during the next 5 to 10 years new hardware will be available with features and costs
that could benefit the project

•the hardware chosen as the standard at this point of time may be no longer available
at some point in the future

•the cost of maintaining an existing hardware standard, even if available, may
exceed the costs of adopting a new hardware standard
These constraints recognize that the majority of the expense in changing hardware
standards is the cost of the software. Particular constraints are:

A.Computers used at the Gemini 8m Telescopes site, particularly in the test phase
when they are outside the control room and near the subsystem under test, shall be
checked against altitude and humidity specifications for the Gemini 8m Telescopes
site (see also [EDS] in Section 1.3).

B.Computer hardware must be able to run the Gemini 8m Telescopes software environment (operating systems, Gemini 8m Telescopes software) and provide compatibility in data format (identical internal data representation).

C.Common development and implementation tools must be both available and supported

D.Identical network access must be supported
E.Local processing power must be such that telescope and instrument control does not
represent a significant overhead in the whole process of executing an observing program (the overhead, if any, should be limited by the time it takes for physical devices
to act)

G ENERAL C ONSTRAINTS

F.The choice of a scalable hardware architecture with computers at various performance
levels should solve the problem of adequate on-line data assessment, as the amount of this
activity is very variable and dependent upon the kind of detector and method used.

G.Due to the limited bandwidths which may be available remotely, there will be constraints
on the functionality of remote operations and access.
Depending on funding, it is probably reasonable here to make a minimum and a desirable
specification. The minimum situation could also coincide with what is needed in the test
period before coming to full remote operation.
In any case, remote operation must include remote monitoring from the Gemini 8m Telescopes base facilities, together with access tools for diagnostic and test use. It should be a
goal to support remote observing from the Gemini 8m Telescopes base facilities.

Some of the general requirements which have a direct effect on the software are here
explicitly transformed into software constraints.
These are:

A.Individual instruments must be able to run fully independently.
B.Telescope software at the two telescopes must be maintained to be identical in the upper
layers (even if hardware should differ).

C.Additions of new instruments should aim, as a goal, at introducing no modification to
already operational parts. Modifications should be confined to the operational procedures
and should not affect the bulk of the existing software.

D.Switching to different configurations must be possible at any time with appropriate procedures.

E.There must be easy procedures to reconfigure the system when subsystems are modified
or removed.

F.The number of main packages of software must be kept to a minimum to facilitate maintenance, but compatibly with the need to have the right degree of modularity.

G.Commercial and public domain packages should be used whenever possible.
H.Existing software packages should be reused wherever possible.
I.Existing software expertise should be consulted whenever possible.
J.All software which does not directly control specific hardware must be written as
machine independent, portable code. Even for microprocessor software, the software
should be hardware independent, to allow a later choice of the target microprocessors.

A TTRIBUTES

K.To allow for expansion and maintenance, Gemini 8m Telescopes standards must be
defined for the on-line software and the development environment.

L.On-line version control must be implemented. That is, the version control system
must be available to recover/restore versions at all times.

M.At boot time, the Gemini 8m Telescopes software shall check the consistency of versions of all the various software components.

N.Table-driven software should be used whenever possible, to avoid unnecessary compilations.
Whether the software is table driven, message driven, or a combination of both is a
function of the individual work packages and defined in the appropriate work package description.
Changing system constants, such as arcseconds/bit for an encoder, shall not require
recompiling but will be updated as part of system startup, and, for some constants,
will be modifiable during operation. System status parameters will be maintained to
an extent that will allow restarting the system and regaining the previous state. The
extent of duplication of the previous state will be dictated by safety and practical considerations.
Strict checking should be applied on this to preserve maintainability and reconfiguration of the system.

Regardless of application, the software and control systems produced as part of the
Gemini Project Work Packages exhibit numerous common attributes. The specific
attributes described in this document are:

• Simplicity
• Supportability
• Reliability and Availability
• Maintainability
• Human Engineering
• Security and Safety
• Environmental Compatibility
• Testability

A TTRIBUTES

• Expandability
• Modularity
• Concurrency

I think you should include Rick’s information about complexity criteria here, so show that
we are aiming to achieve as simple as system as we can which meets the requirements. —
Steven.

A supportability plan will be part of the Gemini Control System. The goals and issues to
be addressed by this plan and the elements of the plan are detailed below. The plan is
TBD.

• have supportability influence design
• translate availability and readiness requirements into supportability requirements
• identify and plan for necessary support
• provide support at minimum cost

• maintenance personnel availability and work hour constraints
• personnel skill level constraints
• operating and support cost constraints
• target failures correctable at each maintenance level
• allowable downtime at site
• turnaround time to fix and maintain system
• standardization requirements

• maintenance planning
• manpower and personnel

A TTRIBUTES

• supply support
• support equipment
• technical data
• training and training support
• computer resources support
• facilities
• packaging, handling, storage and transportation
• design interface

A reliability program is part of the Gemini Control System. The requirements for this
program and some measures of reliability are detailed below. The plan is as provided
by Glen Heriot of the Canadian Gemini Project Office.

Reliability is defined as “The duration or probability of failure-free performance
under state conditions” or “The probability that an item can perform its intended
function for a specified interval under stated conditions”. The [GSR] sets as a
requirement 2% and a goal 1% for total system (mechanical, electrical, and software)
downtime due to failures - this translates to a maximum of 15 minutes per night or 1
night per month of downtime. This in turn sets quite stringent requirements on both
MTBF and MTTR for the software and controls.
To guarantee maximum availability of the control system, retry procedures must be
embodied in the software in case of error or failure (e.g. time-out, hardware failure)
to achieve recovery on-line whenever possible.
Should recovery also fail, the error or failure has to be reported in a clear form (to
identify the cause of the problem) and the system shall put itself into a safe state,
whenever a safety aspect might be involved.
To avoid unnecessary downtime, it must be possible for the system to reconfigure
itself in order to continue observing, in a different mode if required, given the failure
of a single non-critical subsystem.

A TTRIBUTES
To increase software robustness, range checking and validity checking shall be supported
before execution of any input command. This must be possible ahead of time, preparing
observing sequences for automatic observations and simulating observations to estimate
results.
On-line pre-checking of the operational status of equipment should be done prior to sending critical or time consuming commands. It must be possible to apply continuous monitoring to all subsystems on request, both when in operation and when idle, to check their
operational status.
A measure of fault rates should be done during commissioning to establish baseline rates
for system reliability monitoring.
There are to be recovery procedures to restart after error failure.
The system should be constantly monitoring active subsystems to be sure they are operating correctly before sending command to each subsystem. This monitoring should continue on inactive subsystems.
The goal for recover and/or reconfiguration is 5 minutes from onset of the error condition
to observing again.
Specific requirements are:

A.measurable, realistic reliability needs
B.performance criteria for the system
C.definition of failure
D.conditions of use and environments
E.means of verification
F.period of time during system life

A detailed plan for maintaining and periodically upgrading the Control System over its
lifetime will be part of the Gemini Control System. The plan will consider:

A.Maintenance requirements including an estimate of required resources.
B.The method of upgrading the system to add capabilities and performance. Areas where
upgrades are anticipated should be identified with an estimate of the required effort and
resources.
These issues will be addressed in the context of the mountain environment where the system will be operating. The plan will be delivered with the control system.

A TTRIBUTES

Maintenance of commercial software (Solaris, VxWorks) used by this work package
is the responsibility of the WPR and the maintenance costs are not covered by the
work package budget.
Community software support (EPICS) is available nominally free-of-charge through
the normal release and bug-fix procedures used in the community.
All subsystem software is to include modules to aid in the maintenance and testing of
the subsystem. For example, each subsystem is to include a simulator that provides a
reference behavior for that subsystem. Simple mechanisms should exist for replacing
a subsystem with its simulation.
The following self-check levels are to be supplied with sub-system software:

A.Monitor level. Each subsystem should have a background task running whenever
that subsystem is operational, performing such tasks as checking power supply levels, temperatures, performance, correct responses to commands. The OCS is to be
notified of any detected problems.

B.Self-test level. Each subsystem should provide a module for fully exercising all subsystem components, both hardware and software. This module is executed automatically during start-up and on demand through the defined interface. Problems are to be
automatically reported to the OCS via the defined interface.

C.System level. There are also software modules for testing the subsystem as an integrated portion of the entire system. This software would be executed on demand during maintenance operation level.

The levels at which maintenance may be performed are:

These should be done in situ during an observing session.

• repair by unit replacement (for instance, an extra computer system)
• repair units by module replacement (e.g. replace a VME card in an IOC)

This could be done at an Gemini 8m Telescopes base facility during the day.

A TTRIBUTES

• repair by module replacement

This could be done at an Gemini 8m Telescopes base facility during the day.

• module repair

Done at the contractor/vendor’s site.

• repair or replace

The prime objectives are to minimize:

A.downtime due to maintenance
B.cost of maintenance
C.numbers and skill levels of personnel
D.efforts to perform maintenance
E.errors in maintaining systems
F.failures induced in maintenance

A.maintenance worker constraints
B.levels of maintenance
C.sparing plans
D.periodic testing
E.scheduled or preventative maintenance
F.planned support equipment
G.turnaround time
H.repair versus discard

A.operating hours
B.downtime or availability

A TTRIBUTES

C.attended / unattended operation
D.environment

Quantitative maintenance requirements will be allocated to the system, subsystems,
and each component. The requirements must be achievable and stated in such a way
that verification is permitted. The requirements will be expressed as:

A.Mean Time to Repair for each maintenance level
B.Maximum Time to Repair for each maintenance level
C.Preventative Maintenance hours per year

All equipment shall support a programmed adjustment and maintenance interval of
30 days or longer.

All Gemini Software must be designed with human engineering requirements under
consideration. The human engineering requirements for Gemini Software include:

A.provisions for minimizing stress effects and fatigue
B.feedback on operation on specific tasks
C.people and machine interfaces
D.procedures
E.training and experience
F.interaction with team members
G.management and organizational behavior

The Gemini Control System development effort will obey and abide by both the letter
and the spirit of all applicable engineering practices, laws, regulations, and policies.
All necessary safety approvals will be obtained before devices will be accepted. The
safety precedents and requirements are detailed below.

A TTRIBUTES

MIL-STD-822B, System Safety Program Requirements, defines safety and risk as:
Safety: Freedom from those conditions that can cause death, injury, occupational illness,
or damage to or loss of equipment or property
Risk: An expression of the possibility of a mishap in terms of hazard severity and hazard
probability
In addition the Gemini project defines a hazard as:
Hazard: Something that could cause death, injury, illness, or damage/loss.

The Gemini system must be self-monitoring to invoke safety monitoring to prevent risk to
people or damage to equipment. The software should be able to quickly bring the Gemini
system to a safe state upon notification of such danger. Subsystems must be able to detect
such danger and report it appropriately. In the event that the risk persists, subsystems must
be able to move themselves into safe states to protect people and equipment (i.e. if there is
a failure in the higher-level systems).
Safety protection must be applied whenever there is the risk that the actions of the control
software could endanger people or cause damage to any Gemini 8m Telescopes subsystem, for example, by driving beyond limits or by overexposing detectors. This protection, where implemented, must be independent of the software. In general this will require
mechanical hard stops, electrical interlocks, electrical hard limit switches, soft limit
switches, software limits, and watch dogs,.
The order in which these systems will work is as follows:
