"""
Blockchain Integration for AutoVest
Logs trades and portfolio changes on Fetch.ai blockchain
"""

import os
import json
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Try importing Fetch.ai blockchain SDK
try:
    from cosmpy.aerial.client import LedgerClient, NetworkConfig
    from cosmpy.aerial.wallet import LocalWallet
    from cosmpy.crypto.keypairs import PrivateKey
    COSMPY_AVAILABLE = True
except ImportError:
    COSMPY_AVAILABLE = False
    print("⚠️ CosmPy not installed. Run: pip install cosmpy")

load_dotenv()


class BlockchainLogger:
    """Log financial transactions on Fetch.ai blockchain"""
    
    def __init__(self):
        """Initialize blockchain client"""
        self.client = None
        self.wallet = None
        self.enabled = False
        self.demo_mode = False  # Disable demo mode - we want REAL transactions
        
        if not COSMPY_AVAILABLE:
            print("❌ CosmPy not installed - blockchain logging disabled")
            print("   Install with: pip install cosmpy")
            return
        
        # Get configuration
        self.network = os.getenv("FETCHAI_NETWORK", "dorado-1")  # Use dorado-1 testnet
        private_key_hex = os.getenv("FETCHAI_PRIVATE_KEY")
        
        if not private_key_hex or len(private_key_hex) != 64:
            print("❌ FETCHAI_PRIVATE_KEY not configured in .env")
            print("   Run: python generate_wallet.py")
            print("   Then add private key to .env file")
            return
        
        try:
            # Initialize Fetch.ai client for Dorado testnet
            from cosmpy.aerial.client import NetworkConfig
            
            if self.network == "mainnet":
                cfg = NetworkConfig.fetchai_mainnet()
            elif self.network == "dorado-1":
                # Dorado testnet configuration
                cfg = NetworkConfig(
                    chain_id="dorado-1",
                    url="grpc+https://grpc-dorado.fetch.ai:443",
                    fee_minimum_gas_price=1000000000,
                    fee_denomination="atestfet",
                    staking_denomination="atestfet"
                )
            else:
                cfg = NetworkConfig.fetchai_testnet()
            
            self.client = LedgerClient(cfg)
            
            # Create wallet from private key
            private_key = PrivateKey(bytes.fromhex(private_key_hex))
            self.wallet = LocalWallet(private_key)
            
            # Test connection by querying balance
            balance = self.client.query_bank_balance(self.wallet.address())
            balance_testfet = balance / 1e18
            
            self.enabled = True
            print(f"✅ Fetch.ai blockchain connected ({self.network})")
            print(f"   Wallet address: {self.wallet.address()}")
            print(f"   Balance: {balance_testfet:.4f} TESTFET")
            
            if balance_testfet < 0.01:
                print(f"   ⚠️ Low balance! Get testnet tokens from: https://faucet-dorado.fetch.ai/")
        
        except Exception as e:
            print(f"❌ Blockchain connection failed: {e}")
            print("   Check:")
            print("   1. Private key is correct (64 hex chars)")
            print("   2. Network connection is working")
            print("   3. Fetch.ai testnet is online")
            self.enabled = False
            self.demo_mode = False
    
    def log_trade(
        self, 
        trade_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Log trade execution on blockchain
        
        Args:
            trade_data: Trade details (symbol, quantity, price, etc.)
        
        Returns:
            Transaction hash and status
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Blockchain logging not enabled - check credentials"
            }
        
        # Real blockchain mode ONLY
        try:
            # Create transaction memo with trade data
            memo = json.dumps({
                "type": "TRADE",
                "symbol": trade_data.get("symbol"),
                "quantity": trade_data.get("quantity"),
                "side": trade_data.get("side"),
                "price": trade_data.get("price"),
                "timestamp": trade_data.get("timestamp", datetime.now().isoformat()),
                "platform": trade_data.get("platform", "AutoVest"),
                "order_id": trade_data.get("order_id")
            })
            
            # Send small transaction with memo (0.001 FET)
            # This creates an immutable record on blockchain
            denom = "atestfet" if self.network == "dorado-1" else "afet"
            
            print(f"🔄 Creating blockchain transaction...")
            print(f"   Network: {self.network}")
            print(f"   From: {self.wallet.address()}")
            print(f"   Memo: {memo[:100]}...")
            
            tx = self.client.send_tokens(
                self.wallet.address(),  # Send to self
                1000000000000000,  # 0.001 TESTFET in atestfet units
                denom,
                self.wallet,
                memo=memo[:256]  # Blockchain memo limit
            )
            
            # Extract transaction hash from SubmittedTx object
            tx_hash = tx.tx_hash if hasattr(tx, 'tx_hash') else str(tx)
            
            # Build explorer URL
            explorer_base = "https://explore-dorado.fetch.ai"
            explorer_url = f"{explorer_base}/transactions/{tx_hash}"
            
            print(f"✅ Transaction created: {tx_hash}")
            print(f"   Explorer: {explorer_url}")
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "network": self.network,
                "explorer_url": explorer_url,
                "memo": memo,
                "demo_mode": False
            }
        
        except Exception as e:
            print(f"❌ Blockchain transaction failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def log_portfolio_snapshot(
        self, 
        portfolio: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Log portfolio snapshot on blockchain
        
        Args:
            portfolio: Portfolio holdings and values
        
        Returns:
            Transaction hash
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Blockchain logging not enabled"
            }
        
        # Real blockchain mode ONLY
        try:
            memo = json.dumps({
                "type": "PORTFOLIO_SNAPSHOT",
                "total_value": portfolio.get("total_value", 0),
                "num_positions": len(portfolio.get("stocks", [])) + len(portfolio.get("crypto", [])),
                "timestamp": datetime.now().isoformat()
            })
            
            denom = "atestfet" if self.network == "dorado-1" else "afet"
            tx = self.client.send_tokens(
                self.wallet.address(),
                1000000000000000,  # 0.001 TESTFET
                denom,
                self.wallet,
                memo=memo[:256]
            )
            
            # Extract transaction hash from SubmittedTx object
            tx_hash = tx.tx_hash if hasattr(tx, 'tx_hash') else str(tx)
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "network": self.network
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_balance(self) -> Dict[str, Any]:
        """Get FET token balance"""
        if not self.enabled:
            return {"balance": 0, "error": "Not enabled"}
        
        try:
            balance = self.client.query_bank_balance(
                self.wallet.address()
            )
            return {
                "balance": balance,
                "address": self.wallet.address(),
                "network": self.network
            }
        except Exception as e:
            return {"error": str(e)}
    
    def verify_trade_on_chain(self, tx_hash: str) -> Dict[str, Any]:
        """
        Verify a trade record exists on blockchain
        
        Args:
            tx_hash: Transaction hash to verify
        
        Returns:
            Transaction details if found
        """
        if not self.enabled:
            return {"success": False, "error": "Not enabled"}
        
        try:
            # Query transaction
            tx = self.client.query_tx(tx_hash)
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "height": tx.height,
                "memo": tx.tx.body.memo,
                "verified": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Example usage
if __name__ == "__main__":
    logger = BlockchainLogger()
    
    print("\n⛓️ Blockchain Logger Demo\n")
    
    if logger.enabled:
        # Demo: Log a sample trade
        print("1. Logging sample trade on blockchain...")
        trade = {
            "symbol": "AAPL",
            "quantity": 10,
            "side": "buy",
            "price": 175.50,
            "platform": "Alpaca Paper"
        }
        result = logger.log_trade(trade)
        print(f"Result: {result}\n")
        
        # Demo: Check balance
        print("2. Checking FET balance...")
        balance = logger.get_balance()
        print(f"Balance: {balance}\n")
    else:
        print("⚠️ Blockchain logging not enabled")
        print("To enable:")
        print("1. Get Fetch.ai testnet tokens: https://faucet-dorado.fetch.ai/")
        print("2. Set FETCHAI_PRIVATE_KEY in .env")
        print("3. Restart agent\n")
    
    print("✅ Blockchain integration module ready!")
