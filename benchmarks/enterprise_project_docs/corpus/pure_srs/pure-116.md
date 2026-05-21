# 2001 - elsfork - 6 Plant data

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 6 Plant data

6 Plant data
The following section is a description of principles for representation and storage of data. The
description is not specific and thorough, as it does not specify in detail all signals or data that
must be available. It is the intention of this description to establish rules and principles for
what data and what services shall be available from each wind turbine.

DATA

Figure 3: Wind power plant data
The protocol shall have such flexibility that new data can be defined without disturbing old
versions of equipment’s that comply to a specific version of the specification. A ‘naming convention’ is described in this specification.
6.1 Information structure
Data is represented by a number of attributes. The number of attributes for a specific data may
vary. The number and formats of the attributes sent at configuration time is different than the
number and formats of the attributes that is transmitted in any message (data transmission).
Each wind power plant shall have defined the total set of data, the naming, the type and default value of the data according to this specification. The information should be standardised
according to the following principles:
• Each device or object shall be self-descriptive (generic part) and the system has to have a
function to extract the information contained in the wind power plants objects. It shall be
possible to issue an identify request and get a list of all objects in a wind power plant,
their names and possibly a short description for each object. It should be possible to get
the attributes and services for each object. The list should at minimum include, Name,
Type/Kind, Unit, Time requirements, and possibly a short Description.
• For the HMI such information shall be contained in the device using standard readable
text, such as ASCII or Unicode (UTF16) (at least optional in the language of the operator). The presentation of the information itself is out of the scope of this specification.
• At least for default naming a hierarchical name structure and an object data dictionary
specialised for wind power plants should be used.
• During data transmission the message should at least include the following parts; Name,
Value(s), Scan frequency, Time tag and Quality.

6.1.1 Example: PICOM
This section presents one example of an information structure.
To describe the data being exchanged within a substation the CIGRE WG34.03 has introduced the concept of PICOM (Piece of information for Communication). By definition, it is a
given data element on a given logical path with given communication attributes. The PICOM
Page 19

ELFORSK

can be compared to a "soft wiring". It is used for defining essential features of communicated
data from the application point of view. The main components of a PICOM are summarised
mainly by the term’s data, type, performance, and path.
Data means the content of the information and its identification as needed by the functions
Type describes the structure of the data, i.e. if it’s an analogue or a binary value, if it’s a single value or a set of data, etc.
Performance means the permissible transmission time, the data integrity and the method or
cause of transmission (e.g. periodic, event driven, on demand).
Path contains the logical source and the logical destination
These PICOMs can been used for data type identification.
PICOM attributes to be transmitted at configuration time only (subscription, negotiation, etc.)
Value for transmission (see above): test or default value if applicable
Attributes for transmission (see above)
Format:
data format of the signal : I, UI, R, B, BS, BCD, etc.
Length:
the length: i bit, j byte, k word
Accuracy:
classes of values
Tag information:
if time tagged or not (most data will be time tagged for validation)
Type:
analogue, binary, file, etc.
Kind:
alarm, event, status, command, etc.
Importance:
high, normal, low
Data integrity:
the importance of the transmitted information for checks and retransmissions
PICOM and related attributes to be transmitted in any message (data transmission)
Value:
value of the information itself if applicable
Name:
for identification of the data
Source:
where the signal comes from
Sink:
where the signal goes
Time tag:
absolute time (7 bytes) to identify the age of the data if applicable
Priority of transmission: to be used for input queues or relaying of messages
Time requirements:
cycle time or response times to check the validity with help of the
time tag
6.2 Naming convention
Communication and objects in the wind power plant shall be object based. Gear and generator
could, for instance, be separate objects. Each including measurements, calculated data, and
control services. The system shall be able to manage naming of objects and variables (measurements, etc) in a hierarchical naming system in several levels.

6.2.1 Naming system example
In the following example a naming system with 18 characters is illustrated. The number of
characters may, in other naming systems, be extended, e.g. to handle more than 100 wind turbines.
AN NN BBBNN CCNNN DDNN (here 18 characters used)
First group of letters A followed by a number N

Page 20

Wind power plant, e.g. H1

ELFORSK

Second group of numbers with two digits NN
Third group of letters BBB followed by two digits NN
Fourth group of letters CC followed by three digits NNN
Fifth group of letters DD followed by two digits NN

Number within the wind power plant, e.g. 11
Object or system, e.g. gear MCD01
Component, e.g. temperature sensor CT003
Calculated value, e.g. mean value ZA01, or
signal, e.g. Input XQ01

Number within farm: 12
Number within farm: 11
Variable: Mean value ZA02
Variable: Status [InOperation]

Object/system: Gear MCD02
Object/system: Generator MKD01

Object/system: Gear MCD02
Object/system: Gear MCD01

Component: Temp.sensor CTD004
Component: Temp.sensor CTD003
Variable: Input XQ02
Variable: Input XQ01

Component: Temp.sensor CTD004
Component: Temp.sensor CTD003
Variable: Input XQ02
Variable: Input XQ01

Variable: Mean value ZA02
Variable: Mean value ZA01

Variable: Mean value ZA02
Variable: Mean value ZA01

Figure 4: Object model example

6.2.2 Gearbox signal naming example.
The following is a list over the signals available from a gearbox with 3 bearing temperatures,
1 lube oil sump temperature and 3 vibration sensors. The signal list further comprises the
gearbox lube oil pump, a sensor for differential pressure over the filter, an oil cooler fan and,
finally, an oil temperature sensor after the cooler.
Wind turbine number:

11

Sensors:
Temperature sensors:
Vibration sensors:
Pressure sensor:CPnnn

CTnnn
CYnnn

Signals:
Instantaneous value:
Average value:
Maximum value:
Minimum value:

Gearbox designation:

XA01
ZA01 (10 minutes based)
ZA02 (10 minutes based)
ZA03 (10 minutes based)

Page 21

MCD01

ELFORSK

Standard deviation:
RMS value:
FFT spectrum: ZA22
FFT-enveloped spectrum
Binary information:

ZA04 (10 minutes based)
ZA21
ZA23
XB01

Signal list example:
