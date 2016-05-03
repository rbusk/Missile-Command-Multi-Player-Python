# Paradigms_Project
Our final paradigms project including the twisted and pygame libraries.

The game is currently set up to run through the local host, so if you want to change this please change server.py and player.py where it needs to be changed. (PORT and HOST)
First, the players should run the server.

python server.py

Player 1: python player.py 1

Player 2: python player.py 2

(The numbers specify the port that the player will connect to)

The game will start automatically. The first player to connect will be assigned the MISSILES and the second player will be assigned BOMBS. Each player will get 1 turn with each type, and the player that has the most points at the end of the game wins. 

MISSILES: 
When you are the MISSILES type (you can see what type you are by looking at the top bar of the screen) your goal it to defend your 6 cities with the 27 missiles given to you. 

To shoot a missiles, you use your mouse to point where on the screen you want to the missile to explode, and then press a,s, or d to shoot a missile. Each key corresopnds to a different base on the screen. Each base has 9 missiles. 

To blow up a bomb, you must explode a missile near it and capture the bomb within your blast radius. When a missile hits its destination, it will explode. If a bomb is caught in this explosion, it will also explode. 

BOMBS:
When you are the BOMBS type, your objective is to blow up the other players cities and bases. 

To launch a bomb, press 1-9 to launch at a specific base or city. the bomb will drop from the same x-position that your mouse is at. 

You are given 10 Bombs each round

ROUNDS:
Each round lasts as long as the BOMBS type as bombs left and there are no animations happening on the screen. If the cities are not all destroyed at the end of the round, another round starts resetting the bombs and missiles. 

TURNS:
A turn lasts as long as the MISSILE type still has active cities. When the cities are all destroyed, the turn ends or the game is over.

POINTS:
You can only score points when you are the MISSILES type. You get your points for the cities and missiles oyu have left, as well as the number of bombs you defused.

Cities: 50 points
Missiles: 1
Defused Bombs: 5

