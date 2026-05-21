# 1999 - tcs - Chapter 3 Engineering Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: Chapter 3 Engineering Requirements

Chapter 3 Engineering Requirements
The TCS system will be capable of controlling the Predator and Outrider AVs with a single control system,
using existing military services standard hardware and software, and supporting interfaces with various
C4I systems.
The TCS shall consist of the TCS workstation Hardware Configuration Items (HWCIs), TCS Computer
Software Configuration Items (CSCIs), and additional TCS Support HWCIs and CSCIs. [SSS004]
All TCS HWCI’s and CSCI’s shall be Year 2000 compliant. [SSS567].
The primary function of the TCS is to provide command and control of the payload, Air Vehicle (AV), data
link, and other necessary support equipment in order to employ tactical UAVs to conduct reconnaissance,
surveillance, target acquisition, and target identification missions. The TCS will interface with and export
and disseminate payload data to military supported units via external (not part of TCS) tactical
communications systems, and C4I systems. Communications procedures, formats, and interfaces will be
interoperable with selected standard DoD C4I systems, architectures, and protocols.
The operational capabilities to be performed by the system will be determined by task analysis in
accordance with MIL STD 1388 Task 401 as a guide based on a thorough understanding of Outrider and
Predator mission requirements. Tasks will be evaluated and allocated based on operator skills and
proficiencies. The initial TCS task analysis will produce a system baseline which will be optimized by
engineering analysis and operator evaluations.
The TCS shall meet the applicable capability and characteristic criteria established by the Operational
Requirements Document (ORD) CAF 003-90-I-A for the RQ-1A Predator Medium Altitude Endurance
Unmanned Aerial Vehicle/System (MAE UAV) and the Close Range – Tactical Unmanned Aerial Vehicle
(CR-TUAV). [SSS008] Appendix B and C identify applicable capability and characteristic criteria to
TCS.
The TCS shall support 5 levels of UAV interaction: [SSS010]
Level 1: receipt and transmission of secondary imagery and/or [as well as] data
Level 2: direct receipt of imagery and/or [as well as] data
Level 3: control of the UAV payload in addition to direct receipt of imagery/data
Level 4: control of the UAV, less launch and recovery, plus all the functions of level three
Level 5: capability to have full function and control of the UAV from takeoff to landing
The TCS system shall provide software capabilities and hardware configurations necessary to fulfill the
operational tasking requirements across the 5 levels of interaction. [SSS009]
Table 3-2 identifies the payloads with which the TCS shall be interoperable. [SSS013]
Table 3-2 Interoperable TCS Payloads

7

PAYLOAD TYPE

UAV

EO/IR

Predator

SAR

Predator

EO/IR

Outrider
Future

3.1 Required States And Modes
The states of operation of the TCS shall include Startup, Operation, and Shutdown. [SSS014]
The TCS states shall not exist concurrently. [SSS015] Figure 3.1-1 shows the existing states of the TCS.

STARTUP
OPERATIONS

SHUTDOWN
Figure 3.1-1 TCS State Diagram

3.1.1 Startup State
Upon application of power the TCS shall enter the Startup State. [SSS016]
The Startup State shall be comprised of the following modes: Normal Startup Mode and Recovery Startup
Mode. [SSS017]
Figure 3.1.1-1 shows the modes that exist in the Startup State.

8

STARTUP

RECOVERY
STARTUP

NORMAL
STARTUP

Figure 3.1.1-1 TCS Startup State and Associated Modes Diagram

The TCS will execute the particular startup mode which corresponds with the manner in which the TCS
Software was halted.
When the TCS Software is terminated normally the TCS shall enter the Normal Startup Mode of operation
upon application of power. [SSS019]
When the TCS software is halted due to an unplanned power interruption as well as abnormal program
termination, then the TCS shall enter the Recovery Startup Mode upon application of power. [SSS020]
During startup, the TCS shall determine which of the 5 levels of interaction are achievable by the TCS
configuration. [SSS021]
Levels of interaction higher than those achievable by a particular TCS configuration shall be prohibited.
[SSS022]
The TCS shall inform the operator if the operator attempts to execute a function prohibited as a result of
the determined level of interaction. [SSS023]
3.1.1.1 Normal Startup Mode
When executing in the Normal Startup Mode, the TCS shall provide the system functionality necessary to
initialize the system to place it in the Operations State within 60 seconds from the time power is supplied
and the TCS application is launched. [SSS024]
Initialization of the TCS HWCIs shall include startup of HWCIs [SSS542], download of software
[SSS026], startup of CSCIs [SSS027], execution of Startup FD/L [SSS025], and establishment of the
state of readiness of all interfaces. [SSS028]
3.1.1.2 Recovery Startup Mode
The TCS in the Recovery Startup Mode shall provide the system functionality to resume the Operations
State within 45 seconds. [SSS029]

9

Recovery of the TCS HWCIs shall include startup of HWCIs [SSS543], download of software [SSS544],
startup of CSCIs [SSS545], and establishment of the state of readiness of all interfaces. [SSS546]
The TCS shall be capable of automatically recording system state data, interface communications and other
information necessary to support event reconstruction. [SSS528]
**DELETED**. [SSS030]
For recovery from abnormal termination, TCS shall prompt the operator to select the type of recovery to be
executed: (1)Resume in the Same Modes And Data; (2)Resume in the Same Modes but Review and Modify
the Command Data as Necessary; or, (3) Perform a Command Shutdown and Startup Via the Normal
Startup Mode. [SSS031]

3.1.2 Operations State
When in the Operations State the TCS shall be capable of operating in three modes: normal operations
mode, training operations mode, and maintenance operations mode. [SSS032]
Figure 3.1.2-1 shows the Mode Diagram for the Operations State of TCS.

OPERATIONS

NORMAL
OPERATIONS

TRAINING
MAINTENANCE
OPERATIONS OPERATIONS

Figure 3. 1.2-1 TCS Operations State and Associated Modes Diagram
The Operations State modes shall not exist concurrently. [SSS033]
The operator shall have the capability to command the system to the Shutdown State from all modes under
the Operations State. [SSS035]
The TCS hardware and software shall execute periodic Fault Detection/Location (FD/L) while in the
Normal Operations Mode and Training Mode, to include a periodic determination of level of interaction.
[SSS036]
3.1.2.1 Normal Operations Mode
In the Normal Operations Mode the TCS shall support the following functions: [SSS037]

10
