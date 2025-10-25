"""
AutoVest - Simplified Intelligent Financial Advisor Agent
Following SingularityNET Innovation Lab pattern
~150 lines vs 3000+ lines, but SMARTER with MeTTa + LLM
"""

import asyncio
from datetime import datetime, timezone
from uuid import uuid4
import os
from dotenv import load_dotenv
from uagents import Context, Model, Protocol, Agent
from hyperon import MeTTa

from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Import our MeTTa components
from metta.generalrag import GeneralRAG
from metta.knowledge import initialize_knowledge_graph
from metta.utils import LLM, process_query

# Load environment variables
load_dotenv()

# Get mailbox key from environment (optional - for Agentverse mailbox)
AGENT_MAILBOX_KEY = os.getenv("AGENT_MAILBOX_KEY")

# Initialize agent as mailbox agent
# For mailbox agents, DO NOT provide endpoints - the mailbox handles communication
agent = Agent(
    name="AutoVest_Intelligent_Advisor",
    port=8005,
    seed="autovest_seed_phrase_change_this",  # Change this to your own seed
    mailbox=AGENT_MAILBOX_KEY if AGENT_MAILBOX_KEY else True,  # Enable mailbox
    # No endpoint needed - mailbox agents communicate through Agentverse
)

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Create a text chat message."""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=content,
    )

# Initialize intelligence components
print("🚀 Initializing AutoVest Intelligence System...")
print("   📚 Loading MeTTa knowledge graph...")
metta = MeTTa()
initialize_knowledge_graph(metta)
rag = GeneralRAG(metta)

# Initialize LLM
asi_api_key = os.getenv("ASI_API_KEY") or os.getenv("ASI_ONE_API_KEY")
if asi_api_key:
    llm = LLM(api_key=asi_api_key)
    print("   ✅ ASI:One LLM enabled!")
else:
    llm = None
    print("   ⚠️  No ASI_API_KEY - LLM disabled (set in .env)")

print("✅ AutoVest ready: MeTTa + Live Market Data + LLM")

# Chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle investment queries with MeTTa RAG + LLM + Live Data
    This replaces 2000+ lines of rule-based code!
    """
    ctx.storage.set(str(ctx.session), sender)
    
    # Acknowledge
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        ),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"💬 Session started: {sender}")
            welcome = (
                "👋 **Welcome to AutoVest!**\n\n"
                "I'm your AI financial advisor powered by:\n"
                "• 🧠 **MeTTa Knowledge Graph** (SingularityNET Hyperon)\n"
                "• 🤖 **ASI:One LLM** for natural conversation\n"
                "• 📊 **Live Market Data** (Polygon.io + CoinGecko)\n\n"
                "Ask me anything:\n"
                "• \"Should I invest in Bitcoin?\"\n"
                "• \"Should I invest in Solana?\"\n"
                "• \"I'm 28, how should I plan for retirement?\"\n"
                "• \"Compare Bitcoin vs stocks\"\n"
                "• \"What's a good portfolio for aggressive growth?\""
            )
            await ctx.send(sender, create_text_chat(welcome))
            
        elif isinstance(item, TextContent):
            user_query = item.text.strip()
            ctx.logger.info(f"💡 Query: {user_query}")
            
            if not llm:
                error = (
                    "⚠️ **LLM Not Configured**\n\n"
                    "Please set `ASI_API_KEY` in your `.env` file.\n"
                    "Get your API key from: https://asi1.ai/\n\n"
                    "The agent needs LLM to generate intelligent responses."
                )
                await ctx.send(sender, create_text_chat(error))
                continue
            
            try:
                # THE MAGIC: MeTTa queries knowledge + Live API data + LLM generates response
                ctx.logger.info("🔍 Processing with MeTTa RAG + Market Data + LLM...")
                response = process_query(user_query, rag, llm)
                
                # Extract and format response
                if isinstance(response, dict):
                    answer = response.get('humanized_answer', 'Could not process query.')
                    
                    # Add data attribution
                    footer = (
                        "\n\n---\n"
                        "📊 *Live data: Polygon.io (stocks) | CoinGecko (crypto)*\n"
                        "🧠 *Intelligence: MeTTa Knowledge Graph + ASI:One LLM*"
                    )
                    answer += footer
                else:
                    answer = str(response)
                
                ctx.logger.info(f"✅ Generated {len(answer)} char response")
                await ctx.send(sender, create_text_chat(answer))
                
            except Exception as e:
                ctx.logger.error(f"❌ Error: {e}")
                error_msg = (
                    "I encountered an error processing your query. "
                    "Please try rephrasing or ask a different question."
                )
                await ctx.send(sender, create_text_chat(error_msg))
        
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"👋 Session ended: {sender}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements."""
    ctx.logger.info(f"✓ ACK from {sender}")

# Register protocol
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 AutoVest Financial Advisor - SIMPLE & SMART")
    print("="*70)
    print(f"📍 Agent Address: {agent.address}")
    print(f"🔑 Mailbox: ✅ Enabled")
    print(f"🤖 ASI:One LLM: {'✅ Enabled' if llm else '⚠️  Disabled (set ASI_API_KEY)'}")
    print(f"📊 Market APIs: ✅ Polygon.io + CoinGecko")
    print(f"🧠 MeTTa Graph: ✅ Financial knowledge loaded")
    print("="*70)
    print("\n💡 Key Difference from Innovation Lab Example:")
    print("   • Their agent: General Fetch.ai/uAgents documentation")
    print("   • Our agent: Financial advisor with LIVE market data + calculations")
    print("\n🎯 Why This is Better Than 3000+ Line Version:")
    print("   ❌ OLD: 2000+ lines of hardcoded rules for each query type")
    print("   ✅ NEW: ~150 lines, LLM generates intelligent responses")
    print("   ❌ OLD: Rigid pattern matching, can't handle variations")
    print("   ✅ NEW: Natural language understanding via LLM")
    print("   ❌ OLD: Manual response templating")
    print("   ✅ NEW: MeTTa provides knowledge, LLM formats naturally")
    print("="*70 + "\n")
    
    # Run agent - this should block and keep running
    try:
        print("🔄 Agent is now running... (Press CTRL+C to stop)\n")
        agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
    except Exception as e:
        print(f"\n\n❌ Agent error: {e}")
        import traceback
        traceback.print_exc()
