# Finds the optimal number of latent factors for our HMM.

import random
import numpy as np
from nltk.tag.hmm import HiddenMarkovModelTagger, HiddenMarkovModelTrainer
# Self-written module.
import shakespeare

lstates = range(10, 101, 10)

if __name__ == '__main__':
	tokens, obs = shakespeare.parseTok("shakespeare.txt", "spenser.txt")
	# Need tuples for each token where second element is the tag (or None if
	# unlabeled).
	training = []
	for poem in obs:
		training.append([(i, None) for i in poem])
	for states in lstates:
		hmm = HiddenMarkovModelTrainer(range(states), range(len(tokens)))
		# Automatically creates a random model if no model argument specified.
		model = hmm.train_unsupervised(training)
		# Need an object with a random method.
		rng = random.Random()
		rng.seed(0)
		# Get a random "poem" from our model.
		print model.random_sample(rng, 110)