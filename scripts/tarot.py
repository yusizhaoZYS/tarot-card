#!/usr/bin/env python3
"""
tarot-card skill - 塔罗牌洗牌与抽牌工具
用法: python3 tarot.py <牌阵类型> <数字...>
牌阵类型: single(单张) / three(过去/现在/未来)
单张示例: python3 tarot.py single 35
三张示例: python3 tarot.py three 54 8 66
"""
import json
import random
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DECK_FILE = SKILL_DIR / "references" / "tarot-deck.json"
ASSETS_DIR = SKILL_DIR / "assets"

# 小阿卡纳花色 → 图片文件名前缀
SUIT_IMAGE_PREFIX = {
    "权杖": "wands",
    "圣杯": "cups",
    "宝剑": "swords",
    "星币": "pentacles",
}


def build_deck():
    """构建78张塔罗牌池"""
    with open(DECK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    deck = []
    # 大阿卡纳 0-21
    for card in data["大阿卡纳"]["cards"]:
        image_path = str(ASSETS_DIR / f"major-{card['id']:02d}.png")
        deck.append({
            "id": f"ma{card['id']}",
            "name": card["name"],
            "nameEn": card["nameEn"],
            "type": "major",
            "image": image_path,
            "upright": card["upright"],
            "reversed": card["reversed"],
            "keywords": card.get("keywords", [])
        })

    # 小阿卡纳
    minor_suits = data["小阿卡纳"]["suits"]
    for suit_key, suit_data in minor_suits.items():
        for idx, card in enumerate(suit_data["cards"]):
            image_name = f"{SUIT_IMAGE_PREFIX[suit_key]}-{idx:02d}.png"
            image_path = str(ASSETS_DIR / image_name)
            deck.append({
                "id": f"mi_{suit_key}_{idx}",
                "name": card["name"],
                "nameEn": f"{suit_data['element']} {idx+1}",
                "type": "minor",
                "suit": suit_key,
                "image": image_path,
                "upright": card["upright"],
                "reversed": card["reversed"],
                "keywords": []
            })

    return deck


def shuffle_deck(deck, seed):
    """用用户数字+时间偏移洗牌，制造用户参与感但保持随机性"""
    import time
    time_offset = int(time.time() * 1000) % 777
    rng = random.Random(seed + time_offset)
    shuffled = deck.copy()
    rng.shuffle(shuffled)
    return shuffled


def determine_orientation():
    """用真实时间戳随机决定正逆位，每张牌独立50/50"""
    import time
    return int(time.time() * 1000000) % 2 == 0


def main():
    if len(sys.argv) < 3:
        print("用法: tarot.py <用户数字> <牌阵类型> [额外数字...]")
        print("牌阵类型: single / three")
        print("单张示例: tarot.py 35 single")
        print("三张示例: tarot.py 54 8 66 three")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("用法: tarot.py <牌阵类型> <数字...>")
        print("牌阵类型: single / three")
        print("单张示例: tarot.py single 35")
        print("三张示例: tarot.py three 54 8 66")
        sys.exit(1)

    spread_type = sys.argv[1]

    if spread_type == "single":
        try:
            user_numbers = [int(sys.argv[2])]
        except (ValueError, IndexError):
            print("错误: 单张需要提供1个整数数字")
            sys.exit(1)
    elif spread_type == "three":
        try:
            numbers = [int(x) for x in sys.argv[2:]]
        except ValueError:
            print("错误: 三张牌需要三个整数数字")
            sys.exit(1)
        if len(numbers) < 3:
            print("NEED_THREE_NUMBERS")
            print("当前数字数量: " + str(len(numbers)))
            sys.exit(1)
        user_numbers = numbers[:3]
    else:
        print("错误: 未知牌阵类型，请使用 single 或 three")
        sys.exit(1)

    deck = build_deck()

    # 抽牌：每个数字独立洗牌后取第一张
    drawn = []
    for user_num in user_numbers:
        shuffled = shuffle_deck(deck, user_num)
        cut_pos = user_num % len(deck)
        cut_deck = shuffled[cut_pos:] + shuffled[:cut_pos]
        drawn.append(cut_deck[0])

    # 输出结果
    result = {
        "seed_numbers": user_numbers,
        "spread": spread_type,
        "drawn_cards": []
    }

    for i, card in enumerate(drawn):
        is_upright = determine_orientation()
        result["drawn_cards"].append({
            "position": i + 1,
            "id": card["id"],
            "name": card["name"],
            "nameEn": card["nameEn"],
            "type": card["type"],
            "image": card["image"],
            "orientation": "upright" if is_upright else "reversed",
            "meaning": card["upright"] if is_upright else card["reversed"],
            "keywords": card.get("keywords", [])
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
