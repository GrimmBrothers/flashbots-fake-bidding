from flashbots import flashbot
import json
import time
from brownie import project, Contract
from brownie_utils import change_network

project.check_for_project('contract_part')
project.load('contract_part')
contract_part = project.ContractPartProject


def if_goerli(goerli):
    if goerli:
        change_network('goerli')

    else:
        change_network('homeETH')

    # load contract
    if goerli:
        contract_address = "0x87D8B355b2a2dc16bD3846063c074Ca3e4378064"
    else:
        contract_address = "0xA1066515A47B01496A0D3422695f2CEdce7F1aCf"

    return contract_address


def send_bundle(n, w3, bundle, flashbots_account, goerli):
    if goerli and n == 1:
        flashbots_goerli = "https://relay-goerli.flashbots.net"
        flashbot(w3, flashbots_account, flashbots_goerli)

    elif n == 1:
        flashbot(w3, flashbots_account)

    else:
        pass

    start_block = w3.eth.block_number
    # keep trying to send bundle until it gets mined
    while True:
        block = w3.eth.block_number
        print(f"Simulating on block {block}")
        # simulate bundle on current block
        try:
            w3.flashbots.simulate(bundle, block)
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
            set_winner(True)
            return receipts[0].blockNumber, True
        except:
            print(f"Bundle not found in block {block + 1}")
        if block > start_block + 20:
            print(f"\nBundle was not mined within 20 blocks.")
            set_winner(False)
            return block, False
        if check_winner():
            set_winner(False)
            print("Bundle lost!")
            return block, False,


def check_winner():
    with open("dump/win.json", "r") as f:
        win = json.load(f)['win']
    if win == 0:
        return True
    else:
        return False


def set_winner(winner):
    if winner:
        win = 0
    else:
        win = 1
    with open("dump/win.json", "w") as f:
        json.dump({'win': win}, f)


def make_bundle(w3, w3_contract, random, account, gas_price):
    nonce = w3.eth.getTransactionCount(account.address)

    if random:
        tx = w3_contract.functions.random().buildTransaction({
            "gas": 200000,
            "gasPrice": gas_price,
            "nonce": nonce
        })
    else:
        tx = w3_contract.functions.notRandom().buildTransaction({
            "gas": 200000,
            "gasPrice": gas_price,
            "nonce": nonce
        })

    tx_signed = w3.eth.account.sign_transaction(tx, account.private_key)

    return [{"signed_transaction": tx_signed.rawTransaction}]


def load_contract(w3, contract_address):
    contract = Contract.from_abi("FlashbotsBug", contract_address, contract_part.flasbhot_bug.abi)
    w3_contract = w3.eth.contract(address=contract_address, abi=contract_part.flasbhot_bug.abi)
    return contract, w3_contract


def write_start(start_dic):
    with open("dump/start.json", "w") as f:
        json.dump(start_dic, f)


def read_start():
    with open("dump/start.json", "r") as f:
        start_dic = json.load(f)
    return start_dic


def check_win(goerli, block, probability, pre_balance, post_balance, win):
    with open("dump/results.json", "r") as f:
        results = json.load(f)
    results[block] = {}
    if win and (pre_balance - post_balance < 0.0015 * 10 ** 18):
        results[block]['win'] = True
        print("Random bundle won!")
    elif win:
        results[block]['win'] = False
        results[block]['auction winner'] = True
    else:
        results[block]['win'] = False
        results[block]['auction winner'] = False
        print("Random bundle lost!")
    results[block]['goerli'] = goerli
    results[block]['probability'] = probability
    with open("dump/results.json", "w") as f:
        json.dump(results, f)


def wait_block(w3, n):
    _wait_block = w3.eth.block_number + n
    while _wait_block > w3.eth.block_number:
        time.sleep(12)


def init_wait():
    with open("dump/random_behind.json", "w") as f:
        json.dump({'behind': 0}, f)
    with open("dump/no_random_behind.json", "w") as f:
        json.dump({'behind': 0}, f)


def start_wait(random):
    if random:
        with open("dump/random_behind.json", "w") as f:
            json.dump({'behind': 0}, f)
    else:
        with open("dump/no_random_behind.json", "w") as f:
            json.dump({'behind': 0}, f)


def wait(random):
    if random:
        with open("dump/random_behind.json", "w") as f:
            json.dump({'behind': 1}, f)
    elif not random:
        with open("dump/no_random_behind.json", "w") as f:
            json.dump({'behind': 1}, f)
    waiting = True
    while waiting:
        if random:
            print("\nWaiting for no random!\n")
        elif not random:
            print("\nWaiting for random!\n")
        time.sleep(5)
        with open("dump/random_behind.json", "r") as f:
            random_behind = json.load(f)['behind']
        with open("dump/no_random_behind.json", "r") as f:
            no_random_behind = json.load(f)['behind']
        if random_behind == 1 and no_random_behind == 1:
            waiting = False
    print("Synced!")
    time.sleep(10)
    waiting = True
    while waiting:
        if random:
            start_wait(True)
        elif not random:
            start_wait(False)
        time.sleep(1)
        with open("dump/random_behind.json", "r") as f:
            random_behind = json.load(f)['behind']
        with open("dump/no_random_behind.json", "r") as f:
            no_random_behind = json.load(f)['behind']
        if random_behind == 0 and no_random_behind == 0:
            waiting = False
    print("Wait reset!")
