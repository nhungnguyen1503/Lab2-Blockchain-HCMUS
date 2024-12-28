from bitcoinlib.keys import Key

# Generate a random private key
private_key = Key(network='testnet').private_hex

# Create a Key object from the private key
key = Key(import_key=private_key, network='testnet')

# Derive the public key and Bitcoin address
public_key = key.public_hex
address = key.address()  # Correctly invoke the address method

# Save results to a text file
output = f"""
Private Key (hex): {private_key}
Public Key (hex): {public_key}
Bitcoin Address: {address}
"""

# Specify the file name
file_name = "bitcoin_keys.txt"

# Write the output to the file
with open(file_name, "w") as file:
    file.write(output)

print("Keys have been generated and saved to 'bitcoin_keys.txt'.")
