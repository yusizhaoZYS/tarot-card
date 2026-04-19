#!/usr/bin/env python3
"""
tarot-card image generator
批量生成78张塔罗牌图片，保存到 assets/ 目录
"""
import json
import time
import random
import urllib.request
import urllib.error
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
DECK_FILE = SKILL_DIR / "references" / "tarot-deck.json"
COMFYUI_URL = "http://127.0.0.1:8188"

os.makedirs(ASSETS_DIR, exist_ok=True)

# 塔罗牌核心意象描述（用于生成图片prompt）
CARD_PROMPTS = {
    # 大阿卡纳
    "ma0": "A young fool standing at the edge of a cliff, holding a white rose, a small dog jumping at him, carefree expression, bright sky behind, tarot card art style",
    "ma1": "A magician standing before an altar with a wand pointing upward, four mystical items on the altar (cup pentacle sword wand), one hand raised to heaven, infinite symbol above his head, tarot card style",
    "ma2": "A high priestess sitting between two pillars, a crescent moon at her feet, holding a scroll marked with letters, mysterious veil behind her, tarot card style",
    "ma3": "A pregnant woman sitting on a throne surrounded by lush green nature, wheat in one hand, crown of stars, Venus symbol on shield, abundant earth mother, tarot card style",
    "ma4": "A stern emperor sitting on a throne adorned with eagles, holding an orb, four rams heads on throne, authoritative father figure, tarot card style",
    "ma5": "A hierophant pope sitting on a throne between two pillars, one hand raised in blessing, two keys at his feet, religious mystical style, tarot card art",
    "ma6": "A man and woman standing before an angel, the man offering a ring to the woman, eagle and angel above, paradise garden behind, sacred union, tarot card style",
    "ma7": "A warrior in armor driving a chariot pulled by two sphinxes, star on his chest, crescent moon on shoulder, triumphant forward motion, tarot card art style",
    "ma8": "A gentle woman gently closing the mouth of a lion with her bare hands, wreath of flowers, peaceful confident expression, inner strength, tarot card style",
    "ma9": "An old hermit holding a lantern that glows with golden light, staff in hand, solitary on a mountain peak, searching for truth within, tarot card art",
    "ma10": "A great wheel of fortune with mystical symbols around it, letters of the tarot at the edge, winged angel at top, devil and snake at bottom, cosmic destiny turning, tarot card style",
    "ma11": "A woman holding a double-edged sword perfectly upright, wearing a crown, perfect balance, one foot on platform, justice and truth, tarot card art style",
    "ma12": "A man hanging upside down from a wooden frame by one foot, serene peaceful expression despite the position, halo of light around his head, surrender and sacrifice, tarot card style",
    "ma13": "A skeleton knight in black armor riding a pale horse, passing through living people who kneel before him, scythe in hand, inevitable transformation, tarot card art",
    "ma14": "An angel with one foot on water and one on land, pouring luminous liquid between two cups, wings spread wide, harmony and balance, tarot card style",
    "ma15": "A winged devil standing on an altar with a man and woman chained to it by their necks, the man and woman looking away from each other, temptation and bondage, tarot card art",
    "ma16": "A tower struck by lightning, two figures falling headfirst from the windows, crown flying off the top, fire and chaos, divine intervention awakening, tarot card style",
    "ma17": "A naked woman kneeling by a pool, pouring water from two vases, one into the pool one onto land, bird on her head, eight stars around her, hope and renewal, tarot card art",
    "ma18": "A night scene with a full moon in the sky between two towers, a dog and wolf howling at the moon, a crayfish emerging from water below, path winding between them, illusion and fear, tarot card style",
    "ma19": "A radiant golden sun shining down, a small child riding a white horse, a sunflower field below, joy and vitality, warm light everywhere, tarot card art",
    "ma20": "An angel blowing a trumpet from the sky, people rising from graves below with arms raised, book of judgement, resurrection and rebirth, tarot card style",
    "ma21": "A beautiful winged figure dancing inside a wreath, four symbols around them (eagle man bull lion), cosmic completion and fulfillment, tarot card art",
    # 权杖
    "mi_权杖_0": "A hand emerging from a cloud holding a golden wand with flames bursting from the top, lush landscape below, creative spark, new beginning, tarot card style",
    "mi_权杖_1": "A young man standing between two castles on a cliff, holding a wand extended in his hands, looking thoughtfully at both, decision between two paths, tarot card art",
    "mi_权杖_2": "Three wands standing in the ground, a ship sailing on the horizon behind them, a figure stands confidently with one wand in the middle, expansion and progress, tarot card style",
    "mi_权杖_3": "Four wands decorated with flowers and ribbons, two figures dancing between them, a wreath and banner above, celebration and harmony, tarot card art",
    "mi_权杖_4": "Five wands crossed against each other in combat, five men in colorful clothing fighting with sticks, competition and struggle, tarot card style",
    "mi_权杖_5": "A triumphant figure standing on a chariot pulled by a white horse, holding a laurel wreath high, crowds cheering below, victory and honor, tarot card art",
    "mi_权杖_6": "Six men standing in a row, the leader at the front holding a staff with a flag, five others behind him, triumph and recognition, tarot card style",
    "mi_权杖_7": "A figure standing on one foot on a hill, holding a wand raised high, six attacking wands coming from below, defensive strength and willpower, tarot card art",
    "mi_权杖_8": "Eight wands in the sky flying through the air, some with ribbons, swift action and fast movement, quick progress, tarot card style",
    "mi_权杖_9": "A man standing with one hand raised and a club in the other, a fortified wall behind him with nine wands, resilience and defense, tarot card art",
    "mi_权杖_10": "A bent figure struggling under the weight of ten heavy wands tied across their back, laborious burden and responsibility, tarot card style",
    "mi_权杖_11": "A young page in green and gold, holding a wand upright with both hands, looking at the top of it, discovery and potential, tarot card art",
    "mi_权杖_12": "A young knight riding a brown horse at full gallop, holding a burning wand, passionate and bold, action and adventure, tarot card style",
    "mi_权杖_13": "A queen sitting on a throne decorated with lions and flames, holding a wand with one hand, wearing a crown of flames, passionate and bold leadership, tarot card art",
    "mi_权杖_14": "A king sitting on a throne with lion heads, holding a flowering wand, authoritative and entrepreneurial spirit, tarot card style",
    # 圣杯
    "mi_圣杯_0": "A hand emerging from a cloud holding a chalice with water overflowing, a dove descending from above with a cross, divine love and spirituality, tarot card style",
    "mi_圣杯_1": "A man and woman kneeling facing each other, offering each other a chalice, deep romantic love and partnership, tarot card art",
    "mi_圣杯_2": "Two figures dancing joyfully while a musician plays pipes in the background, five cups of wine on a table, celebration and friendship, tarot card style",
    "mi_圣杯_3": "A woman sitting with her back turned, looking at two cups on the ground with a flower, a bird leaving the cups, nostalgia and indifference, tarot card art",
    "mi_圣杯_4": "A hooded figure standing alone in a graveyard looking at three cups on the ground, the middle one still full, one poured out, loss and regret, tarot card style",
    "mi_圣杯_5": "Five cups arranged in an arc on a table, a bearded king in ermine robes sits at the head, abundance and gratitude, tarot card art",
    "mi_圣杯_6": "Six cups arranged in two rows, a man and woman with a child between them, a servant bringing another child, nostalgia and childhood memories, tarot card style",
    "mi_圣杯_7": "A figure standing before six chalices of gold, an angel above holding a seventh chalice higher, illusions and choices between many paths, tarot card art",
    "mi_圣杯_8": "A man walking away from eight chalices lined up in the distance, walking away from emotional fulfillment, longing and seeking deeper meaning, tarot card style",
    "mi_圣杯_9": "A satisfied man sitting on a bench with arms crossed, nine cups behind him, a bird bringing him a message, wishes fulfilled and contentment, tarot card art",
    "mi_圣杯_10": "A man and woman dancing joyfully, a boy and girl watching and clapping, ten cups forming a rainbow above them, perfect happiness and family, tarot card style",
    "mi_圣杯_11": "A young page in a blue and silver tunic holding a chalice, looking into the cup with wonder, creative possibilities and intuitive messages, tarot card art",
    "mi_圣杯_12": "A knight on a white horse riding slowly, holding a chalice, romantic quest and ideal, poetic and dreamy nature, tarot card style",
    "mi_圣杯_13": "A queen sitting on a throne by the sea, swans nearby, one hand on the throne, holding a chalice, deep emotional wisdom and empathy, tarot card art",
    "mi_圣杯_14": "A king sitting on a throne holding a large chalice, wise and mature leadership in matters of the heart, tarot card style",
    # 宝剑
    "mi_宝剑_0": "A hand emerging from a cloud holding a sword pointed downward, two olive branches and a dove below, clarity of thought and truth, tarot card style",
    "mi_宝剑_1": "A blindfolded figure sitting between two swords crossed above them, scales beside one foot, difficult decisions and mental burden, tarot card art",
    "mi_宝剑_2": "Three swords piercing through a red heart, rain falling from dark clouds above, heartbreak and emotional pain, tarot card style",
    "mi_宝剑_3": "A knight sleeping on a horse in full armor under a canopy of swords, temporary rest and recovery needed, tarot card art",
    "mi_宝剑_4": "Five men in conflict with swords drawn, three in a dark mood, two in bright colors defending, conflict and opposition, tarot card style",
    "mi_宝剑_5": "A man on a white horse sailing through a river under a dark sky, six swords stuck in the boat and in the sail, transition and leaving difficult situations behind, tarot card art",
    "mi_宝剑_6": "A figure walking away from a boat on a river with swords in the water above, swords stuck in the sail, moving forward from conflict, tarot card style",
    "mi_宝剑_7": "A man walking past seven swords stuck in the ground, one sword in his hand raised, strategy and cunning in difficult situations, tarot card art",
    "mi_宝剑_8": "A woman standing straight with five swords surrounding her, two in front three behind, trapped by her own thoughts, restriction and confinement, tarot card style",
    "mi_宝剑_9": "A terrified woman sitting up in bed with nine swords hanging above her in an arc, one stuck in the wall, nightmares and deep anxiety, tarot card art",
    "mi_宝剑_10": "A dead man lying face down with ten swords stuck in his back and above him, violent ending and痛苦, the darkest moment before dawn, tarot card style",
    "mi_宝剑_11": "A young page standing alert with one sword pointed at sky, looking at a bird flying, curiosity and vigilance, tarot card art",
    "mi_宝剑_12": "A knight on a black horse riding hard with one sword raised, determined and aggressive action, tarot card style",
    "mi_宝剑_13": "A queen sitting on a throne with a sword pointing upward, one hand on the hilt, eyes covered with a bandage, rational and principled leadership, tarot card art",
    "mi_宝剑_14": "A king sitting on a throne with sword in one hand and a severed head in the other, intellectual power and authority, tarot card style",
    # 星币
    "mi_星币_0": "A hand emerging from a cloud holding a pentacle with one end wrapped in vines, a dove above with a cross in its mouth, new financial opportunity, tarot card style",
    "mi_星币_1": "A young man standing on one leg playing with a coin between his hands and feet, balance and adaptability in finances, tarot card art",
    "mi_星币_2": "Two figures dancing with coins above their heads, ribbons flowing, financial management and moderation, tarot card style",
    "mi_星币_3": "Three workers in a Gothic cathedral, one carving a coin, teamwork and skilled work, tarot card art",
    "mi_星币_4": "A rich merchant counting coins at a table, two servants guarding him, greed and material security, tarot card style",
    "mi_星币_5": "Two beggars in tattered clothes kneeling at a church door, a wealthy man walking past them, poverty and spiritual wealth, tarot card art",
    "mi_星币_6": "A rich aristocrat in elegant robes giving coins to a beggar and a pilgrim, charity and generosity in balance, tarot card style",
    "mi_星币_7": "A young man standing looking up at one pentacle hanging from a branch above him, patient waiting for financial reward, tarot card art",
    "mi_星币_8": "A craftsman carving a pentacle on a stone block with a hammer and chisel, mastery of craft and skill, tarot card style",
    "mi_星币_9": "A beautiful woman standing with one arm around a cross bearing a wreath, peacocks nearby, wealth and luxury enjoyed, tarot card art",
    "mi_星币_10": "A rich merchant sitting on a throne with coins all around him, one hand on the throne and one raised, a servant nearby, inherited wealth and family fortune, tarot card style",
    "mi_星币_11": "A young page in green and gold standing with one pentacle in hand looking up, opportunities and new ventures in material world, tarot card art",
    "mi_星币_12": "A knight on a brown horse carrying a pentacle, steady progress and efficient material pursuits, tarot card style",
    "mi_星币_13": "A queen sitting on a throne with a harvest wreath, holding a pentacle, abundant and nurturing approach to wealth, tarot card art",
    "mi_星币_14": "A king sitting on a throne holding a large pentacle, mastery of material world and wealth, tarot card style",
}

