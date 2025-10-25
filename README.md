# 🤖 AutoVest Intelligent Financial Advisor

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![ASI Alliance](https://img.shields.io/badge/ASI%20Alliance-Powered-purple.svg)
![Hackathon](https://img.shields.io/badge/Hackathon-2025-gold.svg)

**AI-Powered Financial Investment Advisor with Live Market Data & MeTTa Reasoning**

*SingularityNET MeTTa × ASI:One LLM × Real-Time Market Data*

### 🚀 [Try AutoVest Live Now!](https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7)

**Agent Address:** `agent1qtj8cj3l4shhhayfanc9ce525aum9zhz6kndlxgmkk9e9a25gpwuzergsfe`

[🎬 Watch Demo](#-demo) • [🚀 Try It Live](https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7) • [📚 Documentation](#-documentation) • [🏆 Features](#-8-unique-features)

</div>

---

## 🌟 What Makes AutoVest Different?

> **The Problem:** Most financial AI agents give identical generic responses. Ask about Bitcoin? Generic template. Ask about DeFi protocols? Same template. No personalization, no real intelligence.

> **The Solution:** AutoVest uses **60+ MeTTa reasoning rules** combined with **ASI:One LLM** and **live market data** to deliver intelligent, personalized advice that actually understands your unique situation.

### The AutoVest Difference:

```diff
- Generic Chatbot:
User: "Which DeFi protocols are safest in 2025?"
Bot: "DeFi is risky. Do your own research. Diversify."
[150 characters, no data, no insights]

+ AutoVest:
User: "Which DeFi protocols are safest in 2025?"
AutoVest: 
📊 Current Market (October 2025): S&P +4.2%, Inflation 3.2%
🔐 Safest DeFi Protocols:
  • Aave (Risk: 45/100) - Multi-chain lending, institutional grade
  • Uniswap V4 (Risk: 40/100) - Improved gas efficiency  
  • Compound (Risk: 42/100) - Time-tested, strong governance
🧠 For conservative investors: Allocate only 5-10% to DeFi
💡 Risk Awareness: Smart contract + regulatory risks exist
📈 Wealth Projection: ₹2,025 invested monthly = ₹90k in 20 years
⚠️ Behavioral Warning: Avoid FOMO during pumps, panic during dips
✅ Action Plan: [5 specific steps with DCA strategy]
[2300+ characters, live data, risk analysis, personalized advice]
```

**~600 lines of intelligent code** vs traditional 3000+ lines of hardcoded templates.

---

## 🏆 8 Unique Features

1. **🎯 Risk Scoring System** - 0-100 risk scores for every asset class (stocks, crypto, bonds, REITs)
2. **🌍 Multi-Currency Support** - Auto-converts between USD, INR, EUR with live exchange rates
3. **📊 Market Timing Rules** - Bull/bear indicators, recession signals, optimal entry points
4. **🧠 Behavioral Finance Insights** - FOMO detection, loss aversion warnings, emotional bias alerts
5. **⚖️ Portfolio Rebalancing Logic** - Quarterly rebalancing recommendations with tax optimization
6. **💰 Tax Optimization Strategies** - LTCG vs STCG, India-specific (ELSS, PPF, NPS)
7. **🚨 Emergency Scenario Planning** - Market crash protocols, recession strategies, 6-12 month emergency funds
8. **🎖️ Investment Milestone Tracking** - First ₹1L, ₹10L, ₹1Cr celebration with compounding insights

---

## 🏗️ Architecture

```
User Query: "Should I invest in Solana?"
        ↓
┌───────────────────────────────┐
│   MeTTa Knowledge Graph       │
│   • 60+ financial rules       │
│   • Risk matrices             │
│   • Investment principles     │
│   • Behavioral finance tips   │
└───────────────────────────────┘
        ↓
┌───────────────────────────────┐
│   Live Market Data APIs       │
│   • Polygon.io (stocks)       │
│   • CoinGecko (crypto)        │
│   • Real-time prices          │
└───────────────────────────────┘
        ↓
┌───────────────────────────────┐
│   ASI:One LLM                 │
│   • Natural language          │
│   • Context extraction        │
│   • 2000+ char responses      │
└───────────────────────────────┘
        ↓
Intelligent Response with:
✓ Current price & trend
✓ Risk analysis (0-100 score)
✓ Wealth projections (5, 10, 20 years)
✓ Behavioral psychology insights
✓ Portfolio comparisons
✓ Specific action steps
```

---

## 📁 Project Structure

```
AutoVest/
├── agent_clean.py              # Main agent entry point (~150 lines)
├── metta/
│   ├── knowledge.py            # MeTTa knowledge graph (60+ rules)
│   ├── generalrag.py           # RAG system
│   ├── utils.py                # LLM, market data, risk calculator
│   └── __init__.py
├── requirements.txt            # Python dependencies
├── .env                        # API keys (gitignored)
├── .gitignore                  # Git ignore patterns
├── benchmark_performance.py    # Performance testing tool (optional)
├── README.md                   # This file
└── venv/                       # Virtual environment (gitignored)
```

**Clean & Minimal:** Just ~600 lines of core code + documentation. No bloat!

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Darshan-1812/AutoVest.git
cd AutoVest
```

### 2. Setup Environment (WSL Ubuntu)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows PowerShell
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
# Required for LLM responses
ASI_API_KEY=your_asi_api_key_here

# Market data APIs (optional - defaults provided)
POLYGON_API_KEY=your_polygon_key  # Get free key from polygon.io
COINGECKO_API_KEY=optional        # CoinGecko has free tier
```

**Get ASI API Key:** https://asi1.ai/

### 5. Run the Agent

```bash
python agent_clean.py
```

Expected output:
```
🚀 Initializing AutoVest Intelligence System...
✅ Financial knowledge graph initialized with 8 unique features!
✅ ASI:One LLM enabled!
✅ AutoVest ready: MeTTa + Live Market Data + LLM

Agent Address: agent1qtj8cj3l4shhhayfanc9ce525aum9zhz6kndlxgmkk9e9a25gpwuzergsfe
🔄 Agent is now running... (Press CTRL+C to stop)
```

### 6. Test via Agentverse

Visit: [https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7](https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7)

---

## 💡 Example Queries

### Cryptocurrency Analysis
- "Should I invest in Bitcoin?"
- "Which DeFi protocols are safest in 2025?"
- "Compare Solana and Avalanche for scalability"
- "What about Ethereum vs Bitcoin for long-term holding?"

### Portfolio Planning
- "I'm 28 with moderate risk tolerance. What's the ideal portfolio mix?"
- "Create a retirement portfolio for a 45-year-old"
- "Best aggressive portfolio for a 22-year-old?"

### Market Strategy
- "How to invest during high inflation?"
- "What should I do if the market crashes 30%?"
- "Best time to buy stocks - bull or bear market?"

### Financial Education
- "What's the 4% rule for retirement?"
- "Explain dollar-cost averaging"
- "How to diversify my investments?"
- "What's the difference between LTCG and STCG?"

---

## 🎯 Sample Response

**Query:** "I'm 25 with moderate risk tolerance. What's the ideal portfolio mix for me?"

**AutoVest Response:**

```
Hey there! 👋 At 25 with moderate risk tolerance, you have TIME on your side - 
your biggest asset in investing. Given October 2025 market conditions (S&P +4.2%, 
inflation cooling to 3.2%), it's a solid time to build your foundation.

📊 **Ideal Portfolio Mix (Moderate, Age 25)**

| Asset Class | Allocation | Risk Score | Expected Return |
|-------------|------------|------------|-----------------|
| US Stocks   | 50%        | 65/100     | 8-12% annually  |
| Bonds       | 25%        | 25/100     | 4-6% annually   |
| REITs       | 15%        | 50/100     | 6-9% annually   |
| Cash/Stable | 10%        | 5/100      | 2-4% annually   |

💰 **Wealth Projection (₹10,000/month investment)**

| Years | Total Invested | Projected Value | Growth  |
|-------|----------------|-----------------|---------|
| 5     | ₹6.0L          | ₹7.4L          | +23%    |
| 10    | ₹12.0L         | ₹17.8L         | +48%    |
| 20    | ₹24.0L         | ₹53.5L         | +123%   |

🧠 **Behavioral Finance Tips**
- FOMO Warning: Don't chase hot stocks when everyone's buying
- Loss Aversion: Losses feel 2x worse than gains - stay disciplined
- Market Timing: Time IN the market beats timing THE market

✅ **Action Plan**
1. Set up automatic monthly investments (discipline > emotion)
2. Rebalance quarterly to maintain target percentages
3. Track progress but don't obsess over daily movements
4. Consider tax-advantaged accounts (401k, IRA, or ELSS in India)
5. Build 6-month emergency fund before aggressive investing

You're starting early - that's your superpower! 💪 Keep learning, stay 
consistent, and let compounding work its magic.

📊 Data Sources: Polygon.io (stocks) | CoinGecko (crypto) | October 2025
🧠 Intelligence: MeTTa Knowledge Graph + ASI:One LLM
```

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Agent Framework** | Fetch.ai uAgents | Mailbox, chat protocol |
| **AI Reasoning** | SingularityNET Hyperon MeTTa 0.2.8 | Knowledge graph, symbolic reasoning |
| **Language Model** | ASI:One LLM (asi1-mini) | Natural language generation |
| **Stock Data** | Polygon.io API | Real-time US stock prices |
| **Crypto Data** | CoinGecko API | Cryptocurrency prices |
| **Architecture** | RAG Pattern | Retrieval-Augmented Generation |
| **Language** | Python 3.10+ | Core implementation |

---

## 📊 Why This Approach is Better

### Traditional Approach (3000+ lines):
- ❌ Hardcoded templates for each query type
- ❌ Rigid pattern matching ("if query contains 'bitcoin'...")
- ❌ Manual response generation for every scenario
- ❌ Cannot handle variations ("Should I invest in Solana?" fails)
- ❌ Difficult to maintain and extend

### AutoVest Approach (~600 lines):
- ✅ MeTTa knowledge graph stores principles as facts
- ✅ LLM naturally understands any investment question
- ✅ Dynamic response generation based on context
- ✅ Handles ANY asset without pre-programming
- ✅ Easy to extend - just add facts to MeTTa

**Example:** To add support for a new cryptocurrency:

```python
# Traditional: Write 100+ lines of hardcoded logic
def handle_cardano_query(user_query):
    if "cardano" in query.lower():
        response = "Cardano is a proof-of-stake blockchain..."
        # ... 80 more lines ...

# AutoVest: Add 3 lines to knowledge graph
metta.run("""
    (= (crypto-feature Cardano) "Proof-of-stake. Academic approach.")
    (= (volatility Cardano) 65)
""")
# LLM handles everything else automatically!
```

---

## 📚 Documentation

All documentation is contained in this README for simplicity. Key sections:

- **[Quick Start](#-quick-start)** - Setup and installation guide
- **[Example Queries](#-example-queries)** - Sample questions and use cases
- **[Sample Response](#-sample-response)** - See actual agent output
- **[Technology Stack](#-technology-stack)** - Technical details
- **[Architecture](#-architecture)** - How it works under the hood

**For Agentverse deployment:** See the agent's live README at the [Agentverse Overview page](https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7)

---

## 🏆 Hackathon Highlights

### Innovation Points
1. **Hybrid Intelligence**: Combines symbolic reasoning (MeTTa) with neural language models (LLM)
2. **Live Data Integration**: Real-time market data from Polygon.io and CoinGecko
3. **Behavioral Finance**: First agent to integrate psychological bias detection
4. **Dynamic Context Extraction**: Automatically detects age, risk tolerance, location from natural language
5. **Wealth Projections**: Built-in compound interest calculator with milestone tracking

### Judge Appeal
- ✅ **Functionality**: Fully working agent with real conversations
- ✅ **ASI Alliance Tech**: Uses MeTTa, ASI:One LLM, uAgents, Agentverse mailbox
- ✅ **Innovation**: Novel combination of symbolic + neural AI for finance
- ✅ **Real-World Impact**: Solves actual problem of generic financial advice
- ✅ **Code Quality**: Clean, documented, maintainable architecture

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Test performance:** `python benchmark_performance.py` (optional)
5. **Commit your changes:** `git commit -m 'Add amazing feature'`
6. **Push to the branch:** `git push origin feature/amazing-feature`
7. **Open a Pull Request** with a clear description

### Contribution Ideas:
- Add support for more cryptocurrencies/stocks
- Enhance MeTTa knowledge graph with new financial rules
- Improve risk scoring algorithms
- Add more currency support
- Create visualizations for portfolio projections

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## 🙏 Credits

- **Fetch.ai** for the uAgents framework and Agentverse platform
- **SingularityNET** for MeTTa symbolic reasoning engine
- **ASI Alliance** for the hackathon and ASI:One LLM access
- **Innovation Lab** for inspiration from examples

---

## 📞 Contact & Support

- **GitHub Repository**: [https://github.com/Darshan-1812/AutoVest](https://github.com/Darshan-1812/AutoVest)
- **Live Agent**: [Chat with AutoVest](https://chat.agentverse.ai/sessions/04fc6cc8-f6e5-4000-8881-b72b6fa064b7)
- **Issues**: [GitHub Issues](https://github.com/Darshan-1812/AutoVest/issues)
- **Creator**: [@Darshan-1812](https://github.com/Darshan-1812)

---

<div align="center">

**Built with ❤️ for the ASI Alliance Hackathon 2025**

*Demonstrating the power of MeTTa + ASI:One LLM for intelligent financial advisory*

Made with 🧠 **SingularityNET MeTTa** • 🤖 **Fetch.ai uAgents** • 💬 **ASI:One LLM**

</div>

