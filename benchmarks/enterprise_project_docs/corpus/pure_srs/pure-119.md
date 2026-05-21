# 2001 - elsfork - 8 Appendices

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 8 Appendices

8 Appendices
A: Technical Solutions
Appendix A describes some proposed solutions that should correspond to the specification.
The intention is to have these concrete solutions as a guideline for the suppliers affected. It is
therefore important that the solutions have been validated against the requirements.
B: Protocols
Some of the suggested protocols, proposed in Appendix A, have been summarised and investigated in this appendix.
C: Data lists
The data from the wind power plant as well as the data sent to the wind power plant are presented as grouped data lists in this appendix.

Page 27

ELFORSK

Page 28

ELFORSK

A Appendix A, Technical solutions
A.1 Introduction
This appendix present some examples on technical solutions to fulfil the requirements stated
in the main document.
A.2 Network structure and interfaces
The communication network on which data transactions shall take place may be organised as
one of the following systems:
- Network system with interface at the individual nodes
- Network system with interface at the Wind Farm Server
- Network system with interface to existing older control system/RTU
Network System 1 (interface level at the individual nodes)
The basics of this structure are illustrated in Figure A1. The network structure can be summarised as follow:
1. The network consists of interconnected LAN’s. A Wind Farm LAN is established at the
wind farm and is connected to an operator LAN. The wind farm LAN is a logical LAN.
Any topology is possible.
