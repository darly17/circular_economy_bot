# Circular Economy Bot Belarus

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Intelligent AI-powered chatbot for connecting waste producers and consumers in Belarusian circular economy**

> 💡 Transforming industrial waste into valuable resources through AI-powered matchmaking

##  Overview

Circular Economy Bot is an intelligent system that helps Belarusian industrial enterprises find partners for waste utilization and secondary raw materials sourcing. The bot uses advanced AI to semantically analyze enterprise needs and match producers with consumers of industrial by-products.

### Key Features

- ** AI-Powered Matching** - Semantic analysis using LLM (Groq/Llama) for intelligent partner selection
- ** Telegram Integration** - User-friendly chat interface in Telegram messenger
- ** Enterprise Database** - Comprehensive database of Belarusian industrial enterprises
- **Role-Based Search** - Tailored recommendations for technologists and sales representatives
- **Smart Recommendations** - Context-aware business advice and contact strategies
- **Fallback System** - Robust operation even when AI services are unavailable


##  Quick Start

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- Groq API Key ([GroqCloud](https://groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/circular-economy-bot.git
cd circular-economy-bot

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
