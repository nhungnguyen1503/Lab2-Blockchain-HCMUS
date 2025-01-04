from bitcoinlib.keys import HDKey
from bitcoinlib.wallets import Address, wallet_create_or_open

private_key_receive = HDKey('03bb640e0f26e9c3555b7a52a74b89d5ff2b81a37fce43b8ca6224f1aa8ebfa042', network='testnet')
wallet_name_receive = 'wallet_1_receive'
wallet_receive = wallet_create_or_open(wallet_name_receive, private_key_receive, network='testnet')

print("Private Key Receive:", private_key_receive)
wallet_receive.info()