import numpy as np
import random as rand
from shakespeare import parse, parseTok


def main():
    eps = 0.01
    token_vals, obs_seq = parseTok('shakespeare.txt', 'spenser.txt')
    num_obs = len(obs_seq)
    num_states = 7
    A = np.zeros((num_states, num_states))

    # randomly initialize A matrix
    for i in range(num_states):
        for j in range(num_states):
            A[i][j] = rand.random()
        # make each row sum to 1
        A[i][:] = A[i][:] / np.sum(A[i][:])

    O = np.zeros((num_states, num_obs))

    # randomly initialize O matrix
    for i in range(num_states):
        for j in range(num_obs):
            O[i][j] = rand.random()
        # make each row sum to 1
        O[i][:] = O[i][:] / np.sum(O[i][:])

    gamma, xi = eStep(num_states, obs_seq, A, O)
    A_, O_ = mStep(gamma, xi, obs_seq, num_obs)

    diff = np.sum(np.abs(A - A_))
    prev_diff = diff
    prev_A = A_

    while diff/prev_diff > eps:
        prev_diff = diff
        gamma, xi = eStep(num_states, obs_seq, A, O)
        A, O = mStep(gamma, xi, obs_seq, num_obs)
        diff = np.sum(np.abs(prev_A - A))


    A_str = latex_matrix(A)
    O_str = latex_matrix(O)
    with open('1G.txt', 'w') as f:
        f.write(A_str)
        f.write(O_str)


def latex_matrix(matrix):
    matrix_str = '\\begin{bmatrix}\n'
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix_str += str("{0:.3f}".format(matrix[i][j])) + ' & '
        matrix_str = matrix_str[:-2] + '\\\\\n'
    matrix_str += '\\end{bmatrix} \n'
    return matrix_str


# Uses a single Maximization step to compute A (state-transition) and
# O (observation) matrices. See Lecture 6 Slide 65.
def mStep(gamma, xi, obs, num_obs):
    A = [[0. for i in num_states] for j in num_states]
    O = [[0. for i in num_states] for j in num_obs]

    for i in range(num_states):
        for j in range(num_states):
            A[i][j] = np.sum(xi[:][:end-1][i][j]) / np.sum(gamma[:][:end-1][i])

        for j in range(num_obs):
            for o in range(len(obs)):
                for t in range(obs_len):
                    if obs[o][t] == j:
                        O[i][j] += gamma[o][t][i]
            O[i][j] /= np.sum(gamma[:][:][i]) 

    return A, O

def eStep(num_states, obs_seq, A, O):
    # probability of being in state i at time t given the observed sequence
    # and parameters
    obs_len = len(obs_seq)
    gamma = [[[0. for i in range(num_states)] for j in range(obs_len)] for k in range(len(obs_seq))]

    # probability of being in state i and j at time t
    xi = [[[[0. for i in range(num_states)] for j in range(num_states)] for k in range(obs_len)] for l in range(len(obs_seq))]

    for obs_num in range(len(obs_seq)):
        obs = obs_seq[obs_num]

        alpha = forward(num_states, obs, A, O)
        beta = backward(num_states, obs, A, O)
        

        # now we compute the marginals
        obs_len = len(obs)
        num_states = len(alpha[0])


        for length in range(obs_len):

            den = np.sum(alpha[length] * beta[length])
            for state in range(num_states):
                gamma[obs_num][length][state] = alpha[length][state] * beta[length][state] / den



        den = np.sum(alpha[end][:])
        for t in range(obs_len):
            for i in range(num_states):
                for j in range(num_states):
                    xi[obs_num][t][i][j] = alpha[t][i] * A[i][j] * beta[t+1][j] * O[j][obs[t+1]] / den

    return gamma, xi



def forward(num_states, obs, A, O):
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
    prob = [[[0.] for i in range(num_states)] for i in range(len_)]

    # initializes uniform state distribution, factored by the
    # probability of observing the sequence from the state (given by the
    # observation matrix)
    prob[0] = [(1. / num_states) * O[j][obs[0]] for j in range(num_states)]

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

        prob[length] = prob[length][:]  # copies by value

    # return total probability
    return prob

def backward(num_states, obs, A, O):
    len_ = len(obs)                   # number of observations
    # stores p(seqence)
    prob = [[1 for i in range(num_states)] for i in range(len_)]

    for length in range(len_-2, -1, -1):   # length + 1 to avoid initial condition
        for state in range(num_states):
            # stores the probability of transitioning to 'state'
            p_trans = 0

            # probabilty of observing data in our given 'state'
            #p_obs = O[state][obs[length]]

            # We iterate through all possible previous states, and update
            # p_trans accordingly.
            for prev_state in range(num_states):
                p_trans += prob[length + 1][prev_state] * A[prev_state][state] * O[prev_state][obs[length + 1]]

            prob[length][state] = p_trans  # update probability

        prob[length] = prob[length][:]  # copies by value

    # return total probability
    return prob

if __name__ == '__main__':
    main()
