# Parses the text files for Shakespeare and Spenser's sonnets and runs the
# program.
shakespeare = 'shakespeare.txt'
spenser = 'spenser.txt'


# Note that the files are parsed into the following fowm: it is a nested
# list of lists of lines: the outmost list is a list of poems, which
# is a list of lines.

def parse(filename):
	'''Parses the shakespeare.txt file into the format defined in the form
	above.'''
	f = open(filename, 'r')
	corpus = []
	poem = []
	first = True
	for line in f:
		line = line.strip() # Remove whitespace.
		if len(line.split()) == 1:
			# Start a new poem.
			if first:
				first = False
			else:
				corpus.append(poem)
			poem = []
		else:
			poem.append(line)
	return corpus

def parseTok(f1, f2):
	token_vals = []
	observations = []
	shak = parse(f1)
	spen = parse(f2)
	for poem in shak:
		for line in poem:
			for word in line.split():
	 			if word not in token_vals:
	 				token_vals.append(word.lower())
	for poem in spen:
		for line in poem:
	 		for word in line.split():
	 			if word not in token_vals:
	 				token_vals.append(word.lower())

	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				temp.append(token_vals.index(word.lower()))
		
		observations.append(temp)

	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				temp.append(token_vals.index(word.lower()))
		observations.append(temp)
	return token_vals, observations


if __name__ == '__main__':
	# Test to see if parsing works.
	token_vals = []
	observations = []
	shak = parse(shakespeare)
	print "Shakespeare"
	print len(shak)
	print '\n'
	for poem in shak:
		for line in poem:
			for word in line.split():
	 			if word not in token_vals:
	 				token_vals.append(word.lower())
	 				
	spen = parse(spenser)
	print "Spenser"
	print len(spen)
	print '\n'
	for poem in spen:
		for line in poem:
	 		for word in line.split():
	 			if word not in token_vals:
	 				token_vals.append(word.lower())
	
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				temp.append(token_vals.index(word.lower()))
		
		observations.append(temp)

	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				temp.append(token_vals.index(word.lower()))
		observations.append(temp)

	print observations
	#print len(shak)
	#print len(spen)
