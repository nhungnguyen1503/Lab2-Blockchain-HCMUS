from bitcoinlib.keys import HDKey
from bitcoinlib.wallets import wallet_create_or_open, WalletTransaction
from bitcoinlib.services.services import Service

# Generate two private keys (these could be generated from a mnemonic, hardware wallet, etc.)
private_key1 = HDKey('038d4f9af8f47a5d9bd299b211b00dc72db7af8919e1155aa3230d85540f9dcdcc', network='testnet', multisig=True)
private_key2 = HDKey('02cb72bb0aeb8a6be8467a82d47367021430bc96354afa16b1f7462574cbd9f44d', network='testnet', multisig=True)

# Generate the public keys for both participants
pubkey1 = private_key1.public_master_multisig()
pubkey2 = private_key2.public_master_multisig()

# Create multisig wallets for both participants
wallet1 = wallet_create_or_open('multisig_wallet1', sigs_required=2, keys=[private_key1, pubkey2], network='testnet')
wallet2 = wallet_create_or_open('multisig_wallet2', sigs_required=2, keys=[pubkey1, private_key2], network='testnet')

wallet1.utxos_update()
wallet2.utxos_update()
# Create a transaction and send to a new address
# Specify the amount and destination address to send

t = wallet2.transaction_create([('tb1qmxsr7h0ln54wq4caqjs07cpql0fr7edyjmuptl', 10000)])
t.sign()
t2 = wallet1.transaction_import(t)
t2.sign()
print("%s == %s: %s" % (t.outputs[1].address, t2.outputs[1].address, t.outputs[1].address == t2.outputs[1].address))
print("Verified (True): ", t2.verify())

t2.send(broadcast=True)
t2.info()

#service = Service(network='testnet')
#txid = service.sendrawtransaction(t2.raw_hex())

# t.info()
# t2.info()

#print(txid)

# # Output the transaction info
# tx.info()

# Update UTXOs (Unspent Transaction Outputs) for both wallets
wallet1.utxos_update()
wallet2.utxos_update()

# Print the wallet addresses
print("Private Key 1:", private_key1)
print("Private Key 2:", private_key2)
print("Wallet 1 Address:", wallet1.get_key().address)
print("Wallet 2 Address:", wallet2.get_key().address)

# Print wallet details
wallet1.info()
wallet2.info()
