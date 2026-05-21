# 2000 - nasa x38 - 13 April 2001

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2000 - nasa x38.doc

Section: 13 April 2001

13 April 2001
X-38 Fault Tolerant Parallel Processor Requirements, Rev 6.2,
National Aeronautics and Space Administration
Lyndon B. Johnson Space Center
2101 NASA Road 1
Houston, Texas 77058-3696

Non-Government Documents
Document No.
Date
Title
297752

Application Programming Interface,
The Charles Stark Draper Laboratory,
Cambridge, Massachusetts
297746

Certification Test Procedure for the Network Element for the NASA X-38 Flight Critical Computer, The Charles Stark Draper Laboratory, Cambridge, Massachusetts
Publication No. YD681MPCC1
October 1998
MPCC01 Firmware Manual Rev A
Radstone Technology PLC
Publication No. HH681MPCC1
October 1998
MPCC01 Hardware Manual Rev B
Radstone Technology PLC
DOC-12068-ZD-00
4 Apr. 1999
VxWorks Reference Manual, 5.4 Edition 1
Wind River Systems, Inc.

All references to API in this document refer to Draper document number 297752, Application Programming Interface for the X-38 Fault Tolerant System Services.

REQUIREMENTS
Required States and Modes
Fault Tolerant System Services CSCI states are shown in REF _Ref427650859 \* MERGEFORMAT Figure 3-1.

