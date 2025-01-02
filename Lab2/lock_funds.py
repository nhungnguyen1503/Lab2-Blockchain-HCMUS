from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.keys import HDKey

# Step 1: Read keys from bitcoin_keys.txt
with open("bitcoin_keys.txt", "r") as f:
    lines = f.readlines()
    private_key_hex = lines[1].split(": ")[1].strip()
    public_key_hex = lines[2].split(": ")[1].strip()
    bitcoin_address = lines[3].split(": ")[1].strip()


# Step 2: Check balance
service = Service(network='testnet')

try:
    balance_satoshis = service.getbalance(bitcoin_address)  # Get balance in satoshis
    balance_tbtc = balance_satoshis / 1e8  # Convert satoshis to tBTC

    print(f"Balance for address {bitcoin_address}: {balance_tbtc:.8f} tBTC")

    if balance_tbtc == 0:
        print("No funds detected. Please send testnet BTC to this address and try again.")
        exit()
    else:
        print("Funds detected! Proceeding to create a transaction.")
except Exception as e:
    print(f"Error retrieving balance: {e}")
    exit()

# Step 3: Create a transaction
try:
    # Retrieve unspent transaction outputs (UTXOs)
    utxos = service.getutxos(bitcoin_address)
    print(f"UTXOs for address {bitcoin_address}: {utxos}")

    if not utxos:
        print("No UTXOs available to spend.")
        exit()

    # Use the first UTXO for simplicity
    utxo = utxos[0]
    txid = utxo['txid']  # Transaction ID of the UTXO
    output_index = utxo['output_n']  # Use 'output_n' for the output index
    amount_satoshis = utxo['value']  # Amount in satoshis

    if not txid or output_index is None or amount_satoshis <= 0:
        print("Invalid UTXO format or insufficient funds.")
        exit()

    print(f"Using UTXO: {txid} (index {output_index}, amount {amount_satoshis} satoshis)")

    # Define the destination address and amount to send
    destination_address = "mzNNG7GcVwe3AcZzH22bCQudSTiyLV4CVA"  # Example address, replace as needed
    amount_to_send = amount_satoshis - 1000  # Subtract 1000 satoshis for transaction fee

    if amount_to_send <= 0:
        print("Insufficient funds for transaction fee.")
        exit()

    # Create transaction inputs and outputs
    tx_input = Input(txid, output_index, bitcoin_address)
    tx_output = Output(amount_to_send, destination_address)

    # Create and sign the transaction
    tx = Transaction(network='testnet')
    tx.add_input(tx_input)
    tx.add_output(tx_output)
    
    # Use existing private key to sign the transaction
    tx.sign([HDKey(private_key_hex)])

    # Broadcast the transaction
    try:
        tx_id = service.sendrawtransaction(tx.as_hex())
        print(f"Transaction successfully broadcasted! TXID: {tx_id}")
    except Exception as e:
        print(f"Error broadcasting transaction: {e}")

except Exception as e:
    print(f"Error creating or broadcasting transaction: {e}")
