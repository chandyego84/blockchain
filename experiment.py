from hashlib import sha256

# PoW: how new blocks are created or mined on the blockchain. 
    # Goal: Discover a number which solves a problem. 
    # Number must be hard to find, easy to verify
    # Example:
    # hash (x * y) must end in 0. Fix x = 5, find y.

x = 5   # base (previous hash)
y = 0   # don't know what y should be yet (nonce)
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0": # keep hashing
    y += 1

# solution is y = 21, since the produced hash ends in 0
print(f"The solution is y = {y}.")
# sha256() 
# :param: byte string
# :return: hash object that can be digested into hex format using hexdigest()
print(f"Value of hash(x*y): {sha256(f'{x*y}'.encode()).hexdigest()}")
print("------------------------------------------")
# expected value: 1/probability of being below target
print("Mining difficulty doubles with each leading zero required. 2^256 possible values.")
numHashes1 = 2**256 / (2**225 + 1)
numHashes2 = 2**256 / (2**224 + 1)
numHashes3 = 2**256 / (16)
print(f"Target with one leading zeroes: {numHashes1}")
print(f"Target with two leading zeroes: {numHashes2}")
print(f"Two leading zeroes using 2^256/16 since only 16 possibe values with two leading zeroes: {numHashes3}")
print(f"Number of hashes with two leading zeroes is greater than one leading zero is: {numHashes2 / numHashes1} ")
print("------------------------------------------")
print("Simpler example: 100 possible values (1-100).")
target1 = 100 / (25 + 1)
target2 = 100 / (50 + 1)
print(f"Target is 25: {target1}")
print(f"Target is 50: {target2}")
print(f"Number of hashes with two leading zeroes is greater than one leading zero is: {numHashes2 / numHashes1} ")
