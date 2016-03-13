from nltk.corpus import wordnet as wn
import string
def visualize(type, O_Mat, tokens):
    ''' This function helps visualize the meaning of HMM states. It calculates
        the probability of each state emitting a noun, verb, and article '''
        
    # Check against the nouns in wordnet to count nouns
    if type == "noun":
        nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
        for state in range(0, len(O_Mat)):
            prob = 0
            for obs in range(0, len(O_Mat[0])):
                word = tokens[obs].translate(None, ".()?,:!")
                if word in nouns:
                    prob += O_Mat[state][obs]
            print "State " + str(state) + " Noun Prob: " + str(prob)
        return

    # Check against verbs in wordnet to count verbs
    if type == "verb":
        verbs = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
        for state in range(0, len(O_Mat)):
            prob = 0
            for obs in range(0, len(O_Mat[0])):
                word = tokens[obs].translate(None, ".()?,:!")
                if word in verbs:
                    prob += O_Mat[state][obs]
            print "State " + str(state) + " Verb Prob: " + str(prob)
        return

    # There are only 3 articles, check the probability of their emission
    if type == "article":
        art = ["a", "an", "the"]
        for state in range(0, len(O_Mat)):
            prob = 0
            for obs in range(0, len(O_Mat[0])):
                word = tokens[obs].translate(None, ".()?,:!")
                if word in art:
                    prob += O_Mat[state][obs]
            print "State " + str(state) + " Art Prob: " + str(prob)
        return

