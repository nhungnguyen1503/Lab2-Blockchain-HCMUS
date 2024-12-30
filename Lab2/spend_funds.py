import requests
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key

# Read private key and address from bitcoin_keys.txt
with open("bitcoin_keys.txt", "r") as f:
    lines = f.readlines()
    private_key_hex = lines[1].split(": ")[1].strip()
    spender_address = lines[3].split(": ")[1].strip()

# Fixed recipient address
destination_address = "mxbwZYgL4csYS5MambXwWMotxyZ3MuBbBT"

# Fetch UTXOs for the spender's address from a testnet API
def fetch_utxos(address):
    url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching UTXOs: {response.status_code} - {response.text}")
        return []

# Display available UTXOs and allow user to choose one
def select_utxo(utxos):
    print("Available UTXOs:")
    for i, utxo in enumerate(utxos):
        print(f"{i}: txid={utxo['txid']}, vout={utxo['vout']}, value={utxo['value']} satoshis")
    while True:
        try:
            index = int(input("Select a UTXO by its index: ").strip())
            if 0 <= index < len(utxos):
                return utxos[index]
            else:
                raise ValueError("Invalid index")
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

# Fetch and display UTXOs
utxos = fetch_utxos(spender_address)
if not utxos:
    print("No UTXOs available. Please ensure the address is funded.")
    exit()

selected_utxo = select_utxo(utxos)

# Prompt for amount to send
while True:
    try:
        amount = int(input(f"Enter the amount to send in satoshis (UTXO value: {selected_utxo['value']}): ").strip())
        if 0 < amount <= selected_utxo['value']:
            break
        else:
            raise ValueError("Amount must be positive and less than or equal to the UTXO value.")
    except ValueError as e:
        print(f"Invalid input: {e}")

# Prompt for the transaction fee
while True:
    try:
        fee = int(input("Enter the transaction fee in satoshis: ").strip())
        if fee > 0:
            break
        else:
            raise ValueError("Fee must be a positive number.")
    except ValueError as e:
        print(f"Invalid input: {e}")

# Create and broadcast the transaction
try:
    private_key = Key(import_key=private_key_hex)

    # Create the transaction
    tx = Transaction(network='testnet')
    tx.add_input(selected_utxo['txid'], selected_utxo['vout'])  # Add the selected UTXO as input
    tx.add_output(destination_address, amount)  # Add the recipient as output
    tx.fee = fee  # Set the transaction fee

    # Sign the transaction
    tx.sign(private_key)

    # Broadcast the transaction
    result = tx.broadcast()
    print(f"Transaction successfully broadcast. Result: {result}")
except Exception as e:
    print(f"Error creating or broadcasting transaction: {e}")

