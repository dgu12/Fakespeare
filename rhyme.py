# Generating function to generate rhyme.

from hyphen import Hyphenator
import numpy as np
import random
import sys
import shakespeare
from visualize import *

def parseFile(f):
	'''Given a file f which contains the A and O matrices which characterize
	a firt-order HMM, parses it and returns the A and O matrices.'''
	data = open(f)
	
	isO = False
	hasStart = False
	S_Mat = None
	temp = data.readline()
	numStates = int(data.readline())
	numObs = int(data.readline())

	if temp.strip() == "true":
	    hasStart = True
	    S_Mat = np.zeros(numStates)

	A_Mat = np.zeros((numStates, numStates))
	O_Mat = np.zeros((numStates, numObs))
	
	tokens = []
	Arow = 0
	Acol = 0
	Orow = 0
	Ocol = 0
	Srow = 0
	Trow = 0
	isTokens = True
	for line in data:
	    line = line.strip()
	    if line == "":
	        continue
	    if hasStart == True:
	        if line == "Start" :
	            continue
	        S_Mat[Srow] = float(line)
	        Srow += 1
	        if Srow == numStates:
	            hasStart = False
	        continue
	    if isTokens == True:
	        if line == "Tokens":
	            continue
	        tokens.append(line)
	        Trow += 1
	        if Trow == numObs:
	            isTokens = False
	        continue
	    if line == "A":
	        continue
	    if line == "O":
	        isO = True
	        continue
	    if isO == True:
	        O_Mat[Orow][Ocol] = float(line)
	        Ocol += 1
	        if Ocol == numObs:
	            Ocol = 0
	            Orow += 1
	    else:
	        A_Mat[Arow][Acol] = float(line)
	        Acol += 1
	        if Acol == numStates:
	            Acol = 0
	            Arow += 1
	            if Arow == numStates:
	                isO = True
	data.close
	return A_Mat, O_Mat

def addPair(rhyme, r1, r2):
	'''Adds the pair r1 to r2 to the rhyming dictionary, or doesn't change it
	if they are already in it.'''
	added = False
	for l in rhyme:
		if r1 in l and r2 not in l:
			l.append(r2)
			added = True
		elif r1 not in l and r2 in l:
			l.append(r1)
			added = True
		elif r1 in l and r2 in l:
			added = True
	# If we still haven't added r1 and r2, add them in a new list to rhyme.
	if not added:
		new_list = []
		new_list.append(r1)
		new_list.append(r2)
		rhyme.append(new_list)

	return rhyme

# Creates a rhyme dictionary for Shakespearean sonnets, which have the rhyme
# scheme
# abab cdcd efef gg
# Spenserian sonnets have the more intricate structure
# abab bcbc cdcd ee
# but we will ignore the repeated rhymes, sacrificing a larger dictionary for
# ease of parsing.
def rhymingDict(filename):
	'''Parses a source file f (i.e., a corpus) and returns a list of lists:
	each element of our outer list is a list which holds an rhyming equivalence
	class; that is, every word in the list rhymes with every other word.'''
	# Parse the poems and tokenize them, so that our rhyming dictionary is
	# consistent with other parts of the code base.
	f = open(filename, 'r')
	rhyme = []
	poem = []
	first = True
	for line in f:
		line = line.strip() # Remove whitespace.
		if len(line.split()) == 1:
			# Start a new poem.
			if first:
				first = False
			else:
				# Process the current poem to add to our rhyme dictionary.
				if len(poem) == 14:
					# We only process the 14-line sonnets, for convenience.
					a1 = poem[0][-1] # Get the last element
					a2 = poem[2][-1]
					rhyme = addPair(rhyme, a1, a2)
					b1 = poem[1][-1]
					b2 = poem[3][-1]
					rhyme = addPair(rhyme, b1, b2)
					c1 = poem[4][-1]
					c2 = poem[6][-1]
					rhyme = addPair(rhyme, c1, c2)
					d1 = poem[5][-1]
					d2 = poem[7][-1]
					rhyme = addPair(rhyme, d1, d2)
					e1 = poem[8][-1]
					e2 = poem[10][-1]
					rhyme = addPair(rhyme, e1, e2)
					f1 = poem[9][-1]
					f2 = poem[11][-1]
					rhyme = addPair(rhyme, f1, f2)
					g1 = poem[12][-1]
					g2 = poem[13][-1]
					rhyme = addPair(rhyme, g1, g2)
			poem = []
		elif len(line.split()) != 0:
			poem.append(line.split())
	return rhyme

