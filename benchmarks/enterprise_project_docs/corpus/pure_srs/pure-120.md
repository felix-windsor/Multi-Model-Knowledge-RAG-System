# 2001 - elsfork - 2. The specifications for data transmission in this specification apply to the individual nodes

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 2. The specifications for data transmission in this specification apply to the individual nodes

2. The specifications for data transmission in this specification apply to the individual nodes
in the Wind Farm LAN
3. At the individual nodes, the methods for acquisition and compilation of data are conducted on basis of individual, proprietary methods not subject to this specification.
4. Connection to ”other” parties (e.g. vendor) is established through gateways to the communication protocol and media of their choice.
5.
Communication
server

Application
server

HMI’s for supervison
and maintenance

Maintenance
server

WAN/LAN at operator
Wind Farm
Server
LAN at Wind farm

Interface level

Control
unit

Figure A1: Network System 1. Interface level at the individual nodes.

Page A-1

ELFORSK

Network System 2 (interface level at the Wind Farm Server)
The basics of this structure are illustrated in Figure A2. The network structure can be summarised as follow:
1. The network consists of interconnected LAN’s. A Wind Farm LAN is established at the
wind farm and is connected to an operator LAN
2. A Wind Farm Server is gateway between the Wind Farm LAN and the operator LAN. The
server should be transparent for all data necessary for operational or control functions.
