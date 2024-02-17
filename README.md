# Pigeon

> $$About


Automating Riichi City Mahjong Game with Python and YOLOv8

##  Usage

```
Python  3.1.0
CUDA 12.1
```



## Installation


```
pip install -r requirements.txt
```

## How to Use


```
python run.py
```

2.The position defaults are based on a 1366x768 fullscreen resolution, with Simplified Chinese settings.


3.The first match requires manual pairing.

##  Questions and Answers

Q: Why does it only perform Kokushi Musou?

A: Currently, traditional algorithms are utilized in decide_card_to_play.py.


Q: Will it result in account suspension?

A: This is based on image recognition, so if you're worried, don't use it. If you decide to use it, don't worry.

##  TODO

1.Connected to the Mortal deep learning algorithm model

2.Handling image recognition for the discards and actions of other players.