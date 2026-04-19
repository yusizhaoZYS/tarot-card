#!/usr/bin/env python3
"""
Tarot Card Image Generator
Generates 78 tarot card images via ComfyUI API
"""

import json
import requests
import time
import os
import base64
from concurrent import shutil

COMFYUI_URL = "http://127.0.0.1:8188"
ASSETS_DIR = os.path.expanduser("~/.openclaw/workspace-yusi/skills/tarot-card/assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Tarot cards data: (id, name, nameEn, prompt_description)
# Format: (filename_prefix, card_name, image_prompt_suffix)
TAROT_CARDS = []

# Major Arcana (22 cards)
major = [
    (0, "愚人", "The Fool", "a mystical fool holding a white rose, stepping off a cliff edge, jester costume, bright sky, journey begins, whimsical sacred geometry art"),
    (1, "魔术师", "The Magician", "a powerful magician at a wooden altar, one hand pointing to sky, one to earth, red cape, golden symbols, four elements displayed, arcane tools"),
    (2, "女祭司", "The High Priestess", "a mysterious priestess seated between two pillars, silver and gold, crescent moon at her feet, sacred scroll hidden, intuition goddess"),
    (3, "皇后", "The Empress", "a pregnant empress on a throne, surrounded by fields of wheat and roses, Venus symbol in clouds, lush nature, fertility goddess"),
    (4, "皇帝", "The Emperor", "a stern emperor on a stone throne, holding an ankh scepter, red cape, four rams heads, authority and structure"),
    (5, "教皇", "The Hierophant", "a holy pope between two pillars,，左手持三重十字权杖, teaching gesture, two keys at his feet, spiritual guide"),
    (6, "恋人", "The Lovers", "a naked man and woman standing before an angel, beneath a blazing sun, rose garden, sacred love union, choice between two women"),
    (7, "战车", "The Chariot", "a triumphant warrior in a chariot pulled by two sphinxes, one black one white, cosmic armor, victory and willpower"),
    (8, "力量", "Strength", "a gentle woman closing the mouth of a fierce lion with her bare hands, infinity symbol above her head, inner strength and courage"),
    (9, "隐士", "The Hermit", "an old sage holding a lantern in a dark forest, cloak pulled low, solitary path of wisdom, the hermit's journey inward"),
    (10, "命运之轮", "Wheel of Fortune", "a giant cosmic wheel decorated with mystical symbols, letters YHVH at cardinal points, sphinx on top, fate and cycles"),
    (11, "正义", "Justice", "a regal woman holding a sword and scales, one foot on a stone cube, blindfolded, cosmic balance, truth and fairness"),
    (12, "倒吊人", "The Hanged Man", "a young man hanging upside down from a wooden frame by one ankle, halo of light around his head, sacrifice and new perspective"),
    (13, "死神", "Death", "a skeletal figure in black armor riding a pale horse, cloaked victims kneeling before him, the reaper, transformation through endings"),
    (14, "节制", "Temperance", "a winged angel pouring liquid between two cups, one foot on earth one in water, rainbow above, balance and moderation"),
    (15, "恶魔", "The Devil", "a horned devil sitting on a stone throne, chained male and female at his feet, bat wings, material bondage and temptation"),
    (16, "塔", "The Tower", "a tall stone tower being struck by divine lightning, people falling from windows, crown flying off, sudden revelation and chaos"),
    (17, "星星", "The Star", "a naked woman kneeling by a pool of water, pouring from two vessels, stars above, hope and inspiration after darkness"),
    (18, "月亮", "The Moon", "a full moon in a night sky between two towers, a wolf and dog howling, a crayfish emerging from water, path through uncertainty"),
    (19, "太阳", "The Sun", "a radiant sun with a child riding a white horse beneath it, sunflowers and stone walls, joyful vitality and success"),
    (20, "审判", "Judgement", "a winged angel blowing a trumpet from clouds, dead rising from graves below, giant crosses, spiritual rebirth and awakening"),
    (21, "世界", "The World", "a crowned woman dancing inside a great laurel wreath, four figures at cardinal points, cosmic completion and fulfillment"),
]

for id, name, nameEn, desc in major:
    TAROT_CARDS.append((f"major-{id:02d}", f"{name} {nameEn}", desc))

# Minor Arcana helper
suits = [
    ("wands", "权杖", "Wands", "flames, clubs, fire energy, orange and red tones, creative spirit"),
    ("cups", "圣杯", "Cups", "goblets, chalices, water element, blue tones, emotional depth"),
    ("swords", "宝剑", "Swords", "blades, swords, wind element, silver and grey tones, intellectual power"),
    ("pentacles", "星币", "Pentacles", "golden coins, pentagrams, earth element, green and gold tones, material wealth"),
]

# Court card types
court_templates = {
    "侍从": ("Page", "a thoughtful young squire holding a scroll, ready to deliver important news"),
    "骑士": ("Knight", "a determined knight riding a spirited horse, seeking adventure and glory"),
    "王后": ("Queen", "a wise and powerful queen on an ornate throne, embodying sovereignty"),
    "国王": ("King", "a majestic crowned king on a royal throne, holding supreme authority"),
}

# Minor Arcana cards
minor_descriptions = {
    "Ace": "a single glowing ace card hovering, pure elemental energy bursting forth, divine spark",
    "二": "two elemental symbols balanced, partnership and duality, harmonious connection",
    "三": "three elemental symbols arranged, collaboration and teamwork, creative achievement",
    "四": "four elemental symbols, stability and foundation, home and tradition",
    "五": "five elemental symbols in conflict, competition and diversity, contrast and struggle",
    "六": "six elemental symbols celebrated, victory and recognition, public honor",
    "七": "seven elemental symbols defensive, challenge and perseverance, standing your ground",
    "八": "eight elemental symbols in swift motion, speed and rapid action, quick decisions",
    "九": "nine elemental symbols endurance, resilience and inner strength, fierce determination",
    "十": "ten elemental symbols heavy burden, responsibility and workload, weight of duty",
}

# Build minor arcana
suits_data = [
    ("wands", "权杖", [
        ("Ace", "pure creative fire energy bursting from a torch, new venture igniting"),
        ("二", "a figure looking at two wands, planning a journey, choosing direction"),
        ("三", "a figure on a hilltop surveying three wands, leadership and far-sightedness"),
        ("四", "four wands decorated with flowers, celebration and harmony at home"),
        ("五", "five wands in conflict, competition and struggle for victory"),
        ("六", "six wands bearing a victory wreath, triumphant procession and recognition"),
        ("七", "seven wands in defensive stance, challenging authority and keeping guard"),
        ("八", "eight wands flying through the air swift as arrows, rapid movement"),
        ("九", "nine wands standing guard around a fortified position, resilience under siege"),
        ("十", "ten heavy wands burdening a figure, exhaustion and heavy responsibility"),
        ("侍从", "a young messenger holding a wand, enthusiastic news about creative ventures"),
        ("骑士", "a fierce knight charging on horseback with a wand, passionate pursuit of goals"),
        ("王后", "a confident queen seated with a wand, bold creativity and nurturing inspiration"),
        ("国王", "a commanding king on throne with a wand, master of creative enterprise"),
    ]),
    ("cups", "圣杯", [
        ("Ace", "a hand offering a glowing cup, new love and emotional beginnings"),
        ("二", "a man and woman in loving embrace before an angel, sacred partnership"),
        ("三", "three cups in a triangle, three women celebrating with raised cups, friendship"),
        ("四", "a figure at a table with three cups, dissatisfaction and apathy, longing for more"),
        ("五", "a cloaked figure before five cups, loss and regret, grief and disappointment"),
        ("六", "two children with six cups among flowers, nostalgia and innocent memories"),
        ("七", "a figure before seven cups glowing with multiple paths, fantasy and choice"),
        ("八", "a hooded figure walking away from eight cups, disillusionment and seeking meaning"),
        ("九", "a satisfied figure with nine cups, wishes fulfilled and contentment"),
        ("十", "a joyful family with ten cups, emotional fulfillment and family harmony"),
        ("侍从", "a thoughtful youth holding a cup, romantic possibilities and creative ideas"),
        ("骑士", "a romantic knight riding with a cup, poetic quest for love and imagination"),
        ("王后", "a compassionate queen with a cup, nurturing love and emotional wisdom"),
        ("国王", "a generous king offering a cup, emotional abundance and mature love"),
    ]),
    ("swords", "宝剑", [
        ("Ace", "a gleaming sword pointing downward, crowned with a crown of thorns, mental clarity and truth"),
        ("二", "a blindfolded figure with two swords crossed behind, deadlock and difficult choices"),
        ("三", "three swords piercing a heart, heartbreak and grief, painful separation"),
        ("四", "a resting figure beneath four swords, needed rest and contemplation, time out"),
        ("五", "five swords in conflict, defeat and winning at all costs, moral defeat"),
        ("六", "a figure on a boat with six swords, transition and leaving behind, moving forward"),
        ("七", "a sneaky figure with seven swords, strategy and cunning, getting by through cleverness"),
        ("八", "eight swords in the ground trapping a figure, imprisonment and restriction, feeling stuck"),
        ("九", "nine swords above a terrified figure in bed, anxiety and nightmares, deep worry"),
        ("十", "ten swords stabbing a fallen figure, betrayal and devastation, rock bottom ending"),
        ("侍从", "a curious youth with a sword, seeking truth and delivering sharp messages"),
        ("骑士", "a swift knight charging with sword raised, determined action and strong opinions"),
        ("王后", "a stern queen seated with a sword, clear thinking and fierce independence"),
        ("国王", "a bearded king on throne with sword, intellectual authority and truth"),
    ]),
    ("pentacles", "星币", [
        ("Ace", "a hand from cloud offering a glowing pentacle, new financial opportunity manifesting"),
        ("二", "a juggling figure with two pentacles, financial juggling and adaptability"),
        ("三", "a craftsman with three pentacles, skilled teamwork and creative collaboration"),
        ("四", "a miser clutching a pentacle close, greed and security, tight-fisted control"),
        ("五", "two beggars before a cathedral with five pentacles, financial hardship but spiritual wealth"),
        ("六", "a generous patron giving pentacles to a poor figure, giving and receiving charity"),
        ("七", "a figure with seven pentacles assessing growth, patience and long-term investment"),
        ("八", "a dedicated craftsman with eight pentacles, mastery and skill development"),
        ("九", "a wealthy woman with nine pentacles, luxury and self-sufficiency, enjoying the spoils"),
        ("十", "an noble family with ten pentacles, inherited wealth and family legacy"),
        ("侍从", "a studious youth with a pentacle, learning financial skills and new opportunities"),
        ("骑士", "a reliable knight riding with a pentacle, hard work and financial progress"),
        ("王后", "a generous queen with pentacle and harvest, abundance and nurturing prosperity"),
        ("国王", "a successful merchant king with pentacle, mastery of business and material wealth"),
    ]),
]

for suit_key, suit_cn, suit_en, suit_element in suits_data:
    for card_num, desc in minor_descriptions.items():
        card_id = f"{suit_key}-{card_num}"
        card_name = f"{suit_cn}{card_num}"
        TAROT_CARDS.append((card_id, card_name, desc))

for suit_key, suit_cn, suit_en, suit_element in suits_data:
    for cn_rank, (en_rank, desc) in court_templates.items():
        card_id = f"{suit_key}-{cn_rank}"
        card_name = f"{suit_cn}{cn_rank}"
        TAROT_CARDS.append((card_id, card_name, desc))


def generate_tarot_prompt(card_name, card_desc):
    """Create a detailed tarot card generation prompt"""
    return (
        f"masterpiece, best quality, tarot card, {card_name}, "
        f"classic rider-waite tarot illustration style, ornate golden border frame, "
        f"mystical symbolism, sacred geometry, celestial elements, "
        f"{card_desc}, "
        f"art deco composition, high contrast, detailed linework, vibrant colors, "
        f"card sized 2:3 ratio, centered subject, clean background"
    )


def submit_prompt(prompt_text, filename, negative=""):
    """Submit a generation job to ComfyUI"""
    workflow = {
        "3": {"inputs": {"text": prompt_text, " CLIP Text Encoder (Prompt)": ["6", 0]}},
        "4": {"inputs": {"text": "blurry, distorted, low quality, worst quality, bad anatomy, bad hands, text, watermark, signature, cropped, low resolution", "CLIP Text Encoder (Prompt)": ["6", 1]}},
        "5": {"inputs": {"steps": 25, "cfg": 7, "sampler_name": "euler", "scheduler": "normal", "description": "CLIP Text Encoder"}},
        "6": {"inputs": {"model_name": "anything-v5.safetensors", "description": "Load Checkpoint"}},
        "7": {"inputs": {"width": 768, "height": 1152, "batch_size": 1, "description": "Empty Latent Image"}},
        "8": {"inputs": {"sampler_name": "euler", "scheduler": "normal", "description": "KSampler"}},
        "9": {"inputs": {"filename_prefix": filename.replace(".png", ""), "description": "Save Image"}},
        "10": {"inputs": {"latent_image": ["7", 0], "sampler": ["8", 0], "model": ["6", 0], "clip": ["6", 1], "vaecoder": ["6", 2], "prompt": ["5", 0], "description": "KSampler"}},
        "last_node_id": 11,
    }
    
    # Actually build proper workflow for ComfyUI
    # This is a simplified version - we'll use the API directly
    pass


def get_history(prompt_id):
    """Get history of completed prompt"""
    resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
    return resp.json()


def get_history_recursive():
    """Get all historical prompts"""
    resp = requests.get(f"{COMFYUI_URL}/history", timeout=10)
    return resp.json()


# For now, use a direct API approach
def generate_tarot_image_via_api(filename_prefix, prompt, negative_prompt=None):
    """Generate image via ComfyUI API with proper workflow"""
    
    if negative_prompt is None:
        negative_prompt = "blurry, distorted, low quality, worst quality, bad anatomy, bad hands, text, watermark, signature, cropped, low resolution, jpeg artifacts, ugly, duplicate, morbid, mutilated"
    
    # Build proper ComfyUI prompt workflow
    workflow = {
        "last_node_id": 9,
        "prompt": {
            "3": {
                "inputs": {"text": prompt},
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {"text": negative_prompt},
                "class_type": "CLIPTextEncode"
            },
            "5": {
                "inputs": {
                    "model_name": "anything-v5.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "6": {
                "inputs": {
                    "width": 768,
                    "height": 1152,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "7": {
                "inputs": {
                    "sampler_name": "euler",
                    "scheduler": "normal"
                },
                "class_type": "KSampler"
            },
            "8": {
                "inputs": {
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "cfg": 7,
                    "steps": 25,
                    "denoise": 1.0
                },
                "class_type": "KSampler"
            },
            "9": {
                "inputs": {
                    "filename_prefix": filename_prefix
                },
                "class_type": "SaveImage"
            }
        }
    }
    
    # Wire up the nodes properly
    workflow["prompt"]["3"].inputs["clip"] = ["5", 0]
    workflow["prompt"]["4"].inputs["clip"] = ["5", 0]
    workflow["prompt"]["6"].inputs["sampler"] = ["8", 0]
    workflow["prompt"]["7"].inputs["model"] = ["5", 0]
    workflow["prompt"]["7"].inputs["clip"] = ["5", 0]
    workflow["prompt"]["7"].inputs["vae"] = ["5", 1]
    workflow["prompt"]["7"].inputs["positive"] = ["3", 0]
    workflow["prompt"]["7"].inputs["negative"] = ["4", 0]
    workflow["prompt"]["7"].inputs["latent_image"] = ["6", 0]
    workflow["prompt"]["8"].inputs["model"] = ["5", 0]
    workflow["prompt"]["8"].inputs["clip"] = ["5", 0]
    workflow["prompt"]["8"].inputs["vae"] = ["5", 1]
    workflow["prompt"]["8"].inputs["positive"] = ["3", 0]
    workflow["prompt"]["8"].inputs["negative"] = ["4", 0]
    workflow["prompt"]["8"].inputs["latent_image"] = ["6", 0]
    workflow["prompt"]["9"].inputs["images"] = ["8", 0]
    
    resp = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("prompt_id")
    else:
        print(f"Error submitting: {resp.status_code} {resp.text}")
        return None


if __name__ == "__main__":
    print(f"Starting tarot card generation: {len(TAROT_CARDS)} cards")
    print(f"Output directory: {ASSETS_DIR}")
    print()
    
    # Check if ComfyUI is available
    try:
        resp = requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        print(f"ComfyUI status: {resp.status_code}")
    except Exception as e:
        print(f"ComfyUI not available: {e}")
        exit(1)
    
    # Submit all jobs
    submitted = []
    for i, (filename_prefix, card_name, desc) in enumerate(TAROT_CARDS):
        prompt = generate_tarot_prompt(card_name, desc)
        prompt_id = generate_tarot_image_via_api(filename_prefix, prompt)
        if prompt_id:
            submitted.append((prompt_id, filename_prefix, card_name))
            print(f"[{i+1}/{len(TAROT_CARDS)}] Submitted: {filename_prefix} ({card_name}) -> {prompt_id}")
        else:
            print(f"[{i+1}/{len(TAROT_CARDS)}] FAILED: {filename_prefix}")
        time.sleep(0.3)  # Rate limit protection
    
    print(f"\nSubmitted {len(submitted)} jobs")
    print("Waiting for completion...")
    
    # Poll for completion
    done = []
    while len(done) < len(submitted):
        time.sleep(5)
        history = get_history_recursive()
        for prompt_id, filename_prefix, card_name in submitted:
            if prompt_id in history and prompt_id not in done:
                done.append(prompt_id)
                print(f"✓ Done: {filename_prefix} ({len(done)}/{len(submitted)})")
        print(f"Progress: {len(done)}/{len(submitted)}")
    
    print("\nAll done!")
