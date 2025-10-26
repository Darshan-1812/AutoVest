#!/usr/bin/env python
"""Generate Fetch.ai wallet for blockchain logging"""

from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.aerial.wallet import LocalWallet

# Generate wallet
private_key = PrivateKey()
wallet = LocalWallet(private_key)

# Extract credentials
address = str(wallet.address())
# The private key is already a hex string
if hasattr(private_key, '_private_key'):
    if hasattr(private_key._private_key, 'hex'):
        private_key_hex = private_key._private_key.hex()
    else:
        private_key_hex = str(private_key._private_key)
else:
    # Try direct conversion
    import ed25519
    private_key_hex = private_key.hex() if hasattr(private_key, 'hex') else str(private_key)

print("\n" + "="*70)
print("✅ FETCH.AI WALLET GENERATED - DORADO TESTNET")
print("="*70)
print(f"\n📍 Wallet Address:")
print(f"   {address}")
print(f"\n🔑 Private Key (KEEP SECRET!):")
print(f"   {private_key_hex}")
print("\n" + "="*70)
print("📝 ADD TO .env FILE:")
print("="*70)
print(f"\nFETCHAI_NETWORK=dorado-1")
print(f"FETCHAI_PRIVATE_KEY={private_key_hex}")
print("\n" + "="*70)
print("🚰 GET TESTNET TOKENS:")
print("="*70)
print(f"\n1. Copy your address: {address}")
print(f"\n2. Visit: https://explore-dorado.fetch.ai/")
print(f"   OR: https://faucet-dorado.fetch.ai/")
print(f"\n3. Look for 'Faucet' button or 'Request Tokens'")
print(f"\n4. Paste your address and request tokens")
print(f"\n5. Wait 1-2 minutes for tokens to arrive")
print("\n" + "="*70)
print("✅ Once tokens arrive, restart agent_clean.py!")
print("="*70 + "\n")

# Auto-update .env if user confirms
import os
if os.path.exists('.env'):
    response = input("Would you like to automatically add this to .env? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        with open('.env', 'a') as f:
            f.write(f"\n# Fetch.ai Blockchain Integration - Dorado Testnet\n")
            f.write(f"FETCHAI_NETWORK=dorado-1\n")
            f.write(f"FETCHAI_PRIVATE_KEY={private_key_hex}\n")
        print("\n✅ Added to .env file!")
    else:
        print("\n📝 Please manually add the lines above to your .env file")
else:
    print("\n⚠️  .env file not found - please add manually")
