# 2001 - elsfork - 11 MCD01 CT005 ZA04

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 11 MCD01 CT005 ZA04

11 MCD01 CT005 ZA04

Lube oil temperature after cooler.
Lube oil temperature after cooler.
Lube oil temperature after cooler.
Lube oil temperature after cooler.
Lube oil temperature after cooler.

Instantaneous value
10 minute average value
10 minute maximum value
10 minute minimum value
10 minute standard deviation

Page 22

ELFORSK

6.3 Analogue Signals
All analogue process values shall be accessible in standard SI-units or other physical units.
Analogue values “at the source” shall be available as real-time on-line instant data as well as
time averaged values. The values shall be available for display on operator HMI as well as for
storage (databases). Updating of analogue on-line values shall be selectable down to an interval of 1 sec. All averaged values must be stored in the plant controller for retransmission on
demand. For averaged values the accuracy of the start time of the period shall be better than
10 ms.
Some process values are not required as measurements directly at the source. The values shall
be accessible as processed data in a condensed and analysed format. This for instance is the
case for condition monitoring of components such as gearbox bearings.
6.4 Set point commands
Values for local functions could be sent as set points. A confirmation of the set point update is
required.
6.5 Binary Signals
All binary process values shall be accessible. Binary values shall be available as real-time online instant data. The values shall be available for display on operator HMI as well as for storage (databases). The values shall be stored and displayed at level shift with the corresponding
date and time tag. Updating of binary on-line values shall be selectable down to an interval of
1 sec.
6.6 Binary control commands
A handshake procedure is required for all commands that start or stop a mechanical component, influence the status or operation mode of the wind turbine or change the software. All
other control commands shall give a response with the result of the command.
The binary commands may also include activation and deactivation of programs and parameter changes.
6.7 Alarms
Operational alarms must be transmitted immediately after a triggering. A triggering is typically initiated at any event that results in an automatic stop of the wind turbine, any event that
causes an emergency stop or any other alarm-causing event. The alarms shall be available for
display on operator HMI as well as for storage (databases).
6.8 Events
Operational events must be stored in an event log in the plant controller for transmission on
demand.
6.9 Counters
Counters shall be understood as any value accumulated in time originating in the process such
as hour counters, production counters, counters for operational modes, timer’s etc. Counters
shall be available for display on operator HMI as well as for storage (databases). The values
shall be stored with a corresponding date and time tag. Updating of counters shall be selectable down to an interval of 1 sec. All values must be stored in the plant controller for transmission on demand.
Page 23

ELFORSK

6.10 Timers
The timers make it possible to determine the time for the important states in the wind turbine,
e.g. Generator on-time, Yawing time and Free to operate time. It should be possible to reset
all the timers and the ‘Reset date’ shall be stored as a separate item.
6.11 Grouped data
Data values can be grouped based on logical relationships between the data, as chronologically ordered data, as text etc. This section includes a description of different ways to put together sets of data.

6.11.1

Data structures

Data structures typically include several kinds of related data, for example the description of
an object.

6.11.2

Time series data

Time series data are time based data values for a specific object attribute, for example sampled data, metering data, etc.

6.11.3

Short text messages

It should be possible to exchange text messages between the wind power plant and the control
centre using standard readable text, such as ASCII or Unicode (UTF16).

6.11.4

Files

Typically files will be used for upload and download of programs etc.
6.12 Local data storage and handling
The examples in this section are included for informative purpose. Requirements on local data
storage and handling do not effect the communication solution.

6.12.1

Analogue values

Selected analogue values shall be stored in FIFO-buffers. The sampling rate of analogue values shall be high enough to characterise events and to determine the cause of faults. A typical
sampling rate could be 25 Hz.
The size of the buffers for analogue values shall correspond to a time span starting at 1 minute
before a triggering and ending at 1 minute after a triggering. A triggering is initiated at any
event that results in an automatic stop of the wind turbine, any event that causes an emergency stop, or any manual stop command (local or remote request).
Additionally it shall be possible to start a scanning of selected analogue values at a sampling
rate up to 25 Hz and a selectable duration. The entire mentioned high rate scanning must be
stored in the plant controller. Transfer of data in the buffers shall be carried out without synchronism with real-time.

6.12.2

Binary values

All binary values must be stored in the plant controller for retransmission on demand.
Additionally it shall be possible to start a scanning of selected binary values at a selectable
duration. All the mentioned scanning must be stored in the plant controller. Transfer of data in
the buffers shall be carried out without synchronism with real-time.
Page 24

ELFORSK

6.12.3

Alarm logging

Alarms must be stored in an alarm log. All alarms must be stored in the plant controller for
transmission on demand. The buffer depth shall be at least one year. Transfer of data in the
buffer shall be carried out without synchronism with real-time.

6.12.4

Event log

The buffer depth of the event log shall be at least one year. Transfer of data in the buffer shall
be carried out without synchronism with real-time.

6.12.5

Counters

The buffer size for every counter shall be at least 20 years of operation with 5000 full load
hours per year.

Page 25

ELFORSK
