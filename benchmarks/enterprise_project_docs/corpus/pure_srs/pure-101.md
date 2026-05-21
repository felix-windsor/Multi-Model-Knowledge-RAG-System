# 2001 - beyond - 7. Functional specifications and architecture for domain

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - beyond.pdf

Section: 7. Functional specifications and architecture for domain

7. Functional specifications and architecture for domain
Avionics (Intelligent Adaptive Flight Deck)
7.1. Introduction
7.1.1. Purpose of the intelligent adaptive flight deck
BARCO and TUDelft collaborate in this context.It is expected that a well-designed
intelligent adaptive flight deck can significantly increase the flight safety and
efficiency compared to the collection of static (but often adaptable is not adaptive)
and diverse displays in the cockpit of today. Accident analysis has shown that 65%
of all aircraft incidents are caused by human error. Two kinds of human errors can
be distinguished: slips and mistakes [Reason, 1987]. A slip occurs when the
intention is right, but a deviation of that intention occurs. A mistake occurs when the
actions are according to the intended plan, but the plan is inadequate to achieve the
intended goal. It is expected that slips and mistakes in aircraft operation can be
avoided by an intelligent adaptive flight deck that assists the flight crew in performing
their tasks. An intelligent system that knows the human intentions and the actual and
predicted flight status can detect slips from the intended plan. If the system is aware
of the goals of the operation, the intelligent system can even give a recommendation
to the pilot to correct for the error.
In most cases, mistakes are not simply due to a bad knowledge of the theory or
procedure, but are rather a logical consequence of a lack of situation awareness.
The flight deck communicates to the pilot information about the flight status (flight
plan, position, velocity, etc.), the environment (weather, traffic, airports, etc.), and
system status (aircraft system failures, etc.). To form an internal representation of
the flight situation, the crew has to integrate all this information presented to them on
numerous head-down cockpit displays in different formats. In addition, the auditory
channel is used to present advice, warnings and alerts to the crew. Especially during
critical situations, where the situation awareness is of greatest importance, pilots
have difficulties building up a representation of the flight situation. At the same time,
several buttons can lighten up, various alerts can be given, and information is
highlighted on the display. The flight crew then has to determine the most critical
problem and the right procedure to solve it, not an easy task for the human being
with only a limited view of the situation and it is clear that situations like these
contribute considerably to pilot workload. Mistakes can be prevented by assisting the
pilot in building situation awareness. It is expected that an intelligent adaptive
interface that presents the right information in the right format (integrated and
intuitive for that particular situation) at the right time (with an appropriate alerting
strategy) can significantly increase flight safety.
Another contributor to the high workload during critical situations in the cockpit is the
task of decision making. Even if the flight crew is able to determine a good resolution
to solve the problem, they have too little overview to optimize it. An intelligent flight
deck can help the pilot by proposing optimized alternatives out of which the pilot can
choose one. In such a co-operation, the pilot and intelligent flight deck share their
knowledge and capabilities to improve the safety and efficiency of the overall
system.

BEYOND
Functional Specifications and Architecture

30

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

7.1.2. Levels of the adaptation process
Four stages can be distinguished in the adaptation process: initiation, proposal,
decision, and execution [Dieterich et al., 1993]. The agents performing or controlling
these stages are the pilot of the automation. The following levels of adaptation are
applicable to the intelligent adaptive flight deck [Abeloos et al., 2000]:
•

Self-adaptation: the automation performs the tasks on all stages of the
adaptation. This adaptation is contradicting with the human-centered design
philosophy and seems therefore unacceptable. In certain time-critical, high
workload situations, however, it may be necessary or even mandatory to
automatically adapt the interface to draw the crew’s attention and to allow an
immediate but sound response. Because the adaptation is unexpected and may
cause confusion, its occurrence must be well known and trained by the cockpit
crew.

•

User-controlled self-adaptation: the decision to adapt is taken by the user, while
all other tasks are automated. If the automation thinks that for the current
situation a different presentation may be more efficient, it may suggest an
adaptation that has to be agreed upon by the pilot.

•

User-initiated self-adaptation: the user takes the initiative, the automation
proposes, decides and executes. This is in fact self-adaptation, but allowing the
pilot to take the initiative.

•

Computer-aided adaptation: on a user’s initiative, the automation proposes an
adaptation, which it will execute after the user’s approval.

•

System-initiated adaptation: on a system’s initiative, the user proposes, decides
and executes the adaptation. The pilot is then informed if it seems reasonable to
tailor the system.

•

Adaptation: the user performs the tasks on all stages of the adaptation. Simple
adaptation gives the opportunity to users to tailor the system to their own needs
and preferences. This already exists in the cockpit of today, where the pilots can
control the brightness, contrast, etc. of the display directly. This type of adaptation
can better be described as flexibility.

