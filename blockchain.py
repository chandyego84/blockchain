import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()
        
        # create the genesis block
        self.NewBlock(proof=100, previousHash=1)
    
    def NewBlock(self, proof, previousHash=None):
        """
        Creates a new block and adds it to the chain
        :param proof: <int> The proof given by Proof of Work algorithm
        :param previousHash: (Optional) <str> Hash of previous block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previousHash': previousHash or self.Hash(self.chain[-1])
        }

        # by this point, block PoW has been done, so the block is validated and secured
        # reset the current list of transactions
        self.currentTransactions = []

        self.chain.append(block)
        return block


    def NewTransaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined BLock
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this
        """ 

        self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.LastBlock['index'] + 1
    
    def ProofOfWork(self, lastProof):
        """
        Simple PoW algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes,
        where p is the previous proof
        - p is the previous proof
        - p' is the new proof
        :param lastProof: <int>
        :return: <int>
        """

        proof = 0
        while self.ValidProof(lastProof, proof) is False:
            proof += 1
        
        return proof
    
    def RegisterNode(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node, e.g., 'http://192.168.0.5:5000'
        :return: None
        """    

        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)
    
    def ValidChain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> a blockchain
        :return: <bool> True if valid, otherwise False
        """
        pass        
    
    @staticmethod
    def ValidProof(lastProof, proof):
        """
        Validates the proof: Does hash(lastProof, proof) contain 4 leading zeroes?
        :param lastProof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False if not
        """

        guess = f'{lastProof}{proof}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()
        return guessHash[:4] == "0000"
        

    @staticmethod
    def Hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <str>
        """
        # dictionary must be ordered or will have inconsistent hashes
        blockString = json.dumps(block, sort_keys=True).encode() # encoded string in UTF-8
        return hashlib.sha256(blockString).hexdigest() # encoded with sha256

    @property
    def LastBlock(self):
        # returns the last block in the chain
        return self.chain[-1]
    
# Instantiate our Node
app = Flask(__name__)

# Generate globally unique address for this node
nodeIdentifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def Mine():
    """
    Calculates PoW
    Rewards the miner by adding a transaction granting 1 coin
    Forge the new Block by adding it to the chain
    """
    
    # Run PoW algorithm to get next proof
    lastBlock = blockchain.LastBlock
    lastProof = lastBlock['proof']
    proof = blockchain.ProofOfWork(lastProof)

    # Receive reward for finding the proof
    # Sender is "0" to signify that this node has mined a new coin
    blockchain.NewTransaction(
        sender="0",
        recipient=nodeIdentifier,
        amount = 1,
    )

    # Forge the new Block by adding it to the chain
    previousHash = blockchain.Hash(lastBlock)
    block = blockchain.NewBlock(proof, previousHash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous hash': block['previousHash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def NewTransaction():
    values = request.get_json()

    # Check that the required fields are in POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(r in values for r in required):
        return 'Missing Values', 400
    
    # Create a new transaction
    index = blockchain.NewTransaction(values['sender'], 
        values['recipient'], values['amount'])
    
    response = {'message': f"Transaction will be added to Block {index}"}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def FullChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)