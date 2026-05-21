# 1998 - themas - 3.0 Engineering Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1998 - themas.pdf

Section: 3.0 Engineering Requirements

3.0 Engineering Requirements
3.1 Functional Requirements
This section is subdivided into ten main subsections: Initialize
Operational Parameters, Initialize System, Validate Temperature,
Monitor Temperature, Determine Utilization, Generate H/C Signal,
Generate Alarm Data, Generate Event Data, Change Thermostat
Setting, and Generate Reports. Each subsection describes the
software requirement for that individual software component of
the THEMAS system.
3.1.1 Initialize Operational Parameters
The following sections describe the Initialize System component
of the THEMAS system.
3.1.1.1 Load H/C Unit Definitions (SRS -001)
3.1.1.1.1 Introduction
The THEMAS system shall control t he heating and cooling units
that are defined as part of the THEMAS system. The definitions
of the individual heating and cooling systems reside in an
initialization file. The system shall read this file and the
definitions shall be derived from the initialization data in the
file.
3.1.1.1.2 Inputs
Initialization Data
3.1.1.1.3 Processing
The THEMAS system shall use the information contained in the
initialization data file to determine which heating and cooling
units are part of the THEMAS system. Ther e is one heating and
cooling unit that corresponds to one thermostat in each of four
quadrants on each of three floors of the office building.
3.1.1.1.4 Outputs
Operational Parameters
3.1.1.2 Load Thermostat Definitions (SRS -002)
3.1.1.2.1 Introduction
Each thermostat shall have a unique identifier by which that
thermostat is identified in the THEMAS system. This procedure
will load these definitions into the THEMAS software.
3.1.1.2.2 Inputs
Initialization Data
3.1.1.2.3 Processing
Each quadrant of each floor shall have a thermostat which is to
be used to provide temperature data to the THEMAS system. The
3 - 1

D_THEMAS_SRS_001
initialization file shall contain a unique identifier for each
thermostat that the system is to monitor. These identifiers
shall be read from the initialization file and loaded into the
THEMAS system during the initialization process.
3.1.1.2.4 Outputs
Operational Parameters
3.1.1.3 Load Utilization Parameters (SRS -003)
3.1.1.3.1 Introduction
There shall be a maximum number of heating or cooling u nits that
can be on at any given time. This procedure loads the maximum
number of concurrently running units allowed.
3.1.1.3.2 Inputs
Initialization Data
3.1.1.3.3 Processing
The maximum number of heating or cooling units that can run
concurrently shall reside in an initialization file. The maximum
number of concurrently running units shall be read from the
initialization file and stored in the THEMAS system.
3.1.1.3.4 Outputs
Utilization Parameters
3.1.1.4 Set Trigger Values (SRS -004)
3.1.1.4.1 Introduction
The trigger value is used in combination with the current
temperature to determine when a heating or cooling unit shall be
turned on or off.
3.1.1.4.2 Inputs
Initialization Data
3.1.1.4.3 Processing
The trigger values shall reside in an initialization file. This
procedure shall read the initialization file and establish the
trigger value from the data in that file.
3.1.1.4.4 Outputs
Operational Parameters
3.1.1.5 Set Overtemp Values (SRS -005)
3.1.1.5.1 Introduction
The THEMAS system shall en sure the temperature reported by a
given thermostat shall not exceed a maximum deviation value of 3
degrees Fahrenheit.
3 - 2

D_THEMAS_SRS_001