Figure STYLEREF 1 \s 3‑ SEQ Figure \* ARABIC \s 1 1. Fault Tolerant System Services States.
System Initialization is entered when the system is powered up for the first time, or when a power-on reset exception is received by the software. Section REF _Ref469106404 \r \h 3.2.1 gives the requirements for this state. The system transfers to the Normal Operation state after the FCP has been configured into a fault-tolerant computer and enables the timer interrupt.
In the Normal Operation state the software meets the performance and functional requirements (other than those listed as System Initialization requirements) in the no-fault case. The system will transfer to the System Initialization state if a reset exception is received. The system will transfer to the Fault Recovery state if a fault is detected.
In the Fault Recovery state the system is reconfigured. If a single permanent fault has occurred, for example, the system will, when the transfer is made back to Normal Operation state, be capable of handling another fault. The requirements for this state are found in Section REF _Ref469107423 \r \h 3.2.6.2 and its subsections.
CSCI Capability Requirements
System Initialization
System Initialization performs those functions necessary to transform the hardware consisting of the FCP processors, network elements, and on-board I/O devices into a real time system executing tasks with fault tolerant message exchanges.
Whenever a power-on reset occurs, System Initialization shall [SRS194] perform the following functions.
As part of System Initialization , the Boot ROM shall [SRS234] be configured to, after completing IBIT, call the manufacturer-supplied VxWorks Board Support Package (BSP) initialization software followed by a call to the FTSS System Initialization software.
System Initialization shall [SRS014] initiate the watchdog timer.
System Initialization shall [SRS292] enable and reset the processor’s watchdog timer such that, in the absence of a fault, the watchdog timer does not expire and reset the processor..
System Initialization shall [SRS008] synchronize the FCP virtual group in the presence of a power on skew of 2.5 seconds.
System Initialization shall [SRS010] configure the FCP virtual group to use all available synchronized processors, if at least 3 of the 5 FCRs are active.
If any of the FCP processors are not synchronized, System Initialization in the surviving triplex shall [SRS177] attempt to sync with the failed FCP.
If the failed FCP processor has not synced in 2.5 seconds after the surviving triplex has detected the loss of the FCP, then the surviving triplex shall [SRS178], within 1 second, send a single voted VMEbus reset through the NE to the failed FCP.
System Initialization shall [SRS011] align processor state and congruent aligned memory locations. Processor state includes all registers. It also includes those timers used by FTSS.
The FCP shall [SRS296] configure ICP simplex virtual groups for each channel in the FCP virtual group.
The FCP shall [SRS297] wait up to 15 seconds, after configuring the ICP virtual groups, for communication to start from the ICP. The application can use this time on the ICP to initialize I/O boards.
System Initialization shall [SRS215] call an application initialization function to allow the application to (at least) create tasks, create communication sockets, initialize the vehicle mode, and initialize memory alignment allowance.
The FCP shall [SRS221], after application initialization is complete, send an FCP Ready Sync message to the ICP
The FCP shall [SRS189] wait up to 2.5 seconds (from the sending of the FCP Ready Sync) for the ICP Ready signal. Note that FTSS will not fail the FCR if this signal is not received within this time. FTSS will wait until the normal ICP presence test fails.
The FCP shall [SRS243], if the NEFU ICP fails to send its ICP Ready signal, mask out that ICP, but continue to use the NE.
System Initialization shall [SRS199], when all other activities are completed, start the 50 Hz timer and enable the timer interrupt. This will allow the interrupt handler to initiate normal activities.
System Initialization, from hardware reset to starting of the 50 Hz timer, shall [SRS015] take no longer than 1.5 minutes.
Scheduling Services
Scheduling Execution
Whenever the 50 Hz timer interrupt occurs, the interrupt handler invokes the scheduler (there are various ways to implement this invocation, such as using a procedure call or by setting an event; no specific implementation is to be inferred). The scheduler allows the application to create lists of tasks that run during a given segment of time, at various rates. The application can create "vehicle modes" to designate a unique segment. The application can also set up "rate groups". Each rate group has some number of tasks associated with it, and it also has a rate for those tasks. Note that there may be some number of rate groups that have the same rate. These contain the tasks that will run at that rate in different vehicle modes. Some number of rate groups can be associated with a given vehicle mode. When an API call is made to change the vehicle mode, the scheduler will disable the tasks associated with all the rate groups in the old vehicle mode, and enable the tasks associated with all the rate groups in the new vehicle mode. The enabled tasks are then unblocked at the rate given in its associated rate group. An API call is available for the task to call to block itself when it is finished with its cyclic processing.
The scheduler shall [SRS017] provide an API call to install a task into a rate group. The API call is invoked during system initialization.
The scheduler shall [SRS196] support up to 20 tasks per rate group.
The scheduler shall [SRS018] provide an API call to install a rate group into a vehicle mode at system initialization.
The scheduler shall [SRS197] support up to 3 rate groups per vehicle mode.
The scheduler shall [SRS195] support up to 5 vehicle modes.
The FTSS software shall [SRS002] provide the identical services in all vehicle modes.
The scheduler shall [SRS019] provide an API call for an FCP application task to alert the scheduler of a vehicle mode change.
The scheduler shall [SRS020] complete the change from one vehicle mode to the next within 1.02 seconds. There is up to a full major frame from notification of an impending mode change to acting on it in minor frame 0 of the next major frame plus the time it takes during the next minor frame 0 to switch tasking.
The scheduler shall [SRS021] process vehicle mode changes during minor frame 49.
The scheduler shall [SRS022] execute cyclic tasks, providing an API call to allow the application to block until its next iteration.
The scheduler shall [SRS024] execute as the highest priority FTSS or application task in the system.
The scheduler shall [SRS025] keep a minor frame count from 0 to 49.
The scheduler shall [SRS027] give tasks priority values according to their rate - the higher the rate, the higher the priority.
The scheduler shall [SRS028] detect 50 Hz, 10 Hz and 1 Hz rate group over-runs.
The scheduler shall [SRS029] report rate group over-runs to the application via an API service for incorporation in the telemetry data stream.
The scheduler shall [SRS216] provide an API call to specify which task was running within the rate group which over-ran.
The scheduler shall [SRS030] provide a mechanism to inform a task when it did not complete during the previous frame and restart it at the beginning of the task.
The scheduler shall [SRS181] set the 50 Hz interval timer to a count down value so as to cause the next minor frame interrupt at 20 msec from the previous interrupt congruently in all operational FCPs.
The scheduler shall [SRS032] issue a 50 Hz interrupt to the ICPs by means of a VMEbus IRQ5 interrupt.
The scheduler shall [SRS191] issue the 50 Hz interrupt to all the ICPs with a skew no greater than 330 microseconds.
The scheduler shall [SRS033] send the minor frame number, vehicle mode, mission elapsed time (MET), and separation elapsed time (SEP) to the ICP prior to the 50 Hz interrupt. Note: The NE unique identifier (NE ID) is available to the ICPs via the ftss_my_icp() API call.
The scheduler shall [SRS034] take no longer than 1 millisecond to execute scheduler and Time Services FTSS overhead tasks in each rate group. This means that the time from the 50 Hz timer interrupt to the start of the first task in the 50 Hz rate group will be less than or equal to 1 millisecond, assuming 27 packets of data need to be delivered.
The FTSS software shall [SRS278] provide an API call that provides the application program the minor frame number.
The behavior of synchronous tasks executed by the scheduler must be deterministic.
Task and Rate Group Execution
The scheduler shall [SRS035] provide rate groups that execute at 50 Hz, 10 Hz and 1 Hz., with a drift rate no greater than 50 microseconds per second, and with a jitter no greater than 330 microseconds.
The scheduler shall [SRS037] provide a method to schedule tasks at a set rate and in a set order within the rate group.
The scheduler shall [SRS198] execute all the tasks in each of the rate groups that have been installed in the current mode.
The scheduler shall [SRS039] rely on the order used in adding tasks to a rate group to determine the task priorities.
The scheduler shall [SRS042] provide a method for a task to be scheduled as a 50 Hz "helper" task for source congruency input exchanges and voted output exchanges that starts in a particular minor frame but runs only during every 5th or 50th minor frame, effectively running at a lower, sub-rate, 10 Hz or 1 Hz, respectively.
The scheduler shall [SRS270] provide a task deadline capability that allows the application to specify which minor frame a task should start in and finish in.
All tasks in rate groups and their corresponding schedules for all vehicle modes will be setup at system initialization.
Tasks in a rate group must suspend on a scheduler API call at the top of their execution loop.
Exception Handling
For purposes of handling exceptions, exceptions are defined as either software or hardware exceptions. Software exceptions are defined as those mapped into VxWorks signals. All other exceptions are classified as hardware exceptions.
Table 3.2-1 shows the mapping of software exceptions to VxWorks signals.
Table 3.2-1. Software Exception Mapping Table.
SIGNAL
CODE
EXCEPTION
SIGBUS
_EXC_OFF_MACH
Machine check
SIGBUS
_EXC_OFF_INST
Instruction access
SIGBUS
_EXC_OFF_ALIGN
Alignment
SIGILL
_EXC_OFF_PROG
Program
SIGBUS
_EXC_OFF_DATA
Data access
SIGFPE
_EXC_OFF_FPU
Floating point unavailable
SIGTRAP
_EXC_OFF_INST_BRK
Instruction breakpoint
SIGTRAP
_EXC_OFF_TRACE
Trace
SIGILL
_EXC_OFF_SYSCALL
System call

