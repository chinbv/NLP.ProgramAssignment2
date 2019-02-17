import re
import sys
import collections

f = open(sys.argv[1],"r")
contents = f.read()
f.close()
# print contents

ngramDict = {}
# tokenDict = {}

# counts = dict()

def generate_ngrams(s,n):

    # Convert to lowercases
    s = s.lower()

    # Replace all punctuation with space then punctuation then space
    s = re.sub(r'[,]', ' , ', s)
    s = re.sub(r'[.]', ' . ', s)
    s = re.sub(r'[?]', ' ? ', s)
    s = re.sub(r'[!]', ' ! ', s)
    s = re.sub(r'[;]', ' ; ', s)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    count = 0

    for currToken in tokens:

        if currToken in ngramDict:
            tokenDict = ngramDict[currToken]
            if tokenDict is not None:
                if '<frequency>' in tokenDict:
                    tokenDict['<frequency>'] += 1
                else:
                    tokenDict['<frequency>'] = 1
            else:
                tokenDict = { '<frequency>': 1 }
                ngramDict[currToken] = tokenDict
        else:
            tokenDict = { '<frequency>': 1 }
            ngramDict[currToken] = tokenDict

        # print frequencyDict.keys()
        print ngramDict.values()

    # print tokenDict

    # print 'Tokens are = ' + str(tokens)

    for x in tokens:
        count+=1
        # print 'Token Count = ' + str(count)
    print 'Token Count = ' + str(count)


    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    # ngrams = zip(*[tokens[i:] for i in range(n)])
    # return [" ".join(ngram) for ngram in ngrams]

    return ngramDict

    #Build the dictionary with tokens as keys and frequency as values


# contents = "Natural-language processing (NLP) is an area of computer science " \
#     "and artificial intelligence concerned with the interactions " \
#     "between computers and human (natural) languages."

# contents = "my, oh my, i wish i had 100 dollars." \

print (generate_ngrams(contents, n=10))
