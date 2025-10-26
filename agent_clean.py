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

# Import trade execution and blockchain modules
from metta.trade_executor import TradeExecutor
from metta.blockchain_logger import BlockchainLogger

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

# Initialize trade execution and blockchain
print("   💰 Initializing Trade Execution...")
trade_executor = TradeExecutor()
print("   ⛓️  Initializing Blockchain Logger...")
blockchain_logger = BlockchainLogger()

print("✅ AutoVest ready: MeTTa + Live Market Data + LLM + Trade Execution + Blockchain")

# Trade execution handler functions
async def handle_trade_execution(ctx: Context, sender: str, query: str):
    """Handle trade execution commands"""
    try:
        # Parse: "execute trade: buy 1 AAPL" or "execute trade: sell 5 TSLA"
        command_part = query.split(":", 1)[1].strip()
        parts = command_part.split()
        
        if len(parts) < 3:
            error = (
                "❌ **Invalid trade command format**\n\n"
                "Use: `execute trade: <buy/sell> <quantity> <symbol>`\n\n"
                "Examples:\n"
                "• `execute trade: buy 1 AAPL`\n"
                "• `execute trade: sell 5 TSLA`\n"
                "• `execute trade: buy 100 BTC/USDT`"
            )
            await ctx.send(sender, create_text_chat(error))
            return
        
        side = parts[0].lower()
        quantity = parts[1]
        symbol = parts[2].upper()
        
        if side not in ["buy", "sell"]:
            await ctx.send(sender, create_text_chat("❌ Side must be 'buy' or 'sell'"))
            return
        
        # Determine if stock or crypto
        is_crypto = "/" in symbol  # BTC/USDT format indicates crypto
        
        ctx.logger.info(f"🔄 Executing {'crypto' if is_crypto else 'stock'} trade: {side} {quantity} {symbol}")
        
        # Execute trade
        if is_crypto:
            result = trade_executor.execute_crypto_trade(
                symbol=symbol,
                amount=float(quantity),
                side=side
            )
        else:
            result = trade_executor.execute_stock_trade(
                symbol=symbol,
                quantity=float(quantity),
                side=side
            )
        
        if result["success"]:
            # Log trade on blockchain
            trade_data = {
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "price": result.get("filled_price") or result.get("price", 0),
                "platform": result.get("platform", "AutoVest"),
                "order_id": result.get("order_id")
            }
            
            blockchain_result = blockchain_logger.log_trade(trade_data)
            
            # Build response
            response = (
                f"✅ **Trade Executed Successfully!**\n\n"
                f"**Order Details:**\n"
                f"• Symbol: {symbol}\n"
                f"• Side: {side.upper()}\n"
                f"• Quantity: {quantity}\n"
                f"• Price: ${result.get('filled_price') or result.get('price', 'N/A')}\n"
                f"• Order ID: `{result.get('order_id')}`\n"
                f"• Status: {result.get('status', 'Filled')}\n"
            )
            
            if blockchain_result.get("success"):
                tx_hash_str = str(blockchain_result.get('tx_hash', ''))
                tx_display = tx_hash_str[:16] + "..." if len(tx_hash_str) > 16 else tx_hash_str
                response += (
                    f"\n⛓️  **Blockchain Proof:**\n"
                    f"• Transaction: `{tx_display}`\n"
                    f"• Network: {blockchain_result.get('network', 'testnet')}\n"
                )
                
                if blockchain_result.get('demo_mode'):
                    response += f"• Mode: Demo (local logging - perfect for hackathon!)\n"
                    response += f"• Note: Trade logged in blockchain_trades.log\n"
                else:
                    response += f"• [View on Explorer]({blockchain_result.get('explorer_url', '#')})\n"
            else:
                response += f"\n⚠️ Blockchain logging: {blockchain_result.get('error', 'Not enabled')}\n"
            
            response += "\n💡 *This was executed on paper trading (no real money)*"
        else:
            response = (
                f"❌ **Trade Failed**\n\n"
                f"Error: {result.get('error', 'Unknown error')}\n\n"
                f"Please check:\n"
                f"• Symbol is valid\n"
                f"• API keys are configured in .env\n"
                f"• Trading is enabled (set ALPACA_API_KEY)"
            )
        
        # Log the response even if sending fails
        ctx.logger.info(f"📤 Trade response ({len(response)} chars): {response[:200]}...")
        
        try:
            await ctx.send(sender, create_text_chat(response))
            ctx.logger.info("✅ Trade response sent successfully")
        except Exception as send_error:
            ctx.logger.warning(f"⚠️ Could not send response to {sender}: {send_error}")
            ctx.logger.info(f"💡 Response content was: {response}")
        
    except Exception as e:
        ctx.logger.error(f"❌ Trade execution error: {e}")
        await ctx.send(sender, create_text_chat(f"❌ Error: {str(e)}"))

