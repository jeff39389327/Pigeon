import numpy as np

id_to_card = {0: "1m", 1: "2m", 2: "3m", 3: "4m", 4: "5m", 5: "6m", 6: "7m", 7: "8m", 8: "9m",  
              9: "1p", 10: "2p", 11: "3p", 12: "4p", 13: "5p", 14: "6p", 15: "7p", 16: "8p", 17: "9p",  
              18: "1s", 19: "2s", 20: "3s", 21: "4s", 22: "5s", 23: "6s", 24: "7s", 25: "8s", 26: "9s",  
              27: "E", 28: "S", 29: "W", 30: "N", 31: "P", 32: "F", 33: "C",34:"5mr",35:"5pr",36:"5sr"}

# 假設得到的輸出結果是['1p', '3p', '3p', '4p', '1s', '2s', '4s', '5sr', '6s', '8s', '9s', 'W', 'P']根據日本立直麻將的規則和最佳進攻出牌策略寫出程式


# 整合不同的出牌策略
def decide_card_based_on_pattern(hand):

  # 七對策略
  if check_chiitoitsu(hand):
    return chiitoitsu_strategy(hand)
  
    
  # 国士无双策略
  elif check_kokushi(hand):
    return kokushi_strategy(hand)
    
  # 默认策略       
  else:
    return default_strategy(hand)
  

# 七對策略
def chiitoitsu_strategy(hand):
  for card in hand:
    if hand.count(card) == 1:
      return card

# 检查是否可国士无双
def check_kokushi(hand):
  
  terminals = ["1m", "9m", "1p", "9p", "1s", "9s"] 
  honors = ["E", "S", "W", "N", "P", "F", "C"]

  terminal_count = 0
  honor_count = 0

  for card in hand:
    if card in terminals:
      terminal_count += 1 
    elif card in honors:
      honor_count += 1

  return terminal_count >= 6 and honor_count >= 7      
# 国士无双策略  
def kokushi_strategy(hand):
  # 统计手牌中的对子
  pairs = {}
  for card in hand:
    if card not in pairs:
      pairs[card] = 0
    pairs[card] += 1

  # 如果有重复,优先丢掉重复牌
  for card in ["1m", "9m", "1p", "9p", "1s", "9s", "E", "S", "W", "N", "P", "F", "C"]:
    if pairs[card] > 1:
      return card    
# 检查是否為七對    
def check_chiitoitsu(hand):
  pairs = {}
  for card in hand:
    if card not in pairs:
      pairs[card] = 0
    pairs[card] += 1
    
  return len([pair for pair in pairs.values() if pair >= 2]) >= 6




# 默认出牌策略  
def default_strategy(hand):

  # 统计手牌中的对子
  pairs = {}
  for card in hand:
    if card not in pairs:
      pairs[card] = 0
    pairs[card] += 1

  # 尝试保留更多的对子和顺子,打出非对子非顺子的牌
  for card in hand:
    if pairs[card] == 1: # 打出孤立牌
      return card

  return hand[0] # 如果没有更好的选择,打出第一张牌