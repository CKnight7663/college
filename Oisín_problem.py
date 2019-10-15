import numpy as np
import random

#Arrays and Constants
n = 10
N = 100
players = np.linspace(0, n-1, n, dtype=int)
opponents = np.linspace(0, n-1, n, dtype=int)


def fun():
    while True:
        #Shuffling
        matchups = []
        random.shuffle(opponents)                                               #Shuffles our opponents
        for i in range(n):
            if opponents[i] == players[i]:
                opponents[i], opponents[i-1] = opponents[i-1], opponents[i]     #If anybodyplays themselves, the 

        #List Formating
        for i in players:
            a = i
            b = opponents[i]
            if opponents[b] == i:
                break
            matchups.append([a,b])
        if len(matchups) == n:
            return matchups

import time
start_time = time.time()


for i in range(N):
    print(fun())
    print('\n\n')
    matchups = []


time_taken = (time.time() - start_time)
print("--- %s seconds ---" % (time_taken))

f = open('time_elapsed.py', 'a+')
f.write('\n\nreshuffle_method.append({})'.format([time_taken, N]))
f.close()
