# Parses the text files for Shakespeare and Spenser's sonnets and runs the
# program.
shakespeare = 'shakespeare.txt'
spenser = 'spenser.txt'


# Note that the files are parsed into the following fowm: it is a nested
# list of lists of lines: the outmost list is a list of poems, which
# is a list of lines.
import itertools, sys
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
                if word.lower() not in token_vals:
                    token_vals.append(word.lower())
    for poem in shak:
        temp = []
        for line in poem:
            for word in line.split():
                temp.append(token_vals.index(word.lower()))
        
        observations.append(temp)

    for poem in spen:
        for line in poem:
            for word in line.split():
                if word.lower() not in token_vals:
                    token_vals.append(word.lower())
    for poem in spen:
        temp = []
        for line in poem:
            for word in line.split():
                temp.append(token_vals.index(word.lower()))
        observations.append(temp)

    return token_vals, observations

def parseTokLimMin(f1, numPoem1, f2, numPoem2, numPoemChoose):
    shak = parseLim(f1, numPoem1)
    spen = parseLim(f2, numPoem2)
    all_poem = shak + spen

    min_tok_vals = sys.maxint
    best_combo = None
    best_token_vals = None
    best_token_ind = None
    best_observations = None
    for combo in itertools.combinations(all_poem, numPoemChoose):
        token_vals = {}
        token_ind = {}
        observations = []
        index = 0
        for poem in combo:
            temp = []
            for line in poem:
                for word in line.split():
                    w = word.lower()
                    if w not in token_vals:
                        token_vals[w] = index
                        token_ind[index] = w
                        index += 1
                    temp.append(token_vals[w])
            observations.append(temp)
        if len(token_vals) < min_tok_vals:
            min_tok_vals = len(token_vals)
            best_combo = combo
            best_token_vals = token_vals
            best_token_ind = token_ind
            best_observations = observations

    token_vals = []
    for i in range(len(best_token_vals)):
        token_vals.append(best_token_ind[i])

    f = open(str(numPoemChoose) + '.txt', 'w')

    f.write('Tokens\n')
    for i in range(len(token_vals)):
        f.write(token_vals[i] + '\n')

    f.write('Observations\n')
    for i in range(len(best_observations)):
        for j in range(len(best_observations[i])):
            f.write(str(best_observations[i][j]) + '\n')
        f.write('\n')

    f.close()

    return token_vals, best_observations

def parseTok(f1, f2):
    token_vals = []
    observations = []
    shak = parse(f1)
    spen = parse(f2)
    for poem in shak:
        for line in poem:
            for word in line.split():
                if word.lower() not in token_vals:
                    token_vals.append(word.lower())
    for poem in spen:
        for line in poem:
            for word in line.split():
                if word.lower() not in token_vals:
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
