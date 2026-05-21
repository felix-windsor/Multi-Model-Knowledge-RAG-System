# 1999 - tcs - 5. View incoming and outgoing, annotated as well as un-annotated digital imagery messages

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 5. View incoming and outgoing, annotated as well as un-annotated digital imagery messages

5. View incoming and outgoing, annotated as well as un-annotated digital imagery messages

27

[SSS244]

3.2.6 AV Maintenance Function
TCS shall be capable of executing AV maintenance software and displaying appropriate status results.
[SSS245]

3.2.7 Payload Maintenance Function
TCS shall be capable of executing payload maintenance software and displaying appropriate status results.
[SSS246]

3.2.8 Data Terminal Maintenance Function
TCS shall be capable of executing data terminal maintenance software and displaying appropriate status
results. [SSS247]

3.2.9 Workstation and Peripheral Equipment Maintenance Function
TCS shall be capable of executing workstation and peripheral equipment maintenance software and
displaying appropriate status results. [SSS248]

3.2.10 Fault Detection/Location Function
Fault Detection/Location (FD/L) to the Line Replaceable Unit (LRU) level shall be provided to indicate the
readiness status of TCS, if inherent to the COTS hardware and software utilized. [SSS249]
As a minimum, TCS shall provide Startup FD/L for the operator workstation. [SSS250]
The TCS shall allow the operator to control and monitor the AV's FD/L, if required and provided by the
Original Equipment Manufacturer (OEM) [SSS251]; Payload's FD/L, if required and provided by the
Original Equipment Manufacturer (OEM) [SSS252]; and Data Link FD/L, if required and provided by the
Original Equipment Manufacturer (OEM) [SSS253].
3.2.10.1 Startup FD/L
**DELETED** [SSS25405]
**DELETED** [SSS25506]
**DELETED** [SSS25607]
**DELETED** [SSS25708]
**DELETED** [SSS258]

28

**DELETED** [SSS259]
3.2.10.2 Periodic FD/L
**DELETED** [SSS260]
**DELETED** [SSS261]
**DELETED**. [SSS262]
**DELETED** [SSS263]
**DELETED**. [SSS264]
**DELETED** [SSS265]
**DELETED** [SSS267]
3.2.10.3 Extensive FD/L
**DELETED** [SSS268]
**DELETED**. [SSS269]
**DELETED** [SSS27019]
**DELETED** [SSS27120]
**DELETED** [SSS27221]
**DELETED** [SSS27322]
**DELETED** [SSS274]
**DELETED** [SSS275]

3.2.11 Software Upgrade Function
The TCS shall allow authorized operators to install software upgrades via CD-ROM as well as other media
storage devices. [SSS276] The TCS shall restrict operator access to this capability via password
protection. [SSS277]
The TCS shall provide the capability for Authorized Operators to modify all TCS programmable
parameters. [SSS278] As a minimum, the TCS shall restrict Operator access to this capability via
password protection. [SSS279]
The TCS shall be capable of importing National Imagery Mapping Agency (NIMA) Digital Terrain
Elevation Data (DTED), Digital Feature Analysis Data (DFAD), Arc Digitized Raster Graphic and

29

scanned hard copy maps, via compact disk. [SSS280]
The TCS shall be capable of importing map information via operator procedure [SSS555] and shall be
capable of incorporating vector format and Compressed ADRG (CADRG) maps. [SSS281]

3.2.12 Software Debug and Monitoring Function
The TCS shall allow an Authorized Operator to execute a software debug capability and view the resulting
debug diagnostic information. [SSS282] As a minimum, the TCS will restrict Operator access to this
capability via password protection. [SSS283]

