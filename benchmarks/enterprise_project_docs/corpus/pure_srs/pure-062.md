# 1999 - tcs - Chapter 1 Scope

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: Chapter 1 Scope

Chapter 1 Scope
1.1 Identification
This TACTICAL CONTROL SYSTEM (TCS) - SYSTEM / SUBSYSTEM SPECIFICATION (SSS) VERSION 1.0 identifies, specifies, and establishes the detailed system requirements for the Tactical
Control System as set forth by the OPERATIONAL REQUIREMENTS DOCUMENT FOR THE
UNMANNED AERIAL VEHICLE (UAV) TACTICAL CONTROL SYSTEM (TCS) - VERSION 5.0.
The SSS further specifies the methods to be used to ensure that each requirement has been met.
Requirements pertaining to the TCS external interfaces are covered in separate Interface Design
Descriptions (IDDs) to be published. The SSS is published IAW DID DI-IPSC-81431, dated 941205.

1.2 System Overview
The purpose of the TCS is to provide the military services with a single command, control, data receipt,
data processing, data export and dissemination system that is interoperable with the family of all present
and future tactical unmanned aerial vehicles. These UAVs shall include the Tactical Unmanned Aerial
Vehicle (TUAV) and the Medium Altitude and Endurance (MAE) UAV (henceforth referred to as Outrider
and Predator respectively), their associated payloads, and other network communication systems. TCS will
also be capable of receiving and processing information from High Altitude and Endurance (HAE) UAVs,
their associated payloads, future development UAVs and payloads.

1.2.1 TCS Program, Phases, and UAV Interaction
The Unmanned Aerial Vehicle Joint Project Office (UAV JPO) has undertaken development of a TCS for
UAVs. Design and development of the TCS will be conducted in two phases. Phase 1 is defined as the
Program Definition and Risk Reduction phase, and Phase 2 is defined as the Engineering and
Manufacturing Development phase in accordance with Department Of Defense Instruction (DODI) 5000.2R. During Phase 2, TCS Low Rate Initial Production (LRIP) will commence. Phase 1 will be a 24
month period and will demonstrate Level 1 through Level 5 interaction (as defined below) in an Incremental
and Evolutionary strategy as described in accordance with MIL-STD-498. The five discrete levels of
multiple UAV interaction to be provided by the TCS are:
Level 1: receipt and transmission of secondary imagery and/or data
Level 2: direct receipt of imagery and/or data
Level 3: control of the UAV payload in addition to direct receipt of imagery/data
Level 4: control of the UAV, less launch and recovery, plus all the functions of level three
Level 5: capability to have full function and control of the UAV from takeoff to landing

1

1.2.2 Tactical Control System
The TCS consists of the software, software-related hardware and the extra ground support hardware
necessary for the control of the Outrider, and the Predator UAV, and future tactical UAVs. The TCS will
also provide connectivity to specifically identified Command, Control, Communications, Computers, and
Intelligence (C4I) systems. TCS will have the objective capability of receiving High Altitude Endurance
(HAE) UAV payload information. Although developed as a total package, the TCS will be scaleable to
meet the user's requirements for deployment. TCS will provide a common Human-Computer Interface
(HCI) for tactical airborne platforms to simplify user operations, training, and facilitate seamless
integration into the Services’ joint C4I infrastructure across all levels of interaction.
1.2.2.1 Software
The major focus of the TCS program is software. The software will provide the UAV operator the
necessary tools for computer related communications, mission tasking, mission planning, mission
execution, data receipt, data processing, limited data exploitation, and data dissemination. The software
will provide a high resolution computer generated graphical user interface that enables a UAV operator
trained on one system to control different types of UAVs or UAV payloads with a minimum of additional
training. The TCS will operate in an open architecture and be capable of being hosted on computers that
are typically supported by the using Service. Software developed will be Defense Information
Infrastructure / Common Operating Environment (DII/COE) compliant, non-proprietary, and the
architectural standard for all future tactical UAVs. To the extent possible, the TCS will use standard
Department of Defense (DoD) software components to achieve commonality. TCS will provide software
portability, scaleable functionality, and support for operational configurations tailored to the users’ needs.
1.2.2.2 Hardware
To the extent possible, the TCS will use standard DoD components in order to achieve commonality. The
TCS will use the computing hardware specified by the service specific procurement contracts. The
individual armed services will identify TCS computing hardware, the desired level of TCS functionality,
the battlefield C4I connectivity, and the particular type of air vehicle and payloads to be operated
depending upon the deployment concept and area of operations. TCS hardware must be scaleable or
modular to meet varying Service needs. TCS hardware will permit long range communications from one
TCS to another, data storage expansion, access to other computers to share in processing capability, and
multiple external peripherals.

1.2.3 Integration with Joint C4I Systems
TCS integration with C4I systems will be accomplished through development of interfaces that permit
information exchange between the TCS and specified C4I systems. TCS will be capable of entering
DII/COE compliant networks. Network interoperability will include but not be limited to:
Advanced Tomahawk Weapons Control Station (ATWCS)
Advanced Field Artillery Tactical Data System (AFATDS)
All Source Analysis System (ASAS)
Automated Target Hand-off System (ATHS)

2

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
Table 3.3.1.1-1 shows the planned implementation schedule for C4I interface realization. The TCS will
export and disseminate UAV imagery products, tactical communication messages, as well as mission plans
and target coordinates. The TCS will also receive, process, and display tasking orders, and operational
information from Service specific mission planning systems.

1.2.4 System Compliance
The TCS will be developed in compliance with the following military and commercial computing systems
architecture, communications processing, and imagery architecture standards:
a) Defense Information Infrastructure (DII) / Common Operating Environment (COE)
b) Computer Open Systems Interface Processor (COSIP)
c) Common Imagery Ground/Surface System (CIGSS) Handbook
d) Variable Message Format (VMF) and Joint Message Format (JMF)
e) National Imagery Transmission Format (NITF)
f) Assistant Secretary of Defense (ASD) (C3I) Joint Technical Architecture (JTA)

3

1.3 Document Overview
This section has been tailored out. See Table of Contents.

4
