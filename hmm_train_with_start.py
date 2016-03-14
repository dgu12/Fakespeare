import numpy as np
import random
import sys
import signal
from shakespeare import *
from genPoem import *

''' This file contains functions for unsupervised training of a HMM.
'''

kill = False # Global varaible that indicates if the user wants to stop 
             # training and save prematurely


def signal_handler(signal, frame):
    '''Handles the SIGINT signal from the user. The first time it does so, it
       makes it so that the next algorithm update iteration is the last.
       If the handler is called again, it immediately kills the process.
    '''
    global kill
    if kill == False:
        kill = True
    else:
        sys.exit()
    print 'You pressed Ctrl+C! Gonna stop and save matrices after this step.'
    print 'Note: depending on training parameters, this may take a while.'
    print 'If you are in a hurry, press Ctrl+C again to immediately kill.'


def main():
    ''' Does HMM training based on command line args until convergence.
    '''
    signal.signal(signal.SIGINT, signal_handler)

    # Now parse the command line arguments.
    if len(sys.argv) < 3:
        print 'Usage: python', sys.argv[0], \
            'num_hidden_states output_filename', \
            '[num_Shakespeare] [num_Spenser] [num_total]'
        return -1

    num_states = int(sys.argv[1])

    eps = 0.005

    # Values of -1 mean use all of the poems
    num_shak = -1
    num_spen = -1

    if len(sys.argv) >= 4:
        num_shak = int(sys.argv[3])
        if len(sys.argv) >= 5:
            num_spen = int(sys.argv[4])

    # If num total is set, we do different preprocessing. In this case,
    # instead of just using the first n poems from Shakespeare and/or
    # Spenser, we pick the num_total number of poems such that the total
    # number of unique words is minimized. Note: choosing high num_total
    # values takes too long to compute.
    if len(sys.argv) == 6:
        token_vals, obs_seq = parseTokLimMin('shakespeare.txt', num_shak, \
            'spenser.txt', num_spen, int(sys.argv[5]))
    else:
        token_vals, obs_seq = parseTokLim('shakespeare.txt', num_shak, \
            'spenser.txt', num_spen)


    num_obs = len(token_vals) # Number of unique tokens.
    
    A = np.zeros((num_states, num_states)) # Transistion matrix.

    # Randomly initialize A matrix
    for i in range(num_states):
        for j in range(num_states):
            A[i][j] = random.random() + 0.1 # Random, but not too small
        # Make each row sum to 1
        A[i][:] = A[i][:] / np.sum(A[i][:])

    O = np.zeros((num_states, num_obs))

    # Randomly initialize O matrix
    for i in range(num_states):
        for j in range(num_obs):
            O[i][j] = random.random() + 0.1 # Random, but not too small
        # Make each row sum to 1
        O[i][:] = O[i][:] / np.sum(O[i][:])

    # Initialize start state. Initially uniform.
    start = np.ones(num_states) / num_states

    # Save to calculate differences later.
    prev_A = A
    prev_O = O

    # Do first EM iteration.
    gamma, xi = eStep(start, num_states, obs_seq, A, O)
    A, O, start = mStep(num_states, gamma, xi, obs_seq, num_obs)

    # Find resulting A and O matrix differences.
    diff = np.linalg.norm(np.subtract(prev_A, A)) + \
            np.linalg.norm(np.subtract(prev_O, O))
    first_diff = diff

    print 'first diff is ', diff

    # Now we loop the EM algorithm until convergence.
    while diff/first_diff > eps and not kill:
        prev_A = A
        prev_O = O
        gamma, xi = eStep(start, num_states, obs_seq, A, O)
        A, O, start = mStep(num_states, gamma, xi, obs_seq, num_obs)
        diff = np.linalg.norm(np.subtract(prev_A, A)) + \
                np.linalg.norm(np.subtract(prev_O, O))

        print 'diff is ', diff
        print 'diff/first_diff is', diff/first_diff

    
    # Write results to file. We can directly parse this file with genPoem.py
    # so that we do not have to wait for training again.
    f = open(sys.argv[2]+'.txt', 'w')

    # Write some metadata. 
    f.write('true\n') # Start state probabilities exist.
    f.write(str(num_states) + '\n') # Number of hidden states.
    f.write(str(num_obs) + '\n\n')  # Number of unique tokens.

    # Write start state probabilities.
    f.write('Start\n')
    for i in range(num_states):
        f.write(repr(start[i])+'\n')
    f.write('\n')

    # Write list of tokens in order of their ID's
    f.write('Tokens\n')
    for i in range(num_obs):
        f.write(str(token_vals[i])+'\n')
    f.write('\n')

    # Write A matrix, row by row
    f.write('A\n')
    for i in range(num_states):
        for j in range(num_states):
            f.write(repr(A[i][j])+'\n')
        f.write('\n')

    # Write O matrix, row by row
    f.write('O\n')
    for i in range(num_states):
        for j in range(num_obs):
            f.write(repr(O[i][j])+'\n')
        f.write('\n')

    f.close()

    print 'done writing', sys.argv[2]

    # Now generate poems!
    hmmGenerate(A, O, token_vals, start)



