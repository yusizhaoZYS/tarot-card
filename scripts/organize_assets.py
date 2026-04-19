#!/usr/bin/env python3
"""
Organize tarot card images from ComfyUI output to assets folder.
"""

import json
import shutil
import os
import re

ASSETS_DIR = os.path.expanduser("~/.openclaw/workspace-yusi/skills/tarot-card/assets")
COMFYUI_OUTPUT = "/Users/yusizhao/ComfyUI/output"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Load deck data
with open(os.path.join(os.path.dirname(__file__), "../references/tarot-deck.json"), encoding="utf-8") as f:
    deck = json.load(f)

# Build ID → filename mapping from ComfyUI output
files = os.listdir(COMFYUI_OUTPUT)
tarot_files = {f: os.path.join(COMFYUI_OUTPUT, f) for f in files if f.startswith("tarot_")}

print(f"Found {len(tarot_files)} tarot files in ComfyUI output")

# Map major arcana
# tarot_ma{0-21}_00001_.png
major = deck["大阿卡纳"]["cards"]
for card in major:
    idx = card["id"]
    cn = card["name"]
    # Find matching file
    fname = f"tarot_ma{idx}_00001_.png"
    if fname in tarot_files:
        new_name = f"major-{idx:02d}.png"
        shutil.copy(tarot_files[fname], os.path.join(ASSETS_DIR, new_name))
        print(f"✓ major-{idx:02d} = {cn} ({fname})")
    else:
        print(f"✗ MISSING: {fname} ({cn})")

# Map minor arcana
suit_key_map = {"权杖": "wands", "圣杯": "cups", "宝剑": "swords", "星币": "pentacles"}
# Card index in file = array index (0=Ace, 1=二, ... 9=十, 10=侍从, 11=骑士, 12=王后, 13=国王)
rank_names = ["Ace", "二", "三", "四", "五", "六", "七", "八", "九", "十", "侍从", "骑士", "王后", "国王"]

for suit_cn, suit_key in suit_key_map.items():
    cards = deck["小阿卡纳"]["suits"][suit_cn]["cards"]
    for i, card in enumerate(cards):
        fname = f"tarot_mi_{suit_cn}_{i}_00001_.png"
        if fname in tarot_files:
            new_name = f"{suit_key}-{i:02d}.png"
            shutil.copy(tarot_files[fname], os.path.join(ASSETS_DIR, new_name))
            print(f"✓ {suit_key}-{i:02d} = {card['name']} ({fname})")
        else:
            print(f"✗ MISSING: {fname} ({card['name']})")

print(f"\nAssets organized to: {ASSETS_DIR}")
print(f"Total files: {len(os.listdir(ASSETS_DIR))}")