Upon the occurrence of an exception of either kind (hardware or software), the FCP shall [SRS172] make the error type available to the application, via an API service, for incorporation in the telemetry stream and include all context data relevant to the exception, namely the contents of the Machine State Register (MSR), and the machine status Save/Restore Registers (SRR0 & SRR1).
The scheduler shall [SRS031] provide a mechanism for a task optionally to define a user written software-exception-handling routine that runs in the context of the task.
For hardware exceptions and reserved exceptions, the FTSS shall [SRS276] make the error type and its context data available to the application, then return from the exception handler to the task that was running when the exception occurred.
For software exceptions occurring within the FTSS, the FTSS shall [SRS277] make the error type and its context data available to the application, then restart the offending task at its beginning.
For other software exceptions, regardless of whether or not a user written exception handling routine is invoked, if an exception occurs, the scheduler shall [SRS173], after making available the error type and context data to the application, resume processing (after the exception-handling routine runs, if provided) at the initialization point of the offending task.
For software exceptions occurring during Startup, FTSS shall [SRS301] issue a VME reset to the FCR in which the exception occurred.
Memory Management Services
Memory Protection
There are two types of memory violations that might occur: 1) as a result of a hardware fault or SEU and 2) as a result of a common mode (usually, software) error. Memory violations that result from random hardware faults will be detected in the same way as any other hardware fault is detected in the FTPP and don't require memory protection for them to be detected and dealt with. In the second case, NASA has determined that however the memory protection function is implemented, the policy will be to restart the task that is executing when a memory violation (exception) is detected.
The watchdog timer and ground based testing will uncover some but not all of the possible memory faults.
Communication Services
The FTSS communication services provide message-passing capabilities that are layered on top of the packet based network element communication hardware. Messages are contiguous blocks of variable length data that are transferred from one task to another. Messages are addressed with a global unique communication identifier that routes them to the appropriate virtual group (VG) and socket. Associated with the message are descriptor fields describing the sender, receiver, the type of message, and how the message is to be exchanged. The unique identifier for an end point consists of a virtual group identifier and a socket identifier. The sending and receiving end points may live on the same virtual group or on different virtual groups.
Communication Services are divided into two constituent capabilities: "Synchronous" message services and "Immediate" message services. "Synchronous" message services send and receive data on rate group frame boundaries; thus allowing safe inter-rate group communication. "Synchronous" message services are provided by message queue sockets. "Immediate" message services unlike "synchronous" message services initiate a message transfer immediately. When used for inter-VG communication, "immediate" message services interface directly with the Byzantine Resilient Virtual Circuit (BRVC) abstraction level communications interface and force an immediate network element access. "Immediate" message passing between virtual groups is restricted to the highest priority rate group on the FCP. This restriction does not apply to the ICPs. "Immediate" message passing within a virtual group is not restricted to the highest rate group, but must be used carefully by the application to prevent desynchronization. "Pipe" sockets provide "Immediate" message services.
Communication services provide a message passing capability that guarantees congruent use of the network element among the members of a virtual group under fault free conditions.
Communication services shall [SRS047] provide "synchronous" message passing services in the form of "message queues".
Communication services shall [SRS048] provide "immediate" message passing services in the form of "pipes". "Pipes" provide fast data throughput between virtual groups or within a virtual group when minimal data latency is necessary.
Communication services shall [SRS049] provide the capability to "broadcast" messages to all virtual groups.
Communication services shall [SRS050] restrict the use of "immediate" message passing services between virtual groups (from FCP to ICP) to tasks running in the highest rate group on the FCP. This restriction does NOT apply to the ICPs since they are running as simplex VGs.
Communication services shall [SRS051] detect message passing between application tasks living on the same virtual group and bypass the usage of the network element.
Communication services shall [SRS052] route messages to the proper virtual group(s) and socket.
Communication services shall [SRS053] deliver messages in the same order at each member of a virtual group.
Communication services shall [SRS054] perform synchronous message passing at rate group frame boundaries. This ensures that all redundant instantiations of a given rate group task have consistent messages throughout the rate group frame.
Communication services shall [SRS235] detect a babbling NE or ICP within 20 milliseconds of the receipt of the first erroneous packet.
FTSS shall [SRS255] mask out a babbling NE or ICP within 40 milliseconds after it is detected.
Sockets
Sockets are the end points of FTSS communication, which provide a transparent interface to the BRVC communications layer and a useful interface to the application layer. Sockets maintain the buffers between the underlying packet based communication primitives that directly access the network elements and the message based communication services used by the rate group tasks. Sockets used for "synchronous" message passing behave differently than those used for "immediate" message passing.
Synchronous message passing sockets shall [SRS055] queue outgoing messages until they are transmitted at frame boundaries. The "create" and "open" API calls for synchronous sockets allow the application to specify the maximum message size and how many incoming messages the socket may buffer.
If there is insufficient space to enqueue a message for transmission, Communication services shall [SRS059] return an error to the corresponding task. Sockets are non-blocking and place the burden of polling on the application task.
Message Queue Sockets
Message queue sockets allow a single task to queue a variable number of messages, each of variable length. One task is allowed to receive messages from this queue. Message queue sockets define a dedicated communication path between two tasks with guaranteed message delivery. Message queue sockets provide "synchronous" communication and perform sending/receiving of messages at frame boundaries.
Communication services shall [SRS062] provide a message queue communication mechanism that guarantees message delivery between a sending and receiving task.
Communication services shall [SRS063] provide an API for "message queue" communication.
Communication services shall [SRS064] provide the following error handling information as feedback to the "message queue" API calls:
notification of invalid or out of range application specified parameters on all operations,
notification of an attempt to create a broadcast message queue,
message queue "open" of end point ( SENDER/RECEIVER ) by non-assigned virtual group,
message queue is full when performing a send operation,
connection/transmission error,
FTSS unable to create/open message queue, and
notification that a received message was truncated to the buffer size provided.
The message queue "create" API requires the application to specify the sending and receiving virtual group identifiers. Communication services shall [SRS066] only allow a single task living on each specified virtual group to "open" the respective end of the queue.

