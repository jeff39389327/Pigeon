import numpy as np
from collections import Counter

# 紅寶牌映射
def normalize_card(card):
    red_dora_mapping = {'5mr': '5m', '5pr': '5p', '5sr': '5s'}
    return red_dora_mapping.get(card, card)

# 策略接口
class Strategy:
    def apply(self, hand):
        pass

    def check(self, hand):
        pass

# 七對子策略
class ChiitoitsuStrategy(Strategy):
    def check(self, hand):
        return len([pair for pair in hand.values() if pair == 2]) == 7

    def apply(self, hand):
        for card, count in hand.items():
            if count == 1:
                return card

# 國士無雙策略
class KokushiStrategy(Strategy):
    def check(self, hand):
        terminals = ["1m", "9m", "1p", "9p", "1s", "9s"]
        honors = ["E", "S", "W", "N", "P", "F", "C"]
        terminal_count = sum(hand[card] for card in terminals if card in hand)
        honor_count = sum(hand[card] for card in honors if card in hand)
        return terminal_count + honor_count == 13 and any(count == 2 for count in hand.values())

    def apply(self, hand):
        for card, count in hand.items():
            if count > 1:
                return card

class DefaultStrategy(Strategy):
    def check(self, hand):
        return True  # 默认策略总是适用

    def apply(self, hand):
        normalized_hand = [normalize_card(card) for card in hand]
        hand_counter = Counter(normalized_hand)
        pairs, triples, quads, potential_sequences, isolated_tiles = {}, {}, {}, {}, []

        for card, count in hand_counter.items():
            if count == 2:
                pairs[card] = 2
            elif count == 3:
                triples[card] = 3
            elif count == 4:
                quads[card] = 4

        for card in normalized_hand:
            card_number = int(card[:-1]) if card[:-1].isdigit() else 0
            if card_number > 0:
                for offset in [-2, -1, 1, 2]:
                    potential_seq_card = str(card_number + offset) + card[-1]
                    if potential_seq_card in normalized_hand:
                        potential_sequences[potential_seq_card] = potential_sequences.get(potential_seq_card, 0) + 1
            else:
                if hand_counter[card] == 1:
                    isolated_tiles.append(card)

        for card in isolated_tiles:
            return card  # 直接返回原始手牌中的牌

        if potential_sequences:
            min_potential = min(potential_sequences, key=potential_sequences.get)
            return min_potential if min_potential in hand else hand[0]

        return hand[0]  # 如果没有更好的选择，丢出第一张牌

# 決定出牌策略
def decide_card_based_on_pattern(original_hand):
    normalized_hand = [normalize_card(card) for card in original_hand]
    hand_counter = Counter(normalized_hand)
    strategies = [ChiitoitsuStrategy(), KokushiStrategy(), DefaultStrategy()]

    for strategy in strategies:
        if strategy.check(hand_counter):
            return strategy.apply(hand_counter)

# 示例手牌
hands = ['1p', '3p', '3p', '4p', '1s', '2s', '4s', '5sr', '6s', '8s', '9s', 'W', 'P']
card_to_discard = decide_card_based_on_pattern(hands)
print(f"對於手牌 {hands}，建議丟棄的牌是：{card_to_discard}")
