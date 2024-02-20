import numpy as np

id_to_card = {0: "1m", 1: "2m", 2: "3m", 3: "4m", 4: "5m", 5: "6m", 6: "7m", 7: "8m", 8: "9m",  
              9: "1p", 10: "2p", 11: "3p", 12: "4p", 13: "5p", 14: "6p", 15: "7p", 16: "8p", 17: "9p",  
              18: "1s", 19: "2s", 20: "3s", 21: "4s", 22: "5s", 23: "6s", 24: "7s", 25: "8s", 26: "9s",  
              27: "E", 28: "S", 29: "W", 30: "N", 31: "P", 32: "F", 33: "C",34:"5mr",35:"5pr",36:"5sr"}

# 假設得到的輸出結果是['1p', '3p', '3p', '4p', '1s', '2s', '4s', '5sr', '6s', '8s', '9s', 'W', 'P']根據日本立直麻將的規則和最佳進攻出牌策略寫出程式


# 整合不同的出牌策略
def decide_card_based_on_pattern(hand):
  daisangen_potential, honor_counts = check_daisangen_potential(hand)

  # 七對策略
  if check_chiitoitsu(hand):
    return chiitoitsu_strategy(hand)
  
    
  # 国士无双策略
  elif check_kokushi(hand):
    return kokushi_strategy(hand)
  
  #大三元策略
  elif daisangen_potential:
    return daisangen_strategy(hand, honor_counts)
    
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

  return terminal_count >= 5 and honor_count >= 6      
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

# 大三元策略
def daisangen_strategy(hand, honor_counts):
    # 優先丟棄非中、發、白的牌
    for card in hand:
        if card not in honor_counts or honor_counts[card] < 2:
            return card
    # 如果手牌全是中、發、白，則丟棄其中一張數量最多的牌
    max_honor = max(honor_counts, key=honor_counts.get)
    return max_honor
# 檢查是否有實現大三元的潛力
def check_daisangen_potential(hand):
    honors = {"P", "F", "C"}  # 中、發、白
    honor_counts = {h: hand.count(h) for h in honors}
    # 如果中、發、白中至少有兩種牌各有至少2張，則認為有實現大三元的潛力
    potential = sum(1 for count in honor_counts.values() if count >= 2)
    return potential >= 2, honor_counts



# 默认出牌策略  
# 默认出牌策略，将红宝牌视为对应的普通牌进行考虑
def default_strategy(hand):
    # 将红宝牌视为普通牌进行处理，并确保所有牌都被正确统计
    normalized_hand = []
    for card in hand:
        if card == '5sr':
            normalized_hand.append('5s')
        elif card == '5pr':
            normalized_hand.append('5p')
        elif card == '5mr':
            normalized_hand.append('5m')
        else:
            normalized_hand.append(card)

    pairs = {}
    triples = {}  # 新增用于统计刻子的字典
    quads = {}  # 新增用于统计杠子的字典
    potential_sequences = {}
    isolated_tiles = []

    for card in normalized_hand:
        pairs[card] = pairs.get(card, 0) + 1
        if pairs[card] == 3:
            triples[card] = 3  # 如果某张牌达到三张，记录为刻子
        elif pairs[card] == 4:
            quads[card] = 4  # 如果某张牌达到四张，记录为杠子

    # 检查潜在顺子和孤立牌
    
    for card in normalized_hand:
        card_number = int(card[:-1]) if card[:-1].isdigit() else 0
        if card_number > 0:
            for offset in [-2, -1, 1, 2]:
                potential_seq_card = str(card_number + offset) + card[-1]
                if potential_seq_card in normalized_hand:
                    potential_sequences[potential_seq_card] = potential_sequences.get(potential_seq_card, 0) + 1
        else:
            if pairs[card] == 1:
                isolated_tiles.append(card)

    # 优先丢弃孤立的字牌或数牌
    for card in isolated_tiles:
        if card in hand:
            return card  # 直接返回原始手牌中的牌

    # 如果没有孤立的字牌，考虑丢弃潜力最小的牌
    if potential_sequences:
        min_potential = min(potential_sequences, key=potential_sequences.get)
        if pairs.get(min_potential, 0) == 1:
            return min_potential if min_potential in hand else '5sr' if '5s' in hand else '5pr' if '5p' in hand else '5mr' if '5m' in hand else hand[0]

    return hand[0]  # 如果没有更好的选择，丢出第一张牌


# 示例手牌
hands = [
    ['1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '1s', '2s', '3s', '4s', '5sr'],
    ['3p', '3p', '3p', '4p', '5p', '6p', '7s', '7s', '7s', '2s', '3s', '4s', '5s', '5sr'],
    ['6s', '6s', '6s', '6s', '3p', '4p', '5p', '7p', '8p', '9p', '2s', '4s', '5sr', '7s'],
    ['1p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '9p', '9p', '5sr', '5sr']
]

for hand in hands:
    discard = default_strategy(hand)
    print(f"对于手牌 {hand}，建议丢弃的牌是：{discard}")