Pipe Sockets
"Pipe" sockets are used for "immediate" communication. They may be created with a broadcast capability. Pipes may only be opened by one sending task. Pipes may be opened by multiple receiving tasks if they are created with the "broadcast" capability; otherwise they may only be opened by one receiving task. Pipes are the only broadcast mechanism available to the application.
Communication services shall [SRS067] provide a "pipe" communication mechanism allowing immediate message passing through the network and allowing a 50hz FCP transfer task to poll until it can read an immediate message from the ICP.
Communication services shall [SRS068] provide an API for "pipe" communication.
Communication services shall [SRS069] provide the capability to create "pipe"s which "broadcast" their messages to all virtual groups.
Communication services shall [SRS070] provide the following error handling information as feedback to the "pipe" API calls:
notification of invalid or out of range application specified parameters on all operations,
notification of an attempt to create a broadcast pipe with an ICP as the sending virtual group,
pipe "open" of end point ( SENDER/RECEIVER ) by non-assigned virtual group,
notification upon receiving a message that the previous message was overwritten,
connection/transmission error,
FTSS unable to create/open pipe, and
notification that a received message was truncated to the buffer size provided.
If the broadcast option is used, each virtual group should open the pipe and read from it to avoid flow control problems.
The "pipe" "create" API requires the application to specify the sending and receiving virtual group identifiers. Communication services shall [SRS073] only allow a single task living on each specified virtual group to "open" the respective end of the pipe. In the case of a broadcast "pipe", communication services allows one task in each virtual group of the system to open the receiving end of the "pipe".

