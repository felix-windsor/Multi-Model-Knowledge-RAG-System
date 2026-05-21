# 1999 - tcs - 8. Uninterruptible Power Supply

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - tcs.pdf

Section: 8. Uninterruptible Power Supply

8. Uninterruptible Power Supply

3.4.1 AV Standard Interface
The TCS shall implement an AV Standard Interface that will provide the proper data format to ensure
communications with the selected AV. [SSS322] This interface shall allow for addition of future AVs and
will provide the generic architecture to ensure interoperability. [SSS323]
The uplink and downlink information passed between the TCS and the AV shall be in accordance with the
associated AV documentation. [SSS324]
The TCS shall support a concurrent uplink and downlink capability. [SSS325]
The AV Standard Interface requirements and specifications will be defined in the AV Standard IDD, TCS
229 .
The AV Standard Interface is designated as a mission and safety critical interface for the TCS.

3.4.2 Real Time Processor
The TCS shall provide an internal interface for establishing communications with the Real Time Processor
(RTP) within TCS. [SSS326]
This interface shall allow the information from the data server to be made available to other components of
the TCS. [SSS327]
The RTP interface shall support distributed processing capability. [SSS328]
The RTP interface requirements and specifications will be defined in the Data Server IDD, TCS 238.
3.4.2.1 Distributed Processing
Remotely hosted applications shall communicate in a client server relationship via the defined data server
interface. [SSS329]

3.4.3 SAR Processor
The TCS shall provide an internal interface for the SAR Processor in order to disseminate SAR
information (to include imagery and telemetry) to other components of the TCS. [SSS330]
The SAR Processor interface requirements and specifications will be defined in the TCS to SAR Processor
IDD, TCS 240.

3.4.4 Intercom
The TCS shall incorporate an intercom system that provides verbal communicate in the situation where

39

there are multiple operators. [SSS331]
The intercom system shall be compatible with service specific voice communication systems. [SSS332]
The intercom interface requirements and specifications will be defined in the TCS to Intercom IDD, TCS
253.

3.4.5 VCR
The TCS will provide an interface between the TCS and a video cassette recorder.
The TCS shall allow the Operator(s) to fully control the VCR via the TCS Display input device(s).
[SSS334]
The TCS shall be able to route VCR recorded payload video to the C4I Interfaces. [SSS335]
An RS-170A video interface shall be provided for the system to output and input analog imagery and
overlays to and from a Video Cassette Recorder (VCR) for recording and playback. [SSS336]
Details of the VCR interface will be defined in the TCS to VCR IDD, TCS 246.

3.4.6 Printer
The TCS shall have ports for outputting data and imagery to an internal hard copy printer. [SSS337]
The TCS shall, as a minimum, allow the Operator(s) to print freeze-frame video, C4I Messages, Mission
Plans, FD/L information, and current map display to an internal printer. [SSS338]
Details of the printer interface will be defined in the TCS to Printer IDD, TCS 255.

3.4.7 Data Storage Devices
The TCS shall be able to access data storage devices. [SSS339]
The TCS shall have the functionality to transfer digital data as well as digital imagery to and from data
storage devices. [SSS340]
3.4.7.1 CD Drive
The TCS shall provide a CD drive for the retrieval of TCS data. [SSS341]
3.4.7.2 Tape Drive
The TCS shall provide a tape drive for storage and retrieval of TCS data. [SSS342]

40

3.4.7.3 Redundant Array Of Inexpensive Disks (RAID)
The TCS shall provide a RAID for storage and retrieval of TCS data, if required. [SSS343]

3.4.8 Uninterruptible Power
The TCS shall have an interface to an uninterruptible power supply. [SSS344]