3.3 System External Interface Requirements
The TCS will interface with external systems to conduct mission coordination and operations.
The TCS shall provide the capability to interface with equipment necessary to provide connectivity with
standard DoD tactical (VHF, UHF, and UHF/VHF) radios, Mobile Subscriber Equipment, and military
and commercial satellite communications equipment. [SSS285]
The TCS shall interface with external mission tasking systems (e.g., receive tasking orders, coordinate
mission certification). [SSS286]
The TCS shall provide the system functionality necessary to interface with the data terminal. [SSS287]
The TCS shall provide the system functionality to allow interfacing with external systems via a local area
network. [SSS288]
The TCS shall provide external interfaces to launch and recovery systems. [SSS289]

3.3.1 Interface Identification
3.3.1.1 TCS to C4I
Figure 3.3.1.1-1 illustrates the TCS to C4I interfaces.

30

EXPLOITATION SYSTEMS
COMMAND & CONTROL SYSTEMS

TROJAN
SPIRIT II

ASAS
JMCIS

ETRAC

TTC
CS
S

TBMCS

IAS

TEG
JSIPS

JDISS

CCTV

JSIPS-N
MIES

SENSOR SYSTEMS

GCS/ACS
IPF

JSTARS
GSM/CGS

AFMSS

TAMPS

AMPS

CARS
SERVICE MISSION PLANNING SYSTEMS

ADOCS

ATWCS

AFATDS

ATHS

FIRE CONTROL SYSTEMS

Figure 3.3.1.1-1 TCS to C4I Interface Diagram
The TCS will be interoperable with C4I systems, as listed in Section 3.2.5 of this document. Table
3.3.1.1-1 shows the implementation schedule for C4I interfaces. This prioritization schema has been
validated by a Joint Requirements Oversight Council (JROC) Memorandum.
Table 3.3.1.1-1 C4I Interface Integration Priority Schedule
FY 97

FY 98

FY 99

FY 00

FY O1

AFATDS

IAS

JSIPS

ATHS

TBMCS

ADOCS

JDISS

ATWCS

AFMSS

TES(MIES)

ASAS

TROJAN SPIRIT II

CARS

TAMPS

ACS IPF

JSTARS-CGS

ETRAC

AMPS

CCTV

JMCIS/GCCS-M

COMPASS

JSIPS-N

TEG

JMCIS

For external communications to C4I systems the TCS shall utilize the Universal Communication Processor

31

as well as the Common Message Processor (CMP) Government Off The Shelf (GOTS) software
capabilities of the DII/COE to communicate with C4I systems using Tactical Communication (TACOMM)
messages. [SSS290] Details of the TACCOM messages and the associated C4I system will be defined in
the applicable TCS to C4I IDDs.
3.3.1.1.1 TCS to ASAS
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with ASAS. [SSS291] The interface requirements and specifications will be defined in the TCS to ASAS
IDD, TCS 201.
3.3.1.1.2 TCS to JSTARS GSM
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with JSTARS GSM. [SSS292] The interface requirements and specifications will be defined in the TCS to
JSTARS IDD, TCS 209.
3.3.1.1.3 TCS to JMCIS
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with JMCIS. [SSS293] The interface requirements and specifications will be defined in the TCS to JMCIS
IDD, TCS 214.
3.3.1.1.4 TCS to JSIPS-N
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with JSIPS-N. [SSS294] The interface requirements and specifications will be defined in the TCS to
JSIPS-N IDD, TCS 210.
3.3.1.1.5 TCS to AFATDS
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with AFATDS. [SSS295] The interface requirements and specifications will be defined in the TCS to
AFTADS IDD, TCS 200.
3.3.1.1.6 TCS to JSIPS-AF
The interface requirements and specifications will be defined in the TCS to JSIPS-AF IDD, TCS 211.
3.3.1.1.7 TCS to CARS
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with CARS. [SSS297] The interface requirements and specifications will be defined in the TCS to CARS
IDD, TCS 217.

32

3.3.1.1.8 TCS to CCTV
The TCS shall provide the necessary hardware and software functionality to allow the TCS to integrate
with CCTV. [SSS298] The interface requirements and specifications will be defined in the TCS to CCTV
IDD, TCS 205.
