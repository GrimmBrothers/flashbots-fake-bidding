from brownie import network, accounts, project

project.check_for_project('contract_part')
project.load('contract_part')
contract_part = project.ContractPartProject

network.connect('goerli')

my = accounts.load('key12')

contract = contract_part.flasbhot_bug

contract.deploy(2, 1, {'from': my})
