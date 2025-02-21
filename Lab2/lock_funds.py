from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service

# Read the Bitcoin address from bitcoin_keys.txt
with open("bitcoin_keys.txt", "r") as f:
    lines = f.readlines()
    address = lines[3].split(": ")[1].strip()  # Extract Bitcoin Address

# Initialize a connection to the testnet
service = Service(network='testnet')

# Check balance
try:
    balance = service.getbalance(address)
    print(f"Balance for address {address}: {balance} satoshis")

    if balance == 0:
        print("No funds detected. Please send testnet BTC to this address and try again.")
    else:
        print("Funds detected! You can proceed with spending transactions.")
except Exception as e:
    print(f"Error retrieving balance: {e}")
