# Parses the text files for Shakespeare and Spenser's sonnets and runs the
# program.
shakespeare = 'shakespeare.txt'
spenser = 'spenser.txt'


# Note that the files are parsed into the following fowm: it is a nested
# list of lists of lines: the outmost list is a list of poems, which
# is a list of lines.
from hyphen import Hyphenator
def parseLim(filename, numPoem):
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
		elif len(line.split()) != 0:
			poem.append(line)
	return corpus
def parseTokLim(f1, numPoem1, f2, numPoem2):
	shak = parseLim(f1, numPoem1)
	spen = parseLim(f2, numPoem2)
	token_vals = []
	observations = []
	for poem in shak:
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
	return token_vals, observations

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

def parseSyll(f1, f2):
	h_en = Hyphenator('en_US')
	observations = []
	token_vals = []
	shak = parse(f1)
	spen = parse(f2)
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					if s not in token_vals:
						token_vals.append(s.lower())
	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					if s not in token_vals:
						token_vals.append(s.lower())
	for poem in shak:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					temp.append(token_vals.index(s.lower()))
		observations.append(temp)

	for poem in spen:
		temp = []
		for line in poem:
			for word in line.split():
				syls = h_en.syllables(unicode(word))
				for s in syls:
					temp.append(token_vals.index(s.lower()))
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
	print len(token_vals)
	#print len(shak)
	#print len(spen)
