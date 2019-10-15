import numpy as np
import random

#Arrays and Constants
n = 10
N = 100
players = np.linspace(0, n-1, n, dtype=int)                 #List of players as integers, which allows us to 
opponents = np.linspace(0, n-1, n, dtype=int)               #use a player as an iteration number.


def fun():
    while True:    
        #Shuffling
        matchups = []                                                           #Resets Matchup List
        random.shuffle(opponents)                                               #Shuffles our opponents
        for i in range(n):
            if opponents[i] == players[i]:
                opponents[i], opponents[i-1] = opponents[i-1], opponents[i]     #If anybodyplays themselves, the 

        #List Formating
        for i in players:
            a = i
            b = opponents[i]
            c = players[b] 
            if opponents[b] == i:                                               #Here we check if for a given match, is the opponent
                for j in players:                                               #playing the same person in their 'home' match
                    if (players[i-j-1] != i and players[i-j-1] != b):           #Checks the previous match to see if there is a duplicate 
                        opponents[i], opponents[i-j-1] = opponents[i-j-1], opponents[i]     #If not, swaps the opponent in each match
                        b = opponents[i]
                        break
            if opponents[b] == i:
                break
            matchups.append([a,b])                                              #Adds current match to list, only if there is no duplicates
        if len(matchups) == n:                          #If the for loop ran all the way through 
            return matchups                             #It returns our list, if not resets to the top



import time
start_time = time.time()

for i in range(N):                     #Checks a large number of iterations for 
    print(fun())                        #visual conformation to see if it works
    print('\n\n')               
    matchups = []
    print(i)
time_taken = (time.time() - start_time)
print("--- %s seconds ---" % (time_taken))

f = open('time_elapsed.py', 'a+')
f.write('\n\nscan_method.append({})'.format([time_taken, N]))
f.close()



