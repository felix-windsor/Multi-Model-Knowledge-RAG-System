# 1995 - gemini - 2. Long-term logging of engineering data must be possible at slower (1 Hz or less)

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 2. Long-term logging of engineering data must be possible at slower (1 Hz or less)

2. Long-term logging of engineering data must be possible at slower (1 Hz or less)
rates, into a common format (baselined as SYBASE).

A.Fault-tolerance and recovery. See Attributes, Section 4.1 on page 4 - 1.
B.Error logging. All errors should be reported using a common, system-wide procedure.
There are three types of errors:
1. Fatal. Fatal errors occur if there is no acceptable recovery procedure that will allow

operation to proceed. Under fatal error conditions, the system falls back to a safe
"backup" state requiring human intervention for restart.
2. Serious. Under serious errors, the system does not need to move off-line, but the current operation cannot be completed. Serious errors require human intervention to
restart full operation.
3. Warning. All other unexpected conditions result in warnings that are properly
logged. The system continues operation, though perhaps with reduced efficiency.
All subsystems must group errors into these categories. In addition, errors that result
in an "alarm" should be described, along with the proper action required to acknowledge and eliminate the alarm condition.
Besides the time-stamp, error logging should provide enough information to trace the
condition back to its apparent source, both in equipment and in event sequence.
There should be tools available to extract error (and other) logging information by
subsystem component, time- sequence, previous events, and so on.
The Gemini Control System formally distinguishes alarms from errors. Errors result
from failures to successfully complete commands, while alarms represent asynchronous failures. Note that an error may result in an alarm.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS
There are two types of alarm conditions. The first are automatically monitored alarms,
which exist as long as the errors persist and are then automatically cleared. The second
type of alarm require human acknowledgment to clear.

C.Recovery. In addition to start-up procedures, there must be well-defined recovery procedures for any subsystem that has become inoperative.
Command retries must be included in the system for most common timeouts or noresponse conditions. These retries should occur automatically in the command handling
to avoid unnecessary error conditions.

D.Performance. The performance of error-mode recovery is specific to the subsystem and
is defined in the Functional specification for that subsystem.

•Normally, there is no recovery possible from a fatal error except to shut-down and then
restart the subsystem. However, in the case of an instrument failure, it may be possible to continue operation by rescheduling to use observations that do not require that
particular instrument.

•For serious errors, it may be possible to continue operation with degraded performance.
For example, failure of automatic tracking may require manual tracking; other errors
may result in operation with a different instrument.

•Under normal conditions, the number of warnings should be small. The system should
monitor the rate of warning messages since an increase might indicate that some tuning or maintenance is appropriate. Ideally, such conditions should be noted by the
subsystems before reaching the OCS level.

•Failure conditions should not cascade. That is, failure of one subsystem should not
affect other, working, subsystems, including communication links.

Given the size of the Gemini system and its long expected lifetime, it is important that
standards are provided for system design and development.

All Gemini supported software is to be developed using a formally defined model. The
Ward/Mellor approach to developing real-time systems is used and covers:

A.Analysis, design and development methods
B.Review procedures

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS

C.Documentation
D.Coding and debugging
E.Simulation
F.Testing and integration
Functional analysis is done using a CASE tool suitable for use with Ward/Mellor
techniques, such as TSEE, by Westmount Technologies.
The design is to use the techniques and diagrams introduced by Ward and Mellor and
reviewed by the Gemini staff.
Detailed design and development standards are not specified, but expected to conform to system goals and established practice.
An object-oriented approach is encouraged but not required.

The upper levels (User-interface and OCS) are assumed to not require a real-time
operating environment. However, the operating environment at these levels is
expected to provide sufficient performance for both human interaction and communications.
Real-time support is required at the IOC level.

A.Development system software. The choice for a development environment is based
on the following criteria:

•Productivity and development tools
•Software portability and hardware independence
•Vendor independence
•Industry and de-facto standards
•Support for state-of-the-art user interfaces
•Support of a distributed environment
Given these criteria, the following recommendations exist.

O THER C ONTROLS AND S OFTWARE R EQUIREMENTS
