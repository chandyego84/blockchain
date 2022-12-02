from hashlib import sha256

# PoW: how new blocks are created or mined on the blockchain. 
    # Goal: Discover a number which solves a problem. 
    # Number must be hard to find, easy to verify
    # Example:
    # hash (x * y) must end in 0. Fix x = 5, find y.

x = 5
y = 0   # don't know what y should be yet
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1

# solution is y = 21, since the produced hash ends in 0
print(f"The solution is y = {y}.")
print(f"Value of hash(x*y): {sha256(f'{x*y}'.encode()).hexdigest()}")
