import re
import sys
import collections
from decimal import Decimal

f = open(sys.argv[1],"r")
contents = f.read()
f.close()
# print contents

ngramDict = {}
unigramDict = {}

# counts = dict()

def generate_ngrams(s,n):

    lookBackBuffer = []


    # Convert to lowercases
    s = s.lower()

    # Replace all punctuation with space then punctuation then space
    s = re.sub(r'[,]', ' , ', s)
    s = re.sub(r'[.]', ' . ', s)
    s = re.sub(r'[?]', ' ? ', s)
    s = re.sub(r'[!]', ' ! ', s)
    s = re.sub(r'[;]', ' ; ', s)
    s = re.sub(r'[:]', ' : ', s)
    s = s.replace('"', '',)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    ngramCount = 0
    count = 0
    ngramSize = 3
    previousNgramDict = None

    startBoolean = True #initially true for the very first <start> tag

    #the current token you are on of all the tokens
    for currToken in tokens:
        newNgram =''

        print "------------\nProcessing token " + currToken
        #
        print "lookBackBuffer " + str(lookBackBuffer)

        #Adding the <start> tag to beginning of sentences
        if (startBoolean == True):
            # print "Adding a start tag"
            lookBackBuffer.append('<start>')
            startBoolean = False #set to false after it is added

        #Adding the <end> tag when given ending punctuation
        if (currToken == '.' or currToken == '?' or currToken == '!'):
            currToken = '<end>'

        if previousNgramDict is not None:
            print "previus ngram dict exists, adding token " + currToken
            if currToken in previousNgramDict:
                print "previus token exists, count was " + previousNgramDict[currToken]
                previousNgramDict[currToken] += 1
            else:
                print "previus token did not exist, creating one"
                previousNgramDict[currToken] = 1

        lookBackBuffer.append(str(currToken))

        #If lookBackBuffer is the desired size, then create newNgram
        if len(lookBackBuffer) >= ngramSize-1:

            #Removing the first element of the lookBackBuffer if the buffer is size of desired ngram
            if len(lookBackBuffer) == ngramSize:
                print ("Buffer before deletion " + str(lookBackBuffer) + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                    + " ngramSize: " + str(ngramSize))
                del lookBackBuffer[0]
                print ("Buffer after removal of first element " + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                    + " ngramSize: " + str(ngramSize))

            #Creates the new ngram from the full look back buffer
            newNgram = " ".join(lookBackBuffer)

            print ("Joined newNgram = " + newNgram + " len(lookBackBuffer): " + str(len(lookBackBuffer)) + " ngramSize: " + str(ngramSize))

            print "new ngram after join= " + str(newNgram)

            #adding the new ngram to the dictionary and getting frequencies for it)

            if newNgram in ngramDict:
                print "incrementing ngram " + newNgram + " count"
                tokenDict = ngramDict[newNgram]
                if tokenDict is not None:
                    if '<frequency>' in tokenDict:
                        tokenDict['<frequency>'] += 1
                    else:
                        tokenDict['<frequency>'] = 1
                else:
                    tokenDict = { '<frequency>': 1 }
                    ngramDict[newNgram] = tokenDict
            else:
                print "adding ngram " + "|" + newNgram + "|" + " to ngramDict"
                tokenDict = { '<frequency>': 1 }
                ngramDict[newNgram] = tokenDict
                print ("Buffer after newNgram is added to ngramDict " + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                    + " ngramSize: " + str(ngramSize))

            #Save tokenDict for use with the next token
            previousNgramDict = ngramDict[newNgram]


        #if the current token is <end> clear the lookBackBuffer and make the next token the <start> tag
        if (currToken == '<end>'):
            print "currToken is an end"
            lookBackBuffer = [] #resetting lookBackBuffer
            previousNgramDict = None #resetting previousNgramDict
            startBoolean = True #insert <start> tag


    ngramFreqCount = 0

    for ngram, ngramValueDict in ngramDict.items():
        print "ngram key: " + ngram
        frequencyCount = ngramValueDict["<frequency>"]
        print "frequency count: " + str(frequencyCount)
        ngramFreqCount += frequencyCount
        print "ngramFreqCount count: " + str(ngramFreqCount) + " frequencyCount: " + str(frequencyCount)
    print "ngramFreqCount count: " + str(ngramFreqCount)

    for x in tokens:
        count+=1
        print 'Token Count = ' + str(count)
    print 'Token Count = ' + str(count)


    

    for token in tokens:
        if token in unigramDict:
            unigramDict[token] +=1
        else:
            unigramDict[token] = 1
    for key,value in unigramDict.items():
        # print str("value is = " + str(value) + " count is = " + str(count))
        value = Decimal(value)
        count = Decimal(count)
        probability = Decimal(value/count)
        # print str("probability is = " + str(probability))
        roundedProbability = round(probability,4)
        # print str("probability is = " + str(roundedProbability))

        unigramDict[key] = probability

        # print str("probability is = " + str(roundedProbability))
        # print str(key) + " => " + str(unigramDict[key])




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