def choose(dist):
	'''Given a possibly unnormalized probability distribution dist over states,
	chooses a random state according to the distribution.'''
	s = sum(dist)
	dsum = 0.0
	random.seed()
	rand = random.uniform(0, s)
	for i in range(len(dist)):
		if dsum <= rand and rand <= dsum + dist[i]:
			return i
		else:
			dsum += dist[i]
	return -1 # We shouldn't fail, but we might...?

# Keep in mind that A_ij represents the probabilitiy of transitioning from
# state i to state j and O_ij represents the probability of transitioning from
# from state i to token j.
def rhymeGen(A, O, tokens, rhyme):
	'''Generates a rhyming sonnet using the rhyme dictionary rhyme and the HMM
	specified by the A and O matrices. First picks the end rhyme and then
	generates each line backwards until it has 10 syllables.'''
	h_en = Hyphenator('en_US')
	# Create a 14 line sonnet.
	poem = [[] for i in range(14)]
	# Now choose our end rhymes:
	random.seed()
	# a pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[0].append(pair[0])
	poem[2].append(pair[1])
	# b pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[1].append(pair[0])
	poem[3].append(pair[1])
	# c pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[4].append(pair[0])
	poem[6].append(pair[1])
	# d pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[5].append(pair[0])
	poem[7].append(pair[1])
	# e pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[8].append(pair[0])
	poem[10].append(pair[1])
	# f pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[9].append(pair[0])
	poem[11].append(pair[1])
	# g pair
	l = random.choice(rhyme)
	pair = random.sample(l, 2)
	poem[12].append(pair[0])
	poem[13].append(pair[1])
	# Now generate each line backwards.
	for i in range(len(poem)):
		numSyl = 0
		# First, randomly choose a state for the given token.
		tok = tokens.index(poem[i][0])
		dist = [row[tok] for row in O]
		state = choose(dist)
		# Now generate the rest of the line, keeping track of syllables.
		while numSyl < 10:
			# Choose a state to transition to.
			sdist = [row[state] for row in A]
			state = choose(sdist) # state now holds the new (previous) state.
			# Now choose a token to emit from 1 state.
			tdist = O[state]
			token = tokens[choose(tdist)]
			poem[i].append(token)
			if len(h_en.syllables(unicode(token))) == 0:
			    numSyl += 1
			else:
			    numSyl += len(h_en.syllables(unicode(token)))
		# Reverse our list when we're done, since we generated it backwards.
		poem[i].reverse()
	return poem

def genFromFile(filename, tokens, rhyme):
	'''Given a file holding the A and O matrices of a trained HMM, generates
	and prints a poem.'''
	A, O = parseFile(filename)
	poem = rhymeGen(A, O, tokens, rhyme)
	# Now print the poem.
	for line in poem:
		print ' '.join(line)
	print '\n'

if __name__ == '__main__':
	if len(sys.argv) != 2:
	    print 'Usage: python', sys.argv[0], '[file name]'
	else:
	    filename = sys.argv[1]
	    tokens, obs = shakespeare.parseTokLim("shakespeare.txt", -1, "spenser.txt", -1)
	    rhyme1 = rhymingDict("shakespeare.txt")
	    rhyme2 = rhymingDict("spenser.txt")
	    rhyme = rhyme1 + rhyme2
	    genFromFile(filename, tokens, rhyme)