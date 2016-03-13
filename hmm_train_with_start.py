import numpy as np
import random
import sys
import signal
from shakespeare import *
from genPoem import hmmGenerate

kill = False

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C! Gonna stop and save matrices after this step.'
    global kill
    kill = True


def main():
    if len(sys.argv) != 2:
        print 'Usage: python', sys.argv[0], '[num hidden states]'
        return -1
    else:
        num_states = int(sys.argv[1])

    eps = 0.005
    
    signal.signal(signal.SIGINT, signal_handler)
    token_vals, obs_seq = parseTokLimMin('shakespeare.txt', -1, 'spenser.txt', 0, 3)


    num_obs = len(token_vals)
    
    A = np.zeros((num_states, num_states))

    # randomly initialize A matrix
    for i in range(num_states):
        for j in range(num_states):
            A[i][j] = random.random() + 0.1
        # make each row sum to 1
        A[i][:] = A[i][:] / np.sum(A[i][:])

    O = np.zeros((num_states, num_obs))

    # randomly initialize O matrix
    for i in range(num_states):
        for j in range(num_obs):
            O[i][j] = random.random() + 0.1
        # make each row sum to 1
        O[i][:] = O[i][:] / np.sum(O[i][:])

    start = np.ones(num_states) / num_states

    prev_A = A
    prev_O = O

    gamma, xi = eStep(start, num_states, obs_seq, A, O)

    start = np.zeros(num_states)
    for i in range(num_states):
        for o in range(len(obs_seq)):
            start[i] += gamma[o][0][i] / len(obs_seq)
    start_sum = np.sum(start)
    assert(start_sum>0.9 and start_sum<1.1)


    A, O = mStep(num_states, gamma, xi, obs_seq, num_obs)

    diff = np.linalg.norm(np.subtract(prev_A, A)) + np.linalg.norm(np.subtract(prev_O, O))
    first_diff = diff

    print 'diff is ', diff

    while diff/first_diff > eps and not kill:
        prev_A = A
        prev_O = O
        gamma, xi = eStep(start, num_states, obs_seq, A, O)

        start = np.zeros(num_states)
        for i in range(num_states):
            for o in range(len(obs_seq)):
                start[i] += gamma[o][0][i] / len(obs_seq)
        start_sum = np.sum(start)
        assert(start_sum>0.9 and start_sum<1.1)

        A, O = mStep(num_states, gamma, xi, obs_seq, num_obs)
        diff = np.linalg.norm(np.subtract(prev_A, A)) + np.linalg.norm(np.subtract(prev_O, O))

        print 'diff is ', diff
        print 'diff/first_diff is', diff/first_diff

    f = open(sys.argv[1]+'_with_start_fixed.txt', 'w')

    f.write('true\n')
    f.write(str(num_states) + '\n')
    f.write(str(num_obs) + '\n\n')

    f.write('Start\n')
    for i in range(num_states):
        f.write(repr(start[i])+'\n')
    f.write('\n')

    f.write('Tokens\n')
    for i in range(num_obs):
        f.write(str(token_vals[i])+'\n')
    f.write('\n')

    f.write('A\n')
    for i in range(num_states):
        for j in range(num_states):
            f.write(repr(A[i][j])+'\n')
        f.write('\n')

    f.write('O\n')
    for i in range(num_states):
        for j in range(num_obs):
            f.write(repr(O[i][j])+'\n')
        f.write('\n')

    f.close()

    hmmGenerate(A, O, token_vals, start)
    print 'done with', sys.argv[1], 'with start'


def latex_matrix(matrix):
    matrix_str = '\\begin{bmatrix}\n'
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix_str += str("{0:.3f}".format(matrix[i][j])) + ' & '
        matrix_str = matrix_str[:-2] + '\\\\\n'
    matrix_str += '\\-1{bmatrix} \n'
    return matrix_str


# Uses a single Maximization step to compute A (state-transition) and
# O (observation) matrices. See Lecture 6 Slide 65.
def mStep(num_states, gamma, xi, obs_seq, num_obs):

    A = np.zeros([num_states, num_states])
    O = np.zeros([num_states, num_obs])

    for i in range(num_states):
        for j in range(num_states):
            num = 0
            den = 0
            for o in range(len(obs_seq)):
                for t in range(len(obs_seq[o])-1):
                    num += xi[o][t][i][j]
                    den += gamma[o][t][i]
            A[i][j] = num / den

        den = 0
        for o in range(len(obs_seq)):
            for t in range(len(obs_seq[o])):
                den += gamma[o][t][i]
                for j in range(num_obs):
                    if obs_seq[o][t] == j:
                        O[i][j] += gamma[o][t][i]
        for j in range(num_obs):
            O[i][j] /= den

        A_row = np.sum(A[i][:])
        O_row = np.sum(O[i][:]) 
        assert(A_row > 0.9 and A_row < 1.1)
        assert(O_row > 0.9 and O_row < 1.1)

    return A, O

def eStep(start, num_states, obs_seq, A, O):
    # probability of being in state i at time t given the observed sequence
    # and parameters
    gamma = np.zeros([len(obs_seq), max(len(obs) for obs in obs_seq), num_states]) 
    
    # probability of being in state i and j at time t
    xi = np.zeros([len(obs_seq), max(len(obs) for obs in obs_seq), num_states, num_states])
 
    for obs_num in range(len(obs_seq)):
        obs = obs_seq[obs_num]

        alpha = forward(start, num_states, obs, A, O)
        beta = backward(num_states, obs, A, O)
        

        # now we compute the marginals
        obs_len = len(obs)

        for length in range(obs_len):

            den = 0
            for state in range(num_states):
                den += alpha[length][state] * beta[length][state]
            for state in range(num_states):
                gamma[obs_num][length][state] = alpha[length][state] * beta[length][state] / den




        for t in range(obs_len-1):
            den = 0
            for a in range(num_states):
                for b in range(num_states):
                    den += alpha[t][a] * O[b][obs[t+1]] * A[a][b] * beta[t+1][b]
            for i in range(num_states):
                for j in range(num_states):
                    xi[obs_num][t][i][j] = alpha[t][i] * A[i][j] * beta[t+1][j] * O[j][obs[t+1]] / den

    return gamma, xi



def forward(start, num_states, obs, A, O):
    """Computes the probability a given HMM emits a given observation using the
        forward algorithm. This uses a dynamic programming approach, and uses
        the 'prob' matrix to store the probability of the sequence at each length.
        Arguments: num_states the number of states
                   obs        an array of observations
                   A          the transition matrix
                   O          the observation matrix
        Returns the probability of the observed sequence 'obs'
    """
    len_ = len(obs)                   # number of observations
    # stores p(seqence)
    prob = np.zeros([len_, num_states])

    # initializes uniform state distribution, factored by the
    # probability of observing the sequence from the state (given by the
    # observation matrix)
    for i in range(num_states):
        prob[0][i] = (start[i] + 0.1/num_states) * O[i][obs[0]] 
    prob0_sum = 0;
    for i in range(num_states):
        prob0_sum += prob[0][i]
    for i in range(num_states):
        prob[0][i] /= prob0_sum

    # We iterate through all indices in the data
    for length in range(1, len_):   # length + 1 to avoid initial condition
        for state in range(num_states):
            # stores the probability of transitioning to 'state'
            p_trans = 0

            # probabilty of observing data in our given 'state'
            p_obs = O[state][obs[length]]

            # We iterate through all possible previous states, and update
            # p_trans accordingly.
            for prev_state in range(num_states):
                p_trans += prob[length - 1][prev_state] * A[prev_state][state]

            prob[length][state] = p_trans * p_obs  # update probability

        prob[length] = np.divide(prob[length][:], np.sum(prob[length][:]))  # copies by value

    # return total probability
    return prob

def backward(num_states, obs, A, O):
    len_ = len(obs)                   # number of observations
    # stores p(seqence)
    prob = np.ones([len_, num_states])

    for length in range(len_-2, -1, -1):   
        for state in range(num_states):
            # stores the probability of transitioning to 'state'
            p_trans = 0

            # probabilty of observing data in our given 'state'
            #p_obs = O[state][obs[length]]

            # We iterate through all possible previous states, and update
            # p_trans accordingly.
            for prev_state in range(num_states):
                p_trans += prob[length + 1][prev_state] * A[state][prev_state] * O[prev_state][obs[length + 1]]

            prob[length][state] = p_trans  # update probability

        prob[length] = np.divide(prob[length][:], np.sum(prob[length][:]))   # copies by value

    # return total probability
    return prob

if __name__ == '__main__':
    main()
