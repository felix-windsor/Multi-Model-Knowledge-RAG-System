# 2000 - nasa x38 - 0 to 49

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2000 - nasa x38.doc

Section: 0 to 49

0 to 49
FTSS CSCI
ICP
vehicle_mode
Current vehicle mode used to change tasking.
ulong
> 0
FTSS CSCI
ICP
met
FCP mission elapsed time
unsigned int
>0
FTSS CSCI
ICP
sep
FCP separation elapsed time
unsigned int
>0
FTSS CSCI
ICP
VME Interrupt
Interrupt raised from FCP side to vector an ISR on ICP side. This is for 50 Hz minor frame sync across processors
n/a
n/a
FCP
ICP

CSCI Internal Interface Requirements
There are no requirements for internal interfaces.
CSCI Internal Data Requirements
There are no requirements for internal data.
Adaptation Requirements
No requirements related to installation-dependent data or operational parameters have been identified.
Safety Requirements
No safety requirements have been identified.
Security and Privacy Requirements
No security requirements have been identified.
CSCI Environment Requirements
See Section 3.10.3.
Computer Resource Requirements
Computer Hardware Requirements
The FTSS shall [SRS158] execute on the Radstone Power PC 604R.
Computer Hardware Resource Utilization Requirements
The FTSS software and the VxWorks operating system, together shall [SRS193] utilize no more than 3 megabytes of ROM.
The largest single block of data transmitted on the VME Bus by the FTSS shall [SRS223] transmit in no longer than 100 microseconds.
All FTSS data provided for telemetry (as specified in the requirements) shall [SRS250] fit within the allocated budget of 5000 bits per second.
In addition, the FTSS software shall [SRS280] provide up to 600 bits of start-up data that indicates the state of the FTPP system during start-up.
Note that CPU usage limits, where needed, have been included in each of the sections with the requirements for the services provided. It is not possible to limit the total CPU usage of all services provided by the FTSS since the application calls the services an unknown number of times per major cycle.

Computer Software Requirements
The FTSS software shall [SRS159] be written in the C programming language.
FTSS shall [SRS160] use the VxWorks Operating System version 5.4.
The FTSS software and the VxWorks operating system shall [SRS258] utilize no more than 9 Megabytes of DRAM code and data space.

Of the 9 Megabytes of DRAM allocation, only 4 Megabytes of FTSS/VxWork’s DRAM shall [SRS259] be re-aligned during any re-alignment attempts.

FTSS shall [SRS253] be compiled, linked and downloaded using Tornado 2 for the NT environment prior to delivery, for all engineering and formal releases.
FTSS object modules linked to the application on the four FCPs shall [SRS166] be identical.
After initial synchronization, the FCPs shall [SRS168] remain synchronized until a hardware fault occurs. For example, asymmetric I/O calls will not be allowed to induce a large enough skew to force the FCPs to desynchronize.
Computer Communications Requirements
NA
Software Quality Factors
NA
Design and Implementation Constraints
See Section 3.10.3.
Personnel-related Requirements
No personnel-related requirements have been identified.
Training-related Requirements
No training-related requirements have been identified.
Logistics-related Requirements
NA
Other Requirements
This section contains the requirements for the ICP.
ICP Services
FTSS shall [SRS303] provide an API call to allow the ICP application to determine on which channel it resides.
FTSS shall [SRS225] provide an API call to allow applications to send a status message to FDIR running on the FCP.
FTSS shall [SRS226] provide "immediate" message passing services in the form of "pipes". "Pipes" provide fast data throughput between virtual groups or within a virtual group when minimal data latency is necessary.
FTSS shall [SRS227] route messages to the proper virtual group(s) and socket.
If there is insufficient space to enqueue a message for transmission, FTSS shall [SRS228] return an error to the corresponding task. Sockets are non-blocking and place the burden of polling on the application task.
FTSS shall [SRS229] provide the following error handling information as feedback to the "pipe" API calls:
notification of invalid or out of range application specified parameters on all operations,
pipe "open" of end point ( SENDER/RECEIVER ) by non-assigned virtual group,
notification upon receiving a message that the previous message was overwritten,
connection/transmission error,
FTSS unable to create/open pipe, and
notification that a received message was truncated to the buffer size provided.
FTSS shall [SRS230] only allow a single task residing on each specified virtual group to "open" the respective end of the pipe.
The presence or absence of an NEFU ICP shall [SRS220] not impact the FTSS software (i.e. the FTSS ICP load will not be different).
The FTSS shall [SRS231] provide an API call to retrieve the current minor frame number sent from the FCP over the VME interface. Note that the NEFU ICP will not have this information since it does not have an FCP processor.
The FTSS shall [SRS232] provide an API call to retrieve the current MET value sent from the FCP over the VME interface. Note that the NEFU ICP will not have this information since it does not have an FCP processor.
The FTSS shall [SRS233] provide an API call to retrieve the current SEP value sent from the FCP over the VME interface. Note that the NEFU ICP will not have this information since it does not have an FCP processor.
The FTSS shall [SRS295] notify the application on the ICP, via an API call, 2 minor frames prior to an alignment.
Packaging Requirements
FTSS deliveries shall [SRS252] be made using CD ROM media.
Precedence and Criticality of Requirements
No precedence or criticality of requirements has been identified.
QUALIFICATION PROVISIONS
The following qualification methods will be used for the FTSS software.
Demonstration (D) - The operation of the CSCI (or some part of the CSCI) to observe its functional operation. The functional operation is directly observable, and it requires no elaborate instrumentation or special test equipment.
Test (T) - The operation of the CSCI (or a part of the CSCI) using instrumentation or other special test equipment to collect data for later analysis.
Analysis (A) - The processing of data accumulated from other qualification methods to determine correct results (e.g., interpretation of data collected by special test equipment).
Inspection (I) - The visual examination of CSCI code, documentation, etc.
The qualification methods that will be used for each software requirement are specified in the Certification Test Procedures document.
REQUIREMENTS TRACEABILITY
Table 5-1 provides the traceability between the X-38 Fault Tolerant Parallel Processor (FTPP) Requirements document number JSC 28671, and this document. The FTPP Requirements document specifies the FTSS system requirements. Table 5-1 is sorted by the system requirement number.

