# 1999 - tcs - 5. Payload field of view settings, manual as well as automated

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 5. Payload field of view settings, manual as well as automated

5. Payload field of view settings, manual as well as automated
The TCS shall provide the capability to display the payload swath for the selected payload for planning
purposes. [SSS541]
3.2.1.3 Communications Planning Capability
**DELETED** [SSS105]
**DELETED** [SSS106]
**DELETED** [SSS107]

3.2.2 Mission Control And Monitoring Functions
The TCS will have the capability to control and monitor an AV, payload, data link, and C4I interfaces
during the execution of a mission.
While flying two MAE AVs Beyond Line Of Sight (BLOS), the TCS shall provide full control
functionality of each AV. [SSS108]
AV specific components used to perform ground based closed loop command and control functions for

17

TCS shall be initialized upon operator selection of a specific AV. [SSS109]
The TCS shall transmit command and control information to the AV via the uplink to the AV [SSS110],
and receive AV telemetry and payload information via downlink from the AV [SSS111].
3.2.2.1 AV Control And Monitoring Capability
The TCS shall be capable of being interoperable with Predator and Outrider UAVs across the 5 levels of
UAV interaction. [SSS011]
The TCS shall have the capability to control and monitor multiple types of AVs. [SSS112]
TCS shall notify the operator when AV performance parameters are out of limits. [SSS113]
The TCS shall provide the capability to pass control of an AV to another TCS [SSS114], and receive
control of an AV from another TCS [SSS115].
The TCS shall provide the capability to control the AV flight commands as well as to release the AV to an
autonomous flight control mode. [SSS118]
AV telemetry data shall be available to support other TCS functions as required. [SSS119]
The TCS shall provide the capability to control the flight of the selected AV in accordance with the specific
AV's operational performance capabilities. [SSS120]
The TCS shall provide the capability to fully control and display the AV's Identification Friend or Foe
(IFF). [SSS121]
The TCS shall provide the capability to enter AV preset limits which, as a minimum, will include airspeed
limits, altitude limits, and fuel limits. [SSS122]

3.2.2.1.1 AV Flight Control Task
The TCS shall allow the operator to control an AV using the LOS as well as SATCOM data links.
[SSS124]
The TCS shall provide the necessary system capabilities required for AV flight control BLOS via uplink
command to two MAE air vehicles. [SSS125]
The TCS shall support operation of the AV via all flight modes, to include manual controls. [SSS126102]
The TCS shall provide the capability to implement an emergency action plan, if supported by the AV, to
control the AV during equipment failures. [SSS539]
The TCS shall provide interactive displays necessary to command the flight of an AV. [SSS127]

18

3.2.2.1.1.1 Flight Behavior Characteristics
The TCS shall allow the operator to command the flight behavior characteristics inherent to the selected
AV. [SSS128]
The operator shall have the capability to initiate as well as change, to include as a minimum manual
override, flight behaviors by sending the proper control commands to the UAV. [SSS129]
3.2.2.1.2 AV Navigation Control Task
The TCS shall have the capability to command the AV to use the navigation methods inherent to the
selected AV. [SSS130]
The operator shall have the capability to initiate as well as change, to include as a minimum manual
override, UAV navigation methods by sending the proper control commands to the UAV. [SSS131]
3.2.2.1.3 ADT Control Task
The TCS shall provide the functionality to control, monitor, and display the operation of the Air Data
Terminal (ADT). [SSS132] This control will include control of the ADT antenna and of the ADT
transmitter and receiver.
3.2.2.1.3.1 ADT Antenna Control

The TCS shall provide the functionality to control the ADT antenna. [SSS133] This control will including
its pointing direction and mode of transmission (e.g. omni and directional).
3.2.2.1.3.2 ADT Transmitter And Receiver Control
The TCS shall provide the functionality to control the power, transmitter signal strength, and frequencies
used by ADT for data link communication. [SSS134]
3.2.2.1.4 AV Launch/Recovery Task
As an objective, the TCS shall support an automatic launch and recovery system. [SSS135]
As and objective, the TCS shall be interoperable with the Integrity Beacon Landing System (IBLS)
[SSS136], and the Common Automated Recovery System (CARS) [SSS137], both used by Outrider.
As an objective, the TCS shall present sufficient cues to the operator to implement and monitor automatic
launch and recovery, and to initiate abort procedures if required. [SSS138]
3.2.2.1.4.1 Emergency Recovery
The TCS shall allow the operator to initiate the emergency recovery feature of the AV, if the AV has an
emergency recovery feature. [SSS139]

