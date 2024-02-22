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

class ChiitoitsuStrategy(Strategy):
    def check(self, hand):
        # 对于14张牌，理想情况下应有7个对子
        pair_count = sum(count == 2 for count in hand.values())
        return pair_count == 7 or (pair_count >= 5 and sum(hand.values()) == 14)  # 考虑14张牌的情况

    def apply(self, hand):
        # 如果有单张牌（不成对），优先考虑丢弃
        for card, count in hand.items():
            if count == 1:
                return card
        # 如果所有牌都成对，考虑丢弃对子中的一张以优化手牌
        for card, count in hand.items():
            if count == 2:
                return card
        return None



# 國士無雙策略
class KokushiStrategy(Strategy):
    @staticmethod
    def is_yaojiu_or_honor(card):
        # 判断是否为幺九牌或字牌
        yaojiu = {'1m', '9m', '1p', '9p', '1s', '9s'}
        honors = {'E', 'S', 'W', 'N', 'P', 'F', 'C'}
        return card in yaojiu or card in honors

    def check(self, hand):
        yaojiu_honor_counts = Counter({card: count for card, count in hand.items() if self.is_yaojiu_or_honor(card)})
        unique_yaojiu_honor = len(yaojiu_honor_counts)
        return unique_yaojiu_honor >= 12 and sum(hand.values()) == 14

    def apply(self, hand):
        for card, count in hand.items():
            if count > 1 and self.is_yaojiu_or_honor(card):
                return card
        return None

class ToitoiStrategy(Strategy):
    def check(self, hand):
        triples_or_quads = sum(count >= 3 for count in hand.values())
        return triples_or_quads >= 2 and sum(hand.values()) == 14

    def apply(self, hand):
        single_cards = [card for card, count in hand.items() if count == 1]
        if single_cards:
            return single_cards[0]
        for card, count in hand.items():
            if count == 2:
                return card
        return None



class HonitsuStrategy(Strategy):
    def check(self, hand):
        # 统计每种花色的数牌数量
        suit_counts = Counter(card[1] for card in hand if len(card) > 1 and card[1] in 'mps')

        # 如果有字牌，也考虑在内
        honor_count = sum(count for card, count in hand.items() if card[1] in 'ESWNPFC')
        
        # 找出最多的花色数牌数量
        most_common_suit_count = suit_counts.most_common(1)[0][1] if suit_counts else 0
        
        # 计算非主要花色数牌和字牌的总数
        non_main_suit_or_honor_count = sum(hand.values()) - most_common_suit_count
        
        # 如果差最多3张牌可以组成混一色，则认为此策略适用
        return non_main_suit_or_honor_count <= 3

    def apply(self, hand):
        suit_counts = Counter(card[-1] for card in hand if len(card) > 1)
        main_suit, _ = suit_counts.most_common(1)[0]

        for card in hand:
            if len(card) > 1 and card[-1] != main_suit:
                return card

        isolated_tiles, _ = self.analyze_hand_structure(hand, main_suit)
        if isolated_tiles:
            return isolated_tiles[0]

        return None

    def analyze_hand_structure(self, hand, main_suit):
        isolated_tiles = []
        pairs = []
        triples = []
        quads = []
        potential_sequences = {}
        hand_counter = Counter(hand)
        
        for card, count in hand_counter.items():
            if len(card) > 1 and card[-1] == main_suit:
                card_number = int(card[0])
                # 根据牌的数量分类
                if count == 1:
                    isolated_tiles.append(card)
                elif count == 2:
                    pairs.append(card)
                elif count == 3:
                    triples.append(card)
                elif count == 4:
                    quads.append(card)
                
                # 检查潜在顺子
                for offset in [-2, -1, 1, 2]:
                    potential_seq_card = str(card_number + offset) + card[-1]
                    if potential_seq_card in hand_counter:
                        potential_sequences[potential_seq_card] = potential_sequences.get(potential_seq_card, 0) + 1

        return isolated_tiles, pairs, triples, quads, potential_sequences
   
class ChinitsuStrategy(Strategy):
    def check(self, hand):
        # 假设hand是一个Counter对象，已经正规化
        # 统计每种花色的数牌数量
        suit_counts = Counter(card[1] for card in hand if len(card) > 1)
        
        # 检查是否所有牌都是一种花色
        if len(suit_counts) == 1:
            # 已经是清一色
            return True
        elif len(suit_counts) > 1:
            # 包含多种花色，计算非主要花色的牌数
            total_cards = sum(hand.values())
            main_suit_count = max(suit_counts.values())
            non_main_suit_count = total_cards - main_suit_count
            # 如果差最多3张可以转换为清一色
            return non_main_suit_count <= 3
        return False
def apply(self, hand):
    # 确定主要花色
    suit_counts = Counter(card[-1] for card in hand if len(card) > 1)
    main_suit, _ = suit_counts.most_common(1)[0]

    # 分析手牌结构
    isolated_tiles, pairs, triples, quads, potential_sequences = self.analyze_hand_structure(hand, main_suit)

    # 如果有孤立的牌，优先丢弃
    if isolated_tiles:
        return isolated_tiles[0]

    # 如果没有孤立牌，考虑丢弃多余的对子中的一张
    if len(pairs) > 1:
        return pairs[1]  # 假设pairs已经根据某种逻辑排序

    # 如果没有明显的丢弃选择，考虑潜力最小的顺子部分
    if potential_sequences:
        min_potential = min(potential_sequences, key=potential_sequences.get)
        return min_potential if min_potential in hand else None

    return None

    def analyze_hand_structure(self, hand, main_suit):
        isolated_tiles = []
        pairs = []
        triples = []
        quads = []
        potential_sequences = {}
        hand_counter = Counter(hand)
        
        for card, count in hand_counter.items():
            if len(card) > 1 and card[-1] == main_suit:
                card_number = int(card[0])
                # 根据牌的数量分类
                if count == 1:
                    isolated_tiles.append(card)
                elif count == 2:
                    pairs.append(card)
                elif count == 3:
                    triples.append(card)
                elif count == 4:
                    quads.append(card)
                
                # 检查潜在顺子
                for offset in [-2, -1, 1, 2]:
                    potential_seq_card = str(card_number + offset) + card[-1]
                    if potential_seq_card in hand_counter:
                        potential_sequences[potential_seq_card] = potential_sequences.get(potential_seq_card, 0) + 1

        return isolated_tiles, pairs, triples, quads, potential_sequences
        
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

# 決定出牌策略並返回使用的策略名稱
def decide_card_based_on_pattern_with_strategy(original_hand):
    normalized_hand = [normalize_card(card) for card in original_hand]
    hand_counter = Counter(normalized_hand)
    strategies = [ChiitoitsuStrategy(), ToitoiStrategy(),   KokushiStrategy(),DefaultStrategy()]
    # strategies = [ DefaultStrategy()  ]
    for strategy in strategies:
        if strategy.check(hand_counter):
            card_to_discard = strategy.apply(hand_counter)
            strategy_name = strategy.__class__.__name__  # 獲取策略的類名稱
            return strategy_name, card_to_discard  # 返回策略名稱和建議丟棄的牌

    return "No Strategy", None  # 如果沒有策略適用，返回"No Strategy"和None

# 示例手牌
# hands = ["1m", "2m", "3m", "4m", "5m", "6m","7m", "8m", "9m", "9m", "9m", "5m", "5m", "2m"]
# strategy_used, card_to_discard = decide_card_based_on_pattern_with_strategy(hands)
# print(f"對於手牌 {hands}，使用策略 {strategy_used}，建議丟棄的牌是：{card_to_discard}")