NEGATIVE_PROMPT = "blurry, low quality, distorted, ugly, deformed, extra fingers, bad anatomy, bad hands, text, watermark, signature, borders, frames"

def check_comfyui():
    """检查ComfyUI是否运行"""
    try:
        with urllib.request.urlopen(f"{COMFYUI_URL}/system_stats", timeout=5) as r:
            return json.loads(r.read())
    except:
        return None

def queue_prompt(prompt_json):
    """向ComfyUI提交任务"""
    data = json.dumps(prompt_json).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def build_workflow(card_id, card_name, positive_prompt):
    """构建单个塔罗牌的ComfyUI工作流"""
    return {
        "prompt": {
            "3": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "dreamshaper_8.safetensors"}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {
                "text": f"tarot card illustration, {positive_prompt}, ornate gold border frame, card name written at top in elegant gothic calligraphy, dark mystical background, Rider-Waite tarot art style, high detail, dramatic lighting, 2:3 vertical rectangle card format",
                "clip": ["3", 1]
            }},
            "5": {"class_type": "CLIPTextEncode", "inputs": {
                "text": NEGATIVE_PROMPT,
                "clip": ["3", 1]
            }},
            "6": {"class_type": "EmptyLatentImage", "inputs": {"width": 768, "height": 1152, "batch_size": 1}},
            "7": {"class_type": "KSampler", "inputs": {
                "seed": random.randint(0, 9999999999),
                "steps": 30,
                "cfg": 7.5,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["3", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0]
            }},
            "8": {"class_type": "VAEDecode", "inputs": {
                "samples": ["7", 0],
                "vae": ["3", 2]
            }},
            "9": {"class_type": "SaveImage", "inputs": {
                "filename_prefix": f"tarot_{card_id}",
                "images": ["8", 0]
            }}
        }
    }

