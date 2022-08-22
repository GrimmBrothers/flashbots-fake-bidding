import time
from brownie import network
from eth_account.account import Account
from eth_account.signers.local import LocalAccount


# change network functions
def change_network(name):
    if network.is_connected():
        network.disconnect()
    while not network.is_connected():
        try:
            network.connect(name)
        except Exception as e:
            print("Unable to connect, trying again.", e)
            time.sleep(5)
