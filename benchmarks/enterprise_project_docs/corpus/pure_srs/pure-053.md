# 1999 - multi-mahjong - 4. Functional Requirements

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 4. Functional Requirements

4. Functional Requirements

This section states the requirements that relate to the
functionality of the MultiMahjong system. Each requirement has been
prioritised according to the levels set out in the Introduction (
see Section 1
). Requirements that relate to what is displayed on the user's screen are defined in
Section 6
.

Note that for single player games, the MultiMahjongServer will
not be required and the player need not be connected to a TCP/IP
network. Although many requirements mention that the MultiMahjongClient
will send certain information to the MultiMahjongServer, in the single
player game, this is not the case. In a single player game, the
MultiMahjongClient will intercept this information and process it
internally. The reference to the MultiMahjongServer is made to reduce
duplicate requirements.

4.1 The MultiMahjongServer

Level 1 Requirements:

4.1.1

The MultiMahjongServer will be designed to
reside on a central computer (server) that is connected to a TCP/IP
network and has a unique IP address.

4.1.2

The MultiMahjongServer will allow connections from MultiMahjongClients and communicate with them using IP.

4.1.3

The MultiMahjongServer will serve as a node
for MultiMahjongClients. That is, it will be able to relay data received
from one MultiMahjongClient to other MultiMahjongClients that request
it.

Level 2 Requirements:

4.1.4

The MultiMahjongServer will automate the
game initialisation functions (as opposed to the MultiMahjongClient
doing them), such as: randomising tile order, randomising seating
position and storing the "Game Info" database (see
Figure 3.1.2
).

4.1.5

The MultiMahjongServer will contain a High Scores list with the names and scores of the top MultiMahjong players.

Level 3 Requirements:

4.1.6

The MultiMahjongServer will allow players on MultiMahjongClient programs to chat with each other in real time.

4.1.7

The MultiMahjongServer will allow players on
MultiMahjongClient programs to modify their own names and icons during
gameplay (as opposed to only at the beginning).

4.1.8

The MultiMahjongServer will support an
architecture whereby all Computer Opponents (CO) required will reside on
it instead of on the MultiMahjongClient programs.

4.1.9

The MultiMahjongServer will have a graphical
user interface with which the administrator of the server can get log
information and change game settings.

4.1.10

The MultiMahjongServer will be able to save preferences to a file and read from that file at start-up.

Note that all requirements hereafter are concerned with the MultiMahjongClient program.

4.2 Beginning the Game

Level 1 Requirements:

4.2.1

When the user begins the MultiMahjongClient
program, they will be able to choose to create a new multi player game,
to create a new single player game, to join an existing multi player
game, or to quit the program. These options will be available at any
stage while the program is running as long as there is no game currently
being played by the user (see
Section 4.4
for more details about quitting).

4.2.2

When a user creates a new multi player game, they must:

4.2.2.1

Enter their name.

4.2.2.2

Choose an icon from a predetermined list.

4.2.2.3

Decide the number of human and computer
opponents they want. As any game of Mahjong requires 4 players, the
MultiMahjongClient will limit the user to choosing 4 players in total.

4.2.2.4

Set the score limit for winning a hand of Mahjong.

4.2.2.5

When all the necessary human players have joined the game, the user may choose to begin the game.

4.2.3

The MultiMahjongClient must send this game
initialisation information to the MultiMahjongServer so that the
MultiMahjongServer can create a new game.

4.2.4

The processing for any Computer Opponents (CO) (see
Section 4.5

for more detail) will be done by the MultiMahjongClient program. In a
single player game, the MultiMahjongClient will need to process for 3
COs. In a multi player game with 2 human players, each
MultiMahjongClient will support 1 CO. In a multi player game with 3
human players, only 1 of the 3 MultiMahjongClients will support a CO.
Obviously, in a multi player game with 4 human players, no CO is
required.

4.2.5

When a user creates a new single player game, they must:

4.2.5.1

Enter their name.

4.2.5.2

Choose an icon from a predetermined list.

4.2.5.3

Set the score limit for winning a hand of Mahjong.

4.2.6

When a user selects the option to join an
existing game, the MultiMahjongClient will retrieve a list of any games
that still require players from the MultiMahjongServer.

4.2.7

When a user wishes to join a multi player game, they must:

4.2.7.1

Enter their name.

4.2.7.2

Choose an icon from a predetermined list.

4.2.7.3

Choose which of the available games they wish to join.

4.2.8

The MultiMahjongClient must send this join information to the MultiMahjongServer.

4.2.9

In a multi player game, each MultiMahjongClient must retrieve the following data from the MultiMahjongServer:

4.2.9.1

Whether it must support a CO.

4.2.9.2

The score limit for a hand.

4.2.9.3

All players' names, icons and seating positions.

4.2.9.4

The tiles of the human and CO (optional) player supported on the MultiMahjongClient.

Level 2 Requirements:

4.2.10

The list of un-started games that the
MultiMahjongClient fetches from the MultiMahjongServer will be displayed
in such a way that users can see the following information about each
game:

4.2.10.1

The name and icon of the player who created the game.

4.2.10.2

The score limit for winning a hand.

4.2.10.3

The number of places that still need to be filled before the game can commence.

4.2.11

The MultiMahjongClient will save the user preferences in a file and read them in when the program begins.

Level 3 Requirements:

