from bitcoinlib.keys import Key
from bitcoinlib.wallets import wallet_create_or_open

# Function to generate and save wallet details and create a wallet
def generate_wallet(file_name, wallet_name):
    # Generate a random private key
    private_key = Key(network='testnet').private_hex

    print(f"Keys have been generated and saved to '{file_name}'.")
    print(f"Private Key: {private_key}")

    # Create or open a wallet using the generated private key
    wallet = wallet_create_or_open(wallet_name, keys=private_key, network='testnet')

    # Extract public key and address from the wallet
    public_key = wallet.public_master().wif
    address = wallet.addresslist()[0]

    # Save results to a text file
    output = f"""
    Private Key (hex): {private_key}
    Public Key (hex): {public_key}
    Bitcoin Address: {address}
    """
    with open(file_name, "w") as file:
        file.write(output)

    wallet.utxos_update()
    wallet.info()
    print(f"Wallet '{wallet_name}' created or opened and UTXOs updated.")

# Generate two wallets 
generate_wallet("bitcoin_keys.txt", "Wallet 1")
generate_wallet("bitcoin_keys2.txt", "Wallet 2")

print("Keys have been generated and saved to 'bitcoin_keys.txt' and 'bitcoin_keys2.txt'.")