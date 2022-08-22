from flashbots import flashbot
from brownie import accounts, network
from brownie_utils import change_network

my = accounts.load('key12')
my2 = accounts.load('key13')
flashbots_account = accounts.load('key14')
goerli = True

if goerli:
    change_network('goerli')
    w3 = network.web3
    flashbots_goerli = "https://relay-goerli.flashbots.net"
    flashbot(w3, flashbots_account, flashbots_goerli)

else:
    change_network('homeETH')
    w3 = network.web3
    flashbot(w3, flashbots_account)


def make_bundle():
    nonce = w3.eth.get_transaction_count(my.address)
    tx1 = {
        "to": my2.address,
        "value": w3.toWei(0.001, "ether"),
        "gas": 21000,
        "maxFeePerGas": w3.toWei(200, "gwei"),
        "maxPriorityFeePerGas": w3.toWei(50, "gwei"),
        "nonce": nonce,
        "chainId": w3.chain_id,
        "type": 2,
    }

    tx2 = {
        "to": my2.address,
        "value": w3.toWei(0.001, "ether"),
        "gas": 21000,
        "maxFeePerGas": w3.toWei(200, "gwei"),
        "maxPriorityFeePerGas": w3.toWei(50, "gwei"),
        "nonce": nonce + 1,
        "chainId": w3.chain_id,
        "type": 2,
    }

    tx1_signed = w3.eth.account.sign_transaction(tx1, my.private_key)
    tx2_signed = w3.eth.account.sign_transaction(tx2, my.private_key)

    return [
        {"signed_transaction": tx1_signed.rawTransaction},
        {"signed_transaction": tx2_signed.rawTransaction},
    ]


def main(bundle):
    # keep trying to send bundle until it gets mined
    while True:
        block = w3.eth.block_number
        print(f"Simulating on block {block}")
        # simulate bundle on current block
        try:

            print("Simulation successful.")
        except Exception as e:
            print("Simulation error", e)

        # send bundle targeting next block
        print(f"Sending bundle targeting block {block + 1}")
        send_result = w3.flashbots.send_bundle(bundle, target_block_number=block + 1)
        send_result.wait()
        try:
            receipts = send_result.receipts()
            print(f"\nBundle was mined in block {receipts[0].blockNumber}\a")
            break
        except:
            print(f"Bundle not found in block {block + 1}")


# get balance before bundle
print(f"Sender address: {my.address}")
print(f"Receiver address: {my2.address}")
print(f"Sender account balance: {w3.fromWei(my.balance(), 'ether')} ETH")
print(f"Receiver account balance: {w3.fromWei(my2.balance(), 'ether')} ETH")

# execute bundle
_bundle = make_bundle()
main(_bundle)

# get balance after bundle
print(f"Sender address: {my.address}")
print(f"Receiver address: {my2.address}")
print(f"Sender account balance: {w3.fromWei(my.balance(), 'ether')} ETH")
print(f"Receiver account balance: {w3.fromWei(my2.balance(), 'ether')} ETH")
