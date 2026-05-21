# 1998 - themas - 2. For each thermometer, the ratio of the number of requests for

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1998 - themas.pdf

Section: 2. For each thermometer, the ratio of the number of requests for

2. For each thermometer, the ratio of the number of requests for
a heating and cooling unit that was granted to the number of
requests for a heating or cooling unit that was denied.
3.1.10.4 Outputs
Report Data

3 - 10

D_THEMAS_SRS_001

APPENDIX A - TRACEABILITY MATRIX

A - 1

D_THEMAS_SRS_001

SRS
Requirement
SRS-001
SRS-002
SRS-003
SRS-004
SRS-005
SRS-006
SRS-007
SRS-008
SRS-009
SRS-010
SRS-011
SRS-012
SRS-013
SRS-014
SRS-015
SRS-016
SRS-017
SRS-018

Requirement
Description
Load H/C Unit Definitions
Turn off H/C Units
Load Thermostat Definition
Load Utilization Parameters
Set Trigger Values
Set Overtemp Values
Establish Valid Temperature Range
Validate Temperature
Determine Temperature Status
Determine H/C Mode
Determine Status of all H/C Units
Generate Unit Unavailable Event
Generate H/C Request
Generate H/C Signal
Generate Alarm Data
Generate Event Data
Change Thermostat Setting
Generate Reports

A - 2

Statement of Work
Paragraph
2.5

3.1
3.2

2.5
2.1,2.2,2.5
3.1
5.1, 5.2
2.4
5.2

D_THEMAS_SRS_001

APPENDIX B - DATAFLOW DIAGRAMS

B - 1

D_THEMAS_SRS_001

Context Diagram
(Level 0 Dataflow Diagram)

Heating
Unit

Thermostats

ng
ati
He

Event Data

Cooling
Unit

al
ign
it S
Un
g
n
oli
Co
t Data
Even

Te
mp
era
tur
eD
ata

Event
Information

al
ign
it S
n
U

THEMAS
Software

ta
Da
on
i
t
a
liz
tia
Ini

Un
it S
tatu
s+

Event
Information

Alarm Dat
a

Tem
per
atu
re D
Re
ata
po
rt
Da
ta

Audible
Alarm

Thermostats

Initializaton
Information

Reports

B - 2

D_THEMAS_SRS_001

THEMAS Software
(Level 1 Dataflow Diagram)
Generate
Alarm
Data

Te
m
pe
ra
tur
e

ts
en
Ev

Generate
Event
Data

C
H/
t
es
qu
Re

/C
dH
nie
De

C
H/

t
es
qu
Re

l
na
tio
ra
pe
O

Initialize
System

t
es
qu
Re

Ope
ratio
nal
Par
ame
ters

/C
dH
ve
pro
Ap

Determine
Utilization

rameters
Operational Pa

s
er
et
m
ra
Pa

Change
Thermostat
Setting

Event Data

Generate
Reports

B - 3

Generate
H/C
Signal

Temperature Data

Report Data

Event Data

t
es
qu
Re

Syste
m Ev
ents

Monitor
Temperature
s
ter
me
ara
al P
n
tio
era
Op

Alarm Data
m
ar
Al

e
tur
era
mp
Te
lid
Va

Initialization Data

Initialize
Operational
Parameters

Invalid Temperature
Lim
it E
xc
ee
de
d

Validate
Temperature

Ope
ratio
nal P
aram
eter
s

Temperature Data

al
gn
Si
nit
U
ng
ati
He
Signal
g Unit
Coolin
Unit
Statu
s

D_THEMAS_SRS_001

Initialize System
(Level 2 Dataflow Diagram)
Load
H/C Unit
Definitions
Load
Thermostat
Definitions
Load
Utilization
Parameters
Initialization Data
Set Trigger
Values

Set
Overtemp
Values
Establish
Valid
Temperature
Range

B - 4

Operational Parameters

D_THEMAS_SRS_001

Monitor Temperature
(Level 2 Dataflow Diagram)
Valid
Tem
pera
ture

Determine
Temperature
Status

