# 1999 - tcs - 5. improve system availability by the effective selection and incorporation of Built In Test

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 5. improve system availability by the effective selection and incorporation of Built In Test

5. improve system availability by the effective selection and incorporation of Built In Test
Equipment (BITE);
6. allow removal and replacement of replaceable units without soldering and unsoldering.

3.11.4 Availability
The TCS equipment shall achieve an availability (Ao), as defined below, equal to or greater than that which
is specified in the Predator and Outrider ORDs. [SSS413]
Ao = (OT + ST)/(OT + ST + TPM + TCM + TALDT)
where: OT
ST
TPM
TCM
TALDT

denotes Operate Time
denotes Standby Time
denotes Total Preventative Maintenance
denotes Total Corrective Maintenance
denotes Total Administrative and Logistic Downtime

3.11.5 Flexibility
The total, fully useable, addressable, physically present program instruction memory and data storage
memory for each processor shall have at least 50% unused memory during the Normal Operations Mode
over any 10 second period. [SSS414]
The processing speed of each processor shall be such that at least 50% of the throughput of each processor
remains unused over all 10 second periods and at least 20% of the throughput of each processor remains
unused over one second periods regardless of the system function performed. [SSS415]
The I/O channel reserve capability for each processor shall have at least a 50% reserve, addressable and
useable, I/O channel capacity over any 10 second period. [SSS416]
TCS software flexibility and expandability shall be provided through use of the DII COE and through use
of standardized software development practices. [SSS417]

3.11.6 Portability
Hardware and software shall be selected for use in the TCS with the goal of providing ease of future
changes to the TCS elements. [SSS418] The object of portability for the TCS is to select or develop
hardware which will readily host emerging software packages and software which will be as independent of
host hardware as possible.
The selection of processors, interface cards for communication interfaces, disk drives, video, networking
equipment, and all other hardware for use in the TCS shall be made according to standards for production
of an open architecture. [SSS419]

48

The selection of operating system and programming language for use in the TCS shall be made according
to standards for development of an open architecture. [SSS420]

3.11.7 Reusability
This section not applicable, therefore tailored out.

3.11.8 Testability
Testability shall be considered in the design and development of the TCS. [SSS421]
The system shall be functionally and physically partitioned to allow for efficient fault isolation. [SSS422]
Control over internal items and devices shall be provided for detecting and isolating internal faults.
[SSS423]
Test points and data paths shall be defined to support efficient fault isolation. [SSS424]

3.11.9 Usability
This section not applicable, therefore tailored out.

3.12 Design And Construction Constraints
The TCS shall provide the common software architecture for TCS interaction with Predator, Outrider, and
future Tactical UAVs. [SSS425]
In the selection of hardware design solutions to satisfy the requirements herein, Non-Developmental Items
(NDI) (off-the-shelf equipment previously approved for service use) shall be chosen to the maximum
practicable extent. [SSS426] If NDI that provides the desired functions can not be identified, then
Commercial-Off-The-Shelf (COTS) hardware may be used.
During Phase 1, design and construction will be accomplished in accordance with commercial best
practices unless otherwise required to meet a specific service operational environmental factor. Design and
construction requirements for Phase 2 will be revised to reflect appropriate government approved sub-tier
specifications controlling all aspects of electrical and electronic or mechanical designs for new or modified
TCS equipment.

3.12.1 Documentation
System documentation shall be developed as part of the TCS program and will follow MIL-STD-498 for
format. [SSS427]
The documentation developed shall contain sufficient level of detail to identify the functional, operational
and design requirements of the TCS. [SSS428]

49

The documentation shall contain sufficient technical detail to define the hardware and software design
implemented to satisfy the system requirements. [SSS429]
The TCS documentation shall include: [SSS430]
