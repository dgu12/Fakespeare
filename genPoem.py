from hyphen import Hyphenator
import numpy as np
import random

def hmmGenerate(A_Mat, O_Mat, tokens):

	user_input = 'y'
	while (user_input != 'n'):
		# Assuming A_Mat and O_Mat are np matrices
		h_en = Hyphenator('en_US')
		numStates = len(A_Mat)
		numObs = np.shape(O_Mat)[1]
		#random.seed(0)
		start = random.randint(0, numStates-1)
		state = start
		poem = []
		capitalize = False
		for l in range(0,14):
			numSyl = 0
			line = []
			while numSyl < 10:
				prob = random.random()
				ind = 0
				sumP = 0
				if numSyl == 0:
					capitalize = True
				while ind < numObs:

					sumP += O_Mat[state][ind]
					if sumP > prob:
						# Emit this observation
						if capitalize == True:
							line.append(tokens[ind].title())
							capitalize = False
						else:
							line.append(tokens[ind])

						if tokens[ind].endswith(".") or tokens[ind].endswith("?"):
							capitalize = True

						if len(h_en.syllables(unicode(tokens[ind]))) == 0:
							numSyl += 1
						else:
							numSyl += len(h_en.syllables(unicode(tokens[ind])))
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
			print ' '.join(line)
	        print '\n'

		user_input = raw_input('Generate a another poem? [y/n]')

def genFromFile(f, numStates, numObs):
	data = open(f)
	A_Mat = np.zeros((numStates, numStates))
	O_Mat = np.zeros((numStates, numObs))

	data.close