es
alu
er V
g
g
Tri

ues
Val
mp
e
t
r
ve
+O

Temperature Limit Exceeded
Te
mp
era
tur
eS
tatu
sR
eac
hed

Determine
H/C
Mode

B - 5

H/C Request

D_THEMAS_SRS_001

Determine Utilization
(Level 2 Dataflow Diagram)
Stack
Request
H/C

tion
liza
Uti

le
ab
ail
av
n
it U
Un

Re
qu
es
t

rs
ete
ram
Pa

Unit Unavailable

Determine
Status of
All H/C Units

Generate
Unit
Unavailable
Event

System Event Data

H/C
ON/O
FF R
eque
st

Generate
H/C Request

B - 6

Approved H/C Request

D_THEMAS_SRS_001

APPENDIX C - DATA DICTIONARY

C - 1

D_THEMAS_SRS_001
Alarm Data
Allowed Meanings
String
Notes
Defines the various alarm types.
Input To Transforms
(None)
Next Higher Dictionary Where Used
(None)
Output From Transforms
Generate Alarm Data
THEMAS Context Diagram
Alarm Events
Allowed Meanings
String
Notes
Describes the event that caused an alarm to occur.
Input To Transforms
Generate Event Data
Next Higher Dictionary Where Used
(None)
Output From Transforms
Generate Alarm Data
Approved H/C Request
Allowed Meanings
String
Notes
Defines the thermostat and heating or cooling unit to turn
on or off.
Input To Transforms
Generate H/C Signal
Next Higher Dictionary Where Used
(None)

C - 2

D_THEMAS_SRS_001
Output From Transforms
Determine Utilization
Generate H/C Request
Timestamp
Allowed Meanings
String
Notes
Denotes the current system date and time on the supervisor’s
computer.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Report Data
Output From Transforms
(None)
Denied H/C Request
Allowed Meanings
String
Notes
Defines the thermostat that requested heating or cooling,
but was denied the request due to current system loading.
Input To Transforms
Generate Event Data
Next Higher Dictionary Where Used
(None)
Output From Transforms
Determine Utilization
Event Data
Allowed Meanings
String + Date
Notes
Describes the entries that are written to the database that
are associated with each event that occurs in the system.
Input To Transforms
C - 3

D_THEMAS_SRS_001
(None)
Next Higher Dictionary Where Used
(None)
Output From Transforms
Generate Event Data
Generate Unit Unavailable Event
THEMAS Context Diagram
H/C Request
Allowed Meanings
String
Notes
When the system detects a need for heating or cooling, this
defines the thermostat and heating or cooling unit to turn
on or off.
Input To Transforms
Determine Utilization
Determine Status of All H/C Units
Next Higher Dictionary Where Used
(None)
Output From Transforms
Initialize System
Monitor Temperature
H/C ON/OFF Request
Allowed Meanings
String
Notes
Defines a request to generate the signal to turn on or off a
heating or cooling unit resulting from an approved request
for a heating or cooling unit.
Input To Transforms
Generate H/C Request
Next Higher Dictionary Where Used
(None)
Output From Transforms
Determine Status of All H/C Units

C - 4

D_THEMAS_SRS_001
H/C Unit Definitions
Allowed Meanings
String
Notes
Defines each discrete heating and cooling unit in the
system.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Initialization Data
Allowed Meanings
String + Integer
Notes
Information from the initialization file that include the
thermostat definitions, heating and cooling definitions,
temperature limits, and trigger values.
Input To Transforms
Establish Valid Temperature Range
Initialize Operational Parameters
Load H/C Unit Definitions
Load Thermostat Definitions
Load Utilization Parameters
Set Trigger Values
Set Overtemp Values
THEMAS Context Diagram
Next Higher Dictionary Where Used
(None)
Output From Transforms
(None)
Invalid Temperature
Allowed Meanings
String
Notes
C - 5

