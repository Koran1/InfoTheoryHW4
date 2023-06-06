import random
import numpy as np
import matplotlib.pyplot as plt

def bec_channel(p, codeword):
    n = len(codeword)
    codeword_bec = [None] * n
    # Binary Erase Channel with prob p
    for i in range(n):
        prob = [p, 1-p]
        choices = [None, codeword[i]]
        codeword_bec[i] = random.choices(choices, prob)[0]
    
    return codeword_bec

def hamming_enc(message): # Hamming (7,4)
    msg = [int(bit) for bit in message]
    # Parity bits with XOR operator
    p1 = msg[0] ^ msg[1] ^ msg[3]
    p2 = msg[0] ^ msg[2] ^ msg[3]
    p3 = msg[1] ^ msg[2] ^ msg[3]

    codeword = [msg[0], msg[1], msg[2], msg[3], p1, p2, p3]
    return codeword

def check_nones(sets):
    count = 0
    for k in range(len(sets)):
        if sets[k] == None:
            count +=1
    return count

def code_update(codeword):
    global set1, set2, set3, nn_s1, nn_s2, nn_s3
    set1 = [codeword[0], codeword[1], codeword[3], codeword[4]]
    set2 = [codeword[0], codeword[2], codeword[3], codeword[5]]
    set3 = [codeword[1], codeword[2], codeword[3], codeword[6]]

    nn_s1 = check_nones(set1)
    nn_s2 = check_nones(set2)
    nn_s3 = check_nones(set3)

def peeling_decoder(codeword):
    code_update(codeword)
    if nn_s1 == 0 and nn_s2 == 0 and nn_s3 == 0: # No errors
        return codeword

    while(1):
        check = 0
        xor = 0
        if nn_s1 == 1:
            for i in range(4):
                if set1[i] == None:
                    check = i
                else:
                    xor = xor ^ set1[i]
            
            if check == 0:
                codeword[0] = xor
                code_update(codeword)
            elif check == 1:
                codeword[1] = xor
                code_update(codeword)
            elif check == 2:
                codeword[3] = xor
                code_update(codeword)
            elif check == 3:
                codeword[4] = xor
                code_update(codeword)

        elif nn_s2 == 1:
            for i in range(4):
                if set2[i] == None:
                    check = i
                else:
                    xor = xor ^ set2[i]
            
            if check == 0:
                codeword[0] = xor
                code_update(codeword)
            elif check == 1:
                codeword[2] = xor
                code_update(codeword)
            elif check == 2:
                codeword[3] = xor
                code_update(codeword)
            elif check == 3:
                codeword[5] = xor
                code_update(codeword)

        elif nn_s3 == 1:
            for i in range(4):
                if set3[i] == None:
                    check = i
                else:
                    xor = xor ^ set3[i]
            
            if check == 0:
                codeword[1] = xor
                code_update(codeword)
            elif check == 1:
                codeword[2] = xor
                code_update(codeword)
            elif check == 2:
                codeword[3] = xor
                code_update(codeword)
            elif check == 3:
                codeword[6] = xor
                code_update(codeword)
        
        else: 
            return codeword

def frame_error_rate(p):
    num_trials = 1000 
    error_count = 0

    for _ in range(num_trials):
        message = np.random.randint(2, size=4)          # Generate a random 4bit message
        codeword = hamming_enc(message)                 # Hamming Encoding
        codeword_bec = bec_channel(p, codeword)         # Simulate BEC channel
        decoded_word = peeling_decoder(codeword_bec)    # Peeling Decoder
        if None in decoded_word:
            error_count += 1
    
    return error_count / num_trials

erasure_probs = np.arange(0, 1.00, 0.01)
FER_values = []

for p in erasure_probs:
    FER = frame_error_rate(p)
    FER_values.append(FER)

# Plotting the Frame Error Rate (FER)
plt.plot(erasure_probs, FER_values)
plt.axis()
plt.xlabel('Erasure Probability')
plt.ylabel('Frame Error Rate (FER)')
plt.title('Num of trials : 1000')
plt.grid(True)
plt.show()
