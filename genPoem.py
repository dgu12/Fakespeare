from hyphen import Hyphenator
import numpy as np

def hmmGenerate(A_Mat, O_Mat, tokens):
	# Assuming A_Mat and O_Mat are np matrices
	h_en = Hyphenator('en_US')
	numStates = len(A_Mat)
	numObs = np.shape(O_Mat)[1]
	random.seed()
	start = random.randint(1, numStates)
	state = start
	poem = []
	for l in range(0,14):
		numSyl = 0
		line = []
		while numSyl < 10:
			prob = random.random()
			ind = 0
			sumP = 0
			while ind < numObs:
				sumP += O_Mat[state][ind]
				if sumP > prob:
					# Emit this observation
					line.append(tokens[O_Mat[state][ind]])
					numSyl += len(h_en.syllables(unicode(tokens[O_Mat[state][ind]])))
					break
				ind += 1
			# Transition to the next state
			prob = random.random()
			ind = 0
			sumP = 0
			while ind < numStates:
				sumP += A_Mat[state][ind]
				if sumP > prob:
					state = A_Mat[state][ind]
					break
				ind += 1
		poem.append(line)

	#Print line
	for line in poem:
		print line
