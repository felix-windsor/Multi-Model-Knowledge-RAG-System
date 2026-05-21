# 2001 - beyond - 3. Functional specifications and architecture for domain

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - beyond.pdf

Section: 3. Functional specifications and architecture for domain

3. Functional specifications and architecture for domain
public (public terminals and kiosks)
3.1. Introduction
APC (apc interactive solutions AG) is working on the development of information
networks, terminals and kiosk solutions to address people's needs for information in
public space. The core component in this project is the information terminal which is
called accesspoint. It resembles the interface between users and the network which
transports and provides context sensitive information. The accesspoint is higly
multimodal and provides a good basis for adaptive services.
APC has devoted part of its development to user interface design. Many features
have been implemented in a first multimodal Accesspoint prototype. This is
considered to be crucial not only for the accesspoint services but the acceptance of
the whole system where essential functionalities are speech controlled dialogs. The
second prototype will follow and offer adaptive features as well. It will enable
enhanced understanding of voice commands and beter dialog design will be an
important step towards natural language understanding.

3.2. Project Status
During the first year, comprehensive analysis and functional specifications have
culminated into the first multi-modal prototype accesspoint. Its basic technological
implementation has been tested during operations in numerous public space
applications as a geographical information system and marketing support media
among many others.
By previous customer projects experience and internal evaluations we derived the
need for a new extended architecture and to re-implement most of the software
solutions in order to comply with originally defined functional specifications,
implement usability and new functional requirements, establish a control and
distribution network for the terminals and tune overall performance.
During the second year, development of modular component based modules will
address the lack of functionality and interoperability that are currently missing. Goals
for the second prototype are guidelines for basic user interface design and the
simulation of a sample application. Another focus is to comply with open architecture
standards and maintain accessibility of web-hosted data.

3.3. Methods and results concerning usability
As indicated in the project status, usability data has been acquired by log file
analysis and video surveillance of user sessions. Furthermore, users have been
asked to participate in opinion polls and fill in questionnaires.
Pre-evaluation of the user interface has been carried out together with design
experts by APC corporate partners. Results were mostly focused on acceptance of
the system in public space, and address the design of the solid, speech and
graphical user interface. It has been found that a major issue in the design of the
solid user interface is ergonomics.
BEYOND
Functional Specifications and Architecture

8

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

The limiting factor is usability of the graphical user interface. It is followed by the
integration of speech control features into the user interface.

3.4. Functional Specifications
The most important requirement is the stability of the system on a high-level user
application level, which is a consequence of the availability of basic network and
terminal functionality.
System failures caused by user operation or network malfunctions have to be
avoided. Dead ends in dialogs have to be addressed by a special help system and
contextual understanding has to be provided. The system must guide users
throughout the interaction process quickly and effectively and it has to be designed
to avoid cognitive overloads caused by information overflow.
The accesspoint has to be controllable through different modalities. A switch
between modalities must not affect the system operations, consequently there
should be no need to re-initiate the dialog status. Likewise, it should be possible to
switch the current context without loosing perspective in case the system does not
estimate the context properly.
3.4.1. General changing requirements and extensions
There is an urgent need for extensibility of the software system. The monolithic
implementation which is used at the moment does not support modelling of
upcoming functionality requests and it is very difficult to maintain and extend.
Although the first prototype complies with the specified functionality we have decided
to re-implement it from scratch and carefully design all application interfaces for
process communications.
Better development tools to handle the speech system on an abstract level are
required to improve the process of extending its rule database. For better
extensibility, context engines need to be implemented rather than interfaces and the
method of choice are neural networks. As for training purposes new tools are
needed and should be able to derive input from rule databases which are used at the
moment.
3.4.2. Usability related specifications
There are two major aspects which are of vital importance for the acceptance of the
terminal in public space applications. Firstly the solid user interface requires high
standards in ergonomics and robustness. Secondly the system needs to have a
``subtle notion'' of its services to guide users quickly and effectively.
The terminal pro actively offers its services i.e. must be able to attract and help
people. It must be self explicable and understand users' needs. It must also be able
to handle context specific dialogs. Dialogs which it doesn't understand clearly should
be handled properly to limit user frustration. Context switches must be supported at
any state of the session and the system should offer alternatives and rank them by
guessing its likelyhood.
The graphical and speech user interface need to complement each other. They
represent input and output channels and provide access to the state of the context
BEYOND
Functional Specifications and Architecture

9

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

engine. The information flow must be compatible with average user capabilities to
avoid cognitive overload. The graphical user interface model presents information in
an abstract two dimensional way and supports virtual characters.
Further points address training of the context engine of which some have already
been mentioned above.
3.4.3. Adaptivity related specifications
The following adaptivity specifications are limited to single user sessions. It is
assumed that multiple user sessions are not very likely to occur in public space
applications. They are treated elsewhere.
A general single user session occurs when one person in front of the terminal
interacts with the system. An onlooker, or person inside the interaction area of the
terminal is already considered to be a user.
Some adaptivity related specifications are partly indicated in section ``Usability
related specifications'' above. Contextual understanding is an example and support
of context switches without explicit requests are another. The interaction process
should be as natural as possible and the development should ultimatly enable
natural language understanding.
``Technically'' speaking, the system should be able to detect people automatically
and doesn't need to be approached by a subject. It should be able to initiate the first
step and react adaptively because it can recognize people and distinguish humans
from other life, e.g. dogs.
Another requirement is speaker independent voice recognition which is essential in
public space applications, i.e. every single user is understood instantly irrelevant of
age, gender or other distinct characteristics.
3.4.4. Multimodality related specifications
The terminal is designed to support classical input-output channels like typing or
reading, and complement them with speech and visual capabilities.
Except for high level features, most of the above mentioned adaptivity specifications
primarily rely on multimodality related features. Visual and audio surveillance enable
user detection and language understanding through face and speech recognition. At
the moment, higher level functions and more powerful features for enhanced sensing
can be implemented by combining speech and visual information.
Mode switches which are not initiated by the system are only possible through input
channels. Output presentation is determined by the system and the user has no
direct influence in this case. If desired the user can override default settings, but
because of privacy issues, certain output channels are preferred.
3.4.5. Simulation related specifications
Certain new usage scenarios require extended functionality which has not been
implemented yet. Simulation and testing will provide further insight into the
integration process and give more practical hints on usability, before new features
BEYOND
Functional Specifications and Architecture

10

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

materialize. The system functionality should be extensible and able to be integrated
into the simulation environment to interface existing and new features at the same
time.
To describe the newly defined specification, the simulation environment should
provide an abstract high level scripting language thus providing an interpreter.
3.4.6. Architectural issues
To ensure extensibility of the software system, an open architecture has been
chosen. All functionalities will be implemented using components or even distributed
components in a client-server oriented approach.
Because of multimedia capabilities operating system selection is virtually limited to
the MS Windows based platform.
The implementations of the context engine with near natural language capabilities,
the multiple modality support functions and the speech and graphical interfaces are
heavily component based.

BEYOND
Functional Specifications and Architecture

11

Public Deliverable 8
February 2001

ITEA 99002 BEYOND
