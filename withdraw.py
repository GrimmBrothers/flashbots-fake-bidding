from relay_test_functions import load_contract, change_network
from brownie import accounts, network

my = accounts.load('key12')

change_network('goerli')
w3 = network.web3

contract_address = "0x1655430F892C80A669a66a5E759c96B63ff2F6F4"

contract, w3_contract = load_contract(w3, contract_address)

contract.withdraw({'from': my})