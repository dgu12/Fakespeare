# Parses the text files for Shakespeare and Spenser's sonnets and runs the
# program.
shakespeare = 'shakespeare.txt'
spenser = 'spenser.txt'


# Note that the files are parsed into the following fowm: it is a nested
# list of lists of lines: the outmost list is a list of poems, which
# is a list of lines.
from hyphen import Hyphenator
import string

def parseLim(filename, numPoem):
	''' Function to parse a limited number of poems from a file.
	    A value of -1 for numPoem parses all of the poems '''
	f = open(filename, 'r')
	corpus = []
	poem = []
	first = True
	p = 0
	for line in f:
		line = line.strip() # Remove whitespace.
		if len(line.split()) == 1:
			# Start a new poem.
			if first:
				first = False
			else:
				corpus.append(poem)
				p += 1
				if numPoem != -1:
					if p > numPoem:
						break
			poem = []
		elif len(line.split()) != 0:
			poem.append(line)
	return corpus

def parseTokLim(f1, numPoem1, f2, numPoem2):
	''' This function tokenizes some number of poems by word.
		numPoem1 and numPoem2 determine how many poems from each file we 
		tokenize. A value of -1 is used to tokenize all available poems. '''
	shak = parseLim(f1, numPoem1)
	spen = parseLim(f2, numPoem2)
	token_vals = []
	observations = []
	# Find all the unique words from the poems
	for poem in shak:
		for line in poem:
			for word in line.split():
				# Make sure the words are lowercase, we will make sure
				# correct capitalization is used elsewhere
				word = word.lower()
				# Strip parenthesis 
				word = word.translate(None, "()")
	 			if word not in token_vals:
	 				token_vals.append(word)

	# Convert poems into lists of values
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				# Make sure word is lowercase to match the tokens array
				word = word.lower()
				# Make sure there are no parens
				word = word.translate(None, "()")
				temp.append(token_vals.index(word))
		
		observations.append(temp)

	# Repeat above for Spenser's poems
	for poem in spen:
		for line in poem:
			for word in line.split():
				# Make sure the words are lowercase, we will make sure
				# correct capitalization is used elsewhere
				word = word.lower()
				# Strip parenthesis 
				word = word.translate(None, "()")
	 			if word not in token_vals:
	 				token_vals.append(word)
	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				# Make sure word is lowercase to match the tokens array
				word = word.lower()
				# Make sure there are no parens
				word = word.translate(None, "()")
				temp.append(token_vals.index(word))
		observations.append(temp)

	return token_vals, observations

def parseSyll(f1, f2):
	''' This function tokenizes poems by syllable. Each unique syllable 
	    corresponds to a unique value. '''
	h_en = Hyphenator('en_US')
	observations = []
	token_vals = []
	shak = parseLim(f1, -1)
	spen = parseLim(f2, -1)
	# Find the unique syllables and assign them values
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					if s.lower() not in token_vals:
						token_vals.append(s.lower())
	# Repeat for Spenser's Poems
	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					if s.lower() not in token_vals:
						token_vals.append(s.lower())

	# Convert the poems into lists of values
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					temp.append(token_vals.index(s.lower()))
		observations.append(temp)
	# Repeat for Spenser
	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					temp.append(token_vals.index(s.lower()))
		observations.append(temp)
	return token_vals, observations
