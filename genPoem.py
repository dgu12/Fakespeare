from hyphen import Hyphenator
import numpy as np
import random
import sys
from visualize import *
from rhyme import *

def hmmGenerate(A_Mat, O_Mat, tokens, startP = None):

    user_input = 'y'
    while (user_input != 'n'):
        # Assuming A_Mat and O_Mat are np matrices
        h_en = Hyphenator('en_US')
        numStates = len(A_Mat)
        numObs = np.shape(O_Mat)[1]
        #random.seed(0)
        state = 0
        if startP == None:
            state = random.randint(0, numStates-1)
        else:
            sumP = 0
            prob = random.random()
            index = 0
            for p in startP:
                sumP += p
                if sumP > prob:
                    state = index
                    break
                index += 1
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
                            line.append(tokens[ind].capitalize())
                            capitalize = False
                        else:
                            if tokens[ind] == "i":
                                line.append("I")
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
                        state = ind
                        break
                    ind += 1
            poem.append(line)

        #Print line
        for line in poem:
            print ' '.join(line)
        print '\n'

        visualize("noun", O_Mat, tokens)
        print '\n'
        visualize("verb", O_Mat, tokens)
        print '\n'
        user_input = raw_input('Generate a another poem? [y/n]')

def genFromFile(f, rhyme):
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
    if rhyme == 1:
        hmmGenerate(A_Mat, O_Mat, tokens, S_Mat)
    else:
        rhyme1 = rhymingDict("shakespeare.txt")
        rhyme2 = rhymingDict("spenser.txt")
        rhyme = rhyme1 + rhyme2
        rhymeLim = rhymeDictLim(tokens, rhyme)
        poem = rhymeGen(A_Mat, O_Mat, tokens, rhymeLim)
        # Now print the poem.
        for line in poem:
            print ' '.join(line)
        print '\n'

def main():
    if len(sys.argv) != 3:
        print 'Usage: python', sys.argv[0], '[file name] [1 - naive, 0 - rhyme]'
        return -1
    else:
        file = sys.argv[1]
        rhyme = int(sys.argv[2])
    genFromFile(file, rhyme)
    
if __name__ == '__main__':
    main()