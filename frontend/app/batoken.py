from web3 import Web3

def retrieve_pocs(sender_address : str, contract_address : str, node_url : str, abi : str):
    # Create the node connection
    web3 = Web3(Web3.HTTPProvider(node_url))
    
    # Verify if the connection is successful
    if web3.isConnected():
        print("-" * 50)
        print("Connection Successful")
        print("-" * 50)
    else:
        print("Connection Failed")

    contract = web3.eth.contract(address=contract_address, abi=abi)
    pocs = contract.functions.readAll().call()

    print(pocs)
    return pocs