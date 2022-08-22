import time

from relay_test_functions import make_bundle, init_wait, wait, wait_block, send_bundle, load_contract, \
    if_goerli, write_start, check_win, set_winner
from brownie import accounts, network

my = accounts.load('key12')
flashbots_account = accounts.load('key16')
goerli = False
change = False
iterations = 100
n = 1
probability = 1 / 2
my_balance = 0.1
init_wait()
set_winner(False)
while n < iterations and my_balance > 0.01:
    # initiate start_dic
    write_start({'start': 0, 'iterations': int(iterations)})

    # if goerli function
    contract_address = if_goerli(goerli)
    w3 = network.web3

    # load contract
    contract, w3_contract = load_contract(w3, contract_address)

    # transfer ether to contract
    if contract.balance() < 0.003 * 10 ** 18:
        my.transfer(contract, "0.003 ether")

    # set change
    if change:
        contract.changeVariable({'from': my, 'required_confs': 0})

    # pause to avoid nonce errors
    wait_block(w3, 3)
    print(w3.eth.getTransactionCount(my.address))

    # set gas price
    gas_price = w3.eth.gas_price
    while gas_price > 6*10**9:
        print("Gas price too high!")
        time.sleep(12)
        gas_price = w3.eth.gas_price

    # write start_dic values
    write_start({'start': 1, 'gas_price': int(gas_price), 'goerli': bool(goerli), 'iterations': int(iterations)})

    # make bundle (random = True)
    bundle = make_bundle(w3, w3_contract, True, my, gas_price)

    # get pre balance
    pre_balance = contract.balance()

    # wait for both to catch up
    set_winner(False)
    wait(True)
    write_start({'start': 0})

    # send bundle
    block, win = send_bundle(n, w3, bundle, flashbots_account, goerli)

    # wait for both to catch up
    wait(True)

    post_balance = contract.balance()
    print(pre_balance, post_balance)

    # check win
    check_win(goerli, block, probability, pre_balance, post_balance, win)

    # increase n
    n = n + 1

    # get balance
    my_balance = my.balance()

    #reset change
    change = True