3.1.1.5.2 Inputs
Initialization Data
3.1.1.5.3 Processing
The overtemperature values shall reside in an initialization
file. This procedure shall read the initialization file and
establish the overtemperature value from the data in that file.
3.1.1.5.4 Outputs
Operational Parameters
3.1.1.6 Establish Valid Temperature Range (SRS -006)
3.1.1.6.1 Introduction
The THEMAS system shall onl y respond to temperatures that are
within a reasonable value.
3.1.1.6.2 Inputs
Initialization Data
3.1.1.6.3 Processing
The valid temperature range value shall reside in an
initialization file. This procedure shall read the
initialization file and establish the valid temperature range
from the data in it.
3.1.1.6.4 Outputs
Operational Parameters
3.1.2 Initialize System (SRS -007)
3.1.2.1 Introduction
When the THEMAS system is initialized, it shall first turn off
all the heating and cooling units. Then , it shall check all the
thermostats and determine if any thermostat’s settings require a
heating or cooling unit to be turned on back on.
3.1.2.2 Inputs
Operational Parameters
3.1.2.3 Processing
This process shall first determine a known state of all the
heating and cooling units by issuing a request to turn off all
the units. It shall then read the current temperature values and
current temperature settings of each thermostat. If the settings
reflect a need for a heating or cooling unit to be turned o n, the
process shall issue a request to turn on the appropriate unit.
This determination shall be made in accordance with the rules
outlined in section 3.1.4.1 and 3.1.4.2.
3 - 3

D_THEMAS_SRS_001
3.1.2.4 Outputs
H/C Request
3.1.3 Validate Temperature (SRS -008)
3.1.3.1 Introduction
The THEMAS system shall only respond to temperatures from the
thermostats that are within the specified valid range.
3.1.3.2 Inputs
Operational Parameters
Temperature Data
3.1.3.3 Processing
Two types of temperature data shall be recognized from th e
thermostats: 1) the temperature setting and 2) the current
temperature. This module shall process both types of data.
A current temperature value that is received from an individual
thermostat shall be compared to the valid temperature range
values. If the current temperature value is strictly less than
the lower value of the valid temperature range or if the received
temperature value is strictly greater than the upper value of the
valid temperature range, then the THEMAS system shall identify
the current temperature value as an invalid temperature and shall
output an invalid temperature status. Otherwise, the THEMAS
system shall output a valid temperature status.
A temperature setting value that is received from an individual
thermostat shall be compared to the valid temperature range
values. If the temperature setting value is strictly less than
the lower value of the valid temperature range or if the
temperature setting value is strictly greater than the upper
value of the valid temperature range, then the THEMAS system
shall identify the temperature setting as an invalid temperature
and shall output an invalid temperature status. Otherwise, the
THEMAS system shall realize the value for that thermostat’s
temperature setting.
3.1.3.4 Outputs
Invalid Temperature
Valid Temperature
3.1.4 Monitor Temperature
The following sections describe the Monitor Temperature component
of the THEMAS system.
3.1.4.1 Determine Temperature Status (SRS -009)
3.1.4.1.1 Introduction
The THEMAS system shall determine wh en a reported temperature or
a changed temperature setting exceeds the limits set by the
3 - 4

D_THEMAS_SRS_001
overtemperature values. Temperatures that exceed the
overtemperature limits shall be reported as such. Temperatures
that do not exceed these limits shall be output for subsequent
processing.
3.1.4.1.2 Inputs
Valid Temperatures
Trigger Values
Overtemp Values
3.1.4.1.3 Processing
The THEMAS system shall compare the reported temperature value to
the temperature setting and detect when the temperature value
exceeds the specified limits. To clarify these conditions, the
following definitions will be used:
LO : Lower Overtemperature Value = TSET - OD
UO : Upper Overtemperature Value = TSET + OD
If T < LO or UO < T then the THEMAS system shall recognize this
condition as the temperature limit has been exceeded. In this
case this process shall output the condition of the temperature
limit having been exceeded.
If LO < = T < = UO, then this process shall output the
temperature status.
3.1.4.1.4 Outputs
Temperature Trigger Exceeded
Temperature Limit Exceeded
3.1.4.2 Determine H/C Mode (SRS -010)
3.1.4.2.1 Introduction
When the current temperature value exceeds the current
temperature setting by a pre -defined amount, the THEMAS system
shall activate the appropriate heating or cooling unit.
3.1.4.2.2 Inputs
Temperature Trigger Exceeded
3.1.4.2.3 Processing
There are two conditions for each individual thermostat that
shall be tested for: 1) the thermostat’s settings are satisfied
and 2) the thermostat’s temperature indica tes it requires a
heating or cooling unit to be turned on. To clarify these
conditions, the following definitions will be used:
LT : Lower Trigger Value = TSET - TD
UT : Upper Trigger Value = TSET + TD
3 - 5