19

3.2.2.1.5 AV Monitoring Task
TCS shall provide the capability to monitor specific telemetry elements real-time, and record all telemetry
elements for future review and processing. [SSS140]
TCS shall provide the capability to monitor AV adherence to the uplinked mission plan, detecting any
deviations greater than 10% from projected flight path, and notifying the operator if deviations are detected.
[SSS141]
TCS shall provide the capability to monitor the status of all AV subsystems reporting status. [SSS142]
3.2.2.1.5.1 AV Monitoring Displays
The TCS shall display the AV status, to include but not be limited to the AV location and flight and
avionics system status. [SSS143]
When the data link is interrupted, the TCS shall present the last known AV status values and the time at
which the last values were reported. [SSS144]
The TCS shall be capable of displaying fuel parameters to the operator to include as a minimum, remaining
fuel, flow rate, and bingo fuel. [SSS145] Bingo fuel is the minimum amount of fuel necessary to return to
the designated Recovery site with reserve fuel.
The TCS shall compute the estimated position of the AV during Loss of Link (LOL) based upon the last
known AV position and anticipated flight path based on current flight mode (e.g. flight route plan mode,
emergency flight route plan mode, maintain current heading mode). [SSS146]
TCS shall display a LOL timer to the operator initiating a LOL onset. [SSS536]
3.2.2.2 Payload Control And Monitoring Capability
The TCS shall be capable of being interoperable with the installed payloads across the 5 levels of UAV
interaction. [SSS012]
The TCS will have the capability to control and monitor the AV payload(s). [SSS147]
The TCS shall have the capability to receive data from and control payloads on an AV that is being
controlled from another TCS. [SSS148]
The TCS shall provide the necessary system capabilities required for payload control beyond line of sight
via uplink command of two air vehicles of the same type using sequential communication techniques.
[SSS149] Sequential communication means alternatively communicating with one air vehicle and then the
other. Current air vehicle design does not permit concurrent communications with two air vehicles at the
same time.
The TCS shall receive, process, and present payload data to the operator so that the status of the payload
can be determined. [SSS151]

20

3.2.2.2.1 Payload Control Task
The TCS shall permit the operator to control the payload using all methods supported by the payload
installed in the selected AV. [SSS152]
The TCS shall provide a graphical user interface display for the purpose of controlling the payload.
[SSS153]
The TCS shall provide override of payload automated as well as preprogrammed inputs. [SSS154]
3.2.2.2.2 Payload Monitoring Task
TCS shall provide the capability to monitor payload adherence to the uplinked mission plan. [SSS155]
3.2.2.2.2.1 Payload Monitoring Displays
The TCS shall display the current search footprint and the search history of the payload on the map.
[SSS157]
3.2.2.3 Data Terminal Control And Monitoring Capability
The TCS shall have the capability to simultaneously control and monitor a line-of-sight as well as a BLOS
data terminal. [SSS158]
The TCS shall provide the system functionality necessary to record data obtained via the data link.
[SSS527]
3.2.2.3.1 Data Terminal Control Task
The TCS shall be capable of interfacing with the specified data terminal and issuing data link terminal
commands required to establish, control, and maintain the data link with a selected AV. [SSS159]
Data terminal control shall include, but is not limited to, antenna pointing control, transmitter control, and
receiver control. [SSS160]
The TCS shall be capable of automatically selecting the proper mode of operation for the selected data
terminal. [SSS161]
As a minimum the TCS LOS data terminal control modes shall include acquisition, autotrack, search,
manual point, omni directional, as well as directional modes of operation, if applicable to the selected data
link. [SSS162]
The operator shall be able to manually override any automatic data terminal control mode selection if
desired, except during Emission Control (EMCON) and Hazards of Electromagnetic Radiation to Ordnance
(HERO) conditions. [SSS163]
The TCS shall support a LOS data link and SATCOM data link capability. [SSS164]

21

For shipboard operations, the TCS shall provide the capability to switch to a second LOS antenna, if a
second antenna is available, when desired (e.g. the currently active antenna is masked by shipboard
obstructions). [SSS116]
The TCS shall provide the capability to switch to a SATellite COMmunication (SATCOM) antenna, if the
selected AV has SATCOM capability, when desire (e.g. the AV proceeds beyond LOS range as well as
when LOS is obstructed). [SSS117]
The TCS shall provide an interactive display for the purpose of controlling the data link terminal.
[SSS165]
3.2.2.3.1.1 Antenna And Pedestal Control

The TCS shall provide automatic pointing commands for directional antennas [SSS167], and shall allow
for the manual pointing of directional antennas when desired by the operator [SSS168].
The TCS shall be capable of positioning antennas to maintain LOS as well as SATCOM. [SSS170]
The TCS shall incorporate antenna pedestal 3 -axis stabilization to compensate for platform (e.g. ship, or
HMMWV) motion, if applicable. [SSS557]
3.2.2.3.1.2 Transmitter And Receiver Control

The TCS shall be capable of automatically controlling the transmitter and receiver functions of the selected
data terminal. [SSS171]
The operator shall be able to manually override the automatic function selection of the selected data
terminal, if desired. [SSS172]
The TCS shall be capable of automatically controlling the transmitter and receiver modes of the selected
data terminal. [SSS173]
The operator shall be able to manually override the automatic mode selection of the selected data terminal,
if desired. [SSS174]
The TCS shall be capable of automatically controlling the transmitter and receiver frequencies of the
selected data terminal. [SSS175]
The operator shall be able to manually override the automatic frequency selection if desired. [SSS176]
3.2.2.3.2 Data Terminal Monitoring Task
The TCS shall receive, process, and present status data to the operator so that the status of the data
terminal and the supported AV data link can be monitored. [SSS177]
The TCS shall be capable of monitoring and displaying the signal strength of the received and transmitted
signals for the selected data terminal. [SSS178]

22

The TCS shall be capable of monitoring and displaying the signal quality of the received and transmitted
signals for the selected data terminal. [SSS179]
The TCS shall be capable of presenting to the operator a visual depiction of the minimum and maximum
data link operational ranges. [SSS180]

3.2.3 Payload Product Management Function
The TCS will have the functionality necessary to manage all aspects of payload product handling to include
receiving, processing, displaying, and performing limited exploitation. The payload product includes the
payload sensor output and the appropriate AV and payload telemetry data.
3.2.3.1 Payload Product Processing Capability
The TCS shall have the functionality to process payload product data from Electro Optical (EO), Infrared
(IR), and Synthetic Aperture Radar (SAR) payloads. [SSS182] This functionality, as a minimum, shall
include: formatting, storing, internally routing, and recording the video [SSS190]; creating and storing a
freeze frame of the video [SSS191]; retrieving and displaying the video [SSS192]; printing a hard copy of
freeze frame video [SSS193]; and processing digital imagery for export and dissemination [SSS194].
Payload data includes the digital and analog imagery and associated telemetry sent to the TCS from each of
these payloads.
The TCS shall be able to store up to 24 hours of payload data. [SSS184] External storage can be utilized
for this purpose.
The TCS shall be in compliance with Common Imagery Ground Surface Station (CIGSS), United States
Imagery Standards (USIS), Video Working Group Standards Architecture, National Imagery Transmission
Format (NITF) Version 2.0, and Global Command Control Systems (GCCS) when processing payload
imagery data. [SSS185]
The NITF 2.0 imagery files generated by the TCS shall contain the necessary telemetry and support data to
permit subsequent imagery exploitation by C4I systems. [SSS186]
The TCS shall have a built-in text entry capability including the ability to annotate textual information on
imagery. [SSS187]
The TCS shall be capable of receiving secondary HAE UAV payload imagery. [SSS188]
Payload telemetry data shall be available to support other TCS functions as required. [SSS189]
3.2.3.2 Payload Product Display Capability
The TCS shall display live and recorded imagery data, with as well as without annotation and overlay,
upon operator request. [SSS195] Annotation includes operator generated comments as well as graphics
which are superimposed on the imagery. Overlays consist of information obtained from external sources
that is selected by the operator for presentation with the imagery.

