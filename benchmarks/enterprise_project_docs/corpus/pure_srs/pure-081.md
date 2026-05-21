# 1999 - tcs - 7) TCS Version Description Document(s) (VDD)

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 7) TCS Version Description Document(s) (VDD)

7) TCS Version Description Document(s) (VDD)

3.12.2 Materials
TCS material factors shall be governed by the NDI, GFE and COTS specifications developed by the
equipment manufacturers, where applicable. [SSS431]

3.12.3 Electromagnetic Radiation
During Phase 1, control techniques to minimize electromagnetic interference, emanation, and susceptibility
shall be used in the design of TCS equipment. [SSS432] This control will be inherent in the design of the
TCS and the electrical and electronic equipment components and assemblies thereof.
The susceptibility to coupling and the propagation of Electromagnetic Interference (EMI) will be minimized
by component location, cable routing, and judicious use of shielding.
There shall be neither unacceptable response nor malfunction of any TCS and associated equipment due to
EMI produced by any as well as all of the TCS and equipment associated with the TCS. [SSS434]
The TCS shall be compatible with the external electromagnetic environment that is typical of the service
specific environment in the TCS will be operated. [SSS435] The specific electromagnetic environment
values will be determined during Phase I of the TCS development.
The TCS design shall ensure that personnel, fuel, and ordinance are not exposed to electromagnetic
radiation as a result of operating the TCS. [SSS436] The specific radiation hazard (RADHAZ) and
HERO values will be determined during Phase I of the TCS development.
As TCS transitions into Phase 2, electromagnetic radiation safety and operation specifications will be
invoked in the LRIP specification.

3.12.4 Software
Newly designed software shall be developed in accordance with a tailored MIL-STD-498. [SSS437]
Software written for other systems shall be used in TCS where it is determined that the existing software is

50

suitable for use within the TCS software. [SSS438]
A modular architecture shall be used by the TCS software in order to support future interoperability with
multiple types of UAVs and payloads while maintaining consistent displays and user interfaces. [SSS439]
Software components satisfying common planning and control functions will allow for vehicle specific
components to be integrated in the future.

3.12.5 Hardware
TCS hardware flexibility and expansion shall be provided through use of GFE, NDI and COTS hardware
designed to be upgraded and expanded. [SSS440]

3.12.6 Responsiveness
After emplacement at the operational site, the TCS shall be capable of planning and launching a mission
within 1 hour of tasking. [SSS441] Required activities include 1) mission planning of a minimum 1
waypoint mission, 2) preparing 2 AVs for flight, 3) data terminal set-up, 4) safety equipment emplaced, 5)
and a single AV launched.

3.12.7 Endurance
The TCS shall be capable of operating continuously in functional Operation Mode for a minimum of 72
hours. [SSS442]

3.13 Personnel-Related Requirements
3.13.1 Human Factors Engineering (HFE)
The TCS shall have ergonomically designed operator controls and displays for the 5th percentile female to
95th percentile male operator. [SSS443]
The controls shall allow the air vehicle and payload operators to perform mission control, mission
monitoring, and mission updates and modifications while wearing cold weather clothing and in a Mission
Oriented Protective Posture. [SSS444]
The TCS shall provide the operator a caution and warning diagnostic when the TCS system has identified a
malfunction. [SSS445]
The TCS shall have monitor(s) that allow reading of displays under direct sunlight and low light level
environments. [SSS446]
The TCS HCI shall be a Graphical User Interface (GUI) based on X-windows and Motif. [SSS447]
When performing a given task during mission execution, the operator shall be given appropriate warning
messages from other concurrently-executing subsystem tasks. [SSS448]

51

TCS Warning messages shall be color coded and flashed based on mission criticality. The color codes and
flash frequencies will follow MIL-STD 1472 guidelines. [SSS449]
The TCS operator shall be required to enter an acknowledgment prior to disabling the display of critical
warning flags for any AV, Payload, ADT, GDT, and TCS faults. [SSS450]
A combination of visual and auditory outputs will be provided to alert the TCS operator to situations which
may require operator response.
Visual alerts to the TCS operator shall be in the form of a displayed message box that has a display
priority greater than other existing windows to ensure that it is viewable immediately by the operator.
[SSS452] The position of the displayed message window shall be easily adjustable by the operator to
ensure that important mission data is not obscured. [SSS453]
In addition to displayed alert messages to the TCS operator, auditory alerts to include tones shall also be
provided. [SSS454] The volume of these auditory tones shall be adjustable by the operator via keyboard
and trackball input to at least 20dB above the speech interference level at the operator’s ear. [SSS455]
All TCS warning messages and HCI actions shall be archived for later review. [SSS456]
All TCS operator inputs shall be error checked such that any erroneous operator entry will not cause
current processing to terminate. [SSS457] The HCI shall prompt the operator for a valid input. [SSS458]
Display jitter and flicker shall not be perceptible by the operator. [SSS459]
The operational tasks to be performed concurrently by the operator during normal operation will be
determined by appropriate task analysis and function allocation.
The TCS shall facilitate Human-Computer Interfaces (HCIs) that support operation of all system modes,
functions, and capabilities. [SSS461]
The Human Computer Interface (HCI) shall be designed and implemented in accordance with the TCS HCI
Specification, TCS 108.[SSS462]
The HCI shall provide redundancy in all operations, so that the loss of any one HCI input device does not
prohibit operation of any TCS function. [SSS463]
The TCS shall provide the functionality to display all HCI elements on any available monitor on the TCS
workstation. [SSS464]
The TCS shall be capable of displaying a window within a window format to include, as a minimum,
displaying a video window overlaid on a map screen as well as a map screen overlaid on a video screen.
[SSS465]
The TCS shall provide full complementary control operations from the keyset as well as the X/Y control
device (e.g., trackball, mouse, joystick). [SSS466]
The TCS shall provide access to the DII Style Manager so that pointing device characteristics can be

52

modified. [SSS467]
The shall provide the functionality to have a maximum delay time of 1 second from operator command to
system acknowledgement and response.[SSS 559]
The TCS shall provide a capability for porting an off-the-shelf, complex control joystick with multiple
toggle and multi-position switches as part of the TCS hardware suite. [SSS468]
The TCS shall use graphical representations to convey information, such as system status, C4I links, and
AV-GDT links. [SSS469]
The TCS shall provide for multi-level information display tailoring by the operator. [SSS470]
The TCS shall provide automated TCS system information, control options, and logical & simple operator
guidance and support for immediate and adaptive responding to crisis situations. [SSS471]
The TCS shall provide maximum automated system software support to system status monitoring and
alerting of the TCS operator when a preset system parameter goes under as well as over a set threshold.
[SSS472]
The TCS shall provide the necessary processing, display, and control capabilities to ensure dynamic
situational awareness input to the TCS operator. [SSS473]
The TCS shall minimize alphanumeric data display in favor of graphic, pictorial information display
[SSS474]
The TCS HCI shall provide unambiguous AV and payload control and status feedback indicators to ensure
safe, efficient operations of two AVs and their payloads by a single TCS station. [SSS475]
The TCS shall provide for a specific icon shape on a constant contrast background, as well as other visual
information coding mechanisms, to cue the TCS operator regarding which UAVs are under his or her
primary control. [SSS476]
The TCS HCI shall provide the capability to select and amplify an object and point on a map as well as
payload screen. [SSS477]
The TCS HCI shall provide coarse and fine payload control capabilities directly on the payload screen.
[SSS478]
The TCS HCI shall display the SAR imaging swath on the map display. [SSS479] The TCS HCI shall
provide the on-screen capability to select and efficiently move as well as reorient a previously defined SAR
imaging swath. [SSS480]
The TCS HCI shall provide the capability to lock onto and hold a coordinate point on the payload imagery
window. [SSS481]
The TCS HCI shall provide the capability to display operator definable “Lock Out” zones around
waypoints, Launch and Recovery Point (LRP), as well as any selected point on the AV flight path.

53

