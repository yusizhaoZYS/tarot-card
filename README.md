# 🃏 Tarot Card Reading Skill

> A mystical tarot card reading experience powered by OpenClaw + ComfyUI.

[English](#english) | [中文](#中文)

---

## ✨ Features

- **Two card spreads**: Single card (simple questions) and Three cards (Past / Present / Future)
- **78 unique tarot card images** generated via ComfyUI — every card has its own illustration
- **Digital shuffling**: Uses your chosen number as a seed to deterministically shuffle the deck
- **Auto upright/reversed**: Each card's orientation is determined by real-time randomness
- **Mystical atmosphere**: Designed to feel like a real tarot session, not a chatbot Q&A

---

## 🃏 Card Spreads

### Single Card
Best for focused, present-moment questions.

> *"What is the core energy surrounding my question?"*

### Three Cards
Best for questions with a timeline or progression.

> - **Past**: How did this situation come to be?
> - **Present**: What is the current core state?
> - **Future**: Where is this heading?

---

## 🚀 Quick Start

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) running locally (for image generation)
- Python 3.7+

### Installation

```bash
# Navigate to your OpenClaw workspace skills directory
cd ~/.openclaw/skills/

# Clone this repo
git clone https://github.com/yusizhaoZYS/tarot-card.git

# Or copy the directory manually
cp -r tarot-card ~/.openclaw/skills/
```

### Usage

Just say **"玩玩塔罗牌"** or **"tarot reading"** in your OpenClaw chat and follow the mystical prompts.

---

## 📁 Project Structure

```
tarot-card/
├── SKILL.md                      # OpenClaw skill definition
├── assets/                       # 78 tarot card images
│   ├── major-00.png ~ major-21.png    # Major Arcana (22 cards)
│   ├── wands-00.png ~ wands-13.png   # Wands suit (14 cards)
│   ├── cups-00.png ~ cups-13.png     # Cups suit (14 cards)
│   ├── swords-00.png ~ swords-13.png # Swords suit (14 cards)
│   └── pentacles-00.png ~ pentacles-13.png # Pentacles suit (14 cards)
├── references/
│   ├── tarot-deck.json          # Full card meanings database
│   └── spreads.md                # Spread position meanings
└── scripts/
    ├── tarot.py                  # Core card drawing logic
    ├── generate_images.py        # ComfyUI batch image generator
    └── organize_assets.py        # Asset organization helper
```

---

## 🔮 How It Works

1. **Choose your question** and **card spread** (single or three)
2. **Pick a number** from 1-78 (think of it silently)
3. The script uses your number as a **seed** to deterministically shuffle the deck
4. Your number determines the **cut position**, revealing the card
5. The card's **orientation** (upright or reversed) is determined by real-time randomness
6. Each card comes with a detailed **meaning** based on rider-waite-tarot symbolism
7. **AI interpretation** provides personalized guidance based on the spread

---

## 🎨 Card Images

All 78 card images are AI-generated via ComfyUI using a fine-tuned prompt approach:

- **Model**: Anything-v5
- **Style**: Rider-Waite tarot illustration aesthetic
- **Aspect ratio**: 2:3 (card proportions)
- **Output**: 768×1152 PNG

Image naming convention: `{suit}-{index}.png`
- Major Arcana: `major-00.png` to `major-21.png`
- Wands: `wands-00.png` (Ace) to `wands-13.png` (King)
- Cups: `cups-00.png` to `cups-13.png`
- Swords: `swords-00.png` to `swords-13.png`
- Pentacles: `pentacles-00.png` to `pentacles-13.png`

---

## 🛠️ Regenerate Card Images

If you want to regenerate the card images (e.g., with a different model):

```bash
# Run the ComfyUI image generator
python3 scripts/generate_images.py

# Organize the output to assets/
python3 scripts/organize_assets.py
```

---

## 🙏 Credit

- Tarot card meanings based on the **Rider-Waite Tarot** tradition
- Card images generated with **ComfyUI** + Anything-v5
- Skill built with **OpenClaw**

---

## 📄 License

MIT

---

# 中文说明

## 🃏 塔罗牌占卜工具

一个充满神秘感的塔罗牌占卜体验，基于 OpenClaw + ComfyUI 构建。

### 功能

- **两种牌阵**：单张（简单当下之问）和三张（过去/现在/未来）
- **78 张专属牌图**：每张牌都有 AI 生成的独特插画
- **数字洗牌机制**：以用户选择的数字为种子，确定性洗牌
- **正逆位自动判断**：由实时随机数决定
- **神秘引导流程**：模拟真实塔罗占卜的仪式感

### 使用方法

在 OpenClaw 对话中直接说 **"玩玩塔罗牌"** 或 **"塔罗占卜"**，跟随神秘提示即可开始。

### 牌阵说明

| 牌阵 | 适用场景 |
|------|----------|
| 单张 | 简单的当下问题 |
| 三张 | 有时间线的事件（过去 → 现在 → 未来） |

### 工作原理

1. 选择问题与牌阵
2. 从 1-78 中默选一个数字
3. 数字决定切牌位置和抽出的牌
4. 实时随机数决定正位或逆位
5. 读取牌义数据库，获取详细解读
6. AI 结合牌阵提供整体指引

---

## Star History

如果你觉得这个项目有趣，欢迎点个 ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=yusizhaoZYS/tarot-card&type=Timeline)](https://star-history.com/#yusizhaoZYS/tarot-card&Timeline)