D_THEMAS_SRS_001
Condition 1: LT < = T < = UT
This condition indicates the thermostat’s current temperature
setting is satisfied. If this condition is true, then the module
shall output a request to turn off both the heating unit and the
cooling unit.
Condition 2: LO < = T < LT or UT < T < = UO
This condition the nee d for a heating or cooling unit to be
turned on. If this condition is true, then this module shall
output a request to turn on the heating unit if LO < = T < LT or
the cooling unit if UT < T < = UO.
3.1.4.2.4 Outputs
H/C Request
3.1.5 Determine Utilization
3.1.5.1 Determine Status of All H/C Units (SRS -011)
3.1.5.1.1 Introduction
The THEMAS system shall control each of the heating and cooling
units that are defined for the system. The THEMAS system shall
limit the number of heating or cooling units t hat may be running
simultaneously.
3.1.5.1.2 Inputs
Operational Parameters
H/C Request
3.1.5.1.3 Processing
The THEMAS system shall maintain the ON/OFF status of each
heating and cooling unit. When a request to turn on or off a
heating or cooling unit, the following processing will occur.
When a request to turn on a heating or cooling unit is received,
the system shall determine if the request can be honored. If the
maximum number of heating or cooling units is already running,
the request will be add ed to a LIFO queue. If the maximum number
of heating or cooling units is not running, this process will
generate a request to turn on the requested unit.
When a request to turn off a heating or cooling unit is received,
this process shall check the queue of waiting heating and cooling
requests. If the queue is not empty, this process shall remove
one request from the LIFO queue and check the current state of
the thermostat for which the queued request was made. If that
thermostat still needs a heating o r cooling unit turned on, this
process shall submit a request to turn that unit on.
3.1.5.1.4 Outputs
Unit Unavailable
3 - 6

D_THEMAS_SRS_001
H/C ON/OFF Request
3.1.5.2 Generate Unit Unavailable Event (SRS -012)
3.1.5.2.1 Introduction
When a request for a heating unit or cooling to be turned is
denied, an event shall be generated and the THEMAS system shall
record that event. The information in these events will be used
for creating statistical reports.
3.1.5.2.2 Inputs
Unit Unavailable
3.1.5.2.3 Processing
This procedure shall realize the thermostat and heating or
cooling information and use this information to generate a
specific system event. This system event shall consist of a
description of the event type (a request denied event), a
designation of the thermostat that made the request, and a
designation of the heating or cooling unit that was not turned
on.
3.1.5.2.4 Outputs
System Event Data
3.1.5.3 Generate H/C Request (SRS -013)
3.1.5.3.1 Introduction
The THEMAS system shall control the heating and cooling units
that are designated as part of the THEMAS system.
3.1.5.3.2 Inputs
H/C ON/OFF Request
3.1.5.3.3 Processing
When a request to turn on or off a heating or cooling unit is
made, this process shall generate the appropriate request to
carry out that request. This request shall include the
designation of the heating or cooling unit and a flag to indicate
whether that unit is to be turned on or off.
3.1.5.3.4 Outputs
Approved H/C Request
3.1.6 Generate H/C Signal (SRS -014)
3.1.6.1 Introduction
Once a request to turn on or off a heating or cooling unit, the
THEMAS system shall provide the necessary control signal for the
unit. This control signal shall also provide an indication of
the unit’s status at the requesting thermostat.
3 - 7

D_THEMAS_SRS_001

