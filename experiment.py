from hashlib import sha256
import random
import numpy as np

print("Mining difficulty doubles with each leading zero required. 2^256 possible values.")
 # (1 / probability) gives expected avg. of hashes for each proof
numHashes1 = 1 / ((2**255) / (2**256))
numHashes2 = 1 / ((2**254) / (2**256))
print(f"Avg. number of hashes with one leading zeroes: {numHashes1}")
print(f"Avg. number of hashes with two leading zeroes: {numHashes2}")
print(f"Number of hashes with two leading zeroes is greater than one leading zero is: {numHashes2 / numHashes1} ")
print("------------------------------------------")
leadingZeroes = 4
target = 2**(256 - leadingZeroes)
expectedAvgHashes = 2**256 / (target)
print(f"Finding a nonce with {leadingZeroes} leading zeroe/s...")
print(f"i.e., get a value below the target {target}.")
print(f"Probability of finding valid hash: {target/(2**256)}")
print(f"Expected avg. of hashes: {expectedAvgHashes}.")

# used to generate a "previous hash"
def RandomHash():
    randomBits = random.getrandbits(256)
    randomHash = sha256(str(randomBits).encode()).hexdigest()

    return int(randomHash, 16)

# Valid PoW: checks if proof (nonce) found hash <= target
def ValidProof(lastHash, nonce):
    guessNum = lastHash * nonce
    guessString = f"{guessNum}".encode()
    guessHash = sha256(guessString).hexdigest()

    return int(guessHash, 16) <= target

def PoW(lastHash):
    nonce = 0

    while (ValidProof(lastHash, nonce) is False):
        nonce += 1

    #print(f"Solved hash: {sha256(f'{lastHash + nonce}'.encode()).hexdigest()}")

    return nonce


allHashes = np.zeros(1000, dtype=int)

# simulate one PoW done
def IndividualHash():
    prevHash = RandomHash() # generate random hash as input for PoW
    solvedHash = PoW(prevHash) # solve for proof

    return solvedHash

""""
:param numProofs: <int> number of proofs to be solved
:return: <int> Avg. number of hashes to find valid proof
"""
def RunNumerousHashes(numProofs):
    sumHashes = 0
    for r in range(numProofs):
        hashes = IndividualHash() # calculate one PoW
        allHashes[r] = hashes # add num of hashes to solve that proof to list
        sumHashes += hashes
    
    return sumHashes / numProofs

RunNumerousHashes(1000)
print("BASIC STATS:")
print(f"Min. hashes: {allHashes.min()}")
print(f"Max. hashes: {allHashes.max()}")
print(f"Avg. hashes: {allHashes.mean()}")