Table 5-1. FTPP to SRS Trace Table.
FTPP Section #
FTPP Section Name
FTPP Requirement
SRS Req #s
3.1
FTPP System Requirements
Each FTPP shall (3.1.1) consist of five (5) NEs (one for each FCC and one for the NEFU) and FTSS software.
NA
3.1
FTPP System Requirements
For the FTPP system (5 NEs per flight system), the contractor shall (3.1.2) deliver the following end products:
NA
3.1
FTPP System Requirements
The FTPP spare hardware shall (3.1.28) include one (1) radiation hardened FTPP set (5 NEs) and three (3) individual NEs including all optical connects, cables, and required accessories which are flight certified to meet the requirements specified herein for the X-38 space flight vehicles.
NA
3.1
FTPP System Requirements
The contractor shall (3.1.3) develop a preliminary design for the FTPP Architecture.
NA
3.1
FTPP System Requirements
This system shall (3.1.4) provide real time redundancy and fault tolerance among the four FCCs and the NEFU.
SRS043, SRS091, SRS093, SRS094, SRS095, SRS096, SRS102, SRS104, SRS106, SRS109, SRS128, SRS183, SRS184, SRS187, SRS235, SRS282, SRS283
3.1
FTPP System Requirements
The FTPP system shall not (3.1.5) solely exceed these timing requirement budgets.
SRS034, SRS035
3.1
FTPP System Requirements
In the presence of a maximum 2.5 second power-on skew, the FTPP system shall (3.1.6) be capable of completing FCC system power-up and initialization without synchronization errors.
SRS008
3.1
FTPP System Requirements
Following power being applied to all five chassis, the FTPP system shall (3.1.7) become operational in at most 1.5 minutes.
SRS015
3.1
FTPP System Requirements
The FTPP shall (3.1.26) detect a babbling NE or ICP within 20 milliseconds of the receipt of the first erroneous packet.
SRS235
3.1
FTPP System Requirements
The FTPP shall (3.1.27) recover from a babbling NE or ICP within 40 milliseconds after it is detected.
SRS255
3.1
FTPP System Requirements
An exchange of a single packet of data from an ICP to the FCPs via the NE shall (3.1.8) take no longer than 200 microseconds.
hw
3.1
FTPP System Requirements
An exchange and broadcast of a single packet of data from the FCPs to the ICPs and the FCPs via the NE shall (3.1.9) take no longer than 150 microseconds. A packet size is assumed to be 60 bytes
hw
3.1
FTPP System Requirements
Under no fault conditions, after initial power on, the FTPP system shall (3.1.10) create six Virtual Groups (VGs), a fault masking FCP, and the five ICPs, and enter the data in the NE Configuration Table (CT).
SRS101, SRS296
3.1
FTPP System Requirements
From the time that the NE failure has been identified, and the NE is recoverable, to the time the NE is recovered shall (3.1.11) be no more than 1.5 minutes.
SRS205
3.1
FTPP System Requirements
The FTPP shall (3.1.12) be capable of restoring a corrected faulty computer into the flight critical computer set.
SRS124, SRS214
3.1
FTPP System Requirements
The FTPP shall (3.1.14) take no more than 1 second per Megabyte of data to be realigned.
SRS203
3.1
FTPP System Requirements
The failed channel, provided it is recoverable, shall (3.1.15) be recovered in less than 1.5 minutes.
SRS205
3.1
FTPP System Requirements
The FTPP voting implementation shall (3.1.16) isolate and remove a faulty computer from the flight critical computer set within 60 milliseconds, once the fault has manifested itself.
SRS109
3.1
FTPP System Requirements
The FTPP system shall (3.1.17) be two fault tolerant for any two non-simultaneous hardware faults through out all phases of the X-38 mission (i.e., from power on to power off, without degradation).
SRS043, SRS091, SRS093, SRS094, SRS095, SRS096, SRS102, SRS104, SRS106, SRS109, SRS128, SRS183, SRS184, SRS187 SRS235, SRS282, SRS283, SRS281
3.1
FTPP System Requirements
The FTPP system shall (3.1.18) be capable of powering up and operating with any combination of 3 of the 5 FCR's active.
SRS010, SRS102
3.1
FTPP System Requirements
The FTPP system shall (3.1.19) be able to accommodate power up of all 5 channels and maintain all 5 NEs active, assuming no failures.
SRS201
3.1
FTPP System Requirements
The FTPP system shall (3.1.20) incorporate additional channels in the active set as they are powered-on by the application software.
SRS124, SRS125, SRS126, SRS214
3.1
FTPP System Requirements
After the initial power-up of only two FCRs and the NEFU, the FTPP system shall (3.1.25) be able to incorporate two more FCRs, upon their simultaneous or separate power-up.
SRS236
3.1
FTPP System Requirements
The FTPP system shall (3.1.21) monitor for the presence of new channels at a 1 Hz periodic rate.
SRS124
3.1
FTPP System Requirements
All healthy FCRs shall (3.1.22) be incorporated as they become available.
SRS125, SRS126, SRS214
3.1
FTPP System Requirements
All FCP processing channels (up to 4) shall (3.1.23) be incorporated into the FCP virtual group as they become available, provided that recovery and memory alignment is allowed by the application software.
SRS123, SRS124, SRS125, SRS126, SRS214
3.1
FTPP System Requirements
When memory realignment is not permitted, the FTPP system shall (3.1.24) maintain, at a minimum, 3 channels of I/O or 2 channels of I/O and the NEFU.
SRS254
3.2.1
Network Element Addressing Convention
The FCC hardware shall (3.2.1.1) use 3-digit binary numbers as outlined above for both addresses.
hw
3.2.2.1
Data Exchange Primitives
The X-38 NE shall (3.2.2.1.1) provide four types of data exchange primitives as described below, in accordance with the Byzantine-resilient replicated determinism requirements described in [1]. (Class 0, 1, 2, Broadcast)
hw
3.2.2.2
Configuration Table Updates
The NE shall (3.2.2.2.1) keep track of the grouping of physical processors into virtual groups. This mapping is contained in the Configuration Table (CT).
hw
3.2.2.2
Configuration Table Updates
The CT shall (3.2.2.2.2) also contain time-outs and vote masks.
hw
3.2.2.2
Configuration Table Updates
It shall (3.2.2.2.3) be possible to modify the CT whenever any of this information is changed by using a CT update primitive in a synchronous and atomic manner.
hw
3.2.2.3
Initial Synchronization (ISYNC)
The NE shall (3.2.2.3.1) be configured to automatically enter ISYNC microcode following power on.
hw
3.2.2.3
Initial Synchronization (ISYNC)
The NE shall (3.2.2.3.2) start transmitting a sync message using class 2 exchanges once 3 fault tolerant clocks have synchronized, thus enabling inter-NE data exchanges.
hw
3.2.2.3
Initial Synchronization (ISYNC)
A time-out period shall (3.2.2.3.3) be started when 3 NEs have joined in.
hw
3.2.2.3
Initial Synchronization (ISYNC)
The ISYNC procedure shall (3.2.2.3.4) terminate when all 5 NEs are synchronized, four NEs are synchronized (when only four NEs are powered), or after the time-out period.
hw
3.2.2.3
Initial Synchronization (ISYNC)
The NE microcode shall (3.2.2.3.6) initialize the time-outs and vote masks in the NE CT using values stored in the NE.
hw
3.2.2.3
Initial Synchronization (ISYNC)
The maximum time-out value shall (3.2.2.3.7) be 327.68 microseconds (256 counts of the least significant bit of the fault tolerant clock which is 1.28 microseconds).
hw
3.2.2.4
Transient NE Recovery (TNR)
An NE that fails to synchronize with other NEs during ISYNC after a pre-defined time-out period shall (3.2.2.4.1) then enter TNR microcode.
hw
3.2.2.4
Transient NE Recovery (TNR)
An NE shall (3.2.2.4.12) directly enter TNR microcode after a voted reset or an NE watchdog timer reset.
hw
3.2.2.4
Transient NE Recovery (TNR)
It shall (3.2.2.4.2) stay in TNR mode indefinitely until a successful TNR exchange is observed.
hw
3.2.2.4
Transient NE Recovery (TNR)
The operational NEs shall (3.2.2.4.3) enter a "working group" TNR routine when the FCPs request to send a TNR packet.
hw
3.2.2.4
Transient NE Recovery (TNR)
If no new NE is observed, the functioning NEs shall (3.2.2.4.6) return to the operational mode within 500 microseconds.
hw
3.2.2.4
Transient NE Recovery (TNR)
If there is a new NE, the state of the reintegrated NE shall (3.2.2.4.13) be made congruent with the state of the operational NEs as follows.
hw
3.2.2.4
Transient NE Recovery (TNR)
The Configuration Table shall (3.2.2.4.7) be exchanged and voted into the newly recovered NE.
hw
3.2.2.4
Transient NE Recovery (TNR)
Time-outs in the scoreboard shall (3.2.2.4.8) be aligned by resetting all time-outs.
hw
3.2.2.4
Transient NE Recovery (TNR)
The global synchronous timer shall (3.2.2.4.9) be realigned by exchanging and voting the timer value. The timer value will stop incrementing until the realignment of the timer is complete.
hw
3.2.2.4
Transient NE Recovery (TNR)
Provided the failed NE is in a recoverable state, recovery of a failed NE shall (3.2.2.4.11) take no longer than 500 microseconds. This recovery requirement includes the time from which the FTSS software initiates the recovery to the time the recovery is complete.
hw
3.2.2.5
Voted Resets
There shall (3.2.2.5.1) be built-in support on the NE for voted resets, including a special packet type for executing the primitive.
hw
3.2.2.5
Voted Resets
The NE shall (3.2.2.5.3) provide the capability to perform a voted VME bus reset.
hw
3.2.2.6
Error Syndrome Reports
The NE shall (3.2.2.6.1) place error syndromes in the input information block whenever a packet is successfully delivered to the FCP.
hw
3.2.2.6
Error Syndrome Reports
The NE syndromes shall (3.2.2.6.2) be located in the second longword of the input information block buffer cell.
hw
3.2.2.6
Error Syndrome Reports
The NE syndromes shall (3.2.2.6.3) include indications of vote errors, fault-tolerant clock synchronization errors, and fiber-optic link errors, as detailed below.
hw
3.2.2.6
Error Syndrome Reports
Each syndrome shall (3.2.2.6.4) represent an occurrence of the indicated error at some time between delivery of the previous packet and delivery of the current packet.
hw
3.2.2.6
Error Syndrome Reports
The scoreboard syndromes shall (3.2.2.6.5) be located in the third longword of the input information block buffer cell.
hw
3.2.2.6
Error Syndrome Reports
They shall (3.2.2.6.6) include indications of scoreboard vote errors, Output Buffer Not Empty (OBNE) time-outs, and Input Buffer Not Full (IBNF) time-outs, as follows.
hw
3.2.2.6
Error Syndrome Reports
When a majority, but not a unanimity, of FCP members are observed with packets in their output buffers, a time-out shall (3.2.2.6.7) be initiated.
hw
3.2.2.6
Error Syndrome Reports
If the time-out expires before the other members transmit the packet, the remaining member shall (3.2.2.6.8) be ignored, the packet exchanged, and an OBNE time-out recorded.
hw
3.2.2.6
Error Syndrome Reports
When a majority, but not a unanimity, of FCP members are observed with room in their input buffers, a time-out shall (3.2.2.6.15) be initiated.
hw
3.2.2.6
Error Syndrome Reports
If the time-out expires before the other members have room in their input buffers, any member without room in their input buffer shall (3.2.2.6.16) be ignored, the packet exchanged, and an IBNF time-out recorded.
hw
3.2.2.7
Timestamps
The NE shall (3.2.2.7.1) place a timestamp in the input information block of each packet successfully delivered to an FCP or ICP.
hw
3.2.2.7
Timestamps
The timestamps shall (3.2.2.7.2) be congruent across all members of the destination FCP.
hw
3.2.2.7
Timestamps
The timestamps shall (3.2.2.7.3) also be congruent across all active processors in the case of a broadcast.
hw
3.2.2.7
Timestamps
The timestamp shall (3.2.2.7.4) be a 32-bit quantity that indicates relative time within the FCC.
hw
3.2.2.7
Timestamps
The resolution of the timestamp shall (3.2.2.7.5) be 1.28 microseconds.
hw
3.2.2.7
Timestamps
When the timestamp counter reaches the maximum value (Hex FFFFFFFF or approximately 5500 seconds), it shall (3.2.2.7.6) wrap around to zero.
hw
3.2.2.7
Timestamps
The timestamp counter shall (3.2.2.7.7) be initialized to zero during ISYNC.
hw
3.2.2.7
Timestamps
The counter shall (3.2.2.7.8) increase monotonically after that, except during TNR.
hw
3.2.2.7
Timestamps
The timestamps shall (3.2.2.7.9) be frozen during TNR until the realignment is complete.
hw
3.2.2.8
Debug Commands
The NE shall (3.2.2.8.1) implement in microcode support commands to aid in debugging new NEs and for performing stand-alone diagnostics and self-tests.
hw
3.2.2.8
Debug Commands
As a minimum, the following diagnostic functionality shall (3.2.2.8.2) be supported. 1. VMEbus Interface test 2. Message wraparound test 3. Class 1 Voter test 4. Class 2 Voter test 5. Input Buffer Test 6. Output Buffer test 7. CT entry test 8. CT update test 9. Timestamp test
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The prototype NE shall (3.2.3.1.1.1) reside on a single commercial grade 6U VME board.
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The prototype NE shall (3.2.3.1.1.2) dissipate no more than 35 Watts.
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The operating temperature range for the prototype NEs shall (3.2.3.1.1.3) be from 0 to 32.2º C at the inlet to the cooling fans.
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The storage temperature range shall (3.2.3.1.1.4) be from - 30º to + 60º C.
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The prototype NEs shall (3.2.3.1.1.5) use convection cooling.
hw
3.2.3.1.1
Prototype NE Physical Characteristics
The prototype NE shall (3.2.3.1.1.6) be fabricated using commercial grade components.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Each flight NE shall (3.2.3.1.2.1) reside on a single ruggedized, wedge-locked, conduction-cooled 6U VME board.
hw
3.2.3.1.2
Flight NE Physical Characteristics
It shall (3.2.3.1.2.2) be able to be installed in an Air Transportable Rack (ATR) Chassis with .8 pitch spacing card slots.
hw
3.2.3.1.2
Flight NE Physical Characteristics
The conduction-cooled boards’ mechanical core shall (3.2.3.1.2.3) be designed in accordance with IEEE 1101.2.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Power de-coupling mechanisms shall (3.2.3.1.2.4) be designed into the NE.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Backplane connector form factors shall (3.2.3.1.2.5) be in accordance with the VME64 with extensions (5 row P1 and P2) draft standard.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Connector P2 shall (3.2.3.1.2.6) have all pins in row z connected to ground;Row d pins 1 through 31 connected to ground and row d pin 32 connected to +5 VDC.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Connector P1 shall (3.2.3.1.2.7) have Row z pins 1 through 32 connected to ground, row d pins 1 and 32 connected to +5 VDC, row d pins 2 through 31 connected to ground with the exception of pins 3 through 8, pins 12, 14, 16, 18, 20, 22, 24, 26, 28, and 30 which will not be connected.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Connector P1 pins 1 and 32 of row d shall (3.2.3.1.2.8) be connected to +5V.
hw
3.2.3.1.2
Flight NE Physical Characteristics
The inter-NE communications shall (3.2.3.1.2.9) be through fiber.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Test points shall (3.2.3.1.2.10) be made available at the P2 connector for examining the operational status of the NE.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Each flight NE shall (3.2.3.1.2.11) dissipate no more than 35 Watts.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Each flight NE shall (3.2.3.1.2.12) be conduction-cooled.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Flight hardware shall (3.2.3.1.2.13) be fabricated using radiation-hardened and/or radiation tolerant components.
hw
3.2.3.1.2
Flight NE Physical Characteristics
Fabrication and assembly of the boards shall (3.2.3.1.2.14) meet NAS 5300.4(3L), NAS 5300.4(3J-1), NHB5300.4(3A-2), IPC 275, IPC 6011, IPC 6012 and GSFC-S-312-P-003.
hw
3.2.3.1.3
Flight NE Environmental Qualification Conditions
The flight NE shall (3.2.3.1.3.1) be capable of meeting all performance requirements specified herein during and after exposure to the environmental service conditions specified herein.
hw
3.2.3.1.3
Flight NE Environmental Qualification Conditions
The flight NE shall (3.2.3.1.3.2) be designed and constructed so that no part of any component shifts in setting, position, or adjustment.
hw
3.2.3.1.3
Flight NE Environmental Qualification Conditions
No degradation shall (3.2.3.1.3.3) be caused in the performance that is specified in Subsections 3.2.3.1.3.1 through 3.2.3.1.3.11
hw
3.2.3.1.3.1
Temperature
The flight NE shall (3.2.3.1.3.1.1) meet the following temperature requirement while operating, 32 F to 149 F (0 C to 65 C) at the card edge.
hw
3.2.3.1.3.1
Temperature
The NE shall (3.2.3.1.3.1.2) operate with a worst case card edge thermal interface temperature of +65 °C for greater than 10 hours.
hw
3.2.3.1.3.1
Temperature
The storage (i.e., non-operating) temperature range for the flight NE shall (3.2.3.1.3.1.3) be from -30 °C to 60 °C.
hw
3.2.3.1.3.1
Temperature
For qualification testing, the flight NE shall (3.2.3.1.3.1.4) meet the following temperature requirement while operating, 12 F to 152 F (-11 C to 66.7 C) at the card edge.
hw
3.2.3.1.3.2
Vibration
The flight NE shall (3.2.3.1.3.2.1) be capable of complying with all of the performance specified herein while not operating during all specified levels.
hw
3.2.3.1.3.2.1
Random Vibration
The flight NE shall (3.2.3.1.3.2.1.1) be capable of withstanding the following environment in non-operational mode: Frequency, Hz Qualification Level g2/Hz 20 0.026 20-50 +3 dB/Octave 50-800 0.16 800-2000 -3 dB/Octave 2000 0.026
hw
3.2.3.1.3.2.1
Random Vibration
For qualification testing, the sweep time per axis shall (3.2.3.1.3.2.1.2) be 3 minutes, 14.1 g-rms overall.
hw
3.2.3.1.3.2.1
Random Vibration
The flight NE shall (3.2.3.1.3.2.1.3) be non operating during the application of this vibration in all axes.
hw
3.2.3.1.3.3
Ionization Radiation
The flight NE shall (3.2.3.1.3.3.1) be designed to be capable of complying with all the performance requirements specified herein while being subjected to the total dose, single event upset and latchup immune requirements in SSP 30512 Rev. C.
hw
3.2.3.1.3.3
Ionization Radiation
All radiation test results shall (3.2.3.1.3.3.7) be characterized and documented.
hw
3.2.3.1.3.4
Shock (Non-operating)
The flight NE shall (3.2.3.1.3.4.1) be designed to be capable of complying with all the performance requirements specified herein after being subjected to a total of six impact shocks, consisting of six shocks (one in each opposite direction) along each of three orthogonal axes.
hw
3.2.3.1.3.4
Shock (Non-operating)
The waveform and amplitude of the shock pulses shall (3.2.3.1.3.4.2) be sawtooth shock pulse 20g peak, 11 milliseconds nominal duration.
hw
3.2.3.1.3.5
Humidity
The flight NE shall (3.2.3.1.3.5.1) be designed to comply with all of the performance requirements specified herein while withstanding the effects of up to 90% relative humidity, non condensing while operating.
hw
3.2.3.1.3.6
Pressure
The flight NE shall (3.2.3.1.3.6.1) be designed to be capable of complying with all the performance requirements specified herein while non-operating in an atmosphere of 8 to 18 Psia.
hw
3.2.3.1.3.8
Electromagnetic Radiation
The flight NE shall (3.2.3.1.3.8.1) be designed to be electromagnetically compatible with the Radstone Power PC 604R
hw
3.2.3.1.3.10.1
MTBF
The design, manufacturing, and radiation environment composite failure rate/Mean Time Between Failures (MTBFs) of the flight NE shall (3.2.3.1.3.10.1.1) be predicted using techniques in MIL-HDBK 217 or other commonly accepted procedures.
hw
3.2.3.1.3.10.2
Operational Service Life
The useful operating service life shall (3.2.3.1.3.10.2.1) be a minimum of 30,000 hours.
hw
3.2.3.1.3.10.2
Operational Service Life
The useful operating life shall (3.2.3.1.3.10.2.2) be determined by analysis and presented at the critical design review.
hw
3.2.3.1.3.10.3
Storage Life
The flight NE storage life shall (3.2.3.1.3.10.3.1) be 5 years or better.
hw
3.2.3.1.3.12.1
Temperature Range
For acceptance testing, the flight NE shall (3.2.3.1.3.12.1.3) meet the following temperature requirement while operating, 32 F to 132 F (0 C to 55.6 C) at the card edge.
hw
3.2.3.1.3.12.2
Random Vibration Requirements
The ESS random vibration Power Spectral Density for the flight NE shall (3.2.3.1.3.12.2.1) be as follows: Total 10.8 grms …[ Frequency, Hz Level g2/Hz 20 0.015 20-50 +3 dB/Octave 50-800 0.09 800-2000 -3 dB/Octave 2000 0.015
hw
3.2.3.2
Operational Characteristics
The X-38 NE shall (3.2.3.2.1) be able to communicate with 4 other NEs.
hw
3.2.3.2
Operational Characteristics
The NE shall (3.2.3.2.2) support at least two physical processors per FCR.
hw
3.2.3.2
Operational Characteristics
The NE shall (3.2.3.2.3) support at least 6 virtual groups.
hw
3.2.3.2
Operational Characteristics
The NE shall (3.2.3.2.5) support class 1 and class 2 bandwidth of at least 1 Mbyte/sec.
hw
3.2.3.2
Operational Characteristics
The skew between NEs, measured at delivery of messages to dual-port RAM accessible by the processors via the VME bus, shall (3.2.3.2.6) be no more than 100 nsecs.
hw
3.2.3.2
Operational Characteristics
The NEs shall (3.2.3.2.7) be able to achieve phase-locked synchronization of the fault-tolerant clocks in less than 5 milliseconds from the time the last FCC powered up and exited the reset state
hw
3.2.4
Miscellaneous NE Requirements
The contractor shall (3.2.4.1) maintain a product identification and tracking system.
NA
3.2.4
Miscellaneous NE Requirements
Each NE and flight cable assembly shall (3.2.4.2) be identified by a part or type number and a unique serial number, consistent with the configuration management system and the specification for the contract.
NA
3.2.5
Network Element Fifth Unit (NEFU) Requirements
The presence, or absence of, an NEFU ICP shall (3.2.5.2) not impact the NE firmware (i.e., the NE firmware will not be different).
hw
3.3.1
Programming Language and Operating System [2]
Fault Tolerant System Services (FTSS) software shall (3.3.1.1) use VxWorks Version 5.4 as the Operating System.
SRS160
3.3.1
Programming Language and Operating System [2]
The software shall (3.3.1.2) be written in the C programming language, with the exception of the system loader software which may be written in scripts, and operate on a PowerPC 604R.
SRS158, SRS159
3.3.1
Programming Language and Operating System [2]
The FTSS software and the VxWorks operating system, together, shall (3.3.1.3) take up no more than 3 Megabytes of ROM, when loaded into FCP or ICP memory.
SRS193
3.3.1
Programming Language and Operating System [2]
The FTSS software and the VxWorks operating system shall (3.3.1.4) utilize no more than 9 Megabytes of DRAM code and data space.
SRS258
3.3.1
Programming Language and Operating System [2]
Of the 9 Megabytes of DRAM allocation, only 4 Megabytes of FTSS/VxWork’s DRAM shall (3.3.1.5) be re-aligned during any re-alignment attempts.
SRS259
3.3.2
Start Up
Upon CPU reset caused by power on, watchdog timer or by other means, Start Up shall (3.3.2.1) execute the initial BIT (IBIT).
SRS237
3.3.2
Start Up
After successfully completing IBIT, the software shall (3.3.2.3) continue with the initialization of VxWorks and FTSS software.
SRS234
3.3.2
Start Up
If MPCC IBIT failed, the FTSS SW shall (3.3.2.24) switch to using the redundant MPCC card in that C&T FCR.
SRS299
3.3.2
Start Up
If the 5th ICP fails, the FTSS SW shall (3.3.2.25) ignore the error and allow the NE to continue the synch process and become part of the voting group, if possible.
SRS243
3.3.2
Start Up
On each FCP, the FTPP system shall (3.3.2.26) configure the Radstone firmware to perform the IBIT tests shown in Table 3.3.2.1, FCP IBIT Table.
SRS260
3.3.2
Start Up
The FTPP system shall (3.3.2.27) configure the Radstone processor to halt processing if any of the MPE tests, mentioned in Table 3.3.2.1, FCP IBIT Table, fail.
SRS261
3.3.2
Start Up
The FTPP system shall (3.3.2.28) configure the Radstone processor to continue processing if any of the Power-up tests or Initial BIT tests mentioned in Table 3.3.2.1, FCP IBIT Table, fail.
SRS262
3.3.2
Start Up
In all FCP IBIT cases, provided the hardware state permits, the FTSS shall (3.3.2.29) log the error and report it in the X-38 telemetry stream.
SRS239
3.3.2
Start Up
Upon completion of logging a Power-up test or Initial BIT test failure, the FTSS system shall (3.3.2.43) consider the FCP failed and attempt recovery actions as stated in requirement 3.3.5.29.
SRS290
3.3.2
Start Up
On each ICP, the FTPP system shall (3.3.2.30) configure the Radstone firmware to perform the IBIT tests shown in Table 3.3.2.2, ICP IBIT Table.
SRS287
3.3.2
Start Up
The FTPP system shall (3.3.2.31) configure the Radstone processor to halt processing if any of the MPE tests, mentioned in Table 3.3.2.2, ICP IBIT Table, fail.
SRS288
3.3.2
Start Up
The FTPP system shall (3.3.2.32) configure the Radstone processor to continue processing if any of the Power-up tests or Initial BIT tests mentioned in Table 3.3.2.2, ICP IBIT Table, fail.
SRS289
3.3.2
Start Up
In all ICP IBIT cases, provided the hardware state permits, the FTSS shall (3.3.2.33) log the error and report it in the X-38 telemetry stream.
SRS239
3.3.2
Start Up
Upon completion of logging a Power-up test or Initial BIT test failure, the FTSS system shall (3.3.2.44) consider the ICP failed and attempt recovery actions as stated in requirement 3.3.5.29.
SRS290
3.3.2
Start Up
On each ICP/PMC1553, the FTPP system shall (3.3.2.34) configure the Radstone firmware to perform the IBIT tests shown in Table 3.3.2.3, ICP/PMC1553 IBIT Table.
SRS264
3.3.2
Start Up
The FTPP system shall (3.3.2.35) configure the Radstone ICP/PMC1553 card to halt processing if any of the MPE tests, mentioned in Table 3.3.2.3, ICP/PMC1553 IBIT Table, fail.
SRS265
3.3.2
Start Up
The FTPP system shall (3.3.2.36) configure the Radstone ICP/PMC1553 card to continue processing if any of the Initial BIT tests mentioned in Table 3.3.2.3, ICP/PMC1553 IBIT Table, fail.
SRS266
3.3.2
Start Up
In all ICP/PMC1553 IBIT cases, provided the hardware state permits, the FTSS shall (3.3.2.37) log the error and report it in the X-38 telemetry stream.
SRS239
3.3.2
Start Up
On each MPCC, the FTPP system shall (3.3.2.38) configure the Radstone firmware to perform the IBIT tests shown in Table 3.3.2.4, MPCC IBIT Table.
SRS267
3.3.2
Start Up
In all MPCC IBIT cases, provided the hardware state permits, the FTSS shall (3.3.2.40) log the error and report it in the X-38 telemetry stream.
SRS239
3.3.2
Start Up
If IBIT fails, the FTSS SW shall (3.3.2.41) handle the failure as stated in the preceding IBIT requirements and in requirement 3.3.5.29’s table, FTPP Failure Response/Recovery Mechanisms.
SRS269
3.3.2
Start Up
However, the FTSS SW shall (3.3.2.42) notify the application software if the 5th ICP’s heartbeat ceases to exist.
SRS098
3.3.2
Start Up
The surviving triplex shall (3.3.2.5) attempt to sync with the failed FCP.
SRS177
3.3.2
Start Up
If the failed FCP has not synced in 2.5 seconds, after the surviving triplex has detected the loss of the FCP, then the surviving triplex shall (3.3.2.6) send a voted VMEbus reset through the NE to the failed FCP.
SRS178
3.3.2
Start Up
Start Up shall (3.3.2.12) synchronize its FCP with other operational FCPs.
SRS008
3.3.2
Start Up
Start Up shall (3.3.2.13) make their state congruent.
SRS011
3.3.2
Start Up
The FCP state shall (3.3.2.14) include all volatile memory, read/write memory, registers, timers, and counters, except that part of the memory exclusively set aside for channel-unique information.
SRS011
3.3.2
Start Up
It shall (3.3.2.17) support normal synchronization following power on or reset.
SRS194
3.3.2
Start Up
Start Up shall (3.3.2.18) be able to synchronize all operational FCPs in the presence of this skew in the power on sequence.
SRS008
3.3.2
Start Up
Start Up shall (3.3.2.19) test to ensure that all four FCPs are synchronized.
SRS008, SRS010
3.3.2
Start Up
Unsynchronized processors shall (3.3.2.20) be excluded from the FCP configuration.
SRS010, SRS296
3.3.2
Start Up
During start up the FCP watchdog timer shall (3.3.2.45) be active.
SRS014, SRS292
3.3.2
Start Up
System Initialization shall (3.3.2.21) initiate execution of FTSS and X-38 application code.
SRS199
3.3.3
Vehicle/Mission Manager
The Mission Manager Template shall (3.3.3.1) provide a mechanism for (but not limited to) creating and controlling task execution, creating message queues and other interprocessor communication mechanisms, and provide on/off capability for processor resynchronization.
SRS215, SRS302
3.3.4
Scheduler
The Scheduler shall (3.3.4.1) support three rate groups: 50 Hz (minor frame), 10 Hz (medium frame), and 1 Hz (major frame).
SRS197, SRS195, SRS035
3.3.4
Scheduler
The FTSS software shall (3.3.4.18) take at most 1 msec of a 50 Hz minor frame.
SRS024, SRS034
3.3.4
Scheduler
The Scheduler shall (3.3.4.3) set the timer to a count down value so as to cause the next minor frame interrupt at 20 msec (+/- 330 usecs) from the previous interrupt congruently in all operational FCPs.
SRS035, SRS181
3.3.4
Scheduler
The FTSS software shall (3.3.4.19) provide an API call which provides the application program the minor frame number.
SRS278
3.3.4
Scheduler
Process scheduling shall (3.3.4.4) only be performed at certain controlled locations (synchronization points).
SRS022
3.3.4
Scheduler
The Scheduler shall (3.3.4.5) place processing time bounds on all rate groups to ensure that no rate group monopolizes the FCC's processor.
SRS028
3.3.4
Scheduler
It shall (3.3.4.6) be possible to reassign a task to a different rate group as a function of the mission mode.
SRS017, SRS018, SRS195, SRS196, SRS197, SRS198
3.3.4
Scheduler
Tasks within a rate group shall (3.3.4.7) be executed in the order in which the mission manager registers the tasks.
SRS022, SRS039, SRS037, SRS198
3.3.4
Scheduler
It shall (3.3.4.8) be possible to alter the execution sequence of tasks within a rate group as a function of mission mode.
SRS002, SRS017, SRS196, SRS018, SRS019, SRS020, SRS021, SRS197, SRS195, SRS198
3.3.4
Scheduler
Higher iteration tasks shall (3.3.4.9) have higher priority over lower iteration tasks.
SRS027
3.3.4
Scheduler
The Scheduler shall (3.3.4.12) detect 50 Hz, 10 Hz, and 1 Hz frame overruns at the next frame following the end of their respective rate boundaries.
SRS028
3.3.4
Scheduler
The Scheduler shall (3.3.4.13) attempt recovery from a frame overrun according to the following policy:
SRS030
3.3.4
Scheduler
if the scheduler determines that a task did not finish within its specified rate boundary, the scheduler shall (3.3.4.14) signal that a task overrun occurred.
SRS030
3.3.4
Scheduler
When the task restart begins, the FTSS shall (3.3.4.15) provide a mechanism to signal the task to execute its startup recovery actions, including updating the I-Load data and pre-stored last good data state.
SRS030
3.3.4
Scheduler
Following a task overrun, the scheduler shall (3.3.4.17) provide an application programmer's interface call which specifies which task was running within the rate group which has overrun.
SRS216
3.3.4
Scheduler
The FTSS software shall (3.3.4.20) provide a task deadline capability which allows an application to specify which minor frame that an application should start in and finish in.
SRS270
3.3.4
Scheduler
The Scheduler in the FTPP shall (3.3.4.16) keep all redundant copies of a process, which are executing in different computers, in synchronization.
SRS181
3.3.5
Fault Detection, Identification, and Recovery
The scope of FDIR shall (3.3.5.1) be limited to the hardware on the four FCP boards, the four MPCC/CTC boards, the five ICPs, and the five NEs.
SRS095, SRS096, SRS184, SRS235, SRS298, SRS299, SRS300, SRS304
3.3.5
Fault Detection, Identification, and Recovery
FDIR shall (3.3.5.2) receive this information and, after two consecutive missed “heartbeats,” conclude that the ICP is failed.
SRS097
3.3.5
Fault Detection, Identification, and Recovery
FDIR shall (3.3.5.3) report the total FCC status to the Vehicle/Mission Manager when requested to do so by the Vehicle/Mission Manager.
SRS098, SRS099
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.4) execute CBIT during all operational phases.
SRS095
3.3.5
Fault Detection, Identification, and Recovery
The CBIT shall (3.3.5.5) be executed at a 50 Hz rate, after all 50 Hz flight critical operations are complete.
SRS093, SRS095, SRS034
3.3.5
Fault Detection, Identification, and Recovery
The CBIT, at a minimum, shall (3.3.5.6) include a "presence test" to ascertain that all FCP processors are synchronized and are at the same relative point in time in the current minor frame.
SRS093, SRS095, SRS184
3.3.5
Fault Detection, Identification, and Recovery
The presence test shall (3.3.5.7) also ascertain that all processors are executing the same 50 Hz, 10 Hz, and 1 Hz frames.
SRS184
3.3.5
Fault Detection, Identification, and Recovery
The CBIT shall (3.3.5.8) also arm and reset the hardware watchdog timer.
SRS014, SRS094
3.3.5
Fault Detection, Identification, and Recovery
The CBIT shall (3.3.5.10) be executed without interfering with the normal execution of the application tasks.
SRS034
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.11) not take more than 2 msec per minor frame under nominal no-fault conditions.
SRS091
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.12) not take more than 3 msec per minor frame while processing faults.
SRS183
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.13) be able to discriminate between permanent and non-permanent faults.
SRS106, SRS110, SRS117, SRS204, SRS208, SRS209, SRS211, SRS282, SRS298
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.14) reset and retry the failed entity, such as an FCP or an NE, to perform this discrimination.
SRS106, SRS110, SRS117, SRS129 SRS204, SRS208, SRS209, SRS211, SRS282
3.3.5
Fault Detection, Identification, and Recovery
To clear the failure, FDIR shall (3.3.5.15) request the Vehicle/Mission Manager to cycle power to that FCR.
SRS208, SRS209
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.16) be able to identify a fault source, at least to an FCR.
SRS095, SRS184, SRS096, SRS097
3.3.5
Fault Detection, Identification, and Recovery
The FDIR shall (3.3.5.17) place all fault and recovery information in shared memory for inclusion in the frames that will be telemetred and recorded by the CTC.
SRS098, SRS044
3.3.5
Fault Detection, Identification, and Recovery
For the first permanent FCP failure, FDIR shall (3.3.5.30) degrade the redundancy level of the FCP from 4 to 3.
SRS106
3.3.5
Fault Detection, Identification, and Recovery
If a second permanent FCP failure occurs, then FDIR shall (3.3.5.31) degrade the redundancy level of the FCP from 3 to 2 and operate in a degraded triplex mode.
SRS282
3.3.5
Fault Detection, Identification, and Recovery
Additionally, FDIR shall (3.3.5.20) reinitialize and integrate an FCP if permitted by the Vehicle/Mission Manager.
SRS104, SRS110, SRS123, SRS124, SRS125, SRS126, SRS281, SRS302
3.3.5
Fault Detection, Identification, and Recovery
FTSS shall (3.3.5.35) notify the applications that memory re-alignment and re-integration of an FCP is going to occur in 1 second.
SRS271
3.3.5
Fault Detection, Identification, and Recovery
FTSS shall (3.3.5.36) wait for the ICP to signal that it has completed initialization before suspending the application for memory re-alignment.
SRS272
3.3.5
Fault Detection, Identification, and Recovery
The FCP watchdog timer shall (3.3.5.38) remain active during memory re-alignment.
SRS293, SRS294
3.3.5
Fault Detection, Identification, and Recovery
Reintegration of an FCP shall (3.3.5.21) be completed in at most 1.5 minutes.
SRS214
3.3.5
Fault Detection, Identification, and Recovery
It shall (3.3.5.22) be possible to perform voted VMEbus resets via the NEs.
SRS204
3.3.5
Fault Detection, Identification, and Recovery
For a permanent NE failure, FDIR shall (3.3.5.23) mask the failed NE.
SRS104, SRS245
3.3.5
Fault Detection, Identification, and Recovery
For a transient NE failure, FDIR shall (3.3.5.24) mask the failed NE.
SRS104, SRS106, SRS245, SRS282
3.3.5
Fault Detection, Identification, and Recovery
Additionally, FDIR shall (3.3.5.25) reinitialize and integrate the NE.
SRS104
3.3.5
Fault Detection, Identification, and Recovery
Intentional powering down of an FCP, ICP, or NE shall (3.3.5.32) not be classified as a fault.
SRS285, SRS274, SRS128
3.3.5
Fault Detection, Identification, and Recovery
FTSS shall (3.3.5.34) provide an API call which allows the application to notify FTSS that an FCP, ICP, or NE is intentionally being powered down.
SRS274
3.3.5
Fault Detection, Identification, and Recovery
FTSS shall (3.3.5.37) provide an API call which allows the application to take an FCR out of the permanently failed state and place it back in the initial recovery state.
SRS285
3.3.5
Fault Detection, Identification, and Recovery
A failed FCP or NE shall (3.3.5.27) be masked within three minor frames of fault detection and isolation.
SRS109
3.3.5
Fault Detection, Identification, and Recovery
The FTSS FDIR shall (3.3.5.28) exchange the status information of detected faults in the FCP, ICP, NE, and MPCC/CTC hardware with the NASA provided software.
SRS044, SRS098
3.3.5
Fault Detection, Identification, and Recovery
The FTPP system shall (3.3.5.29) perform the "FTPP Failure Response/Recovery Mechanisms"as listed in the following matrix and notes of interest.
SRS100, SRS104, SRS242, SRS222, SRS208, SRS209, SRS211, SRS245, SRS283, SRS284, SRS298, SRS299, SRS300, SRS304
3.3.6
Communications
Synchronous communication shall (3.3.6.1) be in the form of messages enqueued for transmission at the start of the next rate group frame and dequeued for reading by the recipient task within the next rate group frame after it is received.
SRS047, SRS052, SRS063, SRS064
3.3.6
Communications
A transmit packet queue and a receive packet queue shall (3.3.6.7) be maintained for each task or Communication ID (CID).
SRS053, SRS054, SRS055, SRS059, SRS062, SRS066
3.3.6
Communications
Access to the transmit queues shall (3.3.6.8) be controlled within the communication service primitives .
SRS062, SRS066
3.3.6
Communications
Message passing communications primitives shall (3.3.6.9) be provided for task-to-task communication as well as for broadcast to all processors.
SRS047, SRS048, SRS049, SRS051 SRS052, SRS062, SRS069
3.3.6
Communications
Broadcast primitives shall (3.3.6.10) not be available on ICPs.
SRS064, SRS070
3.3.6
Communications
For the highest rate group tasks (i.e., tasks that can not be preempted), Immediate Message Services shall (3.3.6.11) also be provided.
SRS048, SRS050, SRS067, SRS068, SRS069, SRS070, SRS073
3.3.6
Communications
A version of the Immediate Message Services shall (3.3.6.12) be provided to the ICPs that allows Class 2 writes to NEs and Class 1 reads from NEs.
SRS226, SRS227, SRS228, SRS229, SRS230, SRS303
3.3.6
Communications
Communications services shall (3.3.6.13) provide a version of Immediate Message Services between rate groups within the FCP that bypasses the NE and that can be used to control and monitor inter-rate group communications.
SRS051
3.3.6
Communications
Communication services shall (3.3.6.14) provide the capability for a “helper” task to be created to run in the 50 Hz rate group, but running in specific minor cycles (every 5th or every 50th) to provide data from the ICP to the lower rate tasks.
SRS042
3.3.7
System Loader
The procedures used to build the executable FTSS software using a cross-compiler and linker, down-load the image to the target processors, and burn the load image into the Radstone PowerPC flash RAM shall (3.3.7.1) be documented in the release notes that accompany Engineering Releases of the FTSS software and in the Software Users Manual.
NA
3.3.7
System Loader
Any makefiles or other automated scripts that support the build, down-load, and flash programming processes shall (3.3.7.2) be delivered with the software to NASA.
NA
3.3.8
Memory Management
For each mission mode, the congruent and non-congruent memory boundaries shall (3.3.8.1) be known and fixed.
SRS217
3.3.8
Memory Management
The Memory Management software shall (3.3.8.2) periodically "scrub" volatile and read/write memory in the FCP.
SRS043
3.3.8
Memory Management
It shall (3.3.8.3) not be necessary to scrub memory that is not used by the flight software.
SRS043
3.3.8
Memory Management
It shall (3.3.8.16) not be necessary to scrub that area used to store telemetry data.
SRS275
3.3.8
Memory Management
Memory scrubbing shall (3.3.8.5) be executed without interfering with normal execution of applications tasks.
SRS187
3.3.8
Memory Management
The memory scrubbing software shall (3.3.8.6) be capable of scrubbing 10 Megabytes in 8 minutes.
SRS187
3.3.8
Memory Management
The RAM scrub software shall (3.3.8.15) at most use 1% of an FCP CPU duty cycle.
SRS187
3.3.8
Memory Management
Even though memory scrubbing is performed locally and the errors would not be congruent, the recording of errors shall (3.3.8.10) be congruent.
SRS044
3.3.8
Memory Management
To support reintegrating a desynchronized channel, as specified in the FDIR requirements, the Memory Management software shall (3.3.8.11) "re-align" all of the volatile and read/write congruent memory, registers, timers and other locations that fit the description of "volatile and read/write congruent locations".
SRS045, SRS126, SRS186, SRS200
3.3.8
Memory Management
The re-align function shall (3.3.8.12) write the voted value from the good channels into the target channel.
SRS186, SRS281
3.3.8
Memory Management
The re-align function shall (3.3.8.13) be allowed only when permitted by the Vehicle/Mission Manager.
SRS110, SRS117, SRS125, SRS302
3.3.8
Memory Management
Memory Management software shall (3.3.8.14) include (but not be limited to) memory scrubbing and memory realignment.
SRS043, SRS044, SRS046, SRS217, SRS045, SRS186, SRS200, SRS203, SRS187
3.3.9
Memory Protection
Memory shall (3.3.9.1) be categorized into congruent (identical data) and non-congruent (data that is not identical) memory.
SRS046
3.3.10
Time Management
Time Management shall (3.3.10.4) provide MET.
SRS142
3.3.10
Time Management
The MET shall (3.3.10.5) be initialized to zero at the first 50 Hz frame.
SRS165
3.3.10
Time Management
The MET shall (3.3.10.6) measure real-time from this event with an accuracy of at most 50 Parts Per Million (PPM).
SRS218
3.3.10
Time Management
The MET shall (3.3.10.7) have a resolution of 20 msec. for 50 Hz tasks, 100 msec for 10 Hz tasks, and 1 second for 1 Hz tasks.
SRS142
3.3.10
Time Management
The MET shall (3.3.10.8) be able to increment to at least 30 days without rolling over.
SRS144
3.3.10
Time Management
The MET shall (3.3.10.9) be congruent across all FCP members.
SRS142
3.3.10
Time Management
Following a processor recovery, during which time is frozen, the FTSS software shall (3.3.10.10) account for the frozen time and update MET to its proper value.
SRS218
3.3.10
Time Management
Time Management shall (3.3.10.11) provide SEP.
SRS142
3.3.10
Time Management
Time Management shall (3.3.10.12) initialize SEP to zero within one minor cycle of the time when the vehicle/mission manager software has notified the FTSS software that the X-38 vehicle is released from the Space Shuttle Remote Manipulator System.
SRS161
3.3.10
Time Management
The SEP shall (3.3.10.13) measure real-time from this event with an accuracy of at most 50 Parts Per Million (PPM).
SRS219
3.3.10
Time Management
The SEP shall (3.3.10.14) have a resolution of 20 msec. for 50 Hz tasks, 100 msec for 10 Hz tasks, and 1 second for 1 Hz tasks.
SRS142
3.3.10
Time Management
The SEP shall (3.3.10.15) be able to increment to at least 1 day without rolling over.
SRS145
3.3.10
Time Management
The SEP shall (3.3.10.16) be congruent across all FCP members.
SRS142
3.3.10
Time Management
Following a processor recovery, during which time is frozen, the FTSS software shall (3.3.10.17) account for the frozen time and update SEP to its proper value.
SRS219
3.3.10
Time Management
If the SEP API call is made prior to actual separation, the call shall (3.3.10.27) return zero (0).
SRS161
3.3.10
Time Management
The Time Services, if dealing with the year designation, shall (3.3.10.21) be Year 2000-compliant.
No year designation used in any requirement
3.3.10
Time Management
Time Management shall (3.3.10.23) provide a utility timer.
SRS246, SRS248
3.3.10
Time Management
The utility timer shall (3.3.10.24) be available via an FTSS API call(s).
SRS246
3.3.10
Time Management
The utility timer shall (3.3.10.25) have a resolution of 60.6 nanoseconds.
SRS256
3.3.10
Time Management
The utility timer shall (3.3.10.26) have an accuracy of at most 50 PPM.
SRS247
3.3.11
Input/Output Services
Load modules of the four FCPs shall (3.3.11.1) be identical.
SRS166
3.3.11
Input/Output Services
Control flow of the four FCPs shall (3.3.11.2) be similar, if not identical.
SRS008, SRS011, SRS181, SRS191, SRS053, SRS054, SRS095, SRS184, SRS123, SRS125, SRS126, SRS045, SRS186, SRS200, SRS166, SRS168
3.3.11
Input/Output Services
Asymmetric I/O calls shall (3.3.11.3) not be allowed to induce a large enough skew to force the FCPs to desynchronize.
SRS168
3.3.11
Input/Output Services
A subset of FTSS shall (3.3.11.7) reside on the ICP.
SRS225, SRS226, SRS227, SRS228, SRS229, SRS230
3.3.11
Input/Output Services
FTSS shall (3.3.11.8) provide an API call which allows the application to specify which MPCC channels in a C&T FCR should be used for telemetry and/or command reception.
SRS286
3.3.12
Exception Handling
Upon occurrence of an exception, the FTPP system shall (3.3.12.1) log the error and include all context data relevant to the exception e.g. the contents of the Machine State Register (MSR) and the machine status Save/Restore Registers (SRR0 & SRR1).
SRS172
3.3.12
Exception Handling
The error type and its context data shall (3.3.12.4) be made available to the application via an API call.
SRS172
3.3.12
Exception Handling
For software exceptions, the FTPP system shall (3.3.12.2) then transfer control to a user specified exception handling routine, if one is provided.
SRS031
3.3.12
Exception Handling
For hardware exceptions, the FTPP system shall (3.3.12.5) “handle” the exception by making the error and its context data available to the application and then returning from the exception handler.
SRS276
3.3.12
Exception Handling
For reserved exceptions, the FTPP system shall (3.3.12.6) “handle” the exception by making the error and its context data available to the application and then returning from the exception handler.
SRS276
3.3.12
Exception Handling
Finally, for software exceptions only, the FTPP system shall (3.3.12.3) then “jump back” to the initialization point for the offending task.
SRS173
3.3.12
Exception Handling
If the exception occurs within the FTSS software, the FTPP system shall (3.3.12.7) “jump” back to the beginning of the task, skip all initialization code, and begin processing the task’s code again.
SRS277, SRS301
3.3.13
Application Interface
An application programming interface shall (3.3.13.3) be documented in a FTSS API document.
SRS164
3.3.14
NEFU
The presence, or absence of, an NEFU ICP shall (3.3.14.1) not impact the FTSS software (i.e., the FTSS ICP load will not be different).
SRS220
3.3.15
Power Down
FTSS services shall (3.3.15) provide an API call which provides the capability to close and delete all communication mechanisms delete all rate groups, and suspend and delete all tasks.
SRS249
3.4.1.1
FCP-ICP Communication Architecture
The FCP-ICP communications shall (3.4.1.1.1) provide the following capabilities (these are written from the viewpoint of the FCP): 1. Signal the start of the 50 Hz rate group in the ICP. 2. Synchronize frames across the four ICPs. 3. Receive congruent sensor data from ICPs. 4. Send voted actuator and other output device commands to ICPs. 5. Receive health and status of the ICPs and all the FCC hardware for which the ICPs are responsible. 6. Provide the ICPs with current minor frame number, X-38 flight phase/segment number, vehicle mode number, MET, and SEP. 7. Provide the ICPs with notification of FCP memory alignment two minor frames prior to the start of the alignment.
SRS025, SRS032, SRS033, SRS048, SRS097, SRS231, SRS232, SRS233, SRS295
3.4.1.2
FCP-ICP Communication Requirements
As part of start-up or after recovering from a transient fault: after completing IBIT, the FCP shall (3.4.1.2.1) wait 15 seconds for the ICP to initialize all of its non-Radstone VME slave boards and its NE interface
SRS297
3.4.1.2
FCP-ICP Communication Requirements
then the FCP VG shall (3.4.1.2.2) send the FCP VG Ready Signal to the ICPs to indicate that the FCP VG is ready to begin FCP-ICP communications.
SRS221
3.4.1.2
FCP-ICP Communication Requirements
To permit these task and pipe initializations in the ICPs, the FCP VG shall (3.4.1.2.8) wait at least 2.5 seconds for the ICP Ready Signals after the FCP VG has been notified that the ICPs received the FCP VG Ready Signals.
SRS189
3.4.1.2
FCP-ICP Communication Requirements
The FCP shall (3.4.1.2.5) signal the start of each minor frame in all ICPs by means of a VMEbus IRQ5 interrupt.
SRS032
3.4.1.2
FCP-ICP Communication Requirements
The interrupts across all channels shall (3.4.1.2.6) have a skew no greater than 330 microseconds.
SRS191
3.4.1.2
FCP-ICP Communication Requirements
Each interrupt shall (3.4.1.2.7) be preceded by the FCP writing the information listed in 3.4.1.1.1-6 to a shared memory block over the VME backplane bus to its counterpart ICP.
SRS033
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.2) provide to the telemetry program the FTPP telemetry data which consists of the following elements: a. FCP status, b. NE status, c. # Transient Errors, d. Transient recovery attempts, e. Frame overruns, f. ICP status.
SRS029, SRS044, SRS098
3.4.2
FCP-CTC Communications
The data mentioned in requirement 3.4.2.2 and any other Draper-provided telemetry data shall (3.4.2.9) fit within Draper’s allocated telemetry budget of 5000 bits/sec.
SRS250
3.4.2
FCP-CTC Communications
In addition, the FTSS software shall (3.4.2.11) provide up to 600 bits of start-up data that indicates the state of the FTPP system during start-up.
SRS280
3.4.2
FCP-CTC Communications
Once every medium frame, the FTSS software shall (3.4.2.3) accept a pointer from the telemetry program to the buffer space containing the telemetry data.
SRS148, SRS151
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.4) move this buffer to the MPCC/CTC over the VMEbus.
SRS149, SRS150
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.10) use no more than 5.2 milliseconds of FCP processing time to move the telemetry data to the MPCC/CTC board and complete communication and error handling for the MPCC/CTC board.
SRS257
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.5) receive telemetry commands from both CTCs via the MPCC/CTC once every medium frame.
SRS152
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.6) congruently decide which FCP channel should be the source of CTC data.
SRS222
3.4.2
FCP-CTC Communications
This decision shall (3.4.2.7) be made based on the health and status of all the physical links from the FCP to the CTC.
SRS222
3.4.2
FCP-CTC Communications
The FTSS software shall (3.4.2.8) deliver to the requisite NASA application program commands received from both CTCs.
SRS153, SRS156
3.5
Miscellaneous Other Requirements
Draper shall (3.5.5) not violate the 100 microseconds requirement.
SRS223
3.5
Miscellaneous Other Requirements
Draper shall (3.5.6) deliver FTSS engineering release version 5/6, and any subsequent versions of the FTSS software, only after the release has been proven to work under Tornado 2 for the NT environment.
SRS253
3.5
Miscellaneous Other Requirements
Draper shall (3.5.7) deliver FTSS engineering release version 5/6, and any subsequent versions of the FTSS software, via CD-ROM.
SRS252