3.1.6.2 Inputs
Approved H/C Request
3.1.6.3 Processing
This process shall recognize the values for the requested heating
or cooling unit and the ON or OFF status that is being requested.
The necessary signal to the heating or cooling unit will be
generated. Since the interface to con trol the units has not been
defined, the part of this process that will issue the signal is
designated as TBD(to be determined).
In order to provide an indication of the status of the heating or
cooling unit back to the requesting thermostat, this procedure
shall output the status information of the heating or cooling
unit.
In order to provide an operational history and statistical
reports, this process shall generate an event each time a change
is made to the status of a heating or cooling unit. This ev ent
shall contain the identification of the heating or cooling unit
whose status is being changed.
3.1.6.4 Outputs
Heating Unit Signal
Cooling Unit Signal
Unit Status
System Events
3.1.7 Generate Alarm Data (SRS -015)
3.1.7.1 Introduction
There are two events that shall result in an alarm condition: 1)
an invalid temperature value is reported from a thermostat, or 2)
the reported temperature has exceeded the defined limits. This
process shall determine which alarm event is to be generated.
3.1.7.2 Inputs
Invalid Temperature
Temperature Limit Exceeded
3.1.7.3 Processing
When the THEMAS system detects a request for an alarm, this
process shall detect which of the two alarms are being requested.
If the system detects an invalid temperature, this process shall
output a continuous series of alternating 500 Hz and 700 Hz beeps
on the supervisor’s computer. Each beep shall have a three quarter second duration. This series of beeps shall continue
until the supervisor manually resets the alarm through the
supervisor’s interface window.
3 - 8

D_THEMAS_SRS_001

If the system detects a temperature limit has been exceeded, this
process shall output a continuous series of alternating 1000 Hz
and 1500 Hz beeps on the supervisor’s computer. Each beep shall
have a one-half second duration. This series of beeps shall
continue until the supervisor manually resets the alarm through
the supervisor’s interface window.
Each time an alarm is requested, an alarm event shall be
recorded. This event shall be used to provide operational and
statistical reports about the system.
3.1.7.4 Outputs
Alarm Data
Alarm Events
3.1.8 Generate Event Data (SRS -016)
3.1.8.1 Introduction
For each event that is generated, the THEMAS system shall
identify each event and generate the appropriate event data.
3.1.8.2 Inputs
Alarm Events
System Events
Denied H/C Request
3.1.8.3 Processing
When an event occurs, the THEMAS system shall identify the event
type and format an appropriate event message. The THEMAS system
shall record each event by a description and the c urrent system
time for that event. This information shall be recorded in a
Microsoft ® Access ® database that shall reside on the supervisor’s
computer.
3.1.8.4 Outputs
Event Data
3.1.9 Change Thermostat Setting (SRS -017)
3.1.9.1 Introduction
The THEMAS system shall provide the supervisor a mechanism to
change the temperature setting of any of the thermostats in the
system.
3.1.9.2 Inputs
Operational Parameters
3.1.9.4 Processing
The supervisor’s interface shall display the available
thermostats and their individual current temperature settings.
3 - 9

D_THEMAS_SRS_001
The supervisor shall be able to select one of the thermostats and
select a value for the current temperature from a list of valid
temperatures.
3.1.9.5 Outputs
Temperature Data
3.1.10 Generate Reports (SRS -018)
3.1.10.1 Introduction
The THEMAS shall provide the ability for the supervisor to select
between two different types of reports: 1) the operational
history of the THEMAS system for the past twelve months and 2) a
statistical summary for any selected mont h.
3.1.10.2 Inputs
Event Data
3.1.10.3 Processing
The supervisor’s interface to the THEMAS system shall provide a
mechanism to select between an operational history report or a
statistical summary report. Either report shall consist of an
ASCII file whose location and name shall be selectable by the
operator.
If the operational history report is selected, the THEMAS system
shall select all the events from the event database, sort the
events by date and time, and create the ASCII report file.
If the statistical report is selected, the THEMAS system shall
present the operator with a list of available months from which
to make a selection. After selecting one of the months, the
system shall generate the ASCII report file. The statistical
reports shall consist of the following statistics:
