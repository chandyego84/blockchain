import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid64
from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.currentTransactions = []
    
    # create the genesis block
    self.NewBlock(previousHash=1, proof=100)
    
    def NewBlock(self, proof, previousHash=None):
        """
        Creates a new block and ads it to the chain
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

        return self.last_block['index'] + 1
    
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
        blockString = json.dumps(block, sort_keys=True).encode() # encoded string
        return hashlib.sha256(block_string).hexdigest() # encoded with sha256

    @property
    def LastBlock(self):
        # returns the last block in the chain
        return self.chain[-1]