NOTES
List of Acronyms
Acronym
Definition
API
Application Programmer's Interface

BIT
Built-in-Test
BRVC
Byzantine Resilient Virtual Circuit
BSP
Board Support Package

CBIT
Continuous Built In Test
COTS
Commercial Off-The-Shelf
CSCI
Computer Software Configuration Item
CT
Configuration Table
CTC
Command and Telemetry Computer

DID
Data Item Description
DIO
Digital Input/Output

ECR
Engineering Change Request

FCC
Flight Critical Computer
FCP
Flight Critical Processor
FCR
Fault Containment Region
FDI
Fault Detection and Isolation
FMG
Fault Masking Group
FTC
Fault Tolerant Clock
FTPP
Fault Tolerant Parallel Processor
FTSS
Fault Tolerant System Services

IBIT
Initial Built In Test
ICP
Instrument Control Processor
ID
IDentifier
IRS
Interface Requirements Specification
ISR
Interrupt Service Routine
ISYNC
Initial Synchronization

MET
Mission Elapsed Time
MPCC
Multi-Protocol Communications Controller
MPE
Minimum Processing Environment

NASA
National Aeronautics and Space Administration
NE
Network Element

PPC
Power PC
PPM
Parts Per Million

RAM
Random Access Memory
ROM
Read Only Memory
RM
Redundancy Management
RTC
Real Time Clock

