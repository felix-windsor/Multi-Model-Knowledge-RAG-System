# 1999 - tcs - 6. System Internal Data Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 6. System Internal Data Requirements

6. System Internal Data Requirements
All TCS internal data decisions will be left to the design and the requirement specifications for system
components.

3.6 Adaptation Requirements
This section not applicable, therefore tailored out.

3.7 Safety Requirements
The TCS design shall consider all safety requirements affecting design and performance except nuclear
safety. [SSS345]
The TCS safety requirements are intended to eliminate as well as control potential hazards to equipment
and personnel involved in the TCS. The TCS shall comply with para 5.3 of MIL-STD 882C, “System
Safety Program Requirements”, dated 19 January 1993 w/ Notice 1 dated 19 January 1996. [SSS346]

3.7.1 Air Vehicle Safety
The TCS shall provide sufficient cues to allow the operator to safely take-off, land and navigate under
Instrument Flight Rules. [SSS347]
The TCS shall provide adequate capability to allow the operator to operate each UAV within its certified
operational flight envelope. [SSS348]
Appropriate cautions and warnings shall be provided to the operator if the air vehicle deviates into unsafe
flight regime. [SSS349]
For mission planning, the TCS shall provide terrain avoidance warning and minimum reception altitude
calculations for line of sight flights. [SSS350]
During mission execution, the TCS shall provide the operator a cautions and warnings when the UAV
system has identified a malfunction. [SSS351]
The TCS shall provide the required information to allow the operator to maintain safe separation from
other aircraft and a safe altitude in civilian airspace per Federal Aviation Administration (FAA) rules.
[SSS352]

41

The TCS shall be designed such that no single hardware failure results in an unsafe command to be
transmitted to the air vehicle. [SSS353]
The TCS shall be designed such that no single software error results in an unsafe command to be
transmitted to the air vehicle. [SSS556]
The TCS shall be capable of restoring power in sufficient time to avoid loss of air vehicle control during
power outages. [SSS354]
The TCS shall monitor the uplink and downlink to each UAV under its control. [SSS355]
Upon detection of loss of link, the TCS shall attempt to reestablish communications with the air vehicle.
[SSS356]

3.7.2 Human Safety
The TCS design shall provide protection against injury to TCS operators and maintenance personnel.
[SSS357] The system design shall use MIL-STD-2036, Section 5.1.3.11 as a guide, with regard to
personnel hazards, and MIL-STD-1472D, Section 5.13, as a guide for safety from a human engineering
viewpoint. [SSS358]

3.7.3 System Safety And Health Hazard Assets
System safety and health hazards, if any, shall be identified and evaluated during Phase I of the TCS
development. [SSS359]
Risk levels and a program to manage the probability and severity of hazards shall also be developed.
[SSS360]

3.8 Security And Privacy Requirements
The TCS is an Automated Information System (AIS). Therefore, as per DoD Regulation 5000.2-R, dated
March 15, 1996, the TCS shall meet security requirements in accordance with DoD Directive 5200.28(D),
“Security Requirements for Automated Information Systems” dated March 21, 1988. [SSS361]
The TCS shall be accredited by the Designated Approving Authority prior to processing classified as well
as sensitive unclassified data. [SSS362]

3.8.1 Computer Security
Using risk assessment procedures defined in DoD 5200.28(D), a risk index and the minimum security
requirements for TCS shall be determined. [SSS363] The inputs to this procedure are the clearance or
authorization of the TCS users and the sensitivities of the data that the TCS processes, stores or transfers.
These requirements pertain to the TCS computer hardware and software.
The TCS data sensitivities shall be determined by the data sensitivities of the systems with which it

42

interfaces, to including the air vehicles, payloads, and C4I systems. [SSS364]

3.8.2 Communications Security
Links that provide communications between the TCS and other systems shall be secured in a manner
appropriate for the sensitivities of the material passed through such links, in accordance with DoD
Directive C-5200.5, “Communication Security (COMSEC)” dated 21 April 1990. [SSS365]

