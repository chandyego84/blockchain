# Learning Blockchains by Building One

ChatGPT's Warning:
![GPTWarning](./assets/chatGptWarning.png)

<b>NOTE</b>: This is just a basic *demo*. It uses the MySQL which is NOT decentralized.

Major TODOs:
- Remove storage of data in database --> purely Nodes
- Distribution of blocks in node network
- Wallets in nodes
- Verification of transactions
- Limit supply of "coins"

Minor TODOs:
- Adjusting mining difficulty
- Using Merkel Tree for faster Block hash computation during mining
- Change proof of work difficulty to be determined from number of leading zeroes to actual Bitcoin protocol

For Fun:
- Prove that expected average of hashes to find a valid PoW is 1/probability using expected value in statistics.
Reference: [Mean or Expected Value and Std Deviation](https://openstax.org/books/statistics/pages/4-2-mean-or-expected-value-and-standard-deviation)

### Running the protocol
Currently, the app is not deployed. For now, you can play around with the current working version (0.1) on your local machine.  
```bash
git clone https://github.com/chandyego84/blockchain.git
source venv/bin/activate
python3 app.py
```

# Overview of Blockchains
According to Investopedia: A blockchain is a digital database or ledger that is distributed among the nodes of a peer-to-peer network. Blocks are closed and linked to previously filled block, forming a new chain of data known as a blockchain. All new information that follows that freshly added block is compiled into a newly formed block that will then also be added to the chain once filled. Different types of information can be stored on a blockchain, but the most common use is as a ledger for transactions.

### Difference Between Database and Blockchain
Database holds its data in tables, blockchain holds data in blocks that are strung together. This makes blokchcains irreversible.

### Transaction Process
![TransactionProcess](./assets/transactionProcess.png)

# Building the Blockchain

### Example of a Block
![ExampleBlock](./assets/blockExample.png)

### Blockchain API
There will be 3 methods:
1. /transactions/new to create a new transaction to a block
2. /mine to tell our server to mine a new block
3. /chain to return the full Blockchain
Example request for a transaction:
![ExampleTransaction](./assets/transactionExample.png)

# Proof of Work
The algorithm used to verify the transaction and create a new block in the blockchain. Bitcoin uses SHA-256 for hashing.
For this build:  
- Find a hash h with n (mining difficulty) leading zeroes such that h = pp'
- p = Hash of previous block in the chain
- p' = Nonce (solution to the problem)

To mimic the consensus validation more closely, we can adjust the difficulty of mining a block by adjusting the target value. More leading zeroes increases the mining difficulty while having less decreases it. A higher difficulty means more hashing is required for a valid proof of work. See chainwork calculation explained later. This [answer](https://www.quora.com/Why-is-difficulty-measured-in-hash-s-leading-zeroes) gives a good explanation for why leading zeroes is used. Note that in Bitcoin the difficulty is not the number of zeroes required; the difficulty is the minimum ratio between a well-defined maximum value, and the hash you got (when interpreted as a 256-bit unsigned integer).

#### Quick Demonstration on Proof of Work
experiment.py contains a basic demo of finding a hash in the described proof of work above up to a difficulty of 4 leading zeroes.

Run `python3 experiment.py`

### More Details on SHA256 Encryption
SHA256 returns a 256-bit number in hexadecimal form. Moreover, it will return a string of 64 characters, each of which is a hexadecimal digit (0-9 and a-f). This is a convenient way to represent the hash, as it can be easily stored and transmitted as a string of characters rather than a raw binary value.  

Why 64 characters?  
Each character in a hexadecimal representation represents 4 bits of information. Since SHA-256 produces a hash with 256 bits of information, it requires 64 hexadecimal digits to represent the full hash value. 

Why does each character represent 4 bits of information?  
Each character in a hexadecimal representation represents 4 bits of information because there are 16 possible values for each digit (0-9 and a-f), and 16 is equal to 2 to the power of 4 (16 = 2^4). Since each hexadecimal digit can represent 4 bits, it takes two digits to represent 8 bits (a byte), and 64 digits to represent the full 256-bit output of the SHA-256 hash function. Thus, a 64-character hexadecimal number would store 64 hexadecimal digits, which would represent 64 / 2 = 32 bytes of information. Each byte can represent a number from 0 to 255, so a 64-character hexadecimal number could represent a number in the range 0 to 255^32, which is a very large number.

# [Consensus](https://learnmeabitcoin.com/technical/longest-chain)
A conflict occurs when one node has a different chain to another node. Resolution is that the longest chain is authoritative. The "longest chain" refers to the blockchain that has taken the most ENERGY to build; this is not necessarily the same as the chain with the most blocks. To calculate chainwork, find how many hashes would be needed to be performed to mine each block in the chain and add them up. Average expected number of hashes for each block depends on what the [TARGET](https://learnmeabitcoin.com/technical/target) was at the time.

### Expected Avg. of Hashes to Find PoW
The expected average of hashes to find a valid proof-of-work (PoW) is 1 / probability because it represents the average number of attempts it takes to find a solution. If the probability of finding a solution in one attempt is p, then the probability of finding a solution in n attempts is (1-p)^(n-1) * p. The expected number of attempts is the sum of the probability of finding a solution on the nth attempt multiplied by n, for all possible values of n. This is concept of "expected value" in statistics.
```
E[X] = ∑ (n * (1-p)^(n-1) * p)
Where E[X] is the expected value of the number of attempts, X is the number of attempts, n is the number of attempts, p is the probability of finding a solution on the first attempt and (1-p)^(n-1) is the probability of not finding a solution in the first n-1 attempts

By solving the above equation we get :
E[X] = 1/p
``` 

#### Chainwork Calculation
To calculate the number of hashes to be performed on each block based on the target:
hashes = 2^256 / (target). When a hash is performed, the hash function spits out a 256-bit number.
To mine this block on the chain, this hash result must be below the target value for that particular height
on the chain. Thus, to find how many hashes are needed to be performed (worst-case) to get below this value, you divide the maximum range of numbers by the number you want to get below.

# Nodes
Currently only supporting full nodes.
- Full nodes: These nodes store the entire blockchain and validate all transactions and blocks. They are responsible for enforcing the consensus rules of the network. Full nodes are necessary for the security and integrity of the network, but they require a significant amount of storage space.

- Lightweight nodes (SPV): These nodes do not store the entire blockchain, instead, they rely on full nodes to provide them with the information they need. They only store the block headers and use a simplified payment verification (SPV) to validate transactions. Lightweight nodes are less secure than full nodes, but they require less storage space and are more suitable for resource-constrained devices.

- Archival nodes: These nodes store the entire blockchain, but they do not validate transactions, they only provide data to other nodes in the network. They act as a historical archive of the blockchain.

