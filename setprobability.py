from relay_test_functions import load_contract, change_network
from brownie import accounts, network

my = accounts.load('key12')

change_network('goerli')
w3 = network.web3

contract_address = "0x87D8B355b2a2dc16bD3846063c074Ca3e4378064"

contract, w3_contract = load_contract(w3, contract_address)

contract.setProbability(2, 1, {'from': my})
