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
        self.hash = Block.Hash(self) # hash of the block

    @staticmethod
    def Hash(block):
        '''
        Creates hash for a block using the new block's timestamp and nonce, and previous hash.
        :param block: <Block> The block whose hash will be made
        :return: <str> Hash of new block.
        '''

        # calculate block's hash using the timestamp, nonce,
        # and the previous hash
        encodedString = (f"{str(block.timestamp)} + {str(block.nonce)} + {block.prevHash}").encode('utf-8')
        
        return sha256(encodedString).hexdigest()
    
    @staticmethod
    def GetBlockInfo(block):
        print("---------------------------")
        print(f"Block {block.index}:")
        print(f"Transactions: {block.transactions}")
        print(f"Prev Hash: {block.prevHash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Nonce: {block.nonce}")
        print(f"Difficulty: {block.difficulty}")
        print(f"Hash: {block.hash}")
        print("---------------------------")
    

class Blockchain(object):
    def __init__(self):
        '''
        :attr chain: <List> Valid (mined) Blocks.
        :attr currentTransactions: <List> Current transactions to be stored in next block mined.
        :attr currentDifficulty: <int> Current difficulty of mining a new block on the chain.
        '''
        self.chain = []
        self.currentTransactions = []
        self.currentDifficulty = 4

        # create genesis block and add to the chain
        self.AddBlock(nonceProof=100, miningDifficulty=1, prevHash="0")
    
    def AddBlock(self, nonceProof, miningDifficulty, prevHash=None):
        '''
        Creates a new block and adds it to the chain.
        :param prevHash: <str> Hash of previous block.
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
        prevHash = self.LastBlock.hash
        target = 2**(256 - self.currentDifficulty)

        nonceSolution = self.ProofOfWork(prevHash, target)

        # Reward miner for finding proof
        self.NewTransaction(
                sender="0", 
                recipient="Chandy's Computer", 
                amount=1
            )

        # Add block to the chain
        self.AddBlock(nonceSolution, self.currentDifficulty, prevHash=prevHash)

        return

    # Proof of Work
    def ProofOfWork(self, prevHash, target):
        '''
        Proof of Work algorithm to solve for the hash.
        :param prevHash: <str> Previous hash in the chain.
        :return: <int> The nonce that solves the proof.
        '''

        nonce = 0

        while self.ValidProof(prevHash, nonce, target) is False:
            nonce += 1

        return nonce
    
    @staticmethod
    def ValidProof(prevHash, nonce, target):
        '''
        Checks to see if a proof is valid (prevHash and nonce generate correct hash).
        :param prevHash: <str> Previous hash in the chain.
        :param nonce: <int> Nonce--potential solution to the proof.
        :param target: <int> Number that the proof must be equal to or less than.
        :return: True if hash is solved for, False otherwise.
        '''
        
        prevHash = int(prevHash, 16) # convert to <int> for PoW calculations 
        guessNum = prevHash * nonce
        guessString = f"{guessNum}".encode()
        guessHash = sha256(guessString).hexdigest()

        return int(guessHash, 16) <= target
    
    @staticmethod
    def GetBlockChainInfo(chain):
        for block in chain.chain:
            Block.GetBlockInfo(block)

        print(f"Length of Chain: {len(chain.chain)}")


    @property
    def LastBlock(self):
        # returns last block in the chain
        return self.chain[-1]

# init a blockchain
blockchain = Blockchain()

blockchain.NewTransaction(sender="Audra", recipient="Chandler", amount="69")
blockchain.Mine()
blockchain.NewTransaction(sender="God", recipient="Chandler", amount="0.69")
blockchain.NewTransaction(sender="Chandler", recipient="Audra", amount="0.69")
blockchain.Mine()
Blockchain.GetBlockChainInfo(blockchain)