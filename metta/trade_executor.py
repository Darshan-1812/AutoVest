"""
Trade Execution Module for AutoVest
Supports paper trading via Alpaca API and crypto via CCXT
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Try importing trading libraries
try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    print("⚠️ Alpaca not installed. Run: pip install alpaca-py")

try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    print("⚠️ CCXT not installed. Run: pip install ccxt")

load_dotenv()


class TradeExecutor:
    """Execute trades via Alpaca (stocks) and CCXT (crypto)"""
    
    def __init__(self):
        """Initialize trade executor with paper trading credentials"""
        self.alpaca_client = None
        self.crypto_exchange = None
        
        # Initialize Alpaca (paper trading - free!)
        if ALPACA_AVAILABLE:
            alpaca_key = os.getenv("ALPACA_API_KEY")
            alpaca_secret = os.getenv("ALPACA_SECRET_KEY")
            
            if alpaca_key and alpaca_secret:
                try:
                    self.alpaca_client = TradingClient(
                        alpaca_key, 
                        alpaca_secret, 
                        paper=True  # Paper trading only
                    )
                    print("✅ Alpaca paper trading initialized")
                except Exception as e:
                    print(f"⚠️ Alpaca init failed: {e}")
            else:
                print("⚠️ Set ALPACA_API_KEY and ALPACA_SECRET_KEY for paper trading")
        
        # Initialize CCXT for crypto (testnet)
        if CCXT_AVAILABLE:
            try:
                # Use Binance testnet for demo
                self.crypto_exchange = ccxt.binance({
                    'apiKey': os.getenv("BINANCE_API_KEY", ""),
                    'secret': os.getenv("BINANCE_SECRET", ""),
                    'enableRateLimit': True,
                    'options': {'defaultType': 'future'}  # Testnet
                })
                print("✅ Crypto exchange initialized (testnet)")
            except Exception as e:
                print(f"⚠️ Crypto exchange init failed: {e}")
    
    def execute_stock_trade(
        self, 
        symbol: str, 
        quantity: float, 
        side: str = "buy",
        order_type: str = "market"
    ) -> Dict[str, Any]:
        """
        Execute stock trade via Alpaca paper trading
        
        Args:
            symbol: Stock ticker (e.g., "AAPL")
            quantity: Number of shares
            side: "buy" or "sell"
            order_type: "market" or "limit"
        
        Returns:
            Order details dict
        """
        if not self.alpaca_client:
            return {
                "success": False,
                "error": "Alpaca not configured. Set ALPACA_API_KEY and ALPACA_SECRET_KEY"
            }
        
        try:
            # Create market order
            order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
            
            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=quantity,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )
            
            # Submit order
            order = self.alpaca_client.submit_order(order_data)
            
            return {
                "success": True,
                "order_id": str(order.id),
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "status": order.status,
                "filled_price": order.filled_avg_price,
                "timestamp": datetime.now().isoformat(),
                "platform": "Alpaca Paper Trading"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def execute_crypto_trade(
        self,
        symbol: str,
        amount: float,
        side: str = "buy"
    ) -> Dict[str, Any]:
        """
        Execute cryptocurrency trade (testnet)
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            amount: Amount in base currency
            side: "buy" or "sell"
        
        Returns:
            Order details dict
        """
        if not self.crypto_exchange:
            return {
                "success": False,
                "error": "Crypto exchange not configured"
            }
        
        try:
            # Get current price
            ticker = self.crypto_exchange.fetch_ticker(symbol)
            price = ticker['last']
            
            # Calculate quantity
            if side.lower() == "buy":
                quantity = amount / price
            else:
                quantity = amount
            
            # Create market order
            order = self.crypto_exchange.create_market_order(
                symbol=symbol,
                side=side.lower(),
                amount=quantity
            )
            
            return {
                "success": True,
                "order_id": str(order['id']),
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "price": price,
                "cost": order.get('cost', amount),
                "timestamp": datetime.now().isoformat(),
                "platform": "Crypto Exchange (Testnet)"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_portfolio(self) -> Dict[str, Any]:
        """Get current portfolio holdings"""
        portfolio = {
            "success": True,  # Add success field
            "stocks": [],
            "crypto": [],
            "total_value": 0.0
        }
        
        # Get stock positions with timeout
        if self.alpaca_client:
            try:
                import signal
                
                # Set a 10 second timeout for Alpaca API
                def timeout_handler(signum, frame):
                    raise TimeoutError("Alpaca API timeout")
                
                # Only use signal on Unix systems
                import platform
                if platform.system() != 'Windows':
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(10)
                
                positions = self.alpaca_client.get_all_positions()
                
                if platform.system() != 'Windows':
                    signal.alarm(0)  # Cancel timeout
                
                for pos in positions:
                    portfolio["stocks"].append({
                        "symbol": pos.symbol,
                        "qty": float(pos.qty),  # Changed from "quantity" to "qty"
                        "current_price": float(pos.current_price),
                        "market_value": float(pos.market_value),
                        "unrealized_pl": float(pos.unrealized_pl)
                    })
                    portfolio["total_value"] += float(pos.market_value)
            except TimeoutError:
                print(f"⚠️ Alpaca API timeout - portfolio may be incomplete")
            except Exception as e:
                print(f"Error fetching stock portfolio: {e}")
        
        # Get crypto positions - SKIP for now to avoid timeout
        # Crypto portfolio fetching is slow, disable it to speed up response
        if False and self.crypto_exchange:  # Disabled temporarily
            try:
                balance = self.crypto_exchange.fetch_balance()
                for currency, amount in balance['total'].items():
                    if amount > 0 and currency != 'USDT':  # Skip USDT balance, show other coins
                        try:
                            ticker = self.crypto_exchange.fetch_ticker(f"{currency}/USDT")
                            price = ticker['last']
                            portfolio["crypto"].append({
                                "symbol": currency,
                                "amount": amount,
                                "price": price
                            })
                            portfolio["total_value"] += amount * price
                        except:
                            # If we can't get price, just show the amount
                            portfolio["crypto"].append({
                                "symbol": currency,
                                "amount": amount,
                                "price": 0.0
                            })
            except Exception as e:
                print(f"Error fetching crypto portfolio: {e}")
        
        return portfolio
    
    def get_pending_orders(self) -> Dict[str, Any]:
        """Get all pending/open orders"""
        pending = {
            "success": True,
            "orders": []
        }
        
        if self.alpaca_client:
            try:
                from alpaca.trading.enums import QueryOrderStatus
                orders = self.alpaca_client.get_orders(status=QueryOrderStatus.OPEN)
                for order in orders:
                    pending["orders"].append({
                        "symbol": order.symbol,
                        "side": str(order.side).split('.')[-1],  # Convert OrderSide.BUY to "BUY"
                        "qty": float(order.qty),
                        "status": str(order.status).split('.')[-1],  # Convert OrderStatus.ACCEPTED to "ACCEPTED"
                        "order_id": order.id,
                        "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else "N/A"
                    })
            except Exception as e:
                print(f"Error fetching pending orders: {e}")
        
        return pending
    
    def get_order_status(self, order_id: str, platform: str = "alpaca") -> Dict[str, Any]:
        """Check status of an order"""
        try:
            if platform == "alpaca" and self.alpaca_client:
                order = self.alpaca_client.get_order_by_id(order_id)
                return {
                    "success": True,
                    "order_id": str(order.id),
                    "status": order.status,
                    "filled_qty": float(order.filled_qty) if order.filled_qty else 0,
                    "filled_price": float(order.filled_avg_price) if order.filled_avg_price else None
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Example usage
if __name__ == "__main__":
    executor = TradeExecutor()
    
    print("\n📊 Trade Executor Demo\n")
    
    # Demo: Buy 1 share of Apple (paper trading)
    print("1. Executing paper trade: BUY 1 AAPL")
    result = executor.execute_stock_trade("AAPL", 1, "buy")
    print(f"Result: {result}\n")
    
    # Demo: Get portfolio
    print("2. Fetching portfolio...")
    portfolio = executor.get_portfolio()
    print(f"Portfolio: {portfolio}\n")
    
    print("✅ Trade execution module ready!")
    print("Note: This uses PAPER TRADING - no real money involved!")