4.2.12

Users who create a new game will be able to
change the ability level of any CO involved in the game. There will be 3
levels available: Beginner, Intermediate and Advanced.

4.2.13

Users who create a new game will be able to choose to play different variations of Mahjong rules other than those described in
Section 4.3.1
. The variations will include the Cleared Hand variation and the Japanese variation (see the
rulebook
for more detail).

4.2.14

Any user who creates or joins a game will be
able to upload their own JPEG or GIF image that they wish to have
displayed above their name, if they do not wish to use a preset icon.

4.3 Playing the Game

Level 1 Requirements:

4.3.1

The MultiMahjongClient must only allow
players to make moves according to the Chinese rules of Mahjong as
described in the rulebook, "
How to Play Mah Jong
".

4.3.2

The MultiMahjongClient will inform the user whose turn it is to pick up a tile.

4.3.3

The MultiMahjongClient will retrieve other
players' changes in the game situation from the MultiMahjongServer. The
user's screen is then updated to display these changes. The following
game changes are displayed:

4.3.3.1

Another player picks up a tile from the wall.

4.3.3.2

Another player exposes/reveals a set of tiles.

4.3.3.3

Another player discards a tile.

4.3.4

If the configurations of: the current
discard, the tiles in a user's hand, and the player whose turn it is,
would allow the user to Chow/Pung/Kong/Mahjong under the Chinese rules
of Mahjong, the MultiMahjongClient will inform the user that they can do
so. If they choose to take this action, then the MultiMahjongClient
must send this information to the MultiMahjongServer.

4.3.5

User's will be able to pick up a tile from
the wall if it is their turn. If they choose to pick up, the
MultiMahjongClient must send this information to the MultiMahjongServer.

4.3.6

User's will be able to discard a tile if
they have picked one up. When they choose to discard, the
MultiMahjongClient must send this information to the MultiMahjongServer.

4.3.7

The MultiMahjongClient must inform the user if another player is fishing.

4.3.8

The MultiMahjongClient must inform the user if another player goes Mahjong. The wind of the round is also updated (if required).

4.3.9

The MultiMahjongClient must inform the user if the hand has ended in a draw.

Level 2 Requirements:

4.3.10

The MultiMahjongClient will keep the user's tiles in order.

4.3.11

The MultiMahjongClient will play sound effects associated with certain game actions.

4.3.12

Users will be able to turn the sound on or off at any stage during the game.

4.3.13

Users will have access to the User's Documentation online (see
Section 7.2
) at any stage during the game.

4.3.14

Users will be able to view the High Scores list that is located on the MultiMahjongServer.

4.3.15

The MultiMahjongClient will automate the picking up of a tile from the wall if the user has no other option.

Level 3 Requirements:

4.3.16

User's will be able to Undo their last move if playing in single player mode.

4.3.17

User's will be able to Save their game if playing in single player mode.

4.3.18

User's will be able to chat with each other in real time.

4.3.19

User's will be able to change their icons/pictures and names during the game.

4.4 Ending the Game

Level 1 Requirements:

4.4.1

The game will end when all 4 rounds have been played or if the user chooses to end the game.

4.4.2

The user will be able to end the game at any
stage of the game. The user will then be able to quit the program or
begin/join a new game.

4.4.3

The MultiMahjongServer will inform all
MultiMahjongClients connected to the game that the game has ended. Users
of any MultiMahjongClient previously connected to the game will have
the choice to quit the program or to begin/join a new game.

Level 2 Requirements:

4.4.4

If a user leaves the game prematurely, a new
CO is created on another user's machine to fill their place. This CO
will take over the user's current position and circumstance within the
game. This CO will play at an ability level as defined in the Level 2
Requirements for the CO (see
Section 4.5.6
).

Level 3 Requirements:

4.4.5

If a user leaves the game prematurely, a new
CO is created on another user's machine to fill their place. The user
who created the game will decide at what level (see
Section 4.5.8
) the CO will play at.

4.5 Computer Opponent (CO)

Level 1 Requirements:

4.5.1

The CO must play moves according to the Chinese rules of Mahjong.

4.5.2

The CO will not have access to the data
containing the faces of any tiles in the wall or any concealed tiles in
any other players' hands.

4.5.3

The CO will have access to the number of tiles in the wall or in a player's hand.

4.5.4

The CO will be able to read any player's exposed or revealed hands.

4.5.5

The CO will be able to pick up tiles off the wall, discard tiles, reveal Kongs, and Chow/Pung/Kong/Mahjong.

Level 2 Requirements:

4.5.6

The CO will be able to determine what tiles
have not been played according to the tiles that have already been
discarded, exposed or revealed.

4.5.7

The CO will be able to recognise "almost
finished" sets of tiles (i.e. 2 tiles in a sequence is an almost
finished Chow) and will not discard tiles in such sets. This is to give
the CO a basic level of strategy.

Level 3 Requirements:

4.5.8

The CO will be able to play at 3 different ability levels: Beginner, Intermediate and Advanced.

4.5.9

The CO will be able to perform look ahead algorithms to determine its best move in the Intermediate and Advanced levels.

4.5.10

The CO will be able to perform calculations at any stage of the game.

4.5.11

The CO will be able to play any version of the rules that are specified by the user who creates the game.

4.5.12

There will be CO's of different playing styles that the user can choose from.