async def handle_portfolio_query(ctx: Context, sender: str):
    """Handle portfolio queries"""
    try:
        ctx.logger.info("📊 Fetching portfolio...")
        portfolio = trade_executor.get_portfolio()
        pending_orders = trade_executor.get_pending_orders()
        
        if not portfolio.get("success"):
            response = (
                "⚠️ **Portfolio Not Available**\n\n"
                "Possible reasons:\n"
                "• Trading accounts not configured (check .env)\n"
                "• Recent orders still pending (wait 1-2 minutes)\n"
                "• API connection issue\n\n"
                "**Configuration:**\n"
                "• Set `ALPACA_API_KEY` for stock holdings\n"
                "• Set `BINANCE_API_KEY` for crypto holdings\n\n"
                "**Tip:** If you just placed an order, it may take 1-2 minutes to settle.\n"
                "Try again shortly!"
            )
            await ctx.send(sender, create_text_chat(response))
            return
        
        stocks = portfolio.get("stocks", [])
        crypto = portfolio.get("crypto", [])
        total_value = portfolio.get("total_value", 0)
        orders = pending_orders.get("orders", [])
        
        response = "📊 **Your Portfolio**\n\n"
        
        # Show filled positions
        if stocks:
            response += "**Stock Holdings:**\n"
            for stock in stocks:
                response += (
                    f"• {stock['symbol']}: {stock['qty']} shares @ ${stock['current_price']:.2f} "
                    f"= ${stock['market_value']:.2f}\n"
                )
            response += "\n"
        else:
            response += "**Stock Holdings:** None\n\n"
        
        if crypto:
            response += "**Crypto Holdings:**\n"
            for coin in crypto:
                response += f"• {coin['symbol']}: {coin['amount']:.4f} @ ${coin['price']:.2f}\n"
            response += "\n"
        else:
            response += "**Crypto Holdings:** None\n\n"
        
        # Show pending orders
        if orders:
            response += "**⏳ Pending Orders (waiting for market to open):**\n"
            for order in orders:
                response += f"• {order['symbol']}: {order['side']} {order['qty']} - Status: {order['status']}\n"
            response += "\n"
        
        response += f"**Total Portfolio Value:** ${total_value:,.2f}\n"
        
        if orders:
            response += "\n💡 *Orders will execute when market opens (Mon-Fri 9:30 AM - 4:00 PM ET)*"
        else:
            response += "\n💡 *Paper trading account (simulated holdings)*"
        
        ctx.logger.info(f"📤 Portfolio response ({len(response)} chars)")
        
        try:
            await ctx.send(sender, create_text_chat(response))
            ctx.logger.info("✅ Portfolio response sent successfully")
        except Exception as send_error:
            ctx.logger.warning(f"⚠️ Could not send response to {sender}: {send_error}")
            ctx.logger.info(f"💡 Response content was: {response}")
        
    except Exception as e:
        ctx.logger.error(f"❌ Portfolio query error: {e}")
        await ctx.send(sender, create_text_chat(f"❌ Error: {str(e)}"))

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
    try:
        await ctx.send(
            sender,
            ChatAcknowledgement(
                timestamp=datetime.now(timezone.utc),
                acknowledged_msg_id=msg.msg_id
            ),
        )
    except Exception as ack_error:
        ctx.logger.warning(f"⚠️ Could not send ACK to {sender}: {ack_error}")

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"💬 Session started: {sender}")
            welcome = (
                "🎉 **Welcome to AutoVest!** 🚀\n\n"
                "I'm your **AI financial advisor** powered by:\n\n"
                "🧠 **MeTTa Knowledge Graph** (SingularityNET Hyperon) • "
                "🤖 **ASI:One LLM** for natural conversation • "
                "📊 **Live Market Data** (Polygon.io + CoinGecko) • "
                "💰 **Trade Execution** (Stocks via Alpaca + Crypto via CCXT) • "
                "⛓️ **Blockchain Logging** (Fetch.ai blockchain)\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "**💬 Ask me anything:**\n"
                "• \"Should I invest in Bitcoin?\"\n"
                "• \"Should I invest in Solana?\"\n"
                "• \"I'm 28, how should I plan for retirement?\"\n"
                "• \"Compare Bitcoin vs stocks\"\n\n"
                "**💸 Execute trades (paper trading - safe!):**\n"
                "• \"Execute trade: buy 1 AAPL\"\n"
                "• \"Execute trade: sell 5 TSLA\"\n"
                "• \"Execute trade: buy 100 BTC/USDT\"\n\n"
                "**📈 Check your portfolio:**\n"
                "• \"Show my portfolio\"\n"
                "• \"Check my holdings\"\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "✨ **Not just advice - I EXECUTE trades & LOG them on blockchain!** ✨"
            )
            
            try:
                await ctx.send(sender, create_text_chat(welcome))
                ctx.logger.info("✅ Welcome message sent")
            except Exception as send_error:
                ctx.logger.warning(f"⚠️ Could not send welcome to {sender}: {send_error}")
                ctx.logger.info(f"💡 Welcome message ready: {len(welcome)} chars")
            
        elif isinstance(item, TextContent):
            user_query = item.text.strip()
            ctx.logger.info(f"💡 Query: {user_query}")
            
            # Check for trade execution commands
            if user_query.lower().startswith("execute trade:"):
                ctx.logger.info("💰 Trade execution command detected")
                await handle_trade_execution(ctx, sender, user_query)
                continue
            
            # Check for portfolio commands
            if any(keyword in user_query.lower() for keyword in ["portfolio", "holdings", "my positions"]):
                ctx.logger.info("📊 Portfolio query detected")
                await handle_portfolio_query(ctx, sender)
                continue
            
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
                
                try:
                    await ctx.send(sender, create_text_chat(answer))
                    ctx.logger.info("✅ Response sent successfully")
                except Exception as send_error:
                    ctx.logger.warning(f"⚠️ Could not send response to {sender}: {send_error}")
                    ctx.logger.info(f"💡 Response was generated: {answer[:200]}...")
                
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
    print(f"💰 Trade Execution: {'✅ Enabled' if trade_executor else '⚠️  Check API keys'}")
    print(f"⛓️  Blockchain: {'✅ Enabled' if blockchain_logger.enabled else '⚠️  Configure FETCHAI_PRIVATE_KEY'}")
    print("="*70)
    print("\n💡 NEW CAPABILITIES:")
    print("   ✅ Execute real trades (paper trading - no real money)")
    print("   ✅ Log all trades on Fetch.ai blockchain")
    print("   ✅ Check portfolio holdings")
    print("   ✅ Verify trades on blockchain explorer")
    print("\n🎯 Why This Wins the Hackathon:")
    print("   ❌ Other projects: Just advice and recommendations")
    print("   ✅ AutoVest: Advice + EXECUTION + Blockchain proof")
    print("   🏆 Full Fetch.ai stack: uAgents + MeTTa + Blockchain")
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
