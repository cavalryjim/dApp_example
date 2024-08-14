from web3 import Web3
import json

# Connect to local Ethereum node (Ganache)
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connected
print(f"Connected to the local Ethereum (Ganche) network: {web3.is_connected()}")

# Set the default account (the first account Ganache provides)
web3.eth.default_account = web3.eth.accounts[0]

# ABI and Bytecode obtained from compiling the Solidity contract
with open('ABI', 'rb') as a:
    abi = json.loads(a.read())
with open('Bytecode') as b:
    bytecode = b.read()


# Deploy the contract
YachtRental = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = YachtRental.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

# Interact with the deployed contract
yacht_rental = web3.eth.contract(address=contract_address, abi=abi)

# Check the availability of the Yacht
availability = yacht_rental.functions.available().call()
print(f"Is the yacht available? {availability}")

# Obtain the daily rate and book the yacht for 2 days and send the appropriate amount of Ether
num_days = 2
daily_rate = yacht_rental.functions.ratePerDay().call()
total_cost = num_days * daily_rate

tx_hash = yacht_rental.functions.bookYacht(num_days).transact({'value': total_cost})
web3.eth.wait_for_transaction_receipt(tx_hash)

# Get the yacht's availability after booking
availability = yacht_rental.functions.available().call()
print(f"Is the yacht available after booking? {availability}")