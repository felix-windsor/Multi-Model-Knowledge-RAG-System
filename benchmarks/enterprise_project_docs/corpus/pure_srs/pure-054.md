# 1999 - multi-mahjong - 5. Non-Functional Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 5. Non-Functional Requirements

5. Non-Functional Requirements

This section states all the requirements of the MultiMahjong
system that are not related to the functionality of the MultiMahjong
system.

5.1 Nature of the Users

5.1.1 MultiMahjongClient

Level 1 Requirements:

5.1.1.1

The potential users of the MultiMahjongClient product will be anyone who enjoys playing or is interested in the game of Mahjong.

5.1.1.2

The product is aimed at users who have a basic knowledge how to operate a PC, Macintosh or Unix box (see
Section 5.3.1
).

5.1.1.3

Users who wish to play multi player Mahjong
will not need to have advanced knowledge of TCP/IP networking. It is
assumed however, that the computer has been configured correctly to
connect to a TCP/IP network.

5.1.1.4

Prior knowledge of Mahjong rules is not necessary, as the product will be designed for both players with some or no experience.

5.1.2 MultiMahjongServer

Level 1 Requirements:

5.1.2.1

The user of the MultiMahjongServer will most likely have general knowledge of a Web Server environment.

5.1.2.2

The user will need to know how to set-up and operate a TCP/IP server.

5.1.2.3

The user will understand the basic
principles of networking and know any networking information associated
with the server the MultiMahjongServer program is run on (hostname and
IP address).

5.2 Error Handling

Every error that occurs during program execution can be
classified into two types - fatal and nonfatal errors. The distinction
between the two is that the program is unable to continue to execute
upon encountering a fatal error.

5.2.1 Nonfatal errors:

Level 1 Requirements:

5.2.1.1

If a nonfatal error occurs, a dialogue box reporting the nature of error will be displayed.

5.2.1.2

As the error is classified 'nonfatal', the user will be able to continue the current game.

Level 2 Requirements:

5.2.1.3

An option to access the online troubleshooting guide (
Section 7.2.4
) is included in the error dialogue box.

5.2.2 Fatal errors:

Level 1 Requirements:

5.2.2.1

If a fatal error occurs, a dialogue box reporting the nature of error will be displayed.

5.2.1.2

The only option to the user is to quit the
game. All processes will be cleaned up (if possible) and the program
execution will terminate.

5.3 Implementation Constraints

Level 1 Requirements:

5.3.1

The MultiMahjong system is to be written using
JDK 1.2
(the Java development kit from
Sun Microsystems
).

5.3.2

The coding standard will be the same as that suggested by
Sun Microsystems
. This document is available in PDF in our repository at:

MultiMahjong/doc/SQAP/CodeConventions.pdf

or online at:

ftp://ftp.javasoft.com/docs/codeconv/CodeConventions.pdf

Level 3 Requirements:

5.3.3

Multiple languages will be supported using Java's Unicode standard.

5.4 Hardware Constraints

Level 1 Requirements:

5.4.1

The software will run on any machine that is capable of running a Java Virtual Machine that supports
JDK 1.2
(see
Section 5.3
). These machines include:

5.4.1.1

A PC operated under Windows 95/98/NT

5.4.1.2

A Macintosh operated under OS 8

5.4.1.3

A Unix box operated under Solaris 2.6 or Solaris 7

Level 2 Requirements:

5.4.2

The minimum system requirements for the product to operate under are:

5.4.2.1

100 MHz processor

5.4.2.2
