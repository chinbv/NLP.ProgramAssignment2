import re
import sys
import collections
from decimal import Decimal
from random import *

f = open(sys.argv[1],"r")
contents = f.read()
f.close()
# print contents

ngramDict = {}

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
    s = re.sub(r'[:]', ' : ', s)
    s = s.replace('"', '',)

    # Replace new lines with spaces
    s = re.sub(r'\s+', ' ', s)

    # Break sentence into the tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    ngramCount = 0
    count = 0
    ngramSize = n
    previousNgramDict = None
    lookBackBuffer = []
    ngramBuffer = [] * ngramSize

    startBoolean = True #initially true for the very first <start> tag

    #the current token you are on of all the tokens
    #
    for currToken in tokens:
        newNgram =''

        # print "------------\nProcessing token " + currToken

        # print "lookBackBuffer " + str(lookBackBuffer)

        #Adding the <start> tag to beginning of sentences
        if (startBoolean == True):
            # print "Adding a start tag"
            lookBackBuffer.append('<start>')
            startBoolean = False #set to false after it is added

        #Adding the <end> tag when given ending punctuation
        if (currToken == '.' or currToken == '?' or currToken == '!'):
            currToken = '<end>'

        if previousNgramDict is not None:
            # print "previus ngram dict exists, adding token " + currToken
            if currToken in previousNgramDict:
                # print "previus token exists, count was " + previousNgramDict[currToken]
                previousNgramDict[currToken] += 1
            else:
                # print "previus token did not exist, creating one"
                previousNgramDict[currToken] = 1

        lookBackBuffer.append(str(currToken))

        #If lookBackBuffer is the desired size, then create newNgram
        if len(lookBackBuffer) >= ngramSize-1:

            #Removing the first element of the lookBackBuffer if the buffer is size of desired ngram
            if len(lookBackBuffer) == ngramSize:
                # print ("Buffer before deletion " + str(lookBackBuffer) + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                #     + " ngramSize: " + str(ngramSize))
                del lookBackBuffer[0]
                # print ("Buffer after removal of first element " + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                #     + " ngramSize: " + str(ngramSize))

            #Creates the new ngram from the full look back buffer
            newNgram = " ".join(lookBackBuffer)

            # print ("Joined newNgram = " + newNgram + " len(lookBackBuffer): " + str(len(lookBackBuffer)) + " ngramSize: " + str(ngramSize))
            #
            # print "new ngram after join= " + str(newNgram)

            #adding the new ngram to the dictionary and getting frequencies for it)

            if newNgram in ngramDict:
                # print "incrementing ngram " + newNgram + " count"
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
                # print "adding ngram " + "|" + newNgram + "|" + " to ngramDict"
                tokenDict = { '<frequency>': 1 }
                ngramDict[newNgram] = tokenDict
                # print ("Buffer after newNgram is added to ngramDict " + " len(lookBackBuffer): " + str(len(lookBackBuffer))
                #     + " ngramSize: " + str(ngramSize))

            #Save tokenDict for use with the next token
            previousNgramDict = ngramDict[newNgram]


        #if the current token is <end> clear the lookBackBuffer and make the next token the <start> tag
        if (currToken == '<end>'):
            # print "currToken is an end"
            lookBackBuffer = [] #resetting lookBackBuffer
            previousNgramDict = None #resetting previousNgramDict
            startBoolean = True #insert <start> tag

    # END FOR LOOP

    ngramFreqCount = 0


    for ngram, ngramValueDict in ngramDict.items():
        # print "ngram key: " + ngram
        frequencyCount = ngramValueDict["<frequency>"]
        # print "frequency count: " + str(frequencyCount)
        ngramFreqCount += frequencyCount
        # print "ngramFreqCount count: " + str(ngramFreqCount) + " frequencyCount: " + str(frequencyCount)
    # print "ngramFreqCount count: " + str(ngramFreqCount)

    for x in tokens:
        count+=1
        # print 'Token Count = ' + str(count)
    # print 'Token Count = ' + str(count)


    for ngram, tokenDict in ngramDict.items():
        denominator = Decimal(tokenDict['<frequency>'])
        # print 'denominator is ' + str(denominator)
        for followingToken, tokenCount in tokenDict.items():
            if followingToken is not '<frequency>':
                # print 'tokenCount is ' + str(tokenCount)
                probability = Decimal(tokenCount/denominator)
                # print 'probability is = ' + str(probability)
                tokenDict[followingToken] = probability
                # print str(tokenDict[followingToken])

    sentenceString =''
    sumOfProbabilities = 0
    previousWord = None
    chosenToken = None
    sentenceEnd = False
    currentNGram = None;
    ngram = ''

    # Find an ngram which begins with a <start> tag
    for ngram, tokenDict in ngramDict.items():
        ngramWordList = ngram.split()
        # print "randomNumber is = " + str(randomNumber)

        if ngramWordList[0] == '<start>':
            # print ("found starting ngram: " + ngram)
            currentNGram = ngram
            break


    sentenceString += ngram
    # print ("sentence now: ") + sentenceString;

    randomNumber = random()
    while sentenceEnd is False:
        # print "fetching tokenDict"
        tokenDict = ngramDict[ngram]
        sumOfProbabilities = 0
        for followingToken, tokenProbability in tokenDict.items():
            if followingToken is not '<frequency>':
                # print "followingToken is " + followingToken
                sumOfProbabilities += Decimal(tokenProbability)
                if sumOfProbabilities > randomNumber:
                    previousWord = followingToken
                    # print "previousWord is " + previousWord

        if previousWord == None:
            # print "previous word doesn't exist, setting chosenToken to " + followingToken
            chosenToken = followingToken
        else:
            chosenToken = previousWord

        sentenceString += " " + chosenToken
        # add new token to ngramWordList and remove the first one to develop new ngram
        ngramWordList.append(chosenToken)
        del ngramWordList[0]

        ngram = ' '.join(ngramWordList)
        # print "new ngram is " + ngram

        if chosenToken == '<end>':
            sentenceEnd = True

        # print "sentenceString now " + sentenceString



    return sentenceString

# contents = "my, oh my, i wish i had 100 dollars." \

for i in range(0, 10):
    print (generate_ngrams(contents, n=4))