3.8.3 Physical Security
The TCS shall be designed to protect its communication and data links against enemy Electronic Warfare
(EW) threats, physical anti-radiation weaponry and physical destruction. [SSS366]
All hardware, software, documentation, and sensitive information processed by TCS shall be physically
protected, minimally at the level determined by the risk index computed in Section 3.8.1, to prevent
intentional as well as unintentional disclosure, destruction, and modification. [SSS367]
The TCS shall be approved for operation at the same level as the systems with which it interfaces.
[SSS368]

3.8.4 Personnel Security
All TCS users, operators, maintainers and other personnel having access to TCS shall be cleared to the
highest sensitivity of the data that the TCS processes, stores and transfers. [SSS369]
Additional local site procedures shall be developed to prevent the intentional or unintentional disclosure of
sensitive information to unauthorized individuals. [SSS370]
A training program consisting of an initial security training and awareness briefing covering AIS security
in general but also tailored to the TCS shall be developed. [SSS371]

3.8.5 Privacy Requirements
This section not applicable, therefore tailored out.

3.9 System Environment Requirements
The TCS shall be capable of operation within environments specified in the System/Subsystem Design
Document for the land-based shelter and shipboard environments. [SSS372]
The TCS hardware shall be mounted as well as ruggedized to withstand inter and intra theater movement.
[SSS373]

43

3.10 Resource Requirements
3.10.1 Hardware Requirements
The TCS hardware will provide the functionality and capability to receive, process, and disseminate video
and telemetry data from the AV and payload; perform mission planning; monitor and control the payload;
monitor and control the AV; and monitor and control the data links.
The hardware of the TCS shall be capable of being scaled as well as being modular to meet the varying
needs of the Services. [SSS374]
The TCS hardware shall allow for long range communications from one TCS to another [SSS375], data
storage expansion [SSS376], access to other computers to share in processing capability [SSS377], and
multiple external peripherals [SSS378].
The TCS hardware shall support the data rate characteristics of the AV, data link and payload to ensure
interoperability. [SSS379]
For each OUTRIDER system, the TCS shall provide full independent computer redundancy. [SSS380]
The TCS shall conform with the National Institute for Standard Technology (NIST) Federal Information
Processing Standard (FIPS) Publication 151-2 (POSIX.1). [SSS381]
3.10.1.1 Performance
The TCS shall have sufficient throughput to support the processing requirements of the selected data link.
[SSS382]
3.10.1.2 Mass Storage
To meet growth requirements, the TCS shall be capable of adding additional storage without major
hardware reconfiguration. [SSS383]
The TCS computer system shall contain a CD-ROM drive that is compatible with National Imagery and
Mapping Agency (NIMA), CD-ROM Digital Terrain Elevation Data (DTED), Digital Feature Analysis
Data (DFAD), and embedded training media. [SSS384]
3.10.1.3 Power
The TCS shall use standard military worldwide 110/220 volt 50/60 hertz generators and commercial power
sources. [SSS385]
The TCS shall use standard electrical power sources available within the DoD family of ground mobile,
airborne, and shipboard electrical power sources. [SSS386]
The TCS shall be capable of restoring power in sufficient time to avoid loss of critical mission data and
loss of air vehicle control during power outages. [SSS387]

44

The TCS shall have an uninterrupted power supply for critical phases (landing and takeoff as a minimum)
of mission execution. [SSS388]

3.10.2 Hardware Resource Utilization Requirements
The TCS throughput shall not exceed 50% of the throughput capability delivered over any 10 second
period [SSS389], and as an objective throughput shall not exceed 25% of throughput capability delivered
over any 10 second period. [SSS390].
The TCS shall be capable of providing a 50% spare memory storage capacity over delivered storage used
[SSS391]. As an objective a 75% spare memory storage capacity over storage used shall be provided.
[SSS392]

