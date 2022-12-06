from hashlib import sha256
import random
import numpy as np
from time import perf_counter

# Expected avg. of hashes to get proof:
# 1 / probability
# binary: 2^n
# hex: 16^n
# where n is number of leading zeroes (difficulty)
numHashes1 = 16**1
numHashes2 = 16**2
print(f"When using hexadecimals, avg. number of hashes to solve a proof increases by factor of 16 with each leading zero in the target.")
print(f"We can calculate the avg. number of hashes using (1/probability) or (16^n) where n is number of leading zeroes.")
probability1 = (16**63)/(16**64)
probability2 = (16**62)/(16**64)
print(f"Probability with one leading zeroes:{probability1}")
print(f"Probability with two leading zeroes:{probability2}")
print(f"Avg. number of hashes with one leading zeroes (16^1): {numHashes1}")
print(f"Avg. number of hashes with two leading zeroes(16^2): {numHashes2}")
print(f"Avg. number with one leading zeroes using probability method: {1/probability1}")
print(f"Avg. number with two leading zeroes using probability method: {1/probability2}")
print(f"Number of hashes with two leading zeroes is greater than one leading zero is: {numHashes2 / numHashes1} ")
print("------------------------------------------")

# used to generate a "previous hash"
def RandomHash():
    randomBits = random.getrandbits(256)
    randomHash = sha256(str(randomBits).encode()).hexdigest()

    return randomHash

# Valid PoW: checks if proof (nonce) found hash <= target
def ValidProof(lastHash, nonce, difficulty):
    guessString = f"{lastHash}{nonce}".encode()
    guessHash = sha256(guessString).hexdigest()

    return guessHash[:difficulty] == '0' * difficulty

def PoW(lastHash, difficulty):
    nonce = 0

    timeStart = perf_counter()
    while (ValidProof(lastHash, nonce, difficulty) is False):
        nonce += 1
    timeEnd = perf_counter()

    hashFound = sha256(f'{lastHash}{nonce}'.encode()).hexdigest()
    elapsedTime = timeEnd - timeStart
    
    return nonce, hashFound, elapsedTime

if __name__ == '__main__':

    # difficulty of 0 == 0 leading bits
        # of 1 == 1 leading bit
    maxDifficulty = 5

    for difficulty in range(maxDifficulty):
        expectedAvgHashes = 16 ** difficulty
        print("------------------------------------------")
        print(f"Difficulty: {difficulty}")
        print(f"Probability of finding valid hash: {(16**(64-difficulty))/(16**64)}")
        print(f"Expected avg. of hashes: {expectedAvgHashes}.")

        # generate a fake prev hash
        prevHash = RandomHash()
        # solve for current hash
        hashesCount, hashFound, elapsedTime = PoW(prevHash, difficulty)
        print(f"Hash Found: {hashFound}")
        print(f"Number of hashes done: {hashesCount}")
        print(f"Elapsed Time: {elapsedTime}")
        print("------------------------------------------")