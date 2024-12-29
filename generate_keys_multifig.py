from bitcoinlib.keys import Key
from bitcoinlib.transactions import Script
from bitcoinlib.wallets import Address

# Generate two private keys (these could be generated from a mnemonic, hardware wallet, etc.)
private_key1 = Key()
private_key2 = Key()

# Get the public keys for both participants
pubkey1 = private_key1.public()
pubkey2 = private_key2.public()

keylist = [pubkey1, pubkey2]

# Create the multisig script: 2 <pubkey1> <pubkey2> 2 OP_CHECKMULTISIG
redeem_script = Script(keys=keylist, sigs_required=2, script_types=['multisig'])

# Create the address from the P2SH script hash
p2sh_address = Address(redeem_script.as_bytes(), script_type='p2sh')

print("Private Key 1:", private_key1)
print("Private Key 2:", private_key2)
print("Redeem Script:", redeem_script.as_hex())
print("Multisig Address:", p2sh_address.address)
