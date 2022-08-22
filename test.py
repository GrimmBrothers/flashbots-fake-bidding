from brownie import network, accounts, project, Contract
import threading
import time
import sys

project.check_for_project('contract_part')
project.load('contract_part')
contract_part = project.ContractPartProject


def transaction_random():
    print("sending tx1")
    contract.random({'from': my, 'value': 3 * 10 ** 15, 'required_confs': 0, 'allow_revert': True})

    print("------")


def transaction_not_random():
    print("sending tx2")
    contract.notRandom({'from': my2, 'value': 10 ** 15, 'required_confs': 0, 'allow_revert': True})

    print("-------")


network.connect('Flashbots')
web3 = network.web3
my = accounts.add('privatekey1')
my2 = accounts.add("privatekey2")
balance = my.balance()
# my.transfer(my2.address,int(balance/3))
contract_address = "0x6Be499A2d675Acfa54797433a5244E2CA865f273"
contract = Contract.from_abi("FlashbotsBug", contract_address, contract_part.flasbhot_bug.abi)


def _main():
    network.disconnect()
    network.connect('Flasbhots')
    web3 = network.web3
    nonce1 = web3.eth.getTransactionCount(my.address)
    nonce2 = web3.eth.getTransactionCount(my2.address)

    change = True  # Or false
    if change:
        print("send transaction change variable")
        network.disconnect()
        network.connect('mainnet')
        contract.changeVariable({'from': my})
    network.disconnect()
    network.connect('Flasbhots')
    web3 = network.web3

    wait_random = threading.Thread(target=transaction_random)
    wait_norandom = threading.Thread(target=transaction_not_random)

    wait_random.start()
    wait_norandom.start()

    while True:
        _nonce1 = web3.eth.getTransactionCount(my.address)
        _nonce2 = web3.eth.getTransactionCount(my2.address)
        if _nonce1 == nonce1 + 2 or _nonce2 == nonce2 + 1:
            print("Killing threads.\n")
            sys.exit()
        time.sleep(3)


_main()
