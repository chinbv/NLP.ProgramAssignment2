import re
import sys
import collections
from decimal import Decimal
from random import *

ngramDict = {}

def main():

    # f = open(sys.argv[1],"r")
    # contents = f.read()
    # f.close()

    n = None


    for arg in sys.argv[1:]:
        n = sys.argv[1]
        numberOfSentences = sys.argv[2]
        f = open(sys.argv[3],"r")
        contents = f.read()
        f.close()

        generate_ngrams(contents, n, ngramDict)
        generate_probabilities(ngramDict)
        for i in range(int(numberOfSentences)):
            index = i + 1
            print ("Sentence number #" + str(index) + ": ")
            print (generate_sentences(ngramDict))

    # print (generate_sentences(ngramDict))


    # counts = dict()

def generate_ngrams(s, n, ngramDict):
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
    ngramSize = int(n)
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


def generate_probabilities(ngramDict):
    ngramFreqCount = 0


    for ngram, ngramValueDict in ngramDict.items():
        # print "ngram key: " + ngram
        frequencyCount = ngramValueDict["<frequency>"]
        # print "frequency count: " + str(frequencyCount)
        ngramFreqCount += frequencyCount
        # print "ngramFreqCount count: " + str(ngramFreqCount) + " frequencyCount: " + str(frequencyCount)
    # print "ngramFreqCount count: " + str(ngramFreqCount)

    # for x in tokens:
    #     count+=1
        # print 'Token Count = ' + str(count)

    #print 'Token Count = ' + str(count)


    #print "-------------\ncalculating probabilities"
    for ngram, tokenDict in ngramDict.items():
        denominator = Decimal(tokenDict['<frequency>'])
        #print 'denominator is ' + str(denominator)
        for followingToken, tokenCount in tokenDict.items():
            if followingToken is not '<frequency>':
                #print 'tokenCount is ' + str(tokenCount)
                probability = Decimal(tokenCount/denominator)
                #print 'probability is = ' + str(probability)
                tokenDict[followingToken] = probability
                #print str(tokenDict[followingToken])
        #print "generated probabilities for ngram " + ngram + " token dict is " + str(tokenDict)



    # generate sentences

def generate_sentences(ngramDict):
    sentenceString =''
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


    sentenceString += ngramWordList[1]

    print ("sentence now: ") + sentenceString;

    randomNumber = random()
    print "random number is: " + str(randomNumber)
    while sentenceEnd is False:
        print "fetching tokenDict for ngram: " + ngram
        tokenDict = ngramDict[ngram]
        print "tokenDict is: " + str(tokenDict)

        # selecting amongst this ngrams's follow on words
        sumOfProbabilities = 0
        previousWord = None
        chosenToken = None

        tokenKeys = tokenDict.keys()
        tokenCount = len(tokenKeys)
        tokenIndex = 0

        while chosenToken is None:
            if tokenIndex == tokenCount:
                raise("tokenIndex exceeded range error")

            followingToken = tokenKeys[tokenIndex]

            if followingToken != '<frequency>':
                tokenProbability = tokenDict[followingToken]
                print "followingToken is: " + followingToken + " probability is : " + str(tokenProbability)
                sumOfProbabilities += Decimal(tokenProbability)

                print "sum of probabilities now " + str(sumOfProbabilities)

                if sumOfProbabilities < randomNumber:
                    # selection not yet reached
                    print "setting previousWord to: " + followingToken
                    previousWord = followingToken
                else:
                    # selection should be the previously token unless there isn't one
                    if previousWord is None:
                        print "there was no previous word, choosing token: " + followingToken
                        chosenToken = followingToken
                        break
                    else:
                        print "setting chosen token to previous word: " + previousWord
                        chosenToken = previousWord
            tokenIndex += 1

        if chosenToken is None:
            # didn't choose one
            print "did not choose one, previous word was " + previousWord + " and token Dict is " + str(tokenDict)
            raise("internal error")

        if chosenToken is '<frequency>':
            print "chosen token can never be frequency"
            raise("internal error")

        print "out of iterating through tokenDict items, chosenToken is " + chosenToken

        # if previousWord == None:
        #     if followingToken is not '<frequency>':
        #         print "previous word doesn't exist, setting chosenToken to " + followingToken
        #         chosenToken = followingToken
        #     else:
        #         print "only found <frequency>, something wrong, look at this tokenDict:\n" + str(tokenDict)
        # else:
        #     chosenToken = previousWord

        if chosenToken != '<end>':
            sentenceString += " " + chosenToken
            # add new token to ngramWordList and remove the first one to develop new ngram
            ngramWordList.append(chosenToken)
            del ngramWordList[0]

            ngram = ' '.join(ngramWordList)
            print "new ngram is " + ngram
        else:
            sentenceEnd = True

        print "sentence currently: " + sentenceString

    return sentenceString

if __name__ == "__main__":
    main()
