# 1999 - tcs - 7. Perform Software Debug and Monitoring

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 7. Perform Software Debug and Monitoring

7. Perform Software Debug and Monitoring
Functions, except for software upgrade and software debug, under the Maintenance Operations Mode
shall operate concurrently without precluding or excluding any of the other functions in accordance with
allowable operations as determined by the appropriate levels of interaction. [SSS042]

12

Figure 3.1.2.3-1 shows the functions that exist under the Maintenance Operations Mode.

MAINTENANCE
OPERATIONS

AIR VEHICLE

PAYLOAD

DATA LINK
TERMINAL

WORKSTATION
AND
PERIPHERALS

FAULT
DETECTION/
LOACTION

SOFTWARE
UPGRADE

SOFTWARE
DEBUG

Figure 3.1.2.3-1 TCS Maintenance Mode and Associated Functions Diagram

3.1.3 Shutdown State
Upon the selection of a shutdown command the TCS shall enter the Shutdown State, which will cause the
TCS to be placed in a condition where power can be removed without impacting operations as well as
causing damage to the system, and from which restart of the system can be accomplished normally.
[SSS043]
Shutdown of the TCS shall include storage as well as deletion, as specified by the operator, of mission data
files [SSS044], shutdown of appropriate functions [SSS045], shutdown of HCIs [SSS046], and proper
termination of all active interfaces [SSS047].
There shall be no modes of operation in the shutdown state. [SSS048]

3.2 System Capability Requirements
The TCS will provide the hardware and software necessary to allow the operator to conduct the following
major functions 1) mission planning, 2) mission control and monitoring, 3) payload product management,
4) targeting, and 5) C4I system interface.

3.2.1 Mission Planning Function
The TCS shall have the functionality to allow the operator to generate a UAV mission plan. [SSS050]
The TCS shall have the functionality to receive and process UAV mission plans from service specific
mission planning systems. [SSS053]
The TCS Mission plan shall include all necessary information required to be interoperable with the service
specific mission planning systems including the Tactical Aircraft Mission Planning System (TAMPS),
Aviation Mission Planning System (AMPS), and Air Force Mission Support System (AFMSS). [SSS051]

13

The TCS shall have the functionality to transmit UAV mission plans to service specific mission planning
systems. [SSS055]
The TCS shall facilitate automated processing of mission plan data received via C4I interfaces in order to
extract the appropriate mission planning data. [SSS052]
The TCS shall have the functionality to receive and process UAV mission plans from other TCSs.
[SSS054]
The TCS shall have the functionality to transmit UAV mission plans to other TCSs. [SSS056]
A Mission Plan shall include a Flight Route Plan for a selected AV, a Payload Plan for the selected
payload, and a Communications Plan. [SSS057] A Flight Route Plan is defined in Section 3.2.1.1. A
Communications Plan is Defined in Section 3.2.1.3. A Payload Plan is defined in section 3.2.1.2.
The TCS shall be capable of storing a minimum of 500 mission plans under unique names to allow for later
retrieval. [SSS058]
The TCS mission planning function shall provide a graphical user interface that gives the operator the
ability to define waypoints on a map based display using a pointing device with full keyset redundancy.
[SSS059]
The TCS shall provide the capability to compute the range and bearing between two geographic positions
on the map display. [SSS561].
As an objective, the TCS shall have the capability to import as well as create and modify map display
overlays for fire support coordination measures [SSS547], airspace control measures [SSS548], and threat
identification measures. [SSS060]
Upon completion of radar cross section analysis and characterization by the Government for each UAV
type, TCS shall utilize a UAV signature versus threat lookup table (database) that identities the lethality of
the threat to the UAV [SSS065], and shall provide the capability of displaying aircraft signature versus
threat, before and during flight. [SSS066]
The TCS shall permit dynamic mission and payload retasking during all phases of operational mission
execution. [SSS067]
The TCS shall allow the operator to enter as well as review mission plan parameters, including AV flight
parameters, payload control parameters, data link control parameters, AV VCR control parameters (if
applicable to the selected AV), and AV loiter patterns. [SSS068]

The TCS shall provide the capability to enter system configuration characteristics in the mission plan, to
include selected AV type, AV identification number, selected payload type, ground control authorization
information, and required communications pre-set for data links, tactical communications, and C4I data
dissemination. [SSS069]

14

The TCS shall provide the system functionality necessary to upload a flight route plan and payload plan (if
applicable) to the AV via the selected system data link as well as direct ground connection. [SSS070]
TCS shall provide the capability for the operator to retrieve a mission plan for viewing, modification, as
well as deletion at the operator's discretion [SSS071], and allow the operator to save the mission plan under
a different name, for future retrieval [SSS072].
The TCS shall automatically check the validity of the intended mission plan prior to being uploaded
including altitude constraints, payload constraints, data link range constraints, airspace restrictions, fuel
limitations, threat constraints, data link terrain masking effects, and Loss of Link (LOL) Plan. [SSS073]
The TCS shall notify the operator of all discrepancies found during the mission plan check as well as
indicate successful completion of the mission plan check. [SSS074]
The TCS shall provide the capability to override validation faults after the fault is acknowledged by the
operator. [SSS540]
The TCS shall allow the operator to set the LOL delay timer(s) during mission planning. [SSS075] The
LOL delay is the time from when the AV detects an unplanned LOL to the time it initiates LOL procedures.
The TCS shall provide the capability to print waypoint data in alphanumeric format. [SSS553]
3.2.1.1 Flight Route Planning Capability
The Flight Route Plan, as a minimum, shall include AV flight path information, Loss of Link plan, AV
VCR control tasking (if applicable to the selected AV), and data link control information. [SSS079]
The TCS shall allow the operator to define the desired AV route in waypoint format [SSS551], and shall
provide the capability to include up to 500 waypoints in each flight route plan. [SSS080]
The TCS shall provide the capability to display mission waypoints and flight path graphically. [SSS081]
The TCS shall provide the capability to enter waypoint data in alphanumeric format. [SSS082]
The TCS flight route planner shall include, as a minimum, the following flight planning tools:
1. Weight and balance take off data calculations. [SSS083]
2. Fuel Calculations. [SSS084]
3. Terrain avoidance warning for line of sight flights. [SSS085]
4. Minimum data link reception altitude calculations for line of sight flights. [SSS554]