Fault Detection and Isolation
Fault Detection and Isolation (FDI) provides the capability to detect and diagnose faults within FCC hardware. The functionality of FDI is decomposed into 2 capabilities-Initial Built-In Test (IBIT) and Continuous BIT (CBIT). FDI IBIT provides the facilities for the detection and diagnosis of faults during system initialization (at power on or CPU reset) on FCPs, ICPs, PMC 1553s, and MPCCs. FDI CBIT provides the facilities for the detection and diagnosis of faults on FCPs during all operational phases. In general, these tests execute system-wide tests using the fault tolerance characteristics of the FTPP architecture.
Initial BIT
Initial BIT constitutes a series of self-tests provided by the manufacturer of the equipment being tested. Initial BIT tests constitute tests of the processors, and I/O devices. Note that by configuring the network elements to automatically enter ISYNC on Power Up, there is no opportunity to perform IBIT on the NEs. The fact that an NE is in sync with the other NEs will have to substitute for a separate NE IBIT function.
FTSS IBIT executes on the Flight Control Processors (FCPs) at system initialization. These tests exercise the functionality of the various system components.
The FTSS software shall [SRS237] configure the FCP to act as the Radstone IBIT master, with the exception that the ICP on the NEFU is the master.
Requirement deleted.
The FTSS shall [SRS260] configure each FCP to perform IBIT Minimum Processing Environment (MPE) Tests, Power-up Tests, and Initial BIT on each FCP, as shown inTable 3.2-2. .
The FTSS shall [SRS261] configure each FCP to halt processing if any of the MPE tests fail.
The FTSS shall [SRS262] configure each FCP to continue processing if any of the Power-up or Initial BIT tests fail.
Table 3.2-2. FCP IBIT Table.
KIND OF TEST
TEST NAME
MPE Test
Program Programmable Read Only Memory (PROM) Test
MPE Test
Flash BootROM Checksum Test
MPE Test
On-board Random Access Memory (RAM) Test
MPE Test
Universe Device Test
Power-up Test
Timebase & Decrementer Test
Power-up Test
System Input Output Industry Standard Architecture (ISA) Bridge Test
Power-up Test
Main RAM Test
Power-up Test
Counter/Timer and Parallel I/O CIO Timers Test
Power-up Test
PowerPC Cache Test (on-chip only)
Power-up Test
PowerPC Memory Management Unit (MMU) Test
Power-up Test
PowerPC Floating Point Unit (FPU) Test
Power-up Test
Boot Flash Test
Power-up Test
Hardware Register Test
Initial BIT
Universe Test on Power-up

The FTSS shall [SRS287] configure each ICP to perform IBIT Minimum Processing Environment (MPE) Tests, Power-up Tests, and Initial BIT on each ICP, as shown inTable 3.2-3.
The FTSS shall [SRS288] configure each ICP to halt processing if any of the MPE tests fail.
The FTSS shall [SRS289] configure each ICP to continue processing if any of the Power-up or Initial BIT tests fail.
Table 3.2-3 ICP IBIT Table
KIND OF TEST
TEST NAME
MPE Test
Program Programmable Read Only Memory (PROM) Test
MPE Test
Flash BootROM Checksum Test
MPE Test
On-board Random Access Memory (RAM) Test
MPE Test
Universe Device Test
Power-up Test
Timebase & Decrementer Test
Power-up Test
System Input Output Industry Standard Architecture (ISA) Bridge Test
Power-up Test
Main RAM Test
Power-up Test
Counter/Timer and Parallel I/O CIO Timers Test
Power-up Test
PowerPC Cache Test (on-chip only)
Power-up Test
PowerPC Mass Memory Management Unit (MMU) Test
Power-up Test
PowerPC Floating Point Unit (FPU) Test
Power-up Test
Boot Flash Test
Power-up Test
Hardware Register Test
Power-up Test
(ICPs only)
Enhanced Serial Communications Controller Test.
(ICPs only)
Initial BIT
Universe Test on Power-up

The FTSS shall [SRS264] configure each ICP/PMC1553 to perform IBIT MPE Tests and Initial BIT as shown in Table 3.2-4.
The FTSS shall [SRS265] configure each ICP/PMC1553 to halt processing if any of the MPE tests fail.
The FTSS shall [SRS266] configure each ICP/PMC1553 to continue processing if any of the Initial BIT tests fail.

Table 3.2-4. ICP/PMC1553 IBIT Test Configuration.
KIND OF TEST
TEST NAME
MPE
Electrically Erasable Programmable Read Only Memory (EEPROM) header contents check to meet the expected values
MPE
EEPROM checksum for correct contents (test code and data are valid)
Initial BIT
Advance Communications Engine (ACE) 0 existence test
Initial BIT
ACE 0 RAM Test
Initial BIT
ACE 0 Register Test
Initial BIT
ACE 0 Interrupt Test

The FTSS shall [SRS267] configure each MPCC to perform MPE Tests as shown in Table 3.2-5.
Each MPCC is configured to halt processing if any of the MPE tests, listed in Table 3.2-5, fails.
Table 3.2-5. MPCC IBIT Test Configuration.
KIND OF TEST
TEST NAME
MPE
Control and Status Register Test
MPE
Erasable PROM Checksum Test
MPE
Local RAM Test
MPE
68020 Processor Test
MPE
Dual-port RAM Test

When the IBIT is complete, the FTSS in the channels that are part of the fault masking group shall [SRS239] report the results of IBIT for all Radstone boards to the application software for telemetry.
In IBIT failure cases that cause processing to halt, the failure shall [SRS269] be handled as described in Section 3.2.6.2, Recovery.
FTSS shall [SRS290], in ICP and FCP IBIT failure cases that allow processing to continue, after saving the results of IBIT for reporting to the application, in the first minor frame after Startup or recovery, consider the FCR to be failed, and start performing recovery actions for the FCR.
Continuous BIT
Continuous BIT executes on the FCP at all times after initialization is complete. In general, these tests execute system-wide tests using the fault tolerance characteristics of the FTPP architecture.
Continuous BIT, in conjunction with Redundancy Management and Scheduler operations running in the 50 Hz rategroup after the application tasks, shall [SRS091] take less than 2 milliseconds under nominal no-fault conditions.
Continuous BIT, in conjunction with Redundancy Management and Scheduler operations running in the 50 Hz rategroup after the application tasks, shall [SRS183] take less than 3 milliseconds while processing faults.
Continuous BIT shall [SRS093] execute on the FCP virtual group.
Continuous BIT shall [SRS094] reset the processor’s built-in watchdog timer at 50 Hz. A failure to reset the watchdog timer within the allotted time (nominally 1.6 seconds) will generate a processor reset.
Continuous BIT shall [SRS095] exercise the presence test at 50 Hz to ensure that all processors in the FCP virtual group are synchronized.
The presence test shall [SRS184] also ascertain that all processors are executing the same 50 Hz, 10 Hz and 1 Hz frames.
Continuous BIT shall [SRS096] diagnose the faulty FCR within 1 second after detecting a failure.
Continuous BIT shall [SRS097] detect a failed ICP processor by detecting the absence of a periodic message for 2 consecutive minor cycles.
Continuous BIT shall [SRS098] report all diagnosed failures and recovery actions to the application for incorporation in the telemetry stream.
RAM Scrub
RAM scrub shall [SRS043] actively trigger the EDAC function by cyclically reading (and writing back if an error is found) all used RAM.
RAM scrub shall [SRS044] report detected errors to the application, congruently on all channels, via an API service for inclusion in the telemetry stream.
RAM scrub shall [SRS187] be capable of scrubbing at least 10 megabytes every 8 minutes, given at least 1% of the CPU is available for this processing.
RAM scrub shall [SRS275] not scrub the area used for telemetry data.
Redundancy Management
Redundancy Management maintains the mapping of physical hardware to virtual groups. This capability reconfigures the mapping in response to a diagnosis of a failed component, which can be a failed processor, failed network element or a link failure. Redundancy Management also performs transient fault analysis within constraints dictated by the mission management application software.
Redundancy Management shall [SRS099] provide an API call to enable the application to retrieve the health status of the processors, network elements, network element links, MPCCs, and ICP controlled interfaces.
Redundancy Management shall [SRS100] provide an API call to enable the application to request that the FTSS RM software initiate a voted reset of a channel.
Redundancy Management shall [SRS201] be able to accommodate power up of all 5 channels and maintain all 5 NEs active, assuming no failures.
Virtual Group Configuration
The virtual group configuration defines the mapping of physical hardware to virtual group(s). It defines the redundancy of each virtual group and the location of the processors in the VME backplane. This mapping of virtual group member(s) is maintained as an ordered pair of network element and port on the associated network element.
Redundancy Management shall [SRS101] define an initial mapping of physical hardware to virtual group identifiers consisting of 1 quadruplex FCP virtual group and 5 ICP simplexes.
If an FCR is diagnosed as faulty during Startup, Redundancy Management shall [SRS102] exclude the FCP in the faulty channel from the initial FCP virtual group configuration.
Recovery
Redundancy Management configures the FCP virtual group, the network element, and the interconnection links for recovery of hardware resources in the operational system. Redundancy Management determines the recovery strategy to be executed based upon current configuration and whether alignment is permitted.
When a fault occurs, the configuration will change. The new configuration depends on the previous configuration. All the possible configuration changes are shown in REF _Ref504962431 \h Figure 3‑2.