For a full review of the applicability of adaptivity in a future intelligent flight deck, the
reader is referred to [Abeloos, 2000].
7.1.3. Proposal for the first prototype
The first prototype of the intelligent adaptive flight deck has to assist the pilot in:
•

Establishing and maintaining situation awareness by presenting the right
information in the right format at the right time.

•

Detecting and correcting errors by comparing the overall system’s goals, the pilot
intentions, and the actual and predicted flight state.

•

Decision making by proposing optimized alternatives.

BEYOND
Functional Specifications and Architecture

31

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

•

Carrying out some simple actions by comparing the active procedures with the
pilot’s actions.

The first prototype should be able to solve conflicting hazardous situations in an
optimized manner. It does so by supporting all levels of adaptation that have been
discussed above. In the case of self-adaptation, the pilot shall always be offered the
opportunity to overrule the adaptation. These issues have all been worked out in
more detail in the requirements document D2. As will be described below, the first
three levels of assistance have been implemented in the first prototype.

7.2. Project status
Description of the first prototype
To observe the environment, the first prototype of the intelligent adaptive flight deck
consisted of the implementation of two aircraft warning systems, the Ground
Proximity Warning System (GPWS) and the Traffic alert and Collision Avoidance
System (TCAS). The agent-oriented system architecture that is applied allows these
systems to be integrated on a system level. This means that the two systems can
communicate on all levels of their functioning. They can exchange rough
environmental information, the detection of hazardous situations, and resolution
advisories to solve for these critical situations. This data exchange allows the
system:
To form one integrated picture of the environment,

To present alerts in the right order, to apply a good alerting strategy, and
To negotiate resolution advisories, so that the resolution of the one critical situation
does not induce another critical situation.
The intelligent interface itself has been implemented as a group of agents
collaborating with the various system agents in a shared ontology (Figure 4). This
means that all functions on all levels of the interface could communicate with each
other. The first three levels of assistance (establishing situation awareness, detecting
and correcting errors, decision making) listed above have been incorporated in the
first prototype.

BEYOND
Functional Specifications and Architecture

32

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

Warning
System
Group

TCAS
agent
GPWS
agent
Weather
agent

‘Local’ communication bus

Facilitator

Collision,
Terrain,
Weather
Avoidance
Sensors

Resolution
agent

‘Global’ communication bus

Figure 4 : Warning system group communication organization (first prototype)
To help the pilot establishing and maintaining situation awareness (assistance
level 1), the pilot interface consisted of two advanced displays showing the pilot a
three-dimensional synthetic view of the environment (the Primary Flight Display
(PFD)) accompanied by a two-dimensional bird’s eye view of the environment (the
Navigation Display (ND)). To detect and correct for errors, and to help the pilot in
his/her decision making (assistance levels 2 and 3), the warning-system adaptation
was implemented in particular on the Navigation Display, including the GPWS and
TCAS systems introduced above. The range in the ND was automatically adapted to
show the pilots the cause(s) for the warning signals. Furthermore, display features
that were not useful when a threat did not occur were ‘darkened’ automatically, i.e.
the dark cockpit concept, or removed automatically. A realistic scenario was
developed to test the functionality of the first prototype.

7.3. Methods and results concering usability
Testing the first prototype
The first prototype has been tested in a future airspace environment, consisting of
other traffic and terrain. Other environmental factors, such as weather and Air Traffic
Control were not considered.
The first prototype has been tested using a
questionnaire. A fixed demonstration has been developed that showed all features of
the adaptive display in a realistic scenario. No user interaction was possible in this
stage. The demonstration has been shown to a group of 23 experts in the field of
avionics: 17 avionics and software engineers, 3 flight test engineers and 3
commercial pilots. The participants were first briefed extensively to introduce the
intelligent flight deck and explain the scenario. After the demonstration the
participants were asked to fill out an extensive questionnaire, addressing pilot
acceptability, workload, situation awareness, and many others. The results of the
questionnaire analysis have been described in a report [Steentjes & Mulder, 2000].
Some of the main outcomes are described below.
BEYOND
Functional Specifications and Architecture

33

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

The questionnaire evaluation can be concluded successful, and guides the future
development of the second prototype. For the near future (around february 2001) a
second group of experts, consisting of pilot trainees, has been invited to see the
demonstration and fill out the questionnaire addressing the first prototype.

