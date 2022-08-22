import time
from relay_test_functions import make_bundle, send_bundle, load_contract, if_goerli, read_start, wait
from brownie import accounts, network

my = accounts.load('key13')
flashbots_account = accounts.load('key17')

start_dic = read_start()
iterations = start_dic['iterations']
n = 1

while n < iterations:
    # wait for random to start
    stop = True
    while stop:
        time.sleep(0.1)
        start_dic = read_start()
        if start_dic['start'] == 1:
            stop = False

    goerli = start_dic['goerli']
    gas_price = start_dic['gas_price']

    if goerli is None or gas_price is None:
        raise ValueError('Goerli or gas price are not defined!')

    # if goerli function
    contract_address = if_goerli(goerli)
    w3 = network.web3

    # load contract
    contract, w3_contract = load_contract(w3, contract_address)

    # make bundle (random = True)
    bundle = make_bundle(w3, w3_contract, False, my, gas_price)

    # stop for wait
    wait(False)

    # send bundle
    send_bundle(n, w3, bundle, flashbots_account, goerli)

    # stop for wait
    wait(False)

    # increase n
    n = n + 1
