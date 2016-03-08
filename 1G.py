

def main():
    raw_moods = []
    raw_genres = []

    with open('./data/ron.txt', 'r') as f:  # read in Ron's data
        for line in f.readlines():
            mood, genre = line.strip().split('\t')
            raw_moods.append(mood)
            raw_genres.append(genre)

    # maps moods to numbers
    moods = {'happy': 0, 'mellow': 1, 'sad': 2, 'angry': 3}

    # list of music genres
    # maps genres to numbers
    genres = {'rock': 0, 'pop': 1, 'house': 2, 'metal': 3, 'folk': 4,
              'blues': 5, 'dubstep': 6, 'jazz': 7, 'rap': 8, 'classical': 9}

    # numerical data of Ron's moods and music genres
    state_seq = [moods[x] for x in raw_moods]
    obs_seq = [genres[x] for x in raw_genres]

    A, O = MStep(moods, genres, state_seq, obs_seq)

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
def MStep(pos_states, pos_observations, state_seq, obs_seq):

    A = [[1. / len(pos_states) for i in pos_states] for j in pos_states]
    O = [[1. / len(pos_observations) for i in pos_observations]
         for j in pos_states]

    # create transition matrix
    for prev_state in pos_states:
        for state in pos_states:
            num = 0.0
            den = 0.0
            for j in range(len(state_seq) - 1):
                if (state_seq[j] == pos_states[prev_state]):
                    den += 1
                    if state_seq[j + 1] == pos_states[state]:
                        num += 1
            A[pos_states[state]][pos_states[prev_state]] = num / \
                den if den != 0 else 0

    # create observation matrix
    for state in pos_states:
        for obs in pos_observations:
            num = 0.0
            den = 0.0
            num = sum([int(obs_seq[j] == pos_observations[obs]) and
                       int(state_seq[j] == pos_states[state]) for j in range(len(state_seq))])
            den = sum([int(state_seq[j] == pos_states[state])
                       for j in range(len(state_seq))])

            O[pos_states[state]][pos_observations[obs]] = float(num) / den

    return A, O

def eStep(A, O, num_states, obs_seq):

def Forward(num_states, obs, A, O):
    """Computes the probability a given HMM emits a given observation using the
        forward algorithm. This uses a dynamic programming approach, and uses
        the 'prob' matrix to store the probability of the sequence at each length.
        Arguments: num_states the number of states
                   obs \       an array of observations
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

def Backward(num_states, obs, A, O):
    len_ = len(obs)                   # number of observations
    # stores p(seqence)
    prob = [[[1] for i in range(num_states)] for i in range(len_)]

    for length in range(len_-2, -1, -1):   # length + 1 to avoid initial condition
        for state in range(num_states):
            # stores the probability of transitioning to 'state'
            p_trans = 0

            # probabilty of observing data in our given 'state'
            #p_obs = O[state][obs[length]]

            # We iterate through all possible previous states, and update
            # p_trans accordingly.
            for prev_state in range(num_states):
                p_trans += prob[length + 1][prev_state] * A[prev_state][state] * O[obs[length + 1]][prev_state]

            prob[length][state] = p_trans  # update probability

        prob[length] = prob[length][:]  # copies by value

    # return total probability
    return prob

if __name__ == '__main__':
    main()
