# 2000 - nasa x38 - 10 Hz Separation Elapsed Time 100 milliseconds, and

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2000 - nasa x38.doc

Section: 10 Hz Separation Elapsed Time 100 milliseconds, and

10 Hz Separation Elapsed Time 100 milliseconds, and
1 Hz Separation Elapsed Time 1 second.
The Mission Elapsed Time shall [SRS218] have a drift rate of at worst 50 PPM.
The Mission Elapsed Time shall [SRS144] not rollover for 30 days.
The Separation Elapsed Time shall [SRS145] not rollover for 1 day.
The Mission Elapsed Time shall [SRS165] be initialized to zero at the first 50 Hz frame.
The Separation Elapsed Time shall [SRS161] be initialized to zero at startup, and start counting up in the next frame after being notified via an API call that the X-38 vehicle has been released from the Space Shuttle Remote Manipulator System.
The Separation Elapsed Time shall [SRS219] have a drift rate of at worst 50 PPM.
Time Services shall [SRS246] provide a utility timer to the application. Note that this timer is not voted, and must be assigned to a variable defined using non-congruent memory.
The utility timer shall [SRS247] have an accuracy equal to or better than 50 PPM.
The utility timer shall [SRS256] have a resolution equal to or better than 60.6 nanoseconds.
The utility timer shall [SRS248] shall be set to zero prior to the first application task running in the first minor frame of each major frame.
System Support Services
CTC Requirements
If transmission status indicates an error in telemetry and/or remote commanding operations 10 consecutive times, the following actions shall [SRS298] be taken:
Support Services shall [SRS299] switch to the redundant MPCC device to continue telemetry and/or remote commanding operations. Note that there are only two CTCs. CTC1 is connected to FCC1 and FCC3. CTC2 is connected to FCC2 and FCC4.
Support Services shall [SRS242] continue to close and reopen a faulty MPCC device until status shows that the device has recovered.
In all error cases, Support Services shall [SRS222] attempt to choose an error-free FCC-MPCC path, switching back and forth between channels if necessary.
Support Services shall [SRS286] provide an API call which allows the application to specify which MPCC channels in a C&T FCR should be used for telemetry and/or command reception.
Telemetry Requirements
The Telemetry Logging capability provides tasks with the capability for transmission to a telemetry-capturing device.
The telemetry capability shall [SRS148] be capable of transferring 12,800 bytes within the 10 Hz frame from the FCP.
The telemetry capability shall [SRS149] transfer the telemetry block from the FCP to the FCC-MPCC connected to the CTC.
The telemetry capability shall [SRS150] signal the FCC-MPCC to transfer the telemetry block to the CTC.
The telemetry capability shall [SRS300] provide status data to FTSS FDI about each FCC-MPCC RS-422 link to the CTC.
Support Services shall [SRS151] provide an API call to specify the address and length of a telemetry buffer.
Support Services shall [SRS257] use no more than 5.2 milliseconds of FCP processing time to move the telemetry data to the FCC-MPCC board and complete communication and error handling for the FCC-MPCC board.
Command Read Requirements
The Command Read capability shall [SRS152] check for the presence of a command and status message from each CTC on each FCC-MPCC at 10hz.
The Command Read capability on each FCP shall [SRS153] read the command data received from each CTC via the FCC-MPCC.
FTSS shall [SRS304] provide status data to the application about each FCC-MPCC RS-422 link to the CTC used for command data.
Support Services shall [SRS156] provide an API call to provide the current command data.
Power Down Services
FTSS shall [SRS249] provide an API call which closes and deletes all rate groups, deletes all communication mechanisms (including any internal to FTSS), and then deletes all tasks.
CSCI External Interface Requirements
Interface Identification and Diagram
The external interfaces to the FTSS CSCI are as follows:
Application Programming Interface
Network Element
Radstone
VxWorks
Flight Critical Processor-Instrument Control Processor
Multi-Processor Communications Controller
These interfaces are shown in REF _Ref515943373 \h Figure 3‑4 and elaborated further in subsequent paragraphs.
EMBED Word.Picture.8
Figure STYLEREF 1 \s 3‑ SEQ Figure \* ARABIC \s 1 4 Fault Tolerant System Services CSCI External Interfaces.
IRIG-B/FTSS Interfaces
This section deleted.
API/FTSS Interfaces
The Application Programmer’s Interface (API) to Fault Tolerant System Services (FTSS) shall [SRS164] be as defined in the Application Programmer’s Interface, Draper Document #297752.
Network Element/FTSS Interfaces
The Network Element (NE) provides fault tolerant communications among multiple virtual groups. The virtual groups are computational sites composed of processors. These processors may be configured as redundant virtual groups referred to as fault masking groups (FMGs) or as simplex virtual groups. Fault masking groups may consist of 2, 3, or 4 processors that execute identical control streams. A fault-masking group is composed of processors that reside in different fault-containment regions (FCR). Each FCR contains a Network Element (NE) and either 1 or 2 Processors (an FCP member on all but the fifth NE chassis, and an ICP). A simplex virtual group consists of a single processor. All virtual groups communicate with each other via the network element.
The Network Elements provide communication between virtual groups, keep the FCRs synchronized, and maintain data consensus among FCRs. The NEs are designed to implement the requirements for Byzantine resilience.
The Processing Elements are the computational sites. Each processor consists of a microprocessor, private RAM and ROM, and miscellaneous support devices, such as timers.
Interfaces between the Network Elements and the FTSS are shown in REF _Ref427651111 \h Figure 3‑6.
Figure STYLEREF 1 \s 3‑ SEQ Figure \* ARABIC \s 1 6. Network Element Interfaces to FTSS CSCI.
All transactions with the Network Element consist of a Data Descriptor Block and a Data Block. Each output transmission consists of an output descriptor block and an output data block. Each input reception consists of an input descriptor block and an input data block. The output descriptor and input descriptor blocks are defined in the Network Element Descriptor Block interfaces identified in Table 3.3-1. The output and input data blocks are defined in the Network Element Data Block Interfaces identified in Table 3.3-2; the format of the data blocks differs with the type of message transmitted. The table first identifies the type of message, and then provides the format of the data block for the given type.
Table 3.3-1. Network Element Descriptor Block Interface.

