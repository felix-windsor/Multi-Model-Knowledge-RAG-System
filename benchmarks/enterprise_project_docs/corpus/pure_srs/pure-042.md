# 1995 - gemini - 5. IOC software development is to be done using a common development environment, as

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 5. IOC software development is to be done using a common development environment, as

5. IOC software development is to be done using a common development environment, as
specified in the Software Programming Standards (SPS)

C.Software below the IOC level. There is likely to be software below the IOC level, but it
should not require downloading, except possibly for upgrades, typically being placed into
ROM or FLASH memory.
Any access to this embedded software while it is connected to the system is strictly
through software in the IOC. From outside the IOC this software appears as part of the
electronics.
Although this software is not considered part of the Gemini software, it is obviously an
advantage (for maintenance purposes) to have it conform to the requirements of Gemini
software.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

D.Installation system software.. The host workstation operating system is Unix, currently baselined as Solaris 2.3 or above.
The installed target IOC operating system is VxWorks, with EPICS as the interface.

Details of these standards can be found in the Software Programming Standards document.

These are defined in the Gemini Configuration Control Plan.

The following recommendations are made:

A.Communication hardware independence is accomplished by using the DARPA
TCP/IP communication protocol over LAN's and the WAN.

B.The communication software must support the standard ARPA services (telnet, FTP,
SMTP, etc) as well as NFS, RPC, IPC, and the Unix socket interface library.

The recommendations are:

A.The software interface between workstation and IOC is to use DRAMA’s IMP protocol for all control communication, using SDS as the command structure..

B.Interprocess communication on the host workstations is through the same IMP protocol.

C.Communications between real-time components is to based on the EPICS Channel
Access protocol.

D.Data communications are typically through IMP/SDS.
E.Further details of the software interfaces are found in the Software Design Description.

A.Off line Data reduction. The off-line data reduction facility is not considered part of
the Gemini software. However, it will be possible to connect such software into the
Gemini system if interface routines are developed for connecting to the Gemini sys-

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS
tem. These interface routines are part of the Gemini software and must conform to the
standards given in this document. Packages that might be used for off-line data reduction
include ADAM, IRAF, Midas, IDL and Khoros.

B.Quick-look analysis will be through PV-Wave/IDL.
C.Archiving. All astronomical data are saved into the Archiving system. Data storage and
transport for astronomical data will be in FITS format. On-line access to the archiver will
be through STARCAT.

D.Star catalogs. The catalogs available on the Gemini system are described in TBD, as are
software access requirements. Both on-line and off-line access is done according to
STARCAT.

Astronomical data are stored both in the Archiving system and in the data storage subsystem.
IOC control databases are distributed across the IOC subsystems, with down-loadable initialization copies available on the Gemini disks.
Configuration, logging, maintenance schedules, and subsystem documentation are to be
kept in the commercial relational database.

Only the development systems are considered here. Installed systems are to be chosen
later, based on available technology and experiences with the development systems.

The computer hardware used for development must conform to the following:

A.Workstations must match specified software standards and present a well-designed development environment, including cross-support for VxWorks development, if needed.

B.Workstations are expected to be state-of-the-art systems (CPU, communications support)
in a scaleable family. This allows the migration of development systems to advancing
technology.

C.It is assumed that workstations support Ethernet IEEE-802.3 and FDDI interfaces for
communications.

D.Internal data formats must be compatible across workstations used for development.
E.SCSI-interface peripherals are to be available.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

F.Reliability, manufacturer support, and upgrade capability of the development systems will be considered when selecting the final target systems.

The following recommendations are made:

A.Workstations.