[SSS482]
The TCS HCI shall provide for a rapid means to cancel aural warnings. [SSS484]
The TCS HCI shall provide for separation, grouping, and visual coding of multiple categories of alerts, to
include Warnings, Cautions, and Advisories. [SSS485]
The TCS HCI shall provide for visual Warnings, Cautions, and Advisories to be displayed at or near the
center of the field of view, i.e., within a 30o cone, of all monitors in a TCS system. [SSS486]
For AV safety as well as mission-critical Warnings, the TCS HCI shall provide a default selection as well
as an override option, along with a selection of adaptive responses, and the minimum information necessary
to assist the operator in responding quickly and adaptively to the emergency. [SSS487]
The TCS HCI shall provide for on-screen information to include, as a minimum, overlays, headers,
cursors, alphanumeric annotation, waypoints, crosshairs, designed to be visible against the complete
spectrum of map and payload video backgrounds. [SSS488]
The TCS HCI shall provide continuously-available, on-screen control functions for time and missioncritical operations, to include as a minimum print, freeze, declassification, mark VCR, declutter, cease RF
transmission. [SSS489]
The TCS HCI shall provide for the capability to automatically designate target locations from the payload
screen onto the map screen. [SSS490]

3.14 Training Related Requirements
Formal training programs shall not be required for TCS Phase 1, Program definition and Risk Reduction.
Trained and proficient personnel from the Original Equipment Manufacturers, Government Engineering
Teams, supporting Contractors, and Military Personnel will support the operation and maintenance of the
demonstration system equipment throughout Phase 1.
TCS training and training support shall include the processes, procedures, techniques, training devices and
equipment to train civilian, active duty and reserve military personnel to operate and support the TCS
system. [SSS491] This will include: individual and crew training; new equipment training; initial, formal,
and on-the-job training. TCS training will strike a balance between institutional, new equipment and unit
training.
The TCS system shall provide, for the operator and maintainer, an embedded or add-on interactive training
courseware with self-paced instruction, duplicating UAV flight performance characteristics, capabilities,
and limitations. [SSS492] The OUTRIDER TCS system shall be compatible with the U.S. Army
Intelligence and Electronic Warfare Tactical Proficiency Trainer as an objective. [SSS493]
The interactive courseware training capability for TCS shall be developed during Phase I and introduced to
the user during scheduled demonstrations and tests. [SSS494]
The training capability for performance of TCS functions shall include primary mission (flight

54

route/payload) planning, mission control and monitoring, imagery processing, tactical communications, AV
control communications and TCS system on line diagnostics. [SSS495] This capability will be qualified
and improved during Phase I based upon use and feedback from qualified operators and users
demonstrating TCS system equipment throughout Phase I. Instructional support materials and training
courseware for classroom discussion and lecture will be developed to support institutional, new equipment
training and unit training.
The TCS shall provide the functional capability to train in the operation of the TCS system, performance of
TCS UAV functions, and on line system troubleshooting. [SSS496]
TCS system training shall include system architecture, component familiarization, and system startup,
initialization, system recovery and shutdown. [SSS497]
The TCS system shall not support formal Training operations concurrent with the execution of an actual
mission. [SSS499] The capability for the conduct of actual communications processing concurrently with
Training operations shall be provided if and only if messages are identified as training messages. [SSS500]
Training shall be adequate to maintain operator and maintainer skills and proficiencies. [SSS501]
TCS shall record operator and maintainer actions for self assessment and performance enhancement.
[SSS502]
Operator and maintainer performance shall be measurable using parameters retrievable from the TCS to
determine proficiency levels. [SSS503]

3.15 Logistics-Related Requirements
During Phase 1, TCS logistic support requirements will be based on known and predicted failure rates of
components, and the criticality of those elements to the system development and flight test processes.
Logistic requirements for Phase 2 will be determined and incorporated into LRIP requirements and
specifications.
Support for the TCS shall be in accordance with the Integrated Logistical Support Plan (ILSP) and the
maintenance concepts and policies of the individual Services. [SSS504]
All TCS Operator Manuals and Technical Manuals shall be verified and validated prior to initial
operational test. [SSS529]
TCS transport and storage containers shall be reusable and enable the operators to set-up equipment within
the established timelines in their ORDs. [SSS505]
The TCS shall adhere to DoD regulations and policy governing military standards for logistics, Petroleum,
Oil and Lubricants (POL), Test, Measurement, and Diagnostic Equipment (TMDE), tools, and other
support items. [SSS506]
Standard tools, TMDE, repair parts, and lubricants shall be used to maintain the TCS. Exceptions shall be
considered on a case by case basis. [SSS507]

