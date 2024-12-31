from bitcoinlib.wallets import Wallet
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key

# Define recipient address and amount to send
recipient_address = "tb1qlj64u6fqutr0xue85kl55fx0gt4m4urun25p7q"
amount_to_send = 0.0001  # Amount in BTC (adjust as needed)

# Read the Bitcoin private key and address from the file
try:
    with open("bitcoin_keys.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        private_key = lines[0].split(":")[1].strip()
        sender_address = lines[2].split(":")[1].strip()
except FileNotFoundError:
    print("Error: bitcoin_keys.txt not found.")
    exit(1)
except IndexError:
    print("Error: bitcoin_keys.txt is malformed.")
    exit(1)

print(f"Sender Address: {sender_address}")
print(f"Recipient Address: {recipient_address}")

try:
    # Initialize the wallet with the sender's address
    wallet = Wallet.create(sender_address, keys=private_key, network='testnet')
    
    # Fetch UTXOs from the wallet
    utxos = wallet.utxos()
    if not utxos:
        print("No UTXOs available for this address. Please fund it and try again.")
        exit(1)

    print(f"UTXOs: {utxos}")

    # Select the first UTXO
    selected_utxo = utxos[0]
    utxo_txid = selected_utxo['txid']
    utxo_vout = selected_utxo['output_n']
    utxo_amount = selected_utxo['value'] / 1e8  # Convert satoshis to BTC

    print(f"Selected UTXO: TXID={utxo_txid}, VOUT={utxo_vout}, Amount={utxo_amount} BTC")

    # Calculate fees and change
    fee_satoshis = 1000  # Adjust fee if needed
    amount_satoshis = int(amount_to_send * 1e8)
    change_satoshis = int(utxo_amount * 1e8 - amount_satoshis - fee_satoshis)

    if change_satoshis < 0:
        print("Error: Insufficient funds to cover amount and fees.")
        exit(1)

    # Create transaction inputs and outputs
    inputs = [{"txid": utxo_txid, "vout": utxo_vout, "value": int(utxo_amount * 1e8)}]
    outputs = [
        {"address": recipient_address, "value": amount_satoshis},
        {"address": sender_address, "value": change_satoshis},  # Send change back to sender
    ]

    # Create and sign the transaction
    key = Key(import_key=private_key, network="testnet")
    tx = Transaction(inputs=inputs, outputs=outputs, network="testnet", witness_type="taproot")
    tx.sign([key])  # Sign with the private key

    # Broadcast the transaction
    txid = tx.send()
    print("Transaction successfully created and broadcasted.")
    print(f"Transaction ID: {txid}")

except Exception as e:
    print(f"Error: {e}")