D_THEMAS_SRS_001
Denotes the condition when an erroneous temperature is
reported from a thermostat.
Input To Transforms
Generate Alarm Data
Next Higher Dictionary Where Used
(None)
Output From Transforms
Validate Temperature
Operational Parameters
Allowed Meanings
Determine Status Of All H/C Units + H/C Unit Definitions +
Overtemp Values + Thermostat Definitions + Trigger Values +
Utilization Parameters + Valid Temperatures
Notes
Information from the initialization file that include the
thermostat definitions, heating and cooling definitions,
temperature limits, and trigger values.
Input To Transforms
Change Thermostat Setting
Determine Utilization
Initialize System
Monitor Temperature
Validate Temperature
Next Higher Dictionary Where Used
(None)
Output From Transforms
(None)
Overtemp Values
Allowed Meanings
Integer
Notes
Defines the delta value relative to the temperature setting
value. A temperature at or beyond this delta indicates the
thermostat has reached a critical value where the heating or
cooling unit cannot satisfy the temperature setting value.
Input To Transforms
(None)
C - 6

D_THEMAS_SRS_001
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Report Data
Allowed Meanings
String + Timestamp
Notes
Contains the formatted report information.
Input To Transforms
(None)
Next Higher Dictionary Where Used
(None)
Output From Transforms
Generate Reports
THEMAS Context Diagram
System Events
Allowed Meanings
String
Notes
Describes each normal operational event that occurs in the
system.
Input To Transforms
Generate Event Data
Next Higher Dictionary Where Used
(None)
Output From Transforms
Generate H/C Signal
Temperature Data
Allowed Meanings
String + Integer
Notes
Temperature and thermostat information to and from the
thermostats.
C - 7

D_THEMAS_SRS_001

Input To Transforms
THEMAS Context Diagram
Validate Temperature
Next Higher Dictionary Where Used
(None)
Output From Transforms
Change Thermostat Setting
Temperature Limit Exceeded
Allowed Meanings
String
Notes
Denotes the condition when the reported temperature has
exceeded the overtemperature value.
Input To Transforms
Generate Alarm Data
Next Higher Dictionary Where Used
(None)
Output From Transforms
Determine Temperature Status
Monitor Temperature
Temperature Trigger Exceeded
Allowed Meanings
String
Notes
Denotes the condition when the reported temperature has
exceeded the triggering value indi cating a heating or
cooling unit should be requested.
Input To Transforms
Determine H/C Mode
Next Higher Dictionary Where Used
(None)
Output From Transforms
Determine Temperature Status
Thermostat Definitions
C - 8

D_THEMAS_SRS_001

Allowed Meanings
String
Notes
The unique identifier associated with each thermostat in the
system.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Trigger Values
Allowed Meanings
Integer
Notes
Defines the delta valu e relative to the temperature setting
value. A temperature beyond this delta indicates the
thermostat is requesting a heating or cooling unit event to
occur.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Unit Status
Allowed Meanings
String
Notes
Defines the current on or off condition of the heating and
cooling units and the thermostat to which they are
associated.
Input To Transforms
(None)
Next Higher Dictionary Where Used
C - 9

D_THEMAS_SRS_001
(None)
Output From Transforms
Generate H/C Signal
Unit Unavailable
Allowed Meanings
String
Notes
Defines the heating or cooling unit that was denied a
request to be turned on. Generated in response to a denied
request.
Input To Transforms
Generate Unit Unavailable Event
Stack Request
Next Higher Dictionary Where Used
(None)
Output From Transforms
Determine Status of All H/C Units
Stack Request
Valid Temperatures
Allowed Meanings
Integer
Notes
Defines the upper and lower limits for a re ported
temperature value.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Utilization Parameters
Allowed Meanings
Integer
Notes
C - 10

D_THEMAS_SRS_001
Defines how many heating and cooling units that can run
simultaneously.
Input To Transforms
(None)
Next Higher Dictionary Where Used
Operational Parameters
Output From Transforms
(None)
Valid Temperature
Allowed Meanings
String
Notes
Denotes the condition when an valid temperature is reported
from a thermostat.
Input To Transforms
Monitor Temperature
Next Higher Dictionary Where Used
(None)
Output From Transforms
Validate Temperature

C - 11
