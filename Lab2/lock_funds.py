from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction, Output, Input
from bitcoinlib.services.services import Service

def lock_funds(source_file, destination_file, amount):
    """Lock funds by creating a transaction."""
    try:
        # Determine wallet name based on source file
        if source_file == "bitcoin_keys.txt":
            wallet_name = "Wallet 1"
        elif source_file == "bitcoin_keys2.txt":
            wallet_name = "Wallet 2"
        else:
            raise ValueError("Invalid source file selected.")

        # Read source wallet details
        with open(source_file, "r") as f:
            lines = f.readlines()
            private_key = lines[1].split(": ")[1].strip()
            source_address = lines[3].split(": ")[1].strip()

        # Validate private key and derived address
        key = Key(import_key=private_key, network='testnet')
        derived_address = key.address()
        if derived_address != source_address:
            print("Warning: Derived address does not match the source address in the file.")
        print(f"Debug: Source Address - {source_address}, Derived Address - {derived_address}")

        # Read destination address
        with open(destination_file, "r") as f:
            destination_address = f.readlines()[3].split(": ")[1].strip()
        print(f"Debug: Destination Address - {destination_address}")

        # Fetch UTXOs for the source address
        service = Service(network='testnet')
        utxos = service.getutxos(source_address)
        if not utxos:
            raise Exception(f"No UTXOs available for address {source_address}.")
        print(f"Debug: UTXOs for {source_address} - {utxos}")

        # Prepare transaction
        tx = Transaction(network='testnet')
        total_input_value = 0

        # Add UTXOs as inputs and calculate total input value
        for utxo in utxos:
            tx.add_input(utxo['txid'], utxo['output_n'], utxo['value'], key)
            total_input_value += utxo['value']
            if total_input_value >= amount * 1e8:
                break

        if total_input_value < amount * 1e8:
            raise Exception("Insufficient funds to create the transaction.")

        # Add the destination output
        tx.add_output(Output(destination_address, int(amount * 1e8), network='testnet'))

        # Add a change output if necessary
        change_value = total_input_value - int(amount * 1e8) - tx.estimate_fee()
        if change_value > 0:
            tx.add_output(Output(source_address, change_value, network='testnet'))

        # Sign the transaction
        tx.sign(key)
        print("Debug: Transaction successfully signed.")

        # Broadcast the transaction
        txid = tx.broadcast()
        print(f"Transaction successfully broadcasted. TXID: {txid}")

    except Exception as e:
        print(f"Error locking funds: {e}")

def main():
    print("Choose a source wallet:")
    print("1. Wallet 1")
    print("2. Wallet 2")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        source_file = "bitcoin_keys.txt"
        destination_file = "bitcoin_keys2.txt"
    elif choice == "2":
        source_file = "bitcoin_keys2.txt"
        destination_file = "bitcoin_keys.txt"
    else:
        print("Invalid choice. Please choose 1 or 2.")
        return

    try:
        amount = float(input("Enter the amount to lock (in BTC): ").strip())
        lock_funds(source_file, destination_file, amount)
    except ValueError:
        print("Invalid amount entered. Please enter a numeric value.")

if __name__ == "__main__":
    main()