55

Each Service shall support the TCS as part of the UAV system which is organic to them. [SSS508]
The TCS shall be maintained in accordance with the UAV ORD for that Service and the level of repair
analysis for the hardware chosen. [SSS509]
A TCS support and fielding package shall be developed and available for operational testing. [SSS510]
The TCS shall be maintained in accordance with Services’ approved UAV maintenance concepts and
procedures. [SSS511]
To the maximum extent possible, general purpose test equipment (GPTE) and common tools resident in
each service shall be used to perform all corrective and preventative maintenance at all authorized levels of
maintenance. [SSS512]
Tools and test equipment required to maintain the TCS but not resident in each service inventory shall be
identified as special tools and special purpose test equipment (SPTE), respectively, and kept to a minimum.
[SSS513]
The environmental support required by the TCS shall be at least the same as that required for the respective
UAV System. [SSS514]
Basing for the system will follow the plan for UAV units and service command echelon requirements as
delineated in the ORD. [SSS515]

3.15.1 Transportability
The TCS shall meet the deployment criteria for the organic unit to which it is assigned. [SSS516]
The TCS shall be transported into the theater as an organic component of the operational UAV system
being deployed. [SSS517]
TCS transportation in theater for Army and Marine Corps systems shall be by ground, air, as well as rail
transportable. [SSS518]
For the Air Force, TCS transportation to the theater shall be by air. [SSS519] Within the theater, the
USAF GCS shall be capable of being moved around an established air field. [SSS520]
3.15.1.1 Ground
The TCS shall be ground transportable. [SSS521]
3.15.1.2 Air
The TCS shall be air transportable by helicopter (CH-47/CH-53D) and C-130 drive-on/drive-off capable.
[SSS522]

56

3.15.1.3 Sea
The TCS shall be sea transportable. [SSS523]
3.15.1.4 Rail
The TCS shall be rail transportable. [SSS524]
3.15.1.5 Preparation Time
The TCS shall be configurable for sea, ground, as well as air transport in 2 hours or less. [SSS525]
The TCS system shall be capable of being de-configured from sea, ground, as well as air transport and
ground-mobile in 2 hours or less. [SSS526]

3.16 Other Requirements
The TCS shall have an objective capability to be integrated and operated from tactical and command and
control aircraft. [SSS531]
The TCS shall have an objective capability to be integrated and operated from submarines. [SSS532]
The TCS shall have a capability to be integrated and operated from land based platforms. [SSS533]
The TCS shall have an objective capability to be integrated and operated from ships. [SSS534]

3.17 Packaging Requirements
This section not applicable, therefore tailored out.

3.18 Precedence And Criticality Of Requirements
All requirements in this specification are of equal weight and criticality unless otherwise identified in the
traceability Table in Appendix A.
When the requirements of the Operational Requirement Document (ORD), this System/Subsystem
Specification (SSS), other related requirement documents, and referenced documents are in conflict, the
following precedence will apply:
7. TCS ORD – The ORD shall have precedence over any other TCS documentation.
8. TCS SSS – This SSS shall have precedence over other requirements documents except item (1.)
above.
9. Other TCS requirement documents – Other requirement documents shall have precedence over
any referenced documents.
10. Referenced documents – Documents referenced herein and in other TCS requirement documents
shall have precedence over all applicable subsidiary documents referenced therein.

57

In the event of conflicting requirements within a TCS requirement document, the requirements shall be
traced to the next higher precedence requirement document for clarification. If further resolution is
required, the developer will notify the procuring agency.

58

11.QUALITY ASSURANCE PROVISIONS
12. Responsibility for Inspections.
The Quality Assurance (QA) Program is an integral part of the development process for the TCS , whereby
all phases of the development of a system must be inspected and tested, as these phases occur. The
objectives and processes of the QA Program applicable to this development effort are contained in the TCS
Integration Program Quality Assurance Plan, NSWCDD/TR-96/XXX.

13. Special Tests and Examinations.
Verification of requirements will be accomplished by the use of appropriate combinations of inspections,
analyses, demonstrations and tests. The method to be used for verification of each requirement is identified
in Appendix B. The following defines verification methods as used in this specification:
