# 1999 - multi-mahjong - 6. User Interface Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 6. User Interface Requirements

6. User Interface Requirements

This section states all the requirements of the MultiMahjong
system that are related to what the user sees and how the user interacts
with the MultiMahjong system.

6.1 User Interface - MultiMahjongServer

Level 1 Requirements:

6.1.1

The MultiMahjongServer will have no graphical user interface and will be run using a command prompt.

Level 2 Requirements:

6.1.2

The MultiMahjongServer will have a graphical
user interface with which the administrator of the server can get log
information and change game settings. No requirements for this graphical
user interface are set in this document.

6.2 User Interface - MultiMahjongClient

Level 1 Requirements:

6.2.1

The MultiMahjongClient will have a graphical
user interface that the user will be able to interact with using a
mouse and a keyboard. The details of this graphical user interface are
described in
Section 6.3
. Where it is appropriate, keyboard shortcuts will be provided for mouse based operations.

Level 2 Requirements:

6.2.2

The MultiMahjongClient will have sound effects associated with the game actions.

Level 3 Requirements:

6.2.3

The MultiMahjongClient will have animation also associated with game actions.

6.3 Graphical User Interface - MultiMahjongClient

The graphical user interface (GUI) described below only
applies to the MultiMahjongClient program. As the validity of these
requirements will not be determined until the design phase, most of them
are Level 2 or Level 3 requirements. As described in
Section 6.2.1
, the
existence
of the GUI is a Level 1 requirement, however, the
detail
of the GUI is not necessarily so.

Level 1 Requirements:

6.3.1

The GUI is to be designed so that the user can perform all of the Level 1 requirements set out in
Section 4
.

6.3.2

The GUI is to be contained within a screen resolution of 800 x 600 pixels.

6.3.3

All graphics will be in 16 bit colour.

6.3.4

There will be a Main Window that will contain the following game elements:

6.3.4.1

The faces of the current user's tiles

6.3.4.2

The wall with the remaining tiles

6.3.4.3

The backs of the other player's tiles

6.3.4.4

Any revealed or exposed tiles from any player

6.3.4.5

The last discarded tile

6.3.4.6

Buttons to allow the user to pick up a tile, to discard a tile, to Chow/Pung/Kong/Mahjong and to reveal a Kong.

6.3.4.7

A button will be made inactive (typically greyed out) if the user is not allowed to perform the associated activity.

Level 2 Requirements:

6.3.5

The Main Window will also contain a tabbed frame (with 3 tabs) to display the following items:

6.3.5.1

Tab1: Player's name

6.3.5.2

Tab1: Player's icon

6.3.5.3

Tab1: Wind of the round

6.3.5.4

Tab2: Score

6.3.5.5

Tab2: Limit of the hand

6.3.5.6

Tab3: Preferences

6.3.6

The options at the beginning of the program, as described in
Sections 4.2.1, 4.2.2, 4.2.5 & 4.2.7
, will be presented to the user using a dialogue box with buttons associated with each option.

6.3.7

The list of available games, as described in
Section 4.2.7
,
will be presented to a user in a dialogue box with a scroll bar and
selectable list items so that the user can select the game they wish to
join.

6.3.8

The Main Window will show the dead tiles.

Level 3 Requirements:

6.3.9

When a button becomes active, it will use animation to get the user's attention.

6.3.10

When a player performs a Chow/Pung/Kong/Mahjong, the tiles involved will be animated.

6.3.11

The user may click in the frame that contains the remaining wall and a frame showing the discarded tiles will be shown.

A draft version of the proposed Main Window appears below:

Figure 6.3.1 - Draft of proposed Main Window