SEP
SEParation elapsed time
SRS
Software Requirements Specification

TAEM
Terminal Area Energy Management
TNR
Transient Network Element Recovery

VG
Virtual Group
VME
Versa Module Eurocard

Glossary
Babbler – A processor or NE that continually unexpectedly sends messages over the fiber network, thus overloading the fiber network with unnecessary traffic.

Byzantine Faults – Faults consisting of arbitrary behavior on the part of failed components, and may include stopping and then restarting execution at a future time, sending conflicting information to different destinations, and in short, anything within a failed component’s power to attempt to corrupt the system. [1]

Byzantine Resilient Virtual Circuit (BRVC) – An abstracted view of the Network Elements and the fiber optic interconnection network. The NE hardware and fiber optic inter-connection network appear to the software a virtual message passing interface with certain guarantees about the order and consistency of message delivery in the face of arbitrarily malicious faults.

Debug mode – A mode of operating the network elements that allows software to control the operation of the network elements as well as to test their operation. This mode is used by the NE stand alone test software and is one of two modes that the NE can be configured to power up into. For X38, the flight NEs will not be configured to power up into this mode.

Degraded triplex – A fault containment region that has 2 processors, but at least 3 NEs. The FCR is configured to have a third processor that is masked out. The third processor could be “on” the NEFU (even thought there is no FCP software loaded on the processor card on that channel), in order to maintain the VG.

