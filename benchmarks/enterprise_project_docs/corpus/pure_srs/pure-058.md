# 1999 - multi-mahjong - 9. Examples of Behaviour

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 9. Examples of Behaviour

9. Examples of Behaviour

This section describes a possible scenario that incorporates
some of the requirements mentioned in this document. As some of the
requirements used are Level 2 and Level 3 requirements, the actual
implementation of the product may not reflect this scenario exactly.

9.1 Beginning the Game

The administrator (
5.1.2
) runs the MultiMahjongServer program on a server (
4.1.1
). This program begins running and waits for MultiMahjongClients to connect (
4.1.2
).

A user (
5.1.1
), Bob, runs the MultiMahjongClient program on another computer. A dialogue box (
6.3.6
) appears on the Bob's computer displaying the options to begin the game (
4.2.1
,
4.2.2
). Bob enters his name (
4.2.2.1
), chooses an icon (
4.2.2.2
), sets the score limit (
4.2.2.4
) and decides to select one human opponent and two CO opponents (
4.2.2.3
). Bob then waits for a human opponent to join.

Another user, Sally, also runs the MultiMahjongClient program, enters her details and selects to join an existing game (
4.2.7
)
from the dialogue box. The MultiMahjongClient retrieves a list of the
available games (including Bob's) from the MultiMahjongServer (
4.2.6
). The MultiMahjongClient displays this list on the screen (
6.3.7
). Sally selects Bob's game and joins the game.

Bob sees that Sally has joined and selects to begin the game (
4.2.2.5
).
The MultiMahjongServer receives the begin game command from Bob's
MultiMahjongClient and it initialises all information necessary to begin
the game (
4.1.4
) and sends it to both Sally's and Bob's MultiMahjongClients (
4.1.3
).
The processing for one CO player will be done by the MultiMahjongClient
running on Bob's machine, the other by the MultiMahjongClient running
on Sally's machine (
4.2.4
).

9.2 Playing the Game

A main window containing all the game information (
6.3.4
) is displayed on both Sally's and Bob's screens.

Bob, Sally and the CO's take turns in picking up (
4.3.5
) and discarding (
4.3.6
) tiles . After Sally discards a certain tile, Bob can Chow (
4.3.4
), and a button named 'Chow' in his main window becomes active (
6.3.4.6
). Bob chooses to Chow by clicking on this button. Bob's MultiMahjongClient sends this move to the MultiMahjongServer (
4.3.4
), which subsequently sends this move to the other MultiMahjongClient (
4.1.3
). The tiles in both Bob's and Sally's main window are updated to show that Bob has Chow'ed (
4.3.3.2
).

The hand continues in this fashion, with all players making moves within the Chinese rules of Mahjong (
4.3.1
).
After a few moves, the combination of tiles in Sally's hand allows her
to Mahjong and a button named 'Mahjong' becomes active in her main
window (
6.3.4.6
). Sally clicks this button and a new hand begins. When all hands have been played, the Wind of the Round indicator is updated (
4.3.8
) and a new round begins. The game continues in this fashion

9.3 Ending the Game

At the end of the 4th round, Bob goes Mahjong. Bob's MultiMahjongClient sends this information to the MultiMahjongServer (
4.3.8
) which sends it to the other MultiMahjongClient (
4.3.1
). The main window on both MultiMahjongClients is closed and the original dialogue box (
6.3.6
) is displayed (
4.4.3
).

Both Bob and Sally choose to quit the program and the MultiMahjongClients on both machines exit (
4.4.1
).
