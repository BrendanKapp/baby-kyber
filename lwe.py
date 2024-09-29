from dataclasses import dataclass
import numpy as np 
import random

@dataclass 
class PrivateKey:
    vector: np.ndarray
    mod: int 
    size: int

@dataclass 
class PublicKey:
    equations: np.ndarray
    mod: int
    size: int
    count: int

@dataclass 
class Message:
    equation: np.ndarray

def decrypt(private_key: PrivateKey, message: Message) -> bool:
    # plug in private values into the message equation
    value = 0
    for i in range(0, private_key.size):
        value += (message.equation[i] * private_key.vector[i])
    value = value % private_key.mod
    encrypted_value = message.equation[private_key.size]
    distance = abs(value - encrypted_value) % private_key.mod
    # compare distance to center to calculate bit value
    center = private_key.mod // 2
    lower_bound = center - (center // 2)
    upper_bound = center + (center // 2) 
    if distance > lower_bound and distance < upper_bound:
        return True
    else:
        return False

def encrypt(public_key: PublicKey, bit: bool) -> Message:
    # select 3 random equations
    equation = np.zeros(public_key.size)
    # add or sub each of them 
    for _ in range(0, 3):
        which_equation = random.randint(0, public_key.count - 1)
        if random.choice([True, False]):
            equation += public_key.equations[which_equation]
        else:
            equation -= public_key.equations[which_equation]
    # encode bit 
    if bit:
        equation[-1] += public_key.mod // 2
    # mod the error
    equation[-1] = equation[-1] % public_key.mod
    # return as a message
    return Message(equation)

def private_key_gen() -> PrivateKey:
    mod = 71
    size = 4
    vector = np.random.randint(0, mod, size)
    return PrivateKey(vector, mod, size)

def public_key_gen(private_key: PrivateKey) -> PublicKey:
    count = 10
    mod = private_key.mod
    size = private_key.size + 1
    shape = (count, size)
    # generate random polynommials 
    equations = np.random.randint(0, mod, shape)
    # calculate sum 
    for i in range(0, count):
        sum = 0
        for j in range(0, size - 1):
            sum += equations[i, j] * private_key.vector[j]
        # add error 
        distance = random.randint(-3, 3)
        # mod
        equations[i, size - 1] = (sum + distance) % mod
    return PublicKey(equations, mod, size, count)

def main():
    private_key = private_key_gen()
    print("Private Key:", private_key)
    public_key = public_key_gen(private_key)
    print("Public Key:", public_key)
    for i in range(0, 10):
        message = encrypt(public_key, True)
        print("Message:", message)
        result = decrypt(private_key, message)
        if not result:
            print("Failed on try:", i)
            return

if __name__ == "__main__":
    main()

