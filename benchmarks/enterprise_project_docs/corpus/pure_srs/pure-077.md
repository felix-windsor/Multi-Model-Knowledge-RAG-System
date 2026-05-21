# 1999 - tcs - 5. TCS to Printer

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 5. TCS to Printer

5. TCS to Printer
Figure 3.3.1.4-1 illustrates the TCS to Printer interface.

Printer

TCS

Figure 3.3.1.3-1 TCS to Printer Interface Diagram
The TCS shall provide an interface between the TCS and an external hard copy printer. [SSS314]
The TCS shall as a minimum, allow Operator(s) to print freeze-frame video, C4I Messages, Mission Plans,
FD/L information, and current map display. [SSS315]
The TCS shall have the functionality to output digital message data and imagery to a hard copy printer.

35

[SSS316]
Details of the Tactical Control System (TCS) to printer interface will be defined in the TCS to Printer
IDD, TCS 255.
3.3.1.4 External Data Storage Systems
Figure 3.3.1.4-1 illustrates the TCS to External Storage Device interface.

External
Data
Storage

TCS

Figure 3.3.1.4-1 TCS to External Data Storage System Interface Diagram
The TCS shall provide an interface between the TCS and external data storage systems. [SSS317]
The TCS shall have the functionality to transfer digital data as well as digital imagery to and from external
data storage systems. [SSS318]
Details of the Tactical Control System (TCS) to external data storage interface will be defined in the TCS
to External Data Storage IDD, TCS256.
3.3.1.5 TCS to External Power
Figure 3.3.1.5-1 illustrates the TCS to External Power interface.

External
Power

TCS

Figure 3.3.1.5-1TCS to External Power Interface Diagram
The TCS shall have an interface between the TCS and DoD standard power supply equipment. [SSS319]
The TCS shall have the functionality to connect to the power supply equipment provided in the TCS
operating environment. [SSS320]
Details of the Tactical Control System (TCS) to external power interface will be defined in the TCS to
External Power IDD, TCS 257.

36

3.3.1.6 TCS to Geopositional Data
Figure 3.3.1.6-1 illustrates the TCS to Geopositional Data interface.

GeoPositional

TCS

Figure 3.3.1.6-1 TCS to Geopositional Data Interface Diagram
The TCS shall have an interface to a source of current navigation information. [SSS321] As a minimum
this information will include the location of all data terminals, launch and recovery sites, and the controlling
TCS.
Details of the Tactical Control System (TCS) to external power interface will be defined in the TCS to
Geopositional Data IDD, TCS 243.

3.4 System Internal Interface Requirements
Figure 3.4-1 illustrates the TCS internal interfaces.

37

IMAGERY
SUBSYSTEM

SAR

POWER
SUPPLY

UNINTERRUPT
POWER
SUPPLY

DOWNSIZED
LINK
MANAGER
ASSEMBLY

REAL
TIME
PROCESSOR

RAID

ANTENNA
CONTROL
CD-ROM
DRIVE
OUTRIDER
DATA LINK
CONTROL
MODULE

NON
REAL
TIME
PROCESSOR

PREDATOR
DATA LINK
CONTROL
MODULE

TAPE
DRIVE

C4I
SPECIFIC

VCR

PRINTER

INTERCOMM

Figure 3.4-1 TCS Internal Interface Diagram

Except for the internal interfaces enumerated under this section, all TCS internal interfaces are left to the
design and to the requirement specifications for system components.
The TCS will provide, as a minimum, the following internal interfaces:
1. AV Standard Interface.