23

The TCS shall provide the capability to simultaneously view imagery as well as data from more than one
payload, when applicable. [SSS537]
The TCS operator shall be able to select the content of the overlay information. [SSS196]
The TCS shall have the capability to select and deselect several types of cross hairs (or other similar
ICON) to identify a selected point on a target. [SSS197]
RS170A video and digital imagery shall be routed to TCS functions and displayed upon operator request.
[SSS198]
3.2.3.3 Payload Product Exploitation Capability
The TCS shall have the functionality to conduct limited exploitation, to include voice and textual reporting
for spot and mission objectives, on the payload product data. [SSS200] Limited exploitation, as a
minimum, will include image enhancement and annotation.
The image enhancement capability shall include contrast, brightness, edge enhancement, and sharpness.
[SSS201]
The TCS shall provide the capability to capture frozen-frames of imagery and store these frozen images for
further review and processing. [SSS202]
The TCS shall have the capability to display Near-Real Time (NRT) imagery to include, as a minimum,
date/time group, target location coordinates when the target is in the center of the field of view, north
seeking arrow, and AV position and heading. [SSS203]
The TCS shall provide the capability to compute the range and bearing between two geographic positions
located on the payload imagery display. [SSS560]

3.2.4 Targeting Function
The TCS will have the functionality to determine target coordinates, and estimate target coordinate
accuracy.
The TCS shall support a target location function where the operator can request the current ground location
of the payload field-of-view center. [SSS206]
3.2.4.1 Target Coordinate Development Capability
The TCS shall have the functionality to determine the location of items of interest within the payload field
of view, and express these locations in coordinates acceptable for military applications. [SSS207]
3.2.4.2 Target Accuracy Estimation Capability
The TCS shall have the functionality to develop an estimate of the error in computed target coordinates,

24

and associate the error estimate with the appropriate target. [SSS208]

3.2.5 C4I System Interface Function
The TCS shall be capable of entering DII-COE compliant (C4I) networks. [SSS209] Network
interoperability will include, but not be limited to:
Advanced Tomahawk Weapons Control Station (ATWCS)
Advanced Field Artillery Tactical Data System (AFATDS)
All Source Analysis System (ASAS)
Automated Target Hand-off System (ATHS)
Closed Circuit Television (CCTV)
Common Operational Modeling, Planning, and Simulation Strategy (COMPASS)
Contingency Airborne Reconnaissance System (CARS)
Enhanced Tactical Radar Correlator (ETRAC)
Guardrail Common Sensor/Aerial Common Sensor (ACS) Integrated Processing Facility (IPF)
Intelligence Analysis System (IAS)
Joint Deployable Intelligence Support System (JDISS)
Joint Maritime Command Information System (JMCIS)
Joint Service Imagery Processing System – Air Force (JSIPS-AF)
Joint Service Imagery Processing System - Navy (JSIPS-N)
Joint Surveillance Target Attack Radar System (JSTARS) Ground Station Module/Common
Ground Station (GSM/CGS)
Modernized Imagery Exploitation System (MIES)
Service Specific Mission Planners
-

Army Mission Planning System (AMPS)

-

Air Force Mission Support System (AFMSS)

-

Tactical Aircraft Mission Planning System (TAMPS)

Tactical Exploitation Group (TEG)
Tactical Exploitation Systeme (TES)
Theater Battle Management Core System (TBMCS)
TROJAN Special Purpose Integrated Remote Intelligence Terminal (SPIRIT) II
The TCS shall have the functionality necessary to manage all aspects of C4I system interfaces to include
receiving, processing, and transmitting tactical information to include but not limited to character based
text messages, NITF 2.0 imagery files, and RS-170A video. [SSS210]
The TCS shall provide the functionality necessary to interface with various C4I systems in order to satisfy
the operational requirements for: [SSS211]

25

1. Tasking TCS to plan and conduct a mission.
2. Presentation of payload product and target coordinates for export and dissemination.
