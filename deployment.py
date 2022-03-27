from solcx import compile_standard, install_solc
import json
from  web3 import Web3


with open("ContactList.sol", "r") as file:
    contact_list_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ContactList.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiler_output.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["evm"]["bytecode"]["object"]

# get abi
abi =compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["metadata"]["output"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" # leaving the private key like this is very insecure if you are working on real world project

# Create the contract in Python
ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)
# Submit the transaction that deploys the contract
transaction = ContactList.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