def eStep(start, num_states, obs_seq, A, O):
    '''Computes the E step of the EM unsupervised training algorithm.
    '''

    # For each observation sequence, the probability of being in each state at
    # each sequence time.
    # ex. gamma[0][1][2] means for the 0th observation sequence, the
    # probability of being in state 2 at time 1.
    gamma = np.zeros([len(obs_seq), max(len(obs) for obs in obs_seq), \
                                                                 num_states]) 
    
    # For each observation sequence, the probability of being in each state at
    # each sequence time and each state in the next sequence time.
    # ex. xi[0][1][2][3] means for the 0th observation sequence, the joint
    # probability of being in hidden state 2 at time 1 and state 3 at time 2.
    xi = np.zeros([len(obs_seq), max(len(obs) for obs in obs_seq), \
        num_states, num_states])
 
    # Calculate xi and gamma for every observation sequence.
    for obs_num in range(len(obs_seq)):
        obs = obs_seq[obs_num]

        # Run the forward-backward algorithm
        alpha = forward(start, num_states, obs, A, O)
        beta = backward(num_states, obs, A, O)
        
        # Each observation sequence has its own possibly unique length.
        obs_len = len(obs)

        # Update gamma based on equation 12 in the HMM notes.
        for length in range(obs_len):
            den = 0
            for state in range(num_states):
                den += alpha[length][state] * beta[length][state]
            for state in range(num_states):
                gamma[obs_num][length][state] = alpha[length][state] * \
                                                beta[length][state] / den

        # Update xi based on equation 13 in the HMM notes.
        for t in range(obs_len-1):
            den = 0
            for a in range(num_states):
                for b in range(num_states):
                    den += alpha[t][a] * O[b][obs[t+1]] * A[a][b] * beta[t+1][b]
            for i in range(num_states):
                for j in range(num_states):
                    xi[obs_num][t][i][j] = alpha[t][i] * A[i][j] \
                                          * beta[t+1][j] * O[j][obs[t+1]] / den

    return gamma, xi


def mStep(num_states, gamma, xi, obs_seq, num_obs):
    '''Computes the M step of the EM unsupervised training algorithm.
    '''

    A = np.zeros([num_states, num_states])
    O = np.zeros([num_states, num_obs])

    for i in range(num_states):

        # Update A based on equation 14 in the HMM notes.
        for j in range(num_states):
            num = 0
            den = 0
            for o in range(len(obs_seq)):
                for t in range(len(obs_seq[o])-1):
                    num += xi[o][t][i][j]
                    den += gamma[o][t][i]
            A[i][j] = num / den

        # Update O based on equation 15 in the HMM notes.
        den = 0
        for o in range(len(obs_seq)):
            for t in range(len(obs_seq[o])):
                den += gamma[o][t][i]
                for j in range(num_obs):
                    if obs_seq[o][t] == j:
                        O[i][j] += gamma[o][t][i]
        for j in range(num_obs):
            O[i][j] /= den

        # Do some sanity checks.
        A_row = np.sum(A[i][:])
        O_row = np.sum(O[i][:]) 
        assert(A_row > 0.9 and A_row < 1.1)
        assert(O_row > 0.9 and O_row < 1.1)

    # Update the start state probabilities based on the probabilties of being
    # in each state at time zero of each observation sequence.
    start = np.zeros(num_states)
    for i in range(num_states):
        for o in range(len(obs_seq)):
            start[i] += gamma[o][0][i] / len(obs_seq)

    # Do another sanity check.
    start_sum = np.sum(start)
    assert(start_sum>0.9 and start_sum<1.1)

    return A, O, start


def forward(start, num_states, obs, A, O):
    '''Computes the probability a given HMM emits a given observation using the
       forward algorithm. This uses a dynamic programming approach, and uses
       the 'prob' matrix to store the probability of the sequence at each 
       length.
       Arguments:  start      start state probabilities
                   num_states the number of states
                   obs        an array of observations
                   A          the transition matrix
                   O          the observation matrix
       Returns the probability of the observed sequence 'obs'
    '''
    len_ = len(obs) # Number of observations

    # Stores p(seqence)
    prob = np.zeros([len_, num_states])

    # Initializes state distribution, factored by the probability of observing 
    # the sequence from the state (given by the observation matrix).
    # A small twiddle factor is added to start[i] to help prevent divide by
    # zero errors later on. This was just an empirical observation.
    for i in range(num_states):
        prob[0][i] = (start[i] + 0.1/num_states) * O[i][obs[0]] 

    # Normalize prob[0] to help with underflow problems.
    prob0_sum = 0;
    for i in range(num_states):
        prob0_sum += prob[0][i]
    for i in range(num_states):
        prob[0][i] /= prob0_sum

    # We iterate through all indices in the data
    for length in range(1, len_):   # Start at 1 to avoid initial condition
        for state in range(num_states):
            # Stores the probability of transitioning to 'state'
            p_trans = 0

            # Probabilty of observing data in our given 'state'
            p_obs = O[state][obs[length]]

            # We iterate through all possible previous states, and update
            # p_trans accordingly.
            for prev_state in range(num_states):
                p_trans += prob[length - 1][prev_state] * A[prev_state][state]

            prob[length][state] = p_trans * p_obs  # Update probability

        # Normalize to prevent underflow issues. Normalization will cancel out
        # in the future.
        prob[length] = np.divide(prob[length][:], np.sum(prob[length][:]))  

    # Return total probability
    return prob


def backward(num_states, obs, A, O):
    '''Computes the probability a given HMM emits a given observation using the
       backwards algorithm. This uses a dynamic programming approach, and uses
       the 'prob' matrix to store the probability of the sequence at each 
       length.
       Arguments:  num_states the number of states
                   obs        an array of observations
                   A          the transition matrix
                   O          the observation matrix
       Returns the probability of the observed sequence 'obs'
    '''
    len_ = len(obs) # Number of observations

    # Stores p(seqence)
    prob = np.ones([len_, num_states])

    # Iterate backwards.
    for length in range(len_-2, -1, -1):   
        for state in range(num_states):

            # Stores the probability of transitioning to 'state'
            p_trans = 0

            # We iterate through all possible next states, and update
            # p_trans accordingly.
            for next_state in range(num_states):
                p_trans += prob[length + 1][next_state] * A[state][next_state] \
                            * O[next_state][obs[length + 1]]

            prob[length][state] = p_trans  # Update probability

        # Normalize to prevent underflow issues. Normalization will cancel out
        # in the future.
        prob[length] = np.divide(prob[length][:], np.sum(prob[length][:]))   

    # Return total probability
    return prob


if __name__ == '__main__':
    main()
