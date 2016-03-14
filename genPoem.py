from hyphen import Hyphenator
import numpy as np
import random
import sys
from visualize import *
from rhyme import *

''' This file contains functions for generating poems from an HMM description
'''

def hmmGenerate(A_Mat, O_Mat, tokens, startP = None):
    ''' Generates a poem from a HMM's A matrix and O matrix
        Inputs:
            A_Mat: np matrix representing state transition probabilities
            O_Mat: np matrix representing observation emission probabilities
            tokens: Array of words, used to translate tokens into words
            *startP: Optional array of start state probabilities
    '''
    # Allows you prompt the user to generate more poems
    user_input = 'y'
    while (user_input != 'n'):
        # pyHyphen object that allows you to separate words into syllables
        h_en = Hyphenator('en_US')
        numStates = len(A_Mat)
        numObs = np.shape(O_Mat)[1]
        state = 0
        statePath = []
        # If no start probs, assume uniform start distribution
        if startP == None:
            state = random.randint(0, numStates-1)
        else:
            # Use startP to determine the start base
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
        # A sonnet is 14 lines
        for l in range(0,14):
            numSyl = 0
            line = []
            stateTemp = [state]
            # Keep number of syllables per line about 10
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
                            # Capitalize I
                            if tokens[ind] == "i":
                                line.append("I")
                            else:
                                line.append(tokens[ind])
                        # Capitalize after ending punctuation
                        if tokens[ind].endswith(".") or \
                            tokens[ind].endswith("?") or \
                            tokens[ind].endswith("!"):
                            capitalize = True
                        # Default to one syllable
                        if len(h_en.syllables(unicode(tokens[ind]))) == 0:
                            numSyl += 1
                        else:
                            numSyl += len(h_en.syllables(unicode(tokens[ind])))
                        break
                    ind += 1
                if numSyl < 10:
                    # Transition to the next state
                    prob = random.random()
                    ind = 0
                    sumP = 0
                    while ind < numStates:
                        sumP += A_Mat[state][ind]
                        if sumP > prob:
                            stateTemp.append(ind)
                            state = ind
                            break
                        ind += 1
            poem.append(line)
            statePath.append(stateTemp)

        #Print poem
        for line in poem:
            print ' '.join(line)
        print '\n'

        # Verbose option to print analytics
        if user_input == 'v':
            print 'State sequence'
            for l in statePath:
                print l
            print '\n'

            # Print part of speech visualization info
            visualize( O_Mat, tokens)

        # Prompt to generate more poems
        user_input = raw_input('Generate a another poem? [y/n/v]')

def genFromFile(f, rhyme):
    data = open(f)
    d
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
        visualize(O_Mat, tokens)

def main():
    ''' Run this program from the command to generate a poem from an HMM 
        train file'''
    if len(sys.argv) != 3:
        # Use 1 to generate an unrhyming poem
        # Use 0 to generate a rhyming poem
        print 'Usage: python', sys.argv[0], \
                '[file name] [1 - naive, 0 - rhyme]'
        return -1
    else:
        file = sys.argv[1]
        rhyme = int(sys.argv[2])
    genFromFile(file, rhyme)
    
if __name__ == '__main__':
    main()