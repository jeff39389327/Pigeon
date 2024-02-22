# Pigeon

> $$About


Automating Riichi City Mahjong Game with Full Image Recognition

[Any question?Find me on Discord](https://discord.gg/aTwhuds3hX "link")

##  Usage

```
Python  3.1.0
CUDA 12.1(To achieve faster execution, it's necessary to install CUDA)
```



## Installation


```
pip install -r requirement.txt
```

## How to Use


```
python run.py
```

The position defaults are based on a 1366x768 fullscreen resolution, with Simplified Chinese settings.


The first match requires manual pairing.


You need to enable automatic winning of hands in each mini-game through the game settings.

##  Questions and Answers

Q: Why is this AI so weak?

A: This is certain; it is currently underdeveloped based on traditional algorithms, and will subsequently be integrated with deep learning models.


Q: How to change the matchmaking room?

A: Use check.py to determine the top-left and bottom-right positions, then fill them in game.py (#rank NE_region).


Q: Will it result in account suspension?

A: This is based on image recognition, so if you're worried, don't use it. If you decide to use it, don't worry.



##  TODO

1.Handling image recognition for the discards and actions of other players.("I have no idea.")


2.Connected to the Mortal deep learning algorithm model