7.4. Functional specifications
7.4.1. General changing requirements and extensions
General
The first prototype of the intelligent flight deck is able to build and maintain an
internal model of a relatively small sub-set of the environment (objects, possibilities,
constraints) and of some of the interactions within the human-machine system itself
(goals, capabilities, preferences, etc.). The second prototype will extend the first one
considerably. The questionnaire revealed that especially the way of communicating
this internal situation awareness (the ‘system’ awareness) to the pilot should be
improved. Experts expressed a need of ‘seeing through’ the automation and
adaptation, and the user interface should have an option to provide them that
possibility. Furthermore, experts claim the opportunity to overrule the system mental
model, and in this respect the user interface needs to be altered. But these findings
do not call for changing the requirements as such. The findings from the pilot
questionnaire were in general in line with, or were envisaged in the requirements as
specified in Deliverable D2 of this project. Hence, the number of changes in the
general requirements is small.
The existing multi-agent system architecture of the first prototype (Figure 4) will not
be altered, but rather be upgraded and significantly extended (Figure 5). The
extensions will be directed almost exclusively towards the automatic, adaptive
management of content information on the display (Display Group and Control
Group in Figure 5), as defined by the integrated warning system architecture.
Questions to be answered include the manner in which information that is not critical
but still valuable should be handled (dark cockpit?). The multi-agent subsystem that
deals with managing content and inferring user intent needs to be extended, an effort
that will require considerable attention.

BEYOND
Functional Specifications and Architecture

34

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

Figure 5 : Multi-agent system architecture of the second prototype (the warning
system architecture is included in this figure as the Warning Systems group)

Data and BDI information flow
Signal flow

Changed requirements
One requirement from D2 is dropped:
The second prototype will incorporate the use of touch-screen technology.
This will not be feasible within the available time.
7.4.2. Usability related specifications
The use of a pilot/expert questionnaire in the evaluation of the first prototype has
been successful. It has lead to a significant insight into how the user group perceives
the purpose and use of the adaptive system. Therefore, also the second prototype
will be evaluated using a questionnaire. The user group will again consist of a mixed
group consisting of pilots, flight test engineers and avionics specialists.
7.4.3. Adaptivity related specifications
The adaptivity related specifications of D2 need not be changed at all. The adaptive
interface shall adapt to the situation and the pilot’s state and task. The adapted
constituents are modality (see below), display configuration, information presented,
level of detail, and timing strategy.
Special interest will be given to the aforementioned issue that the adaptation should
leave the pilot in command, and should be non-intrusive. Furthermore, the
consequences of the adaptation on the user interface itself should be intuitive, and
BEYOND
Functional Specifications and Architecture

35

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

support visual momentum. The usability analysis will put extra attention to these
aspects.
7.4.4. Multimodality related specifications
As indicated in the requirements, the second prototype shall incorporate an auditory
warning signal, augmenting the visual channel. The warning signal will be the result
of the integrated warning system. In other words, the auditory warning will present
the pilot a resolution that all participating warning systems (intelligent agents) agree
upon.
7.4.5. Simulation related specifications
The multi-agent adaptive intelligent flight deck system will be programmed in Java,
using JACK Intelligent Agents [tm], a product of Agent Oriented Software Pty. Ltd,
Victoria, Australia. Furthermore, all user interfaces (displays, controls) are
programmed in OpenGL. The platform is a Windows NT workstation. No efforts are
being conducted to generalize the real-time simulation software for product
simulation purposes.
7.4.6. Architectural issues
These have been covered above.

BEYOND
Functional Specifications and Architecture

36

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

References
[1] Abeloos, A.L.M. (2000). The Intelligent Adaptive Flight Deck. Technical Report, Delft University
of Technology in co-operation with Barco Display Systems.
[2] Abeloos, A..L.M., Mulder, M., and van Paassen, M.M. (2000). The Applicability of an Adaptive
Human-Machine Interface in the Cockpit. 19th European Annual Conference on Human Decision
Making and Manual Control, Ispra, Italy, June, 26-28, 2000.
[3] Dieterich, H., Malinowski, U., Kühme, T., and Schneider-Hufschmidt, M. (1993). State of the Art
in Adaptive User Interfaces. In Schneider-Hufschmidt, M. et al. (Eds.), Adaptive User Interfaces,
Principles and Practices, North-Holland, pp. 13-48.
[4] Reason, J. (1987). Generic Error-Modelling System (GEMS): A Cognitive Framework for
Locating Common Human Error Forms. In Rasmussen, J. et al. (Eds.), New Technology and Human
Error, John Wiley & Sons Ltd., pp. 63-83.
[5] Steentjes, A. and Mulder, M. (2000). Analysis of a Questionnaire addressing Free Flight’s “Big
Picture” Displays. Report, Delft University of Technology in co-operation with Barco Display Systems.

BEYOND
Functional Specifications and Architecture

37

Public Deliverable 8
February 2001

ITEA 99002 BEYOND