def main():
    # 检查ComfyUI
    stats = check_comfyui()
    if not stats:
        print("❌ ComfyUI 未运行，请先启动")
        return

    print(f"✅ ComfyUI 运行中: v{stats['system']['comfyui_version']}")

    # 加载牌堆
    with open(DECK_FILE, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    # 构建完整78张牌的ID列表
    cards_to_generate = []

    # 大阿卡纳
    for card in deck_data["大阿卡纳"]["cards"]:
        card_id = f"ma{card['id']}"
        if card_id in CARD_PROMPTS:
            cards_to_generate.append((card_id, card["name"], CARD_PROMPTS[card_id]))

    # 小阿卡纳
    suits = deck_data["小阿卡纳"]["suits"]
    for suit_key, suit_data in suits.items():
        for idx, card in enumerate(suit_data["cards"]):
            card_id = f"mi_{suit_key}_{idx}"
            if card_id in CARD_PROMPTS:
                cards_to_generate.append((card_id, card["name"], CARD_PROMPTS[card_id]))

    print(f"📦 共 {len(cards_to_generate)} 张牌需要生成")
    print(f"📁 保存至: {ASSETS_DIR}")

    # 检查已生成的牌
    existing = set()
    for f in os.listdir(ASSETS_DIR):
        if f.endswith(".png"):
            existing.add(f.replace("tarot_", "").replace(".png", ""))

    print(f"✅ 已存在: {len(existing)} 张")

    # 逐张提交（慢速提交，避免Mac过载）
    for i, (card_id, card_name, prompt) in enumerate(cards_to_generate):
        filename = f"tarot_{card_id}.png"
        if filename in existing:
            print(f"[{i+1}/{len(cards_to_generate)}] ⏭️  跳过 {card_name} (已存在)")
            continue

        print(f"[{i+1}/{len(cards_to_generate)}] 🎴 生成中: {card_name} ({card_id})")

        try:
            workflow = build_workflow(card_id, card_name, prompt)
            result = queue_prompt(workflow)
            if "prompt_id" in result:
                print(f"    ✅ 已提交 prompt_id: {result['prompt_id']}")
            else:
                print(f"    ❌ 提交失败: {result}")
        except Exception as e:
            print(f"    ❌ 错误: {e}")

        # 提交间隔3秒（MacBook Air需要喘息时间）
        time.sleep(3)

    print(f"\n🎉 全部提交完成！")
    print(f"请在ComfyUI查看生成进度，图片保存至: {ASSETS_DIR}")

if __name__ == "__main__":
    main()
