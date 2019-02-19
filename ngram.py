# -*- coding: utf-8 -*-
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
#####
##### Brandon Chin
##### Tuesday, February 19th, 2019
##### CMSC 416 - Natural Language Processing
##### Programming Assignment 2 - Ngram Modeling
#####
##### 1. The Problem
##### Design and implement a Python3 program called ngram.py, that will learn an N-gram language model from an arbitrary number of plain text files.
##### The program should generate a given number of sentences based on that N-gram model.
#####
##### 2. Example Input/Output
#####
##### [Input] python ngram.py 3 10 theMenofBoru.Jack.A.Nelson.txt theOsbornes.E.F.Benson.txt blackIvory.R.M.Ballantyne.txt
##### [Output] Command line settings: ngram.py n = 3 m = 10
##### [Output] Sentence number #1:
##### [Output] bradley has another map.
##### [Output] Sentence number #2:
##### [Output] harold agreed with you about things of far greater import , had got some nice thick pieces of raw flesh , so plausible through its naturalness , that he's in the slavemarket of zanzibar.
##### [Output] Sentence number #3:
##### [Output] white ivory do come from the source of american power and the rich tropical foliage of that distressing species.
##### [Output] Sentence number #4:
##### [Output] 'twere better to enjoy a picture , i don't mind if i am over things like that.
##### [Output] Sentence number #5:
##### [Output] today she could see that , whenever he had acted on no secret and mysterious tips from the bush and poured a small antelope , which soon reduced them to go through.
##### [Output] Sentence number #6:
##### [Output] down in a style that has been out : savages have no money , and campequipage into bundles of a carter's horse , and mopped his streaming forehead with a band of manganja men and the awful cruelties that goes the pace of thatlor’ ,
#####          my dear sir , don't be a woman short at dinner and giving a little to doan' sole hisself to him had come down , ” claude turned to harold and his flesh was deeply lacerated by the slavers.
##### [Output] Sentence number #7:
##### [Output] d'ye think it right to a thing in a day on the chiefnot very heavily , and reptiles , all that in this one defeat to get in return is this consistent.
##### [Output] Sentence number #8:
##### [Output] providence , however , turned the corrugated building into a coil which hung down their backs and limbs.
##### [Output] Sentence number #9:
##### [Output] contrast them with an appetite that was biondinetti all over , ” it required no gifts of perception whatever to their satisfaction , as they pleased.
##### [Output] Sentence number #10:
##### [Output] “but claude , and wherever you put on.
#####
##### 3. Algorithm
#####
##### #1. Read the arguments from the command line to determine number of sentences (m) using the specified size ngram (n) and the text files to build your corpus
#####
##### #2. Break each word/punctuation into a token, removing certain punctuations and record the frequency of each token, also inserting <start> at the
#####     beginning of the sentence, and <end> at the end of a sentence (ending punctuation)
#####
##### #3. With frequency recorded, generate probabilities for the words that appear after the word that you are currently on
#####
##### #4. Build the sentences based on the probabilities and a random generated number to help you choose the following word, thereby building the sentence
#####
##### #5. Continue until reaching an ending punctuation, which should end the sentence, and then begin building a new sentence
#####
##### #6. Do this for the specified number of sentences (m) using the specified size ngram (n) which is determined in the command line argument
#####
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################


import re
import sys
import collections
from decimal import Decimal
from random import *

ngramDict = {}

def main():

    print("This program generates random sentences based on an Ngram model.")
    print("Created by Brandon Chin")

    n = 3

    numberOfArgs = len(sys.argv)
    #print "there are " + str(numberOfArgs) + " arguments"
    if numberOfArgs < 3:
        # print "Usage: " + sys.argv[0] + " n m <filenames> where n = number of grams, m = number of sentences"
        exit(1)

    n = int(sys.argv[1])
    if n < 2:
        print "n must be 2 or greater"
        exit(1)

    numberOfSentences = sys.argv[2]
    numberOfArgs -= 1 # adjust
    argsIndex = 3

    print("Command line settings: " + "ngram.py " + "n = " + str(n) + " m = " + str(numberOfSentences))

    while argsIndex <= numberOfArgs:
        loadFileName = sys.argv[argsIndex]
        # print "opening file " + loadFileName
        f = open(loadFileName,"r")
        contents = f.read()
        f.close()
        generate_ngrams(contents, n, ngramDict)
        argsIndex += 1


    generate_probabilities(ngramDict)

    #print "n is: " + str(n)
    if n > 2:
        # with n is greater than 2, can look at bigrams or higher so picking <start> <something>
        # can be done - get a list of all ngrams that have <start>
        startingnGramsList = findAllnGramsWithStart(ngramDict)
    else:
        startingnGramsList = None

    index = 0
    while index < (int(numberOfSentences)):
        # pick a random starting ngram
        if startingnGramsList is not None:
            ngramIndex = randint( 0, len(startingnGramsList) - 1)
            #print "picked index " + str(ngramIndex)
            startingnGram = startingnGramsList[ngramIndex]
        else:
            ngramKeys = ngramDict.keys()
            ngramIndex = randint( 0, len(ngramKeys))
            startingnGram = ngramKeys[ngramIndex]

        (newSentence, newSentenceLength) = generate_sentences(ngramDict, startingnGram)
        if( newSentenceLength > 2 ):
            print ("Sentence number #" + str(index + 1) + ": ")
            print newSentence
            index += 1


    # print (generate_sentences(ngramDict))


    # counts = dict()

