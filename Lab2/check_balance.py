from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service

def get_address_from_file(file_name):
    """Extract the Bitcoin address from the given file."""
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            address = lines[3].split(": ")[1].strip()  # Extract Bitcoin Address
            return address
    except Exception as e:
        print(f"Error reading address from {file_name}: {e}")
        return None

def main():
    print("Choose a wallet to check the balance:")
    print("1. Wallet 1")
    print("2. Wallet 2")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        file_name = "bitcoin_keys.txt"
    elif choice == "2":
        file_name = "bitcoin_keys2.txt"
    else:
        print("Invalid choice. Please choose 1 or 2.")
        return

    # Get the Bitcoin address from the chosen file
    address = get_address_from_file(file_name)

    if not address:
        print("Failed to retrieve the Bitcoin address.")
        return

    print(f"Checking balance for address: {address}")

    # Initialize a connection to the testnet
    service = Service(network='testnet')

    # Check balance
    try:
        balance_satoshis = service.getbalance(address)  # Get balance in satoshis
        balance_tbtc = balance_satoshis / 1e8  # Convert satoshis to tBTC

        print(f"Balance for address {address}: {balance_tbtc:.8f} tBTC")

        utxos = service.getutxos(address)
        print(f"UTXOs for {address}: {utxos}")


        if balance_tbtc == 0:
            print("No funds detected. Please send testnet BTC to this address and try again.")
        else:
            print("Funds detected! You can proceed with spending transactions.")
    except Exception as e:
        print(f"Error retrieving balance: {e}")

if __name__ == "__main__":
    main()
