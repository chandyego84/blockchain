import hashlib
from hashlib import sha256
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse

class Block(object):
    def __init__(self, index, transactions, prevHash, timestamp, nonce, difficulty):
        ''''
        :param index: <int> Index of block in the chain.
        :param transactions: <List> The transactions stored in the block.
        :param prevHash: <str> SHA256-encrypted hash of previous block in the chain.
        :param timestamp: <int> Time this block was generated, expressed in seconds since the epoch.
        :param difficulty: <int> Mining difficulty to generate this block.
        '''
        self.index = index
        self.transactions = transactions
        self.prevHash = prevHash
        # used in the mining process
        self.timestamp = timestamp # time when this block was generated
        self.nonce = nonce # nonce to solve this block
        self.difficulty = difficulty # PoW difficulty to generate this block
        self.hash = Block.Hash(self)

    @staticmethod
    def Hash(block):
        '''
        Creates hash for a block using the new block's timestamp and nonce, and previous hash.
        :param block: <Block>
        :return: <str> Hash of new block.
        '''
        # calculate block's hash using the timestamp, nonce,
        # and the previous hash
        encodedString = (f"{block.timestamp} + {block.nonce} + {block.prevHash}").encode('utf-8')
        
        return sha256(encodedString).hexdigest()

class Blockchain(object):
    def __init__(self):
        '''
        :attr chain: <List> Valid Blocks.
        :attr currentTransactions: <List> Current transactions to be stored in next block mined.
        '''
        self.chain = []
        self.currentTransactions = []
        self.currentDifficulty = 1

        # create genesis block and add to the chain
        self.AddBlock(nonceProof=100, miningDifficulty=1, prevHash=0)
    
    def AddBlock(self, nonceProof, miningDifficulty, prevHash=None):
        '''
        Creates a new block and adds it to the chain.
        :param prevHash: <int> Hash of previous block.
        :param nonceProof: <int> Nonce found to solve for this block.
        :param miningDifficulty: <int> Difficulty to produce this block.
        :return: <Block> The new block added to the chain.
        '''

        NewBlock = Block(
            index = len(self.chain),
            transactions = self.currentTransactions,
            prevHash = prevHash,
            timestamp = time(),
            nonce = nonceProof,
            difficulty = miningDifficulty
        )

        # block stored unvalidated transactions
        # reset current transactions
        self.currentTransactions = []

        self.chain.append(NewBlock)

        return NewBlock

    def NewTransaction(self, sender, recipient, amount):
        '''
        Creates a new transaction to be stored in the next mined block.
        :param sender: <str> Sender of transaction
        :param recipient: <str> Recipient of transaction
        :param amount: <float> Amount being sent
        :return: <int> Index of the block to store the transaction
        '''

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.currentTransactions.append(transaction)

        return self.LastBlock.index + 1
    
    def Mine(self):
        '''
        Mines for a new block by going through PoW process.
        Adds mined block to the chain.
        '''

        # Proof of Work
        previousHash = int(self.LastBlock.hash, 16) # convert to <int> for PoW calculations 
        target = 2**(256 - self.currentDifficulty)

        nonceSolution = self.ProofOfWork(previousHash, target)

        # Reward miner for finding proof
        self.NewTransaction(
                sender="0", 
                recipient="Chandy's Computer", 
                amount=1
            )

        # Add block to the chain
        self.AddBlock(nonceSolution, self.currentDifficulty, prevHash=previousHash)

        return

    # Proof of Work
    def ProofOfWork(self, prevHash, target):
        '''
        Proof of Work algorithm to solve for the hash.
        :param prevHash: <int> Previous hash in the chain.
        :return: <int> The nonce that solves the proof.
        '''

        nonce = 0

        while self.ValidProof(prevHash, nonce, target) is False:
            nonce += 1

        return nonce
    
    def GetChain(self):
        for block in self.chain:
            print(f"Block {block.index} Transactions: {block.transactions}")

        print(f"Length of Chain: {len(self.chain)}")

    @staticmethod
    def ValidProof(prevHash, nonce, target):
        '''
        Checks to see if a proof is valid (prevHash and nonce generate correct hash).
        :param prevHash: <int> Previous hash in the chain.
        :param nonce: <int> Nonce--potential solution to the proof.
        :param target: <int> Number that the proof must be equal to or less than.
        :return: True if hash is solved for, False otherwise.
        '''
        
        guessNum = prevHash * nonce
        guessString = f"{guessNum}".encode()
        guessHash = sha256(guessString).hexdigest()

        return int(guessHash, 16) <= target

    @property
    def LastBlock(self):
        # returns last block in the chain
        return self.chain[-1]

# init a blockchain
blockchain = Blockchain()

blockchain.NewTransaction(sender="Audra", recipient="Chandler", amount="69")
blockchain.Mine()
blockchain.GetChain()