# 2001 - beyond - 5. Functional specifications and architecture for domain

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - beyond.pdf

Section: 5. Functional specifications and architecture for domain

5. Functional specifications and architecture for domain
Home (2) (UI editor for the consumer domain)
5.1. Introduction
Home entertainment systems are embedded-computer systems that deliver
entertainment content to consumers in their homes. The home environment places
special constraints on entertainment systems, such as audio-video systems.
The expected evolution is that home systems can adapt to suit to individual
preferences, different contexts of use, and different types of content.
The user interfaces of adaptive home systems will have to communicate this
adaptivity to the user.
A first step towards adaptive user interfaces is to have an easy way to create
customisable or “flexible” user interfaces.
Flexibility means here: adaptivity in the development phase. However, the process to
develop these flexible user interfaces needs to be improved and supported by tools.
Currently, user interfaces are mostly specified on paper with sometimes-limited tool
support, and it takes many man-years to develop them. Prototypes or simulations, if
developed well, are far more comprehensive than lots of pages of description and
they allow early validation of the usability in a cost-effective way.
In the computer world, authoring tools or Rapid Application Development tools are
used to prototype and build the graphical parts of an application. These parts are
compiled into executable code.
An authoring tool for the consumer world can use a similar approach as the user
interface development tools in the computer world. However, the consumer world
has extra constraints that have to be taken into account: in particular, these are
limited RAM, lack of hard disk and comparably slow processors.
Philips DVS aims at developing a prototype of an authoring tool for visualisation,
specification, design, code generation of user interfaces for consumer products, with
particular emphasis on screen based user interfaces and control, and taking into
account the constraints of the consumer world as mentioned above.
The high level requirements for this authoring tool are:
•

The authoring tool should allow easy modification of the behaviour of
interfaces.

•

The authoring tool should support easy development of adaptive user interfaces.

•

The authoring tool should allow the functional requirements specification of the
next generation of consumer products to be developed in a much faster and
efficient manner.

BEYOND
Functional Specifications and Architecture

14

user

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

The first prototype of the authoring tool offers a basic functionality. This functionality
has been testing extensively by expert users in a pilot project. Their experiences
resulted in more knowledge, needed to specify new requirements.
In the mean time, a common reference model for adaptive systems has been
developed.
The second prototype should offer a more extended functionality based on the new
requirements and it should take into account the common reference model.
The specific requirements are listed in section 5.4.1.
The aim of the two prototypes is to give us insight in the feasibility of the
development of an authoring tool for user interface development of consumer
products.

5.2. Project status
In the first year of the project, we started with an early version of the first prototype
and focussed on the specification of the requirements for this prototype, by doing
usability tests. This resulted in a list of requirements for the first prototype as
described in section 5.4.1.
Also our contribution to the reference model for adaptivity (document D3) gave us a
better insight in the domain of adaptivity.
In the first half of the second project-year, the first prototype has been used in a pilot
project, where a user interface for a specific consumer system, a DVD (Digital
Versatile Disc) player was developed. This usability testing by expert users in a real
project was needed to gain better knowledge on what we expect from an authoring
tool. The requirements for a second prototype, specified in section 5.4.1 are based
on the knowledge gathered in these activities.

5.3. Methods and results concerning usability
The first prototype has been tested extensively by expert users: the user interface of
a DVD player has been simulated, a prototype UI has been developed and tested by
UI developers. Although the first prototype offered a limited functionality, it gave us
the possibility to gain experience on the desired functionality of an authoring tool.

5.4. Functional specifications
5.4.1. General changing requirements and extensions
In general, an authoring tool is a software development tool which aims at the
construction of application programs in a user-friendly way, and which allows a
significant reduction in development lead-time.
Our authoring tool specifically targets specification, design, simulation and code
generation, for the development of on-screen-based user interfaces and control of
consumer products.
BEYOND
Functional Specifications and Architecture

15

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

The first prototype offers a basic functionality: specification, design and simulation on
a PC are supported. Code generation for a target platform is not yet supported. The
requirements of the first prototype are described by the requirements listed below:
•

The authoring tool provides a set of standard widgets. A widget is a graphical
entity representing the interface between a user and the application software. The
set of standard widgets contains widgets of the following types:
•

screen, to define properties for a whole screen;

•

dialog, to provide a container for other widgets, excluding screens;

•

text, to provide a field to display a text string;

•

button, to trigger specific actions on a user request;

•

slider, to show the current state of an analogue value, e.g. volume;

•

picture, to display a bitmap, e.g. a logo.

•

The authoring tool provides for each project a project repository containing a font
definition, a colour palette, bitmap images and strings.

•

The authoring tool allows the user to manage a palette and its colours. Colours
are organised in a palette.

•

The authoring tool allows the user to import bitmaps from an external source.

•

The authoring tool allows the user to simulate a user interface on a PC.

An extensive evaluation of the first prototype, by trying out the tool for the
development of the on-screen-based user interface of a DVD player resulted in new
requirements for a second prototype.
From the UI developer’s point of view, the main need was the addition of the ability
to create menus in an OSD UI.
Besides this important user requirement, the second prototype of the tool should
demonstrate code generation for a target platform, in this case the DVD player.
The extension - requirements for the second prototype are:
•

The authoring tool provides a complex widget containing a menu structure and a
navigation function.

•

The authoring tool should provide a menu editor. This menu editor allows the
user to define items in a menu.

•

The authoring tool allows the user to generate C code for a target platform, e.g. a
DVD player.

BEYOND
Functional Specifications and Architecture

16

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

5.4.2. Usability related specifications
The general requirements, listed in section 5.1, all stress the usability aspects of the
tool.
A possible usability requirement that will be considered for future extensions is: “the
authoring tool should be able to assist the user in the authoring process by a wizard”.
5.4.3. Adaptivity related specifications
The first as well as the second prototype focus on off-line adaptivity: a user interface
developed with the tool is created, simulated and modified on a PC. Once the UI
satisfies, the authoring tool can generate C code for the target platform, e.g. a DVD
player. The compiled C code can then be loaded in the target system.
Off-line adaptivity is a first step towards the development of more adaptive user
interfaces. We called this flexibility instead of adaptivity. The tool offers the UI
developer a more flexible way of developing a UI.
5.4.4. Multimodality related specifications
The target platforms for which user interfaces are developed with this tool, e.g. a
DVD player, have several types of in- and output interfaces. Thus the authoring tool
should be able to support specification, simulation and code generation of UI aspects
related to these i/o peripherals. A Multimodal user interface for the authoring tool is a
possible requirement for future versions.
5.4.5. Simulation related specification
As specified in the requirements of section 5.4.1, the first as well as the second
prototype allow to make simulations of a user interface on a PC. Simulations are a
way to get early feedback on a UI that is being developed.
5.4.6. Architectural issues
Until now, Philips Hasselt concentrated for the Beyond project on usability testing
and on requirements specification. A lot of effort will be done to design the second
prototype conform the requirements specified for the second prototype of the
authoring tool.

BEYOND
Functional Specifications and Architecture

17

Public Deliverable 8
February 2001

ITEA 99002 BEYOND

BEYOND
Functional Specifications and Architecture

18

Public Deliverable 8
February 2001

ITEA 99002 BEYOND