Identifier
Description
Source
Destination
Output Descriptor Block:

Packet class
8-bit field. Selects the data exchange primitive to be executed by the NE.
FTSS CSCI
Network Element
toVID
8-bit field. Specifies the virtual group to which the packet is to be sent.
FTSS CSCI
Network Element
FromVID
8-bit field. Specifies the virtual group that sent the packet.
FTSS CSCI
Network Element
User Field
8-bit field. Used by FTSS.
FTSS CSCI
Network Element
Input Descriptor Block:

Packet class
8-bit field. Selects the data exchange primitive to be executed by the NE.
Network Element
FTSS CSCI
toVID
8-bit field. Specifies the virtual group to which the packet is to be sent.
Network Element
FTSS CSCI
FromVID
8-bit field. Specifies the virtual group that sent the packet.
Network Element
FTSS CSCI
User Field
8-bit field. Used by FTSS.
Network Element
FTSS CSCI
Vote Errors
Indicate if the data emanating from a participant during packet exchange disagreed with the majority in any way.
Network Element
FTSS CSCI
Clock Errors
Indicate that sometime since the last packet was exchanged by the NE, the FTC signal from the indicated NE fell outside the allowable skew window.
Network Element
FTSS CSCI
Link Errors
Indicate that sometime since the last packet was exchanged by the NE, an error was detected on the indicated fiber-optic link.
Network Element
FTSS CSCI
OBNE time-out
Indicates that the members of the source virtual group corresponding to the set bits did not request to send the packet within the allowable time skew.
Network Element
FTSS CSCI
IBNF time-out
Indicates that the members of the destination virtual group corresponding to the set bits did not free enough space in their input buffers to hold the incoming packet within the allowable time skew.
Network Element
FTSS CSCI
Scoreboard Vote Error
Indicates that the corresponding virtual group member did not agree with the majority regarding the type of packet to be exchanged.
Network Element
FTSS CSCI
Time stamp
32-bit field representing the time that the packet was exchanged.
Network Element
FTSS CSCI

Table 3.3-2. Network Element Data Block Interface.
Identifier
Description
Source
Destination
Output Data Packet:

User data
64-byte packet of user data.
FTSS CSCI
Network Element
Input Data Packet:

User data
64-byte packet of user data.
Network Element
FTSS CSCI
Transient Network Element Recovery Packet:

M(A)
TNR message as sourced by Network Element A.
Network Element
FTSS CSCI
M(B)
TNR message as sourced by Network Element B.
Network Element
FTSS CSCI
M(C)
TNR message as sourced by Network Element C.
Network Element
FTSS CSCI
M(D)
TNR message as sourced by Network Element D.
Network Element
FTSS CSCI
M(E)
TNR message as sourced by Network Element E.
Network Element
FTSS CSCI
RESULT
A byte indicating which NEs sourced the expected TNR message.
Network Element
FTSS CSCI
Configuration Table Update Packet:

VID
The virtual group to be updated (VID 255 is reserved for NE and Clock masks).
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Redundancy Level
The redundancy level to be used for the virtual group.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Processing Element Mask
Used to mask in selected members of the virtual group during data voting (VID 255 – NE mask).
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Time-out
Selects the time-out to be used for the virtual group when calculating the OBNE and IBNF conditions (VID 255 – clock mask).
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Member 0
Processor in the virtual group.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Member 1
Processor in the virtual group.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Member 2
Processor in the virtual group.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Member 3
Processor in the virtual group.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
Voted Reset Packet:

VRESET Command
Byte 1- Command to perform the voted reset operation.
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element
User (FTSS) defined
Remaining 63 bytes (unused).
Network Element/
FTSS CSCI
FTSS CSCI/
Network Element

Radstone/FTSS Interfaces
The Radstone firmware provides BIT capability on all Radstone boards on power up or reset. At the end of BIT the Radstone firmware saves the fault log.
Data element definitions for the Radstone/FTSS interface are shown in Table 3.3-3.
Table 3.3-3. Data Element Definition Table for Radstone/FTSS Interfaces.
Identifier
Description
Data Type
Limit/ Range
Source
Destination
Time Services:

start_minor_cycle
count down timer interrupt
interrupt
NA
ISABridge HW timer
FTSS
utility_timer_value
Utility timer output
uword32
2^32
PPC time base register
FTSS
ticks
count down value for next minor cycle interrupt
uword16
65536
FTSS
ISABridge HW timer
Fault Detection and Isolation Services:
rad_fault_log
Radstone self-test log
char []

Radstone firmware
FTSS

VxWorks/FTSS Interfaces
For VxWorks/FTSS interfaces see VxWorks Reference Manual. Appendix A of the API manual defines the allowable subset of VxWorks calls that can be safely used by the FCP application software.
Multi-Protocol Communications Controller (MPCC)/FTSS Interfaces
For MPCC/FTSS interfaces see the Radstone MPCC01 Firmware Manual, Pub #YD681MPCC1, and Radstone MPCC01 Hardware Manual, Pub #HH681MPCC1.
The telemetry serial line on the MPCC cards will be configured as follows:
Mode: 0x1103
SLDC Mode
Buffered Transfer
Single Frame Transfer
Report a Break character, but do not close the RX channel
Normal Operation
Note: CRC is always generated in SDLC mode
Baud Speed: 2,097,152 bps
Buffer size: 13,000 bytes
No parity, 1 stop bit, 8 bit chars: 0x80
The command serial line on the MPCC cards will be configured as follows:
Mode: 0x1103
SLDC Mode
Buffered Transfer
Single Frame Transfer
Report a Break character, but do not close the RX channel
Normal Operation
Note: CRC is always generated in SDLC mode
Buffer size: 332 bytes
Baud Speed: 1,048,576 bps
No parity, 1 stop bit, 8 bit chars: 0x80
FCP-ICP/FTSS Interfaces
The scheduler will populate shared memory with the data defined in Section 3.2.2.1, Item 21. The scheduler will issue a VME interrupt to the ICP every FCP 50 Hz minor frame. This interrupt will alert the ICP to enter a new ICP 50 Hz minor frame cycle. The minor frame number the ICP should be executing on is denoted by the value of the minor_frame identifier in shared memory.
Data element definitions for the ICP/FCP FTSS interface are shown in Table 3.3-4.

Table 3.3-4. Data Element Definition Table for FTSS Scheduler Interface.
Identifier
Description
Data Type
Limit/ Range
Source
Destination
minor_frame number
Minor Frame FCP is currently executing
int
