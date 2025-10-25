"""
Financial Knowledge Graph for AutoVest
Loads investment knowledge into MeTTa space
"""

from hyperon import MeTTa

def initialize_knowledge_graph(metta: MeTTa):
    """Initialize the financial knowledge graph with investment facts."""
    
    # Load investment principles
    metta.run("""
        ; Core Investment Principles
        (= (investment-principle diversification)
            "Diversify across asset classes to reduce risk. Don't put all eggs in one basket.")
        
        (= (investment-principle compounding)
            "Start early to maximize compound growth. Time in market beats timing the market.")
        
        (= (investment-principle risk-return)
            "Higher potential returns come with higher risk. Match investments to risk tolerance.")
        
        (= (investment-principle dollar-cost-averaging)
            "Invest fixed amounts regularly to average out market volatility.")
        
        (= (investment-principle emergency-fund)
            "Keep 6 months expenses in savings before aggressive investing.")
        
        ; Asset Classes
        (= (asset-class stocks) 
            "Stocks offer growth potential with moderate-high risk. Historical 8-10% annual returns.")
        
        (= (asset-class bonds)
            "Bonds provide stability with lower returns. Good for conservative portfolios.")
        
        (= (asset-class crypto)
            "Cryptocurrencies are high-risk, high-reward speculative assets. Very volatile.")
        
        (= (asset-class index-funds)
            "Index funds track market indices. Low fees, broad diversification, consistent returns.")
        
        (= (asset-class real-estate)
            "Real estate offers tangible assets with rental income. Requires significant capital.")
        
        ; Volatility Data
        (= (volatility Bitcoin) 60)
        (= (volatility Ethereum) 65)
        (= (volatility Solana) 70)
        (= (volatility SP500) 15)
        (= (volatility Stocks) 25)
        (= (volatility Bonds) 5)
        
        ; 🎯 ENHANCED: Asset Risk Matrix Data
        (= (asset-risk-matrix US-Stocks)
            (risk-score 65) (return-potential "High") (liquidity "High") 
            (comment "Core growth driver for long-term wealth"))
        
        (= (asset-risk-matrix International-Stocks)
            (risk-score 70) (return-potential "High") (liquidity "High")
            (comment "Geographic diversification reduces country-specific risks"))
        
        (= (asset-risk-matrix Bonds)
            (risk-score 25) (return-potential "Moderate") (liquidity "High")
            (comment "Stability cushion during market volatility"))
        
        (= (asset-risk-matrix REITs)
            (risk-score 55) (return-potential "Moderate-High") (liquidity "Medium")
            (comment "Inflation hedge with real estate exposure"))
        
        (= (asset-risk-matrix Gold)
            (risk-score 35) (return-potential "Low-Moderate") (liquidity "High")
            (comment "Safe haven asset for portfolio protection"))
        
        (= (asset-risk-matrix Bitcoin)
            (risk-score 85) (return-potential "Very High") (liquidity "High")
            (comment "High volatility speculative digital asset"))
        
        (= (asset-risk-matrix Solana)
            (risk-score 90) (return-potential "Very High") (liquidity "Medium")
            (comment "Higher risk than Bitcoin with growth potential"))
        
        ; 🎯 ENHANCED: Portfolio Return Projections (Historical Average)
        (= (portfolio-returns conservative) 
            (allocation "20/70/10") (annual-return 5.5) (volatility 8))
        
        (= (portfolio-returns moderate) 
            (allocation "60/30/10") (annual-return 7.5) (volatility 15))
        
        (= (portfolio-returns aggressive) 
            (allocation "80/15/5") (annual-return 9.2) (volatility 22))
        
        ; 🎯 ENHANCED: Market Sentiment Indicators
        (= (market-sentiment bullish)
            "Market showing positive momentum. Good time for entry but watch for overvaluation.")
        
        (= (market-sentiment bearish)
            "Market experiencing downward pressure. Focus on value and defensive positions.")
        
        (= (market-sentiment sideways)
            "Market consolidating. Good time for rebalancing and DCA strategies.")
        
        ; 🎯 ENHANCED: Wealth-Building Projections
        (= (wealth-projection monthly-10k-20years)
            (total-invested "24L") (projected-value "47.3L") (return-rate 7.5))
        
        (= (wealth-projection monthly-5k-20years)
            (total-invested "12L") (projected-value "23.7L") (return-rate 7.5))
        
        (= (wealth-projection monthly-25k-20years)
            (total-invested "60L") (projected-value "1.18Cr") (return-rate 7.5))
        
        ; Expected Returns (Annual)
        (= (expected-return Bitcoin) 35)
        (= (expected-return Ethereum) 30)
        (= (expected-return Solana) 40)
        (= (expected-return SP500) 10)
        (= (expected-return Stocks) 12)
        (= (expected-return Bonds) 4)
        (= (expected-return Real-Estate) 8)
        
        ; Age-Based Strategies
        (= (age-strategy 20s)
            "Aggressive growth: 80-90% stocks/crypto, 10-20% bonds. Long time horizon allows risk.")
        
        (= (age-strategy 30s)
            "Growth-focused: 70-80% stocks, 20-30% bonds. Balance growth with some stability.")
        
        (= (age-strategy 40s)
            "Balanced: 60% stocks, 30% bonds, 10% alternatives. Reduce risk as retirement nears.")
        
        (= (age-strategy 50s)
            "Conservative: 50% stocks, 40% bonds, 10% cash. Preserve capital for retirement.")
        
        ; Crypto-Specific Knowledge
        (= (crypto-feature Bitcoin)
            "First cryptocurrency. 21 million max supply. Digital gold narrative. Highest adoption.")
        
        (= (crypto-feature Ethereum)
            "Smart contract platform. Powers DeFi and NFTs. Proof-of-Stake consensus.")
        
        (= (crypto-feature Solana)
            "High-speed blockchain. Low transaction costs. Growing DeFi ecosystem. High performance.")
        
        ; Investment Comparisons
        (= (compare-assets Bitcoin SP500)
            "Bitcoin: Higher returns (35% avg) but 60% volatility. S&P 500: Stable 10% returns with 15% volatility.")
        
        (= (compare-assets Crypto Stocks)
            "Crypto offers explosive growth potential but extreme volatility. Stocks provide steady, proven returns.")
        
        ; Risk Tolerance Mapping
        (= (risk-level conservative) 
            "Low risk tolerance: 70% bonds, 30% blue-chip stocks. Capital preservation priority.")
        
        (= (risk-level moderate)
            "Moderate risk: 60% stocks, 30% bonds, 10% alternatives. Balanced growth and stability.")
        
        (= (risk-level aggressive)
            "High risk tolerance: 80% stocks/crypto, 20% bonds. Maximum growth potential.")
        
        ; Retirement Planning
        (= (retirement-rule four-percent)
            "Withdraw 4% annually from retirement corpus for sustainable income.")
        
        (= (retirement-corpus-needed monthly-expense)
            "Need 300x monthly expenses for retirement. ₹50,000/month = ₹1.5 crore corpus.")
        
        ; Market Data Sources
        (= (data-source crypto) "CoinGecko API for real-time cryptocurrency prices")
        (= (data-source stocks) "Polygon.io API for real-time stock market data")
        
        ; 🎯 UNIQUE FEATURE 1: MeTTa Risk Scoring System
        ; Calculates investment risk scores based on multiple factors
        (= (risk-factor volatility-score $vol)
            (if (> $vol 50) 
                high-risk
                (if (> $vol 25) 
                    moderate-risk 
                    low-risk)))
        
        (= (calculate-risk-score $asset $volatility $liquidity $regulation)
            (+ (* $volatility 0.5) (* $liquidity 0.3) (* $regulation 0.2)))
        
        ; Risk scores for different assets (0-100 scale)
        (= (comprehensive-risk Bitcoin) 
            (risk-factors 60 85 70))  ; volatility, liquidity, regulatory-clarity
        (= (comprehensive-risk Ethereum) 
            (risk-factors 65 80 65))
        (= (comprehensive-risk Solana) 
            (risk-factors 70 60 50))
        (= (comprehensive-risk SP500) 
            (risk-factors 15 95 95))
        (= (comprehensive-risk Bonds) 
            (risk-factors 5 90 98))
        
        ; 🎯 UNIQUE FEATURE 2: Multi-Currency Support
        (= (currency INR) "Indian Rupee")
        (= (currency USD) "US Dollar")
        (= (currency EUR) "Euro")
        (= (conversion-rate USD INR) 83.5)
        (= (conversion-rate EUR INR) 91.2)
        (= (conversion-rate USD EUR) 0.92)
        
        ; 🎯 UNIQUE FEATURE 3: Time-Based Investment Wisdom
        (= (market-timing-rule bull-market)
            "During bull markets: Take profits gradually, rebalance to target allocations")
        (= (market-timing-rule bear-market)
            "During bear markets: Dollar-cost average, focus on quality assets")
        (= (market-timing-rule sideways-market)
            "During sideways markets: Accumulate positions, sell covered calls")
        
        ; 🎯 UNIQUE FEATURE 4: Behavioral Finance Principles
        (= (behavioral-bias loss-aversion)
            "Losses hurt 2x more than gains feel good. Combat by setting stop-losses")
        (= (behavioral-bias recency-bias)
            "Recent trends feel permanent. Remember: markets are cyclical")
        (= (behavioral-bias herd-mentality)
            "FOMO drives bad decisions. Stick to your investment plan")
        (= (behavioral-bias confirmation-bias)
            "We seek info confirming our beliefs. Actively seek opposing views")
        
        ; 🎯 UNIQUE FEATURE 5: Portfolio Rebalancing Logic
        (= (rebalancing-trigger deviation)
            "Rebalance when any asset deviates >5% from target allocation")
        (= (rebalancing-frequency quarterly)
            "Review portfolio quarterly, rebalance if needed")
        (= (rebalancing-benefit risk-control)
            "Rebalancing forces 'buy low, sell high' discipline")
        
        ; 🎯 UNIQUE FEATURE 6: Tax Optimization Strategies
        (= (tax-strategy long-term-holdings)
            "Hold >1 year for long-term capital gains (lower tax rate)")
        (= (tax-strategy tax-loss-harvesting)
            "Sell losing positions to offset gains and reduce tax liability")
        (= (tax-strategy retirement-accounts)
            "Maximize tax-advantaged accounts (401k, IRA) before taxable investing")
        
        ; 🎯 UNIQUE FEATURE 7: Emergency Scenarios
        (= (emergency-scenario job-loss)
            "Keep 12 months expenses. Pause aggressive investing. Focus on essentials.")
        (= (emergency-scenario market-crash)
            "Don't panic sell. Stick to plan. Consider buying opportunities.")
        (= (emergency-scenario medical-emergency)
            "Use emergency fund first. Avoid liquidating long-term investments.")
        
        ; 🎯 UNIQUE FEATURE 8: Investment Milestones
        (= (milestone first-10k) 
            "First ₹10,000 invested: Foundation built. Focus on consistency now.")
        (= (milestone first-lakh)
            "First ₹1 lakh: Real momentum. Compound interest accelerating.")
        (= (milestone first-10-lakhs)
            "First ₹10 lakhs: Serious wealth building. Consider tax optimization.")
        (= (milestone first-crore)
            "First ₹1 crore: Financial independence in sight. Diversify wisely.")
    """)
    
    print("✅ Financial knowledge graph initialized with 8 unique features!")
    print("   🎯 Risk scoring system")
    print("   🌍 Multi-currency support")
    print("   📊 Market timing rules")
    print("   🧠 Behavioral finance insights")
    print("   ⚖️ Portfolio rebalancing logic")
    print("   💰 Tax optimization strategies")
    print("   🚨 Emergency scenario planning")
    print("   🎖️ Investment milestone tracking")
