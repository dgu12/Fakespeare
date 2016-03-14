from nltk.corpus import wordnet as wn
import string
def visualize(O_Mat, tokens):
    ''' This function helps visualize the meaning of HMM states. It calculates
        the probability of each state emitting a noun, verb, and article '''

    # Check against the nouns in wordnet to count nouns
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in nouns:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Noun Prob: " + str(prob)
    print '\n'

    # Check against verbs in wordnet to count verbs
    verbs = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in verbs:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Verb Prob: " + str(prob)
    print '\n'

    # There are only 3 articles, check the probability of their emission

    art = ["a", "an", "the"]
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in art:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Art Prob: " + str(prob)
    print '\n'

    # Visualize adjectives
    adj = {x.name().split('.', 1)[0] for x in wn.all_synsets('a')}
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in adj:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Adj Prob: " + str(prob)
    print '\n'
    # Visualize adverbs
    adv = {x.name().split('.', 1)[0] for x in wn.all_synsets('r')}
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in adv:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Adv Prob: " + str(prob)
    print '\n'
    # Visualize adj sat
    adjS = {x.name().split('.', 1)[0] for x in wn.all_synsets('s')}
    for state in range(0, len(O_Mat)):
        prob = 0
        for obs in range(0, len(O_Mat[0])):
            word = tokens[obs].translate(None, ".()?,:!")
            if word in adjS:
                prob += O_Mat[state][obs]
        print "State " + str(state) + " Adj Sat Prob: " + str(prob)

    return