Figure STYLEREF 1 \s 3‑ SEQ Figure \* ARABIC \s 1 2 Fault-down Map
Redundancy Management shall [SRS104] implement the following strategies to reconfigure hardware resources:
degrade the FCP virtual group,
re-integrate an FCP processor into the FCP virtual group,
re-integrate a Network Element, or
mask a Network Element.
When the FCP virtual group is configured as a quadruplex and a failed FCR other than the NEFU has been diagnosed, Redundancy Management shall [SRS106] degrade the FCP virtual group to triplex, removing the FCR. The NE and the processors on the failed FCR will be removed from the NEs’ Configuration Table (CT) and recovery of that channel will then take place, if alignment is permitted. Note that a failed FCR could be diagnosed using any method, including (but not limited to) Continuous BIT, ICP presence test, or NE syndrome analysis.
When the FCP virtual group is configured as a triplex, and if the NEFU is still active (4 NEs active total), and a failed FCR other than the NEFU has been diagnosed, Redundancy Management shall [SRS282] degrade the FCP virtual group to degraded triplex, removing the FCR. The NE and the processors on the failed FCR will be removed from the NEs’ Configuration Table (CT) and recovery of that channel will then take place, if alignment is permitted. Note that a failed FCR could be diagnosed using any method, including (but not limited to) Continuous BIT, ICP presence test, or NE syndrome analysis.
If the FCP is configured as a triplex, and if the NEFU is not still active (3 NEs active total), and another failure in the FCP FCR is diagnosed, Redundancy Management shall [SRS284] mask out the processors on the failed FCR. The NE will remain in the CT and no recovery will take place. Note that a failed FCR could be diagnosed using any method, including (but not limited to) Continuous BIT, ICP presence test, or NE syndrome analysis.
If a failure in an FCR other than the NEFU is diagnosed when the FCP is configured as a degraded triplex, no action shall [SRS254] be taken. Note that a failed FCR could be diagnosed using any method, including (but not limited to) Continuous BIT, ICP presence test, or NE syndrome analysis.
For the NEFU, if the first failure is diagnosed, Redundancy Management shall [SRS245] issue a configuration update to mask out the failed processor. Note that the NE is allowed to remain in the configuration and no recovery will take place. Note also that the failed NEFU could be diagnosed using any method, including (but not limited to) ICP presence test, or NE syndrome analysis.
For the NEFU, if errors are identified after the processor has been masked out, and if at least 4 NEs are still active, the NE shall [SRS283] be removed from the configuration and recovery will be attempted. Note that the NEFU recovery does not depend on whether alignment is permitted.
If the configuration needs to be changed due to a fault, as specified above, Redundancy Management shall [SRS128] issue a configuration update to mask out the failed network element.
Redundancy Management shall [SRS109] degrade the FCP virtual group within 3 minor frames of fault detection and isolation.
Recovery consists of the following steps:
Redundancy Management shall [SRS204] issue a voted reset to the failed channel, if alignment is permitted. (Note that NEFU recovery does not depend on whether alignment is permitted.)
Redundancy Management shall [SRS129] initiate transient NE recovery to restore Byzantine-resilient communications, if alignment is permitted. (Note that NEFU recovery does not depend on whether alignment is permitted.)
Redundancy Management shall [SRS110] reintegrate a failed FCP processor with the FCP virtual group when alignment is permitted and when the processor failure is not permanent.
From the time that the FCR failure has been identified, if the components of the FCR are recoverable and alignment is permitted, to the time the FCR is recovered, shall [SRS205] be no more than 1.5 minutes.
Redundancy Management shall [SRS208], within 60 milliseconds after 1.5 minutes has elapsed since the voted reset was sent to the failed channel, if the voted reset fails to recover the failed channel and alignment is still allowed, request from the application a power cycle of the channel. (Note that NEFU recovery does not depend on whether alignment is permitted.)
Redundancy Management shall [SRS209], within 60 milliseconds after 1.5 minutes has elapsed since the first power cycle request, if the FCR has not been recovered and alignment is still allowed, issue another request to the application for a power cycle of the channel. (Note that NEFU recovery does not depend on whether alignment is permitted.)
Redundancy Management shall [SRS211], if power cycle requests fail to result in a recovered channel, request the application to power down the channel and declare the channel to be permanently failed. Note that the same result will occur if the application software ignores or fails to respond to power cycle requests.
The application software shall [SRS285] have the capability to reset a permanently failed channel to its initial recovery state.
Redundancy Management shall [SRS117] reintegrate a processor that is temporarily disabled during a time when alignment was not permitted, when alignment is subsequently permitted. Redundancy Management picks up where it left off in these attempts. For example, if Redundancy Management is at 1 minute in its 1.5 minute wait for a channel after the first power cycle request, and alignment is not allowed, when alignment is subsequently allowed Redundancy Management will wait another half minute and then try the next power cycle request.
An API call shall [SRS274] be provided that allows the application to notify FTSS that an FCR is intentionally being powered down.
Redundancy Management shall [SRS302] provide an API call to allow the application to specify whether recovery and alignment of failed FCRs is permitted. Note that recovery of the NEFU is always considered to be permitted.
Recovery from Processor Failure
This section deleted
Degrade Virtual Group
This section deleted.
Reintegrate Processor
When memory alignment is permitted, Redundancy Management attempts to reintegrate a processor with the other members of its original FCP virtual group by commanding the affected FCP virtual group to perform re-synchronization operations. Redundancy Management aligns the memory, clocks, cache, and other internal registers of the failed processor after synchronization has been achieved.
While synchronization is being attempted, the FCP virtual group shall [SRS123] maintain synchronous operations.
Only when memory alignment is permitted, Redundancy Management shall [SRS124] initiate periodic re-synchronization attempts on the FCP virtual group at a 1 second rate.
Redundancy Management shall [SRS125] perform memory alignment on a major frame boundary upon successful synchronization of all members of the FCP virtual group.
Redundancy Management shall [SRS281], during memory alignment, configure the NE to mask out the processor being re-synchronized.
Redundancy Management shall [SRS271] notify the application that alignment and reintegration of a processor will take place in 1 second.
Redundancy Management shall [SRS272] wait for the ICP to signal that it has completed initialization before suspending the application for memory re-alignment.
During alignment, Redundancy Management shall [SRS126] update MET (and, by extension, SEP).
Redundancy Management shall [SRS214], if alignment is permitted, incorporate a new channel within 1.5 minutes after power is applied to the channel.
Redundancy Management shall [SRS236], if alignment is permitted, serially incorporate two new channels if they are powered on simultaneously.
Data Management
Three types of memory are defined:
Congruent aligned - always aligned
Congruent initialized - initialized from nonvolatile memory
Non-congruent - never aligned
The FTSS API shall [SRS046] define a methodology for segregating and managing congruent aligned, congruent initialized, and non-congruent memory such that congruent aligned memory is aligned and congruent initialized memory is initialized during channel recovery. Non-congruent memory is not modified during realignment.
The FTSS API shall [SRS217] specify a memory map that provides the boundaries for congruent aligned memory, congruent initialized memory, and non-congruent memory.
Memory Alignment
Memory alignment occurs when a channel has been out of synchrony for some amount of time and then re-synchronizes with the other channels. The amount of time the channel is out of synchrony depends on the recovery mechanism. It could take as much as 4.5 minutes for the channel to be recovered and re-aligned (1.5 minutes per attempt for 3 attempts). The channel that is being brought back into synchrony is the "target" channel.
Memory alignment shall [SRS045] align processor state and congruent aligned memory locations. Processor state includes all registers. It also includes those timers used by FTSS.
The re-align function shall [SRS186] write the voted value from the currently synchronized channels into the target channel.
FTSS shall [SRS200] initialize congruent initialized memory locations from non-volatile memory.
Memory alignment shall [SRS203] take no more than 1 second per Megabyte of data to be realigned.
The FCP watchdog timer shall [SRS293] remain active during memory re-alignment.
Memory alignment shall [SRS294] reset the watchdog timer such that, in the absence of a fault, the timer never expires and resets the processor.
Recovery from Link Failure
This section deleted.
Recovery from Network Element Failure
This section deleted.
Time Services
Time Services shall [SRS142] provide Mission Elapsed Time and Separation Elapsed Time, with resolution partitioned as follows according to rate group, in order to guarantee identical copies of time representation across all FCPs:
