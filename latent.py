# Finds the optimal number of latent factors for our HMM.

import random
import numpy as np
from nltk.tag.hmm import HiddenMarkovModelTagger, HiddenMarkovModelTrainer
# Self-written module.
import shakespeare
from genPoem import hmmGenerate

#lstates = range(10, 101, 10)
lstates = 8

def generate(A, O, length):
	'''Given the transition matrix A and observation matrix O which
	characterize a hidden Markov model, randomly generates a sequence
	consistent with the model. Assumes A is S x S and O is T x S, and
	A = a_ij, which represents the probability of transitioning from
	state i to state j.'''
	S = len(A) # Number of hidden states
	T = len(O) # Number of tokens.
	seq = []
	# Pick a starting state uniformly at random.
	random.seed(0)
	current = random.randrange(S)
	# See what token we will emit.
	dist = [row[current] for row in O]
	rand = random.random()
	psum = 0
	for i in range(T):
		if psum <= rand and rand <= psum + dist[i]:
			seq.append(i)
			break
		else:
			psum += dist[i]
	for i in range(1, length):
		# First transition to our next state.
		sdist = A[current]
		ssum = 0.0
		srand = random.random()
		for j in range(S):
			if ssum <= srand and srand <= ssum + sdist[j]:
				current = j
			else:
				ssum += sdist[j]
		# Now see what token this state emits.
		tdist = [row[current] for row in O]
		tsum = 0.0
		trand = random.random()
		for j in range(T):
			if tsum <= trand and trand <= tsum + tdist[j]:
				seq.append(j)
				break
			else:
				tsum += tdist[j]
	return seq


if __name__ == '__main__':
	tokens, obs = shakespeare.parseTok("shakespeare.txt", "spenser.txt")
	# Need tuples for each token where second element is the tag (or None if
	# unlabeled).
	training = []
	for poem in obs:
		training.append([(i, None) for i in poem])
	#for states in lstates:
	states = lstates
	hmm = HiddenMarkovModelTrainer(range(states), range(len(tokens)))
	# Automatically creates a random model if no model argument specified.
	model = hmm.train_unsupervised(training, max_iterations = 1)
	# Need an object with a random method.
	rng = random.Random()
	rng.seed(0)
	# Get a random "poem" from our model.
	#print [tokens[tup[0]] for tup in model.random_sample(rng, 110)]
	# Convert transition and output of model in np.matrices
	A_mat = np.zeros((states, states))
	# for r in range(0, states):
	# 	for c in range(0, states):
	# 		A_mat[r][c] = model._transitions[r][c]

	O_mat = np.zeros((states, len(tokens)))
	# for r in range(0, states):
	# 	for c in range(0, len(tokens)):
	# 		O_mat[r][c] = model._outputs[r][c]

	
	for r in range(0, states):
		for c in range(0, states):
			A_mat[r][c] = model._transitions[r].logprob(c)
	for c in range(0, len(tokens)):
		col = model._outputs_vector(c)
		for r in range(0, states):
			O_mat[r][c] = col[r]

	A_mat = np.exp(A_mat)
	O_mat = np.exp(O_mat)


	hmmGenerate(A_mat, O_mat, tokens)

