import web3
import base64

class BAToken:
    def __init__(self, contract_address : str, node_url : str, abi : str, private_keys: dict):
        self.w3 = web3.Web3(web3.Web3.HTTPProvider(node_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.private_keys = private_keys

    def retrieve_pocs(self):
        pocs = self.contract.functions.readAll().call()
        return pocs

    def mint(self, sender_address : str, value: int):
        transaction = self.contract.functions.mint().buildTransaction({
            "value":web3.Web3.toWei(value, 'ether'),
            "from":web3.Web3.toChecksumAddress(sender_address),
            "nonce":self.w3.eth.get_transaction_count(web3.Web3.toChecksumAddress(sender_address))
        })
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=self.private_keys[sender_address])
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    def publish(self, sender_address : str, poc : str, severity : int, cve : str, type : str, title : str, language : str):
        pocb64 = base64.b64encode(poc.encode('utf-8')).decode('utf-8')
        
        transaction = self.contract.functions.publish(pocb64, int(severity), cve, type, title, language).buildTransaction({
            "from":web3.Web3.toChecksumAddress(sender_address),
            "nonce":self.w3.eth.get_transaction_count(web3.Web3.toChecksumAddress(sender_address))
        })
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=self.private_keys[sender_address])
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    def verify(self, sender_address : str, pocID : int):
        transaction = self.contract.functions.verify(int(pocID)).buildTransaction({
            "from":web3.Web3.toChecksumAddress(sender_address),
            "nonce":self.w3.eth.get_transaction_count(web3.Web3.toChecksumAddress(sender_address))
        })
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=self.private_keys[sender_address])
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    def donate(self, sender_address : str, recipient: str, amount: int):
        transaction = self.contract.functions.donate(web3.Web3.toChecksumAddress(recipient), int(amount)).buildTransaction({
            "from":web3.Web3.toChecksumAddress(sender_address),
            "nonce":self.w3.eth.get_transaction_count(web3.Web3.toChecksumAddress(sender_address))
        })
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=self.private_keys[sender_address])
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)