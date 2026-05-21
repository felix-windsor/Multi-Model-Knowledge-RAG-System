# 1999 - multi-mahjong - 3. The Proposed Logical System

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 3. The Proposed Logical System

3. The Proposed Logical System

As this is only a
suggestion
for the proposed logical system, all requirements mentioned in this section are Level 2 requirements.

3.1 Data Flow Diagrams (DFDs)

The following diagrams show the flow of data between the entities of the MultiMahjong system:

Figure 3.1.1 - Level 0 DFD of the MultiMahjong System

Figure 3.1.2 - Level 1 DFD of the MultiMahjong System

Note that these diagrams only describe the top level
processes and the data that flows between them. They do not describe the
functions of the MultiMahjongClient and MultiMahjongServer programs as
the processes are shared between both programs. The functionality of the
MultiMahjongClient and MultiMahjongServer programs is described in more
detail in
Section 4
.

3.2 Data Dictionary

name:

player action

aliases:

user input

where/how used:

process player action
(input)

description:

player action = [mouse state | keystroke]

mouse state = co-ordinate + button state

co-ordinate = xval + yval

xval = *horizontal distance (in pixels)*

yval = *vertical distance (in pixels)*

keystroke = *character from keyboard*

name:

pref. data

aliases:

preferences data, prefs

where/how used:

process player action
(input and output)

preferences
(input and output)

description:

preference data = [current player's name | icon |

limit for winning hand | sound on/off]

current player's name = *any 30 character unicode-based string*

icon = *colour image in a JPEG or GIF formatted file*

limit for winning hand = *6 digit number*

sound on/off = *boolean*

name:

screen changes

aliases:

where/how used:

update screen
(input)

description:

screen changes = ["display preferences window" command |

"update icon" command |

"update name" command |

"update game area" command |

"display action button" command |

"updated score" command]

"display preferences window" command = *content to be decided

in
SDD*

"updated icon" command = *content to be decided in SDD*

"updated name" command = *content to be decided in SDD*

"updated game area" command = *content to be decided in SDD*

"display action button" command = *content to be decided in SDD*

"updated score" command = *content to be decided in SDD*

name:

game data

aliases:

where/how used:

process player action
(input and output)

handle game
(input and output)

determine computer opponent action
(input and output)

game info
(input and output)

description:

game data = [tile position | current round |

first
Wind of the Round | current Wind of the Round |

current player]

tile position = [The Wall | Discard | Dead Tile | Exposed Set |

Revealed Kong]

Exposed Set = [Exposed Kong | Exposed Pung | Exposed Chow]

current round = *1 digit number*

first Wind of the Round = *content to be decided in SDD, will be

player
ID*

current Wind of the Round = *content to be decided in SDD,

will
be player ID*

current player = *content to be decided in SDD, will be player ID*

name:

game action

aliases:

where/how used:

process player action
(output)

handle game
(input and output)

determine computer opponent action
(input and output)

description:

game action = [discarded tile | picked up tile | exposed tile]

discarded tile = *tile class (tile class to be decided in SDD)*

picked up tile = *tile class (tile class to be decided in SDD)*

revealed tile = *tile class (tile class to be decided in SDD)*

name:

graphic data

aliases:

where/how used:

update screen
(input)

graphics
(output)

description:

graphic data = *colour image file*

name:

graphic request

aliases:

where/how used:

graphics
(input)

update screen
(output)

description:

graphic request = *command to be determined in SDD*

name:

screen image

aliases:

where/how used:

player
(input)

update screen
(output)

description:

screen image = *what appears on screen*
