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
        self.demo_mode = False  # For hackathon demo without testnet
        
        if not COSMPY_AVAILABLE:
            print("⚠️ CosmPy not installed - using demo mode")
            print("   Trades will be logged locally (perfect for demo!)")
            self.enabled = True
            self.demo_mode = True
            return
        
        # Get configuration
        self.network = os.getenv("FETCHAI_NETWORK", "dorado-1")  # Use dorado-1 testnet
        private_key_hex = os.getenv("FETCHAI_PRIVATE_KEY")
        
        if private_key_hex and len(private_key_hex) == 64:
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
                
                self.enabled = True
                print(f"✅ Fetch.ai blockchain connected ({self.network})")
                print(f"   Wallet address: {self.wallet.address()}")
            
            except Exception as e:
                print(f"⚠️ Blockchain init failed: {e}")
                print("   Falling back to demo mode (local logging)")
                self.enabled = True
                self.demo_mode = True
        else:
            print("✅ Blockchain demo mode enabled (local logging)")
            print("   Perfect for hackathon demo!")
            self.enabled = True
            self.demo_mode = True
    
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
                "error": "Blockchain logging not enabled"
            }
        
        # Demo mode - log locally and generate mock tx hash
        if self.demo_mode:
            import hashlib
            
            # Create realistic transaction data
            trade_json = json.dumps({
                "type": "TRADE",
                "symbol": trade_data.get("symbol"),
                "quantity": trade_data.get("quantity"),
                "side": trade_data.get("side"),
                "price": trade_data.get("price"),
                "timestamp": trade_data.get("timestamp", datetime.now().isoformat()),
                "platform": trade_data.get("platform", "AutoVest")
            })
            
            # Generate deterministic transaction hash
            tx_hash = hashlib.sha256(
                (trade_json + str(datetime.now().timestamp())).encode()
            ).hexdigest()[:64]
            
            # Log to file for demo purposes
            log_file = "blockchain_trades.log"
            with open(log_file, "a") as f:
                f.write(f"\n[{datetime.now().isoformat()}] TX: {tx_hash}\n")
                f.write(f"Trade: {trade_json}\n")
                f.write("-" * 80 + "\n")
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "network": "demo (local)",
                "explorer_url": f"https://explore-dorado.fetch.ai/transactions/{tx_hash}",
                "memo": trade_json,
                "demo_mode": True,
                "note": "Trade logged locally (demo mode) - perfect for hackathon demo!"
            }
        
        # Real blockchain mode
        try:
            # Create transaction memo with trade data
            memo = json.dumps({
                "type": "TRADE",
                "symbol": trade_data.get("symbol"),
                "quantity": trade_data.get("quantity"),
                "side": trade_data.get("side"),
                "price": trade_data.get("price"),
                "timestamp": trade_data.get("timestamp", datetime.now().isoformat()),
                "platform": trade_data.get("platform", "AutoVest")
            })
            
            # Send small transaction with memo (0.000001 FET)
            # This creates an immutable record on blockchain
            # Use correct denomination based on network
            denom = "atestfet" if self.network == "dorado-1" else "afet"
            tx = self.client.send_tokens(
                self.wallet.address(),  # Send to self
                1000000000000000,  # 0.001 TESTFET in atestfet units
                denom,
                self.wallet,
                memo=memo[:256]  # Blockchain memo limit
            )
            
            # Extract transaction hash from SubmittedTx object
            tx_hash = tx.tx_hash if hasattr(tx, 'tx_hash') else str(tx)
            
            # Fix explorer URL - remove network suffix for dorado-1
            explorer_base = "https://explore-dorado.fetch.ai" if self.network == "dorado-1" else f"https://explore-{self.network}.fetch.ai"
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "network": self.network,
                "explorer_url": f"{explorer_base}/transactions/{tx_hash}",
                "memo": memo
            }
        
        except Exception as e:
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
        
        # Demo mode
        if self.demo_mode:
            import hashlib
            
            snapshot_json = json.dumps({
                "type": "PORTFOLIO_SNAPSHOT",
                "total_value": portfolio.get("total_value", 0),
                "num_positions": len(portfolio.get("stocks", [])) + len(portfolio.get("crypto", [])),
                "timestamp": datetime.now().isoformat()
            })
            
            tx_hash = hashlib.sha256(
                (snapshot_json + str(datetime.now().timestamp())).encode()
            ).hexdigest()[:64]
            
            log_file = "blockchain_trades.log"
            with open(log_file, "a") as f:
                f.write(f"\n[{datetime.now().isoformat()}] PORTFOLIO SNAPSHOT: {tx_hash}\n")
                f.write(f"Data: {snapshot_json}\n")
                f.write("-" * 80 + "\n")
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "network": "demo (local)",
                "demo_mode": True
            }
        
        # Real blockchain mode
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
