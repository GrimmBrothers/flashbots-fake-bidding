import requests
import json
from brownie import network


def get_txs():
    endpoint = "https://api-goerli.etherscan.io//api?module=account" \
               "&action=txlist" \
               f"&fromBlock={from_block}" \
               f"&toBlock={last_block}" \
               f"&address={contract_address}" \
               f"&apikey=7T3I2Y1YYWFFSYWD1JZQURCGE422S1PFP2"

    return json.loads(requests.get(endpoint).text)['result']

def get_internals():
    endpoint = "https://api-goerli.etherscan.io//api?module=account" \
               "&action=txlistinternal" \
               f"&fromBlock={from_block}" \
               f"&toBlock={last_block}" \
               f"&address={contract_address}" \
               f"&apikey=7T3I2Y1YYWFFSYWD1JZQURCGE422S1PFP2"

    return json.loads(requests.get(endpoint).text)['result']

apikey = "EQG3K86V1N9WHW7RCCGU1UGCGI1TQU7KZW"
network.connect('goerli')

contract_address = "0x87D8B355b2a2dc16bD3846063c074Ca3e4378064"
last_block = network.web3.eth.get_block_number()
from_block = 7357537

random_address ="0xa3b60a4Ca2DA8DE87301A77919Ba8335697940ED".lower()
non_random_address ="0xdC0b174902D5C8b9d260F5B3528673E12826E127".lower()

transactions = get_txs()
internal = get_internals()

tx_hashes = [tx['hash'] for tx in internal]
number_random_wins = 0
number_random_lose = 0
number_non_random = 0

for transaction in transactions:
    if transaction['from']==random_address:
        if transaction['hash'] in tx_hashes:
                number_random_lose+=1
        else:
            if transaction['methodId']=='0x5ec01e4d':
                number_random_wins+=1
    else:
        number_non_random+=1

total = number_random_wins + number_random_lose +number_non_random
print(f"Number random wins and wins {number_random_wins} and ratio {number_random_wins/total}")

print(f"Number random wins and lose {number_random_lose} and ration {number_random_lose/total}")

print(f"Number non random wins {number_non_random} and ratio {number_non_random/total}")

