from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key

# Read private key and address from bitcoin_keys.txt
with open("bitcoin_keys.txt", "r") as f:
    lines = f.readlines()
    private_key_hex = lines[1].split(": ")[1].strip()
    address = lines[3].split(": ")[1].strip()

# Example UTXO details (replace with actual values)
txid = "your_utxo_txid_here"  # Transaction ID
vout = 0  # Output index of the UTXO
destination_address = "recipient_address_here"  # Replace with recipient's address
amount = 10000  # Amount to send in satoshis
fee = 1000  # Fee in satoshis

# Create Key object
private_key = Key(import_key=private_key_hex)

# Create and sign the transaction
tx = Transaction.create([{'txid': txid, 'vout': vout}], [(destination_address, amount)], fee=fee)
tx.sign(private_key)

# Broadcast the transaction
broadcast_result = tx.broadcast()
print(f"Broadcast result: {broadcast_result}")
