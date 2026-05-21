# 1999 - multi-mahjong - 1. Introduction

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1999 - multi-mahjong.html

Section: 1. Introduction

1. Introduction

This document formally states the requirements for the MultiMahjong product.

These requirements have been prioritised into three levels:

Essential

The minimum set of requirements for the product to be accepted (see
Section 8
).

Highly Desirable

Requirements that are considered to be likely inclusions to the product, time permitting.

Desirable

Requirements that are not likely to be added in this version, but should be considered for future modifications.

MultiMahjong is a product consisting of two programs - a
MultiMahjongServer and a MultiMahjongClient. This Server/Client
architecture will allow up to 4 players to play Mahjong against each
other over a TCP/IP network. The MultiMahjongClient program will also
allow 1 player to play in a stand-alone mode.

As any game of Mahjong requires 4 players to play, and there
may not be 4 people available for a network game, the game will allow
users to choose enough computer opponents to make up the required 4
players. In a single player game, the user will play against 3 computer
opponents.

To play the game, users will use the MultiMahjongClient. The
MultiMahjongServer is to reside on a TCP/IP server and will communicate
with MultiMahjongClients.

The client requires the product for commercial purposes. The MultiMahjongClient program is to be sold to potential users (see
Section 5.1.1
) and the MultiMahjongServer is to initially reside on a server owned or operated by the client.

The client for this project is:

Steve Goschnick, Managing Director

Solid Software Pty Ltd

Level 3, Bouverie Street,

Carlton VIC, 3053

Ph: 03 9344 9322, 03 9344 0154

E-Mail:
gosh@solidsoftware.com.au
,
gosh@cs.mu.oz.au

Our team for the project is called K-Team and consists of:

Joanna Araminta (
jiar
)

Victor Leung (
vhle
)

Joel Brakey (
jebr
)

Michael Hart (
mwhart
)

Dean Cortinovis (
dcort
)

Long Tang (
lqkt
)

Ph: 9889 4423 (Project Manager)

Ph: 9706 1560

Ph: 9859 6038

Ph: 9859 5419

Ph: 9798 2684

Ph: 9540 8992

The supervisor for the project is:

Anthony Senyard (
anthls
)

Ph (W): 9344 1940

Ph (H): 9417 2839

This document contains many
references to the rules of Mahjong, specifically the Chinese rules of
Mahjong. It is assumed that the reader of this document is familiar with
these rules as many of the requirements are Mahjong specific. These
rules can be found in the following book:

Carkner, K.J. "How to play Mah Jong",

1993, Penguin Books Australia Ltd.