def generate_ngrams(s, n, ngramDict):
    # print "loading in contents"
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
    s = s.replace('-', '',)

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
        #print "ngram key: " + ngram
        frequencyCount = ngramValueDict["<frequency>"]
        #print "frequency count: " + str(frequencyCount)
        ngramFreqCount += frequencyCount
        #print "ngramFreqCount count: " + str(ngramFreqCount) + " frequencyCount: " + str(frequencyCount)
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
            if followingToken != '<frequency>':
                #print 'tokenCount is ' + str(tokenCount)
                probability = Decimal(tokenCount/denominator)
                #print 'probability is = ' + str(probability)
                tokenDict[followingToken] = probability
                #print str(tokenDict[followingToken])
        #print "generated probabilities for ngram " + ngram + " token dict is " + str(tokenDict)


def findAllnGramsWithStart(ngramDict):
    #print "finding ngrams with start"
    ngramsWithStartList = []
    currentNGram = None

    # Find an ngram which begins with a <start> tag
    for ngram, tokenDict in ngramDict.items():
        #print "looking at ngram " + ngram
        ngramWordList = ngram.split()

        if ngramWordList[0] == '<start>':
            #print ("found starting ngram: " + ngram)
            ngramsWithStartList.append(ngram)

    #print "found these start ngrams " + str(ngramsWithStartList)
    return ngramsWithStartList

    # generate sentences

def generate_sentences(ngramDict, startingnGram):
    sentenceString =''
    sentenceEnd = False
    ngram = ''
    sentenceLength = 0

    ngram = startingnGram
    tokenDict = ngramDict[ngram]
    ngramWordList = ngram.split()
    # print ("sentence now: ") + sentenceString;

    ngramWordListCount = len(ngramWordList)
    for ngramToken in ngramWordList:
        if ngramToken != '<start>':
            if len(sentenceString) != 0:
                sentenceString += " "
            sentenceString += ngramToken

    # print ("sentence now: ") + sentenceString;

    randomNumber = random()
    #print "random number is: " + str(randomNumber)
    while sentenceEnd is False:
        #print "fetching tokenDict for ngram: " + ngram
        tokenDict = ngramDict[ngram]
        #print "tokenDict is: " + str(tokenDict)

        # selecting amongst this ngrams's follow on words
        sumOfProbabilities = 0
        previousWord = None
        chosenToken = None

        tokenKeys = tokenDict.keys()
        tokenCount = len(tokenKeys)
        tokenIndex = 0

        while chosenToken is None:
            randomNumber = random()

            # make sure tokenIndex
            if tokenIndex >= tokenCount:
                chosenToken = previousWord
                break

            followingToken = tokenKeys[tokenIndex]

            if followingToken != '<frequency>':
                tokenProbability = tokenDict[followingToken]
                # print "followingToken is: " + followingToken + " probability is : " + str(tokenProbability)
                sumOfProbabilities += Decimal(tokenProbability)

                # print "sum of probabilities now " + str(sumOfProbabilities)

                if sumOfProbabilities < randomNumber:
                    # selection not yet reached
                    # print "setting previousWord to: " + followingToken
                    previousWord = followingToken
                else:
                    # selection should be the previously token unless there isn't one
                    if previousWord is None:
                        # print "there was no previous word, choosing token: " + followingToken
                        chosenToken = followingToken
                        break
                    else:
                        #print "setting chosen token to previous word: " + previousWord
                        chosenToken = previousWord
            tokenIndex += 1

            # if the tokenIndex is now out of range, then choose the last token encountered
            if tokenIndex >= tokenCount:
                # out of other possibilities
                if previousWord is not None:
                    chosenToken = previousWord

        if chosenToken is None:
            # didn't choose one
            # print "did not choose one, previous word was " + previousWord + " and token Dict is " + str(tokenDict)
            chosenToken = '<end>'

        if chosenToken is '<frequency>':
            # print "chosen token can never be frequency"
            raise("internal error")

        #print "out of iterating through tokenDict items, chosenToken is " + chosenToken

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
            sentenceLength += 1
            #print "new ngram is " + ngram
            #print ngram + " "
        else:
            sentenceEnd = True
            sentenceString += "."

        #print "sentence currently: " + sentenceString

    return (sentenceString, sentenceLength)

if __name__ == "__main__":
    main()
