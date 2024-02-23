# Pigeon

> $$About


Riichi City Mahjong Game with Full Image Recognition

The goal of this project is to offer people a convenient way to instantly see how they're doing in game competitions and to explore the feasibility of image recognition with existing Mahjong games, helping them learn and improve from this insight. This project is meant purely for educational and experimental purposes, and the creator assumes no responsibility for any actions taken by its users. Any consequences like account suspension due to abnormal behavior detection by the official Mahjong community are not the responsibility of the author.

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

The default positions are set for a fullscreen resolution of 1366x768, with the settings in Simplified Chinese, and a zoom scale of 125% .


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
