# 1999 - tcs - 5. Level five is the capability to have full function and control of the UAV from takeoff to

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 5. Level five is the capability to have full function and control of the UAV from takeoff to

5. Level five is the capability to have full function and control of the UAV from takeoff to
landing

SSS409
The TCS data latency shall not be greater than that present in the Predator ground control station or
Outrider ground control station, whichever is smaller.
SSS329
Remotely hosted applications shall communicate in a client server relationship via the defined data
server interface.
SSS328
The RTP interface shall support distributed processing capability.
SSS327
This interface shall allow the information from the data server to be made available to other
components of the TCS.
SSS326
The TCS shall provide an internal interface for establishing communications with the RTP within
TCS.
SSS175
The TCS shall be capable of automatically controlling the transmitter and receiver frequencies of the
selected data terminal.
SSS173
The TCS shall be capable of automatically controlling the transmitter and receiver modes of the
selected data terminal.
SSS172
The operator shall be able to manually override the automatic function selection if desired.
SSS171
The TCS shall be capable of automatically controlling the transmitter and receiver functions of the
selected data terminal.
SSS170
The TCS shall be capable of properly selecting and positioning antennas to maintain line-of-sight or
satellite communication.
SSS167
The TCS shall provide automatic pointing commands for directional antennas.
SSS557

64

The TCS shall incorporate antenna pedestal 3 –axis stabilization to compensate for platform (e.g.
ship, or HMMWV) motion, if applicable.
SSS165
The TCS shall provide an interactive display for the purpose of controlling the data link terminal.
SSS164
The TCS shall support a sequential LOS data link and beyond LOS data link capability.

TCS Block 0
Version 2.0
ORD012

ORD013

TCS 102
2/12/99

The TCS shall provide full interoperability between the Services and their UAV systems with SSS009
varying levels of UAV interaction.
The TCS system shall provide software capabilities and hardware configurations necessary to fulfill
the operational tasking requirements across the 5 levels of interaction.
The TCS core software shall be generically written to provide Level Five interaction for both SSS396
TUAV and MAE UAVs and establish the architecture for future tactical UAVs.
The TCS core software shall be generically written to provide level one through level five interaction
for both Outrider and Predator UAVs and establish the architecture for future tactical UAVs.
SSS437
Newly designed software shall be developed in accordance with a tailored MIL-STD-498.

ORD014

ORD015

The TCS software and software related hardware shall be developed so that it is scaleable to meet SSS004
the users’ needs.
The TCS shall consist of the TCS workstation Hardware Configuration Items (HWCIs), TCS
Software Compute Software Configuration Items (CSCIs), and additional TCS Support HWCIs and
CSCIs. .
The TCS shall prevent users from entering levels of interaction for which they are not authorized SSS403
by software and/or hardware configuration.
The TCS software shall restrict the operator(s) from exercising levels of interaction not achievable
by the system.
SSS023
The TCS shall inform the operator if the operator attempts to execute a function that is prohibited
based upon the determined level of interaction.
SSS022
Levels of interaction higher than that achievable by a particular TCS configuration shall be
prohibited.
SSS021
During startup, the TCS shall determine which of the 5 levels of interaction are achievable by the
TCS configuration being used.

65

TCS Block 0
Version 2.0
ORD016

TCS 102
2/12/99

The TCS shall enable the UAV operator to communicate, receive mission tasking, conduct mission SSS500
planning, execute the mission, and collect, process, and disseminate data for the TUAV and MAE The capability for the conduct of actual communications processing concurrently with Training
UAV, and support data collection from HAE UAV.
operations shall be provided if and only if messages are identified as training messages.
SSS047
Shutdown of the TCS shall include proper termination of all active interfaces.
SSS046
Shutdown of the TCS shall include shutdown of HCIs.
SSS045
Shutdown of the TCS shall include shutdown of appropriate functions.
SSS028
Initialization of the TCS shall include establishment of the state of readiness of all interfaces.
SSS027
Initialization of the TCS shall include start of HCIs.
SSS026
Initialization of the TCS shall include download of software.
SSS542
Initialization of the TCS HWCIs shall include startup of HWCIs.
SSS335
The TCS shall be able to route VCR recorded payload video to the C4I Interfaces.
SSS332
The intercom system shall be compatible with service specific voice communication systems.
SSS331
The TCS shall incorporate an intercom system that allows the operator(s) of the TCS to verbally
communicate with each other.
SSS210
The TCS shall have the functionality necessary to manage all aspects of C4I system interfaces to
include receiving, processing, and transmitting tactical information to include but not limited to
character based text messages, NITF 2.0 imagery files, and RS-170A video.
SSS208
The TCS shall have the functionality to develop an estimate of the error in computed target
coordinates, and associate the error estimate with the appropriate target.

66

SSS189
Payload telemetry data shall be available to support other TCS functions as required.
SSS180
The TCS shall be capable of presenting to the operator a visual depiction of the minimum and
maximum data link operational ranges.
SSS121

TCS Block 0
Version 2.0

TCS 102
2/12/99

ORD017