Exceptions.- External signals, errors, or unusual conditions arising in the execution of instructions. When exceptions occur, information about the state of the processor is saved to certain registers and the processor begins execution at an address (exception vector) predetermined for each exception.

Fault Containment Region (FCR) – A set of hardware that meets the following criteria: Electrical Isolation, Independent Power, Independent Clocking and, if necessary, physical separation. Errors internal to an FCR are contained within the FCR and errors outside the FCR do not adversely affect the operation of an FCR, i.e., external errors are prevented from inducing errors in the FCR. Among other characteristics, Byzantine resilience depends upon the concept of Fault Containment Regions. Throughout this document, the terms FCR and channel are used interchangeably.

Hardware Exceptions.- Any exception not mapped to a VxWorks signal.

Initial Synchronization (ISYNC) – The process (mode) by which the network elements initially achieve synchronization at power up.

Link – A one way, point to point connection between the transmitter in one Network Element (NE) and a receiver in another NE.

Lost soul sync – The process by which a lost (i.e., not in sync with the other members of its virtual group) processor is brought into synchronization with the other members of a redundant virtual group.

Masking –Preventing erroneous data from propagating beyond the voters (the act of voting masks any single error from propagating beyond the voters, i.e., the voters deliver a majority result in the presence of one fault.) Also, the setting of the voters to ignore input from a channel known (or suspected) of being faulty. Setting the voters to ignore (mask) the input from a channel know to be faulty is also referred to as reconfiguring the voters.

NE watchdog timer reset – A reset of the network element that arises as a result of the NE's on-board watchdog timer not being pulsed in a timely, periodic manner.

Permanent Failure – A failure is declared permanent when all attempts to reconfigure the channel and remove the failure by means of either a FTSS Response/Recovery Mechanism or a Application Failure Response/Recovery Mechanism have failed.

Power on reset – A reset of an entire channel that is the result of initially powering on the channel or cycling power to the channel.

Power-up skew – Power-on skew is defined here to be the time between switching on power to the first processor and power being applied to the fifth processor.

Re-integration – The process of bringing a "Lost Soul" processor back into synchronization with the other members of a redundant virtual group and then re-aligning its internal state including congruent memory, processor registers, and timers.

Scoreboard – That part of the network element that acts as the message scheduler. Among other things, the scoreboards in the redundant NEs, acting as a group, collectively decide when messages are ready to be sent.

Simplex – A non-redundant virtual group. When a single processor forms a virtual group, this is called a simplex virtual group. In the X-38 architecture, each ICP is a simplex virtual group. The FCPs form a single redundant virtual group (often called a quad).

Simultaneous Failure – A second fault is considered simultaneous if the fault occurs between the time the first fault is observed and when the system is reconfigured in response to the fault. The nature of this reconfiguration will vary depending upon the system’s configuration at the time of the fault and the effect(s) of the fault. Refer to FTSS SRS/IRS section 3.2.6.2 for reconfiguration details.

Software Exceptions.- Any exception mapped to a VxWorks signal.

Start-up – The period of time from when power is initially applied to the system or a reset is asserted to an individual channel until the 50 Hz interrupt is enabled. Activities occurring during this time include but are not limited to IBIT, ISYNC, TNR, processors synchronization, task create and initialization, definition and initialization of Communications Services sockets, etc.

Synchronization – The process of coordinating in time, multiple hardware and/or software entities. For redundant entities, this means bringing them to the same point within some allowable skew. For FCP-ICP communications and operation, this refers to the process of coordinating their activities in time both at start up and during steady-state operation using a variety of methodologies.

TNR mode – The mode that a network element enters when it finds itself alone and unable to synchronize with other NEs.

Transient Failure –Faults, such as those caused by SEUs, that can be recovered either by the FTSS Response/Recovery Mechanism or by the Application Failure Response/Recovery Mechanism.

Transient Network Element Recovery (TNR) – The process of recovering and bringing a lost network element into synchronization with the operating (working group) NEs and aligning or initializing its internal state so that it can resume synchronous operation with the other NEs.

Virtual group –Virtual processor capable of accepting work in a parallel processing environment. They are comprised of processor entities, each of which must be resident in a different fault containment region. [1] In the X-38 architecture, each ICP is a simplex virtual group. The FCPs form a single redundant virtual group (often called a quad).

VMEbus reset – A reset applied to the VMEbus.

Voted reset – A reset that is applied to an NE as the direct result of the FCP processors in the other channels agreeing to use and then actually using the voted reset function of the NEs to reset a faulty channel. An NE will assert a VMEbus reset and enter TNR directly (by-passing ISYNC) as a result of receiving a voted reset from the other NEs.

Working group TNR routine – The software commanded function that causes the NEs still in synch with one another to first look for and then synchronize with a lost NE.

297749 Rev F
