import requests

# Read the Bitcoin address from bitcoin_keys.txt
with open("bitcoin_keys.txt", "r") as f:
    lines = f.readlines()
    address = lines[3].split(": ")[1].strip()  # Extract Bitcoin Address

# List of possible testnet faucet API endpoints
FAUCET_API_LIST = [
    "https://faucet.blockstream.com/api/v1/send",  # Blockstream Testnet Faucet
    "https://testnet-faucet.com/send",  # Replace with verified faucet
    "https://another-working-faucet.com/api"  # Replace with a working faucet
]

# Amount to request (in satoshis)
amount_satoshis = 100000  # 0.001 tBTC

def request_funds_from_faucet(address, amount):
    for api in FAUCET_API_LIST:
        try:
            payload = {"address": address, "amount": amount}
            print(f"Requesting {amount / 1e8:.8f} tBTC to address {address} from {api}...")

            # Send POST request to the faucet
            response = requests.post(api, json=payload)

            # Handle response
            if response.status_code == 200:
                txid = response.json().get("txid")
                print(f"Funds successfully sent to {address} from {api}. Transaction ID: {txid}")
                return  # Exit after successful request
            else:
                print(f"Failed to request funds from {api}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error while requesting funds from {api}: {e}")

    print("All faucet endpoints failed. Please try again later or check your connection.")

# Attempt to lock funds to the provided address
print(f"Attempting to lock funds to address {address}...")
request_funds_from_faucet(address, amount_satoshis)