"""
General RAG (Retrieval-Augmented Generation) for AutoVest
Queries MeTTa knowledge graph for relevant investment information
"""

from hyperon import MeTTa
from typing import List, Dict, Any

class GeneralRAG:
    """RAG system that queries MeTTa knowledge graph."""
    
    def __init__(self, metta: MeTTa):
        self.metta = metta
    
    def query_knowledge(self, query: str) -> List[str]:
        """
        Query the MeTTa knowledge graph for relevant information.
        Returns list of relevant facts and principles.
        """
        results = []
        query_lower = query.lower()
        
        # Determine what to query based on keywords
        queries_to_run = []
        
        # Investment principles
        if any(word in query_lower for word in ["how", "why", "should", "principle", "strategy"]):
            queries_to_run.append("!(investment-principle $x)")
        
        # Specific assets
        if "bitcoin" in query_lower or "btc" in query_lower:
            queries_to_run.extend([
                "!(crypto-feature Bitcoin)",
                "!(volatility Bitcoin)",
                "!(expected-return Bitcoin)"
            ])
        
        if "ethereum" in query_lower or "eth" in query_lower:
            queries_to_run.extend([
                "!(crypto-feature Ethereum)",
                "!(volatility Ethereum)",
                "!(expected-return Ethereum)"
            ])
        
        if "solana" in query_lower or "sol" in query_lower:
            queries_to_run.extend([
                "!(crypto-feature Solana)",
                "!(volatility Solana)",
                "!(expected-return Solana)"
            ])
        
        if any(word in query_lower for word in ["stock", "index", "s&p", "spy"]):
            queries_to_run.extend([
                "!(asset-class stocks)",
                "!(asset-class index-funds)",
                "!(volatility SP500)",
                "!(expected-return SP500)"
            ])
        
        # Age-based strategies
        if any(age in query_lower for age in ["20s", "twenties", "25", "28"]):
            queries_to_run.append("!(age-strategy 20s)")
        elif any(age in query_lower for age in ["30s", "thirties", "35"]):
            queries_to_run.append("!(age-strategy 30s)")
        elif any(age in query_lower for age in ["40s", "forties", "45"]):
            queries_to_run.append("!(age-strategy 40s)")
        elif any(age in query_lower for age in ["50s", "fifties", "55"]):
            queries_to_run.append("!(age-strategy 50s)")
        
        # Comparisons
        if "vs" in query_lower or "versus" in query_lower or "compare" in query_lower:
            if "bitcoin" in query_lower and ("stock" in query_lower or "s&p" in query_lower):
                queries_to_run.append("!(compare-assets Bitcoin SP500)")
            elif "crypto" in query_lower and "stock" in query_lower:
                queries_to_run.append("!(compare-assets Crypto Stocks)")
        
        # Risk tolerance
        if "risk" in query_lower:
            if "low" in query_lower or "conservative" in query_lower or "safe" in query_lower:
                queries_to_run.append("!(risk-level conservative)")
            elif "high" in query_lower or "aggressive" in query_lower:
                queries_to_run.append("!(risk-level aggressive)")
            else:
                queries_to_run.append("!(risk-level moderate)")
        
        # Retirement
        if "retire" in query_lower or "retirement" in query_lower:
            queries_to_run.extend([
                "!(retirement-rule four-percent)",
                "!(retirement-corpus-needed monthly-expense)"
            ])
        
        # 🎯 NEW: Risk scoring queries
        if "risk score" in query_lower or "how risky" in query_lower:
            for asset in ["Bitcoin", "Ethereum", "Solana", "SP500"]:
                if asset.lower() in query_lower:
                    queries_to_run.append(f"!(comprehensive-risk {asset})")
        
        # 🎯 NEW: Currency conversion queries
        if any(curr in query_lower for curr in ["rupee", "₹", "inr", "dollar", "$", "euro", "€"]):
            queries_to_run.extend([
                "!(conversion-rate USD INR)",
                "!(conversion-rate EUR INR)"
            ])
        
        # 🎯 NEW: Market timing queries
        if any(word in query_lower for word in ["bull market", "bear market", "market crash", "timing"]):
            queries_to_run.extend([
                "!(market-timing-rule bull-market)",
                "!(market-timing-rule bear-market)",
                "!(market-timing-rule sideways-market)"
            ])
        
        # 🎯 NEW: Behavioral finance queries
        if any(word in query_lower for word in ["fomo", "panic", "emotion", "psychology", "behavior"]):
            queries_to_run.extend([
                "!(behavioral-bias loss-aversion)",
                "!(behavioral-bias recency-bias)",
                "!(behavioral-bias herd-mentality)",
                "!(behavioral-bias confirmation-bias)"
            ])
        
        # 🎯 NEW: Rebalancing queries
        if "rebalanc" in query_lower or "adjust portfolio" in query_lower:
            queries_to_run.extend([
                "!(rebalancing-trigger deviation)",
                "!(rebalancing-frequency quarterly)",
                "!(rebalancing-benefit risk-control)"
            ])
        
        # 🎯 NEW: Tax optimization queries
        if "tax" in query_lower or "save tax" in query_lower:
            queries_to_run.extend([
                "!(tax-strategy long-term-holdings)",
                "!(tax-strategy tax-loss-harvesting)",
                "!(tax-strategy retirement-accounts)"
            ])
        
        # 🎯 NEW: Emergency scenario queries
        if any(word in query_lower for word in ["emergency", "job loss", "crisis", "crash"]):
            queries_to_run.extend([
                "!(emergency-scenario job-loss)",
                "!(emergency-scenario market-crash)",
                "!(emergency-scenario medical-emergency)"
            ])
        
        # 🎯 NEW: Milestone queries
        if any(word in query_lower for word in ["milestone", "first", "10k", "lakh", "crore", "achievement"]):
            queries_to_run.extend([
                "!(milestone first-10k)",
                "!(milestone first-lakh)",
                "!(milestone first-10-lakhs)",
                "!(milestone first-crore)"
            ])
        
        # Execute queries
        for metta_query in queries_to_run:
            try:
                result = self.metta.run(metta_query)
                if result:
                    for item in result:
                        results.append(str(item))
            except Exception as e:
                print(f"MeTTa query error: {e}")
        
        # If no specific matches, return general principles
        if not results:
            general_queries = [
                "!(investment-principle diversification)",
                "!(investment-principle compounding)",
                "!(investment-principle risk-return)"
            ]
            for metta_query in general_queries:
                try:
                    result = self.metta.run(metta_query)
                    if result:
                        for item in result:
                            results.append(str(item))
                except:
                    pass
        
        return results
    
    def get_context_for_llm(self, query: str) -> str:
        """
        Get knowledge graph context formatted for LLM prompt.
        """
        knowledge_items = self.query_knowledge(query)
        
        if not knowledge_items:
            return "No specific knowledge found. Provide general investment advice."
        
        context = "Relevant Financial Knowledge:\n"
        for i, item in enumerate(knowledge_items, 1):
            context += f"{i}. {item}\n"
        
        return context