3.10.3 Computer Software Requirements
The TCS software will provide the functionality and capability to receive, process, and disseminate video
and telemetry data from the AV and payload; perform mission planning; monitor and control the payload;
monitor and control the AV; and monitor and control the data links.
The TCS shall have software based on Defense Information Infrastructure/Common Operating
Environment per Assistant Secretary of Defense for Command, Control, Communications, and Intelligence
(ASD(C3I)) Joint Technical Architecture (JTA). [SSS393]
The TCS shall comply with the Assistant Secretary of Defense (C3I) Joint Technical Architecture (JTA).
This includes, but is not limited to, the language, the computer, database, architecture, and interoperability.
[SSS394]
The TCS shall provide an open software architecture to be capable of supporting additional CSCIs, CSCs,
and CSUs for future AVs, future payloads, and payload capabilities (e.g. auto-search and automatic target
tracking), and future Tactical UAVs. [SSS395]
The TCS core software shall be generically written to provide level one through level five interaction for
both Outrider and Predator UAVs and establish the architecture for future tactical UAVs. [SSS396]
The TCS software shall provide the UAV operator with the necessary tools for computer related
communications, mission tasking, mission planning, mission execution, data receipt, data processing, and
data dissemination. [SSS397]
The TCS software shall be capable of being hosted on a variety of computer operating systems that are
organic to the various Services. [SSS398]
TCS software shall provide a windows based graphic operator interface. [SSS399]
The TCS software shall be non-proprietary and have unlimited data rights. [SSS400]
The TCS’s operating system and executable software shall be re-programmable without hardware
disassembly. [SSS401]

45

Training software shall be alterable without affecting the configuration of the operational software.
[SSS402] Training software is the software that provides the computer based training functionality for the
system operator.
The TCS software shall restrict the operator(s) from exercising levels of interaction not achievable by the
system. [SSS403]
3.10.3.1 Display
The TCS software shall provide a high resolution, computer generated, graphical user interface that
enables the UAV operator that is trained on one system to control different types of UAVs as well as UAV
payloads with minimal additional training. [SSS404]
Each control console shall have, at a minimum, the capability to display the following four display
windows: (1) display to provide aircraft position, TCS position, flight path, and a waypoint graphics in the
foreground which are positioned in relation to a map displayed in the background, (2) display to provide
aircraft flight data or payload data in the foreground, and downlinked video in the background. (3)A
display to provide graphic presentations of downlinked telemetry data, and (4) display to present the
interface menus for workstation software. [SSS405]

3.10.4 Computer Communication Requirements
The DII/COE UCP/CMP shall provide a consistent and common set of interfaces for United States
Message Text Format (USMTF), Army Tactical Command Control System (ATCSS), and Field Artillery
Tactical Data Systems (FATDS) message sets. [SSS406]
The TACCOM segment shall provide external interfaces for the communications media as indicated in
Table 3.10.4-1: [SSS407]
Table 3.10.4-1 Communication Media and Associated Interface Document
Communication Media

Interface Document

RS-232

IEEE RS-232

RS-422

EIA RS-422

RS-170A

ISO-XXX

Wire line, 2-wire

MIL-C-49104

Wire line, 4-wire

MIL-C-55425

MSE (DNVT, DSVT)

ICD MSE-001

46

Communication Media

Interface Document

MSE TPN

MSE System Specification, Appendix
SR45

SINCGARS

ACCS-A3-409-001

ANG/GYC-7

ICD-016, ICD-017, TIDP for MTS

IEEE 802.3/LAN

ISO/IS 8802/2, ISO/IS 8802/3

The TACCOM segment shall provide API’s for the transmission of imagery in National Imagery
Transmission Formats 1.1a and 2.0 as per MILSTD-2500 and to be compatible with the Common Imagery
Ground/Surface Station (CGIS) Guidelines. [SSS408]

3.11 System Quality Factors
3.11.1 Functionality
The TCS data latency shall not be greater than that present in the Predator ground control station or
Outrider ground control station, whichever is smaller. [SSS409]

3.11.2 Reliability
The TCS reliability will be considered in every phase of the design and development process and shall
achieve a system reliability (Mean Time Between Failures MTBF) equal to or greater than that which is
specified in the Predator and Outrider ORDs. [SSS410]

3.11.3 Maintainability
The TCS maintainability will be considered in every phase of the design and development process and shall
achieve a system maintainability (Mean Time To Repair MTTR) equal to or greater than that which is
specified in the Predator and Outrider ORDs. [SSS411]

The Design features shall be included to: [SSS412]