The TCS shall provide an open software architecture that can support future UAVs.

SSS395
The TCS shall provide an open software architecture to be capable of supporting additional CSCIs,
CSCs, and CSUs for future AVs, future payloads, and payload capabilities (e.g. auto-search and
automatic target tracking), and future Tactical UAVs.

ORD018

The TCS shall have software based on Defense Information Infrastructure/Common Operating SSS393
Environment per Assistant Secretary of Defense for Command, Control, Communications, and The TCS shall have software based on Defense Information Infrastructure/Common Operating
Intelligence (ASD(C3I)) Joint Technical Architecture (JTA).
Environment per Assistant Secretary of Defense for Command, Control, Communications, and
Intelligence (ASD(C3I)) Joint Technical Architecture (JTA).

67

TCS Block 0
Version 2.0
ORD019

TCS 102
2/12/99

The TCS shall have ergonomically designed operator controls and displays.

SSS490
The TCS HCI shall provide for the capability to automatically designate target transmissions from
the payload screen onto the map screen.
SSS489
The TCS HCI shall provide continuously-available, on-screen control functions for time and
mission-critical operations, to include as a minimum print, freeze, declassification, mark VCR,
declutter, cease RF transmission.
SSS488
The TCS HCI shall provide for on-screen information to include, as a minimum, overlays, headers,
cursors, alphanumeric annotation, waypoints, crosshairs, designed to be visible against the complete
spectrum of map and payload video backgrounds.
SSS487
For AV safety or mission-critical Warnings, the TCS HCI shall provide a default selection as well as
an override option, along with a selection of adaptive responses, and the minimum information
necessary to assist the operator in responding quickly and adaptively to the emergency.
SSS486
The TCS HCI shall provide for visual Cautions and Advisories to be displayed at or near the center
of the field of view, i.e., within a 30o cone, of all monitors in a TCS system.
SSS485
The TCS HCI shall provide for separation, grouping, and visual coding of multiple categories of
alerts, to include Warnings, Cautions, and Advisories.
SSS484
The TCS HCI shall provide for a rapid means to cancel aural warnings.
SSS482
The TCS HCI shall provide the capability to display operator definable “Lock Out” zones around
waypoints, Launch and Recovery Point (LRP), or any selected point on the AV flight path.
SSS481
The TCS HCI shall provide the capability to lock onto and hold a coordinate point on-screen.
SSS480
The TCS HCI shall provide the on-screen capability to select and efficiently move or reorient a
previously defined SAR imaging swath.
SSS479
The TCS HCI shall display the SAR imaging swath on the map display.

68

SSS478
The TCS HCI shall provide coarse and fine payload control capabilities directly on the payload
screen.
SSS477
The TCS HCI shall provide the capability to select and amplify an object or point on a map or
payload screen.
SSS476

TCS Block 0
Version 2.0
ORD020

TCS 102
2/12/99

The TCS shall have monitor(s) that provide easy reading of displays.

SSS446
The TCS shall have monitor(s) that provide easy reading of displays under direct sunlight and low
light level environments.
SSS459
Display jitter and flicker shall not be detectable by the operator.

ORD021

The TCS HCI shall be menu driven and have displays in a X-windows motif.

SSS447
The TCS HCI shall be a Graphical User Interface (GUI) based on X-windows and Motif.
SSS399
TCS software shall provide a windows based graphic operator interface.

ORD022

The TCS shall have peripheral ports to drive external devices. As a minimum, ports required will SSS343
be for monitor displays, mouse (or pointer device), keyboard, printer, LAN, EIA-RS-170, and The TCS shall provide a RAID for storage and retrieval of TCS data, if required.
external disk drives (if required)
SSS342
The TCS shall provide a tape drive for storage and retrieval of TCS data.

ORD023

The TCS shall be capable of supporting additional software modules for future payloads, payload SSS439
capabilities (e.g. autosearch and automatic target tracking), and future Tactical UAVs.
A modular architecture shall be used by the TCS software in order to support future interoperability
with multiple types of UAVs and payloads while maintaining consistent displays and user interfaces.
Software components satisfying common planning and control functions will allow for vehicle
specific components to be integrated in the future.

ORD024

The TCS shall allow operators to have simultaneous flight and payload control of at least two air SSS125
vehicles, beyond line of sight, using one TCS.
The TCS shall provide the necessary system capabilities required for AV flight control BLOS via
uplink command to two MAE air vehicles.
SSS124
The TCS shall allow the operator to control an AV using the LOS or SATCOM data links.
SSS149
The TCS shall provide the necessary system capabilities required for payload control beyond line of
sight via uplink command of two air vehicles of the same type using sequential communication
techniques. Sequential communication means alternatively communicating with one air vehicle and
then the other. Current air vehicle design does not permit concurrent communications with two air
vehicles at the same time.

69

TCS Block 0
Version 2.0
ORD025

TCS 102
2/12/99

The TCS shall be capable of being interoperable with different types of UAVs and UAV payloads SSS011
across the 5 levels of UAV interaction.
The TCS shall be capable of being interoperable with Predator and Outrider UAVs across the 5
levels of UAV interaction.
SSS012
The TCS shall be capable of being interoperable with the installed payloads across the 5 levels of
UAV interaction.
SSS322
The TCS shall implement an AV Standard Interface that will provide the proper data format to
ensure communications with the selected AV.
SSS323
This interface shall allow for addition of future AVs and will provide the generic architecture to
ensure interoperability.

ORD026

The TCS shall be capable of being interoperable with multiple platforms/payloads simultaneously.

70

SSS013
Table 3-2 identifies the payloads with which the TCS shall interoperate.
Table 3-2 Interoperable TCS Payloads
PAYLOAD TYPE
UAV
EO/IR
Predator
SAR
EO/IR
Outrider
Future

TCS Block 0
Version 2.0
ORD027

TCS 102
2/12/99

The TCS shall be capable of meeting the operational and physical security requirements of the SSS362
systems with which it is interoperable.
The TCS shall be accredited by the Designated Approving Authority prior to processing classified or
sensitive unclassified data.
SSS361
The TCS is an automated information system (AIS). As such, as per DoD Regulation 5000.2-R,
dated March 15, 1996, the TCS shall meet security requirements in accordance with DoD Directive
5200.28(D), “Security Requirements for Automated Information Systems” dated March 21, 1988.
SSS363
These requirements pertain to the TCS computer hardware and software. Using risk assessment
procedure defined in DoD 5200.28(D), a risk index and the minimum security requirements for
TCS shall be determined. The inputs to this procedure are the clearance or authorization of the TCS
users and the sensitivities of the data that the TCS processes, stores or transfers.
SSS364
The TCS data sensitivities shall be determined by the data sensitivities of the systems with which it
interfaces including the air vehicles, payloads, and C4I systems. The outputs of the procedure are the
TCS mode of operation and a digraph that the TCS must minimally satisfy. The digraph (e.g., B1,
C2) names the class of security requirements, specified in DoD 5200.28-STD, “Trusted Computer
Security Evaluation Criteria (TCSEC)”, that the TCS has to satisfy.
SSS365
Links that provide communications between the TCS and other systems shall be secured in a manner
appropriate for the sensitivities of the material passed through such links, in accordance with DoD
Directive C-5200.5, “Communication Security (COMSEC)” dated 21 April 1990.
SSS366
The TCS shall be designed to protect its communication and data links against enemy Electronic
Warfare (EW) threats, physical anti-radiation weaponry and physical destruction.
SSS367
All hardware, software, documentation, and sensitive information processed by TCS shall be
physically protected, minimally at the level determined by the risk index computed in Section 3.8.1,
to prevent intentional or unintentional disclosure, destruction, or modification.
SSS368
The TCS shall be physically secured to the same degree as the systems with which it interfaces.
SSS369
All TCS users, operators, maintainers and other personnel having access to TCS shall be cleared to
the highest sensitivity of the data that the TCS processes, stores or transfers.

71

SSS370
Additional local site procedures shall be developed to prevent the intentional or unintentional
disclosure of sensitive information to unauthorized individuals.
SSS371
A training program consisting of an initial security training and awareness briefing covering AIS
security in general but also tailored to the TCS shall be developed.

TCS Block 0
Version 2.0
ORD028

TCS 102
2/12/99

The TCS shall be capable of importing NIMA Digital Terrain Elevation Data (DTED), Digital SSS384
Feature Analysis Data (DFAD), Arc Digitized Raster Graphic and scanned hard copy maps.
The TCS computer system shall contain a CD-ROM drive that is compatible with Defense Mapping
Agency (DMA), CD-ROM Digital Terrain Elevation Data (DTED), Digital Feature Analysis Data
(DFAD), and embedded training media.
SSS341
The TCS shall provide a CD drive for the retrieval of TCS data.
SSS280
The TCS shall be capable of importing National Imagery Mapping Agency (NIMA) Digital Terrain
Elevation Data (DTED), Digital Feature Analysis Data (DFAD), Arc Digitized Raster Graphic and
scanned hard copy maps, via compact disk.

ORD029

The TCS shall be capable of importing map information via operator procedure and should be SSS281
capable of incorporating vector format and Compressed ADRG (CADRG) maps.
The TCS shall be capable of importing map information via operator procedure and should be
capable of incorporating vector format and Compressed ADRG (CADRG) maps.
SSS555
The TCS shall be capable of importing map information via operator procedure.

ORD030

The TCS shall include the basic flight planning tools. As a minimum these tools will include:
1. Weight and balance take off data calculations.

SSS083
The TCS flight route planner shall include, as a minimum, the following flight planning tools:
5.
Weight and balance take off data calculations.
SSS088
The TCS shall present to the operator the estimated time of arrival at each programmed waypoint of
the proposed mission plan.
SSS089
The TCS shall analyze the flight route plan selected for uplink to determine that the flight
constraints of the AV and the limitation of the data link are not violated prior to transmission of the
flight route plan to the AV.

ORD031

The TCS shall include the basic flight planning tools. As a minimum these tools will include:
