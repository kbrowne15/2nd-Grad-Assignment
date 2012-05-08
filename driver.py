#!/usr/bin/python

import sys
import math
import time
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node

#################################################
# document
#
#	A class to hold all the document information
#	and the body of the documentation
#################################################
class document:
  def __init__(self):
    self.topics = ""
    self.lewisSplit = ""
    self.newId = -1
    self.date = ""
    self.tags = []
    self.places = []
    self.people = []
    self.orgs = []
    self.exchanges = []
    self.author = ""
    self.dateline = ""
    self.title = ""
    self.body = ""
  
  def addTag(self, tagIn):
    self.tags.append(tagIn)
  def addPlace(self, placeIn):
    self.places.append(placeIn)
  def addPeople(self, peopleIn):
    self.people.append(peopleIn)
  def addOrg(self, orgIn):
    self.orgs.append(orgIn)
  def addExchange(self, exchangeIn):
    self.exchanges.append(exchangeIn)

#################################################
# words in document
#
#	A class to hold all the words in one document
#	and the tag that classifies the document
#################################################
class wordsInDocument:
  def __init__(self):
    self.tag = ""
    self.words = []
 
  def addWord(self, wordIn):
    self.words.append(wordIn)

#################################################
# probability
#
#	A class to hold a term and the probability of
#	its appearence in the documents
#################################################
class probability:
  def __init__(self):
    self.vocabTerm = ""
    self.prob = []
  def addProb(self, probIn):
    self.prob.append(probIn)

#################################################
# max score doc
#
#	A class to hold the actual tag that classifies
#	the document, the tag that our system guessed,
# and the highest score which came from 
# comparing the guessed tag with the doc
#################################################
class maxScoreDoc:
  def __init__(self):
    self.actualTag = ""
    self.guessedTag = ""
    self.score = -1

#################################################
# extract everything for training
#
#	A function which goes through all of the 
# documents that were read in. If the document
# is a training document and it has a tag that
# match one of the tags we are training for, then
# we extract the words from the document, put
# them in a dictionary, and put them in a class
# that contains all the words in all of the 
# documents that match the tag. The number of
# training documents along with the number of
# documents for each tag are recorded and 
# returned.
#################################################
def extractEverythingForTraining(classes, documents):
  vocabularyWord = {}
  vocabularyNum = {}
  numDocs = 0
  vocabIndex = 0
  numDocsInClass = []
  wordsInTheDocuments = [wordsInDocument() for i in range(len(classes))]
  for i in range(len(classes)):
    wordsInTheDocuments[i].tag = classes[i]
    numDocsInClass.append(0)

  #iterate through all documents read in from the files
  for i in range(len(documents)):
    j = 0
    notFound = True
    #go through tags of documents to see if they match the tags we are training for
    #stop once the first set of matching tags has been found
    while j < len(documents[i].tags) and notFound:
      index1 = 0
      #go through classes we are training for to see if the tags match
      #stop once the first set of matching tags has been found
      while index1 < len(classes) and notFound:
        if documents[i].tags[j] == classes[index1]:
          notFound = False
          if documents[i].lewisSplit == "TRAIN": 
            numDocs += 1
            numDocsInClass[index1] += 1
            title = documents[i].title
            tempTitle = ""
            #Go through the whole title to extract all the words in the title
            for w in range(len(title)):
              if (title[w] >= 'a' and title[w] <= 'z') or title[w] == "'" or title[w] == "-":
                tempTitle += title[w]
              #if the character is capitalize, make it lower case
              elif(title[w] >= 'A' and title[w] <= 'Z'):
                tempTitle += title[w].lower()
              #the word being built is finished
              elif title[w] == ' ' or title[w] == '\r' or title[w] == '\n' \
                   or title[w] == '\t' or title[w] == '/':
                #the word is not empty and is not a simple word
                if tempTitle != '' and len(tempTitle) > 3:
                  wordsInTheDocuments[index1].addWord(tempTitle)
                  #if the word is not already in the vocabulary, add it
                  if not(vocabularyWord.has_key(tempTitle)):
                    vocabularyWord[tempTitle] = vocabIndex
                    vocabularyNum[vocabIndex] = tempTitle
                    vocabIndex += 1
                tempTitle = '';
            #the word is not empty and is not a simple word
            if tempTitle != '' and len(tempTitle) > 3:
              wordsInTheDocuments[index1].addWord(tempTitle)
              #if the word is not already in the vocabulary, add it
              if not(vocabularyWord.has_key(tempTitle)):
                vocabularyWord[tempTitle] = vocabIndex
                vocabularyNum[vocabIndex] = tempTitle
                vocabIndex += 1
                    
                     
            dateline = documents[i].dateline
            tempDateline = ""
            #Go through the whole dateline to extract all the words in the dateline
            for w in range(len(dateline)):
              if (dateline[w] >= 'a' and dateline[w] <= 'z') or dateline[w] == "'" \
                  or dateline[w] == "-":
                tempDateline += dateline[w]
              #if the character is capitalize, make it lower case
              elif(dateline[w] >= 'A' and dateline[w] <= 'Z'):
                tempDateline += dateline[w].lower()
              #the word being built is finished
              elif dateline[w] == ' ' or dateline[w] == '\r' or dateline[w] == '\n' \
                   or dateline[w] == '\t' or dateline[w] == '/' or ((w + 1) >= len(dateline)):
                #the word is not empty and is not a simple word
                if tempDateline != '' and len(tempDateline) > 3:
                  wordsInTheDocuments[index1].addWord(tempDateline)
                  #if the word is not already in the vocabulary, add it
                  if not(vocabularyWord.has_key(tempDateline)):
                    vocabularyWord[tempDateline] = vocabIndex
                    vocabularyNum[vocabIndex] = tempDateline
                    vocabIndex += 1
                tempDateline = '';
            #the word is not empty and is not a simple word
            if tempDateline != '' and len(tempDateline) > 3:
              wordsInTheDocuments[index1].addWord(tempDateline)
              #if the word is not already in the vocabulary, add it
              if not(vocabularyWord.has_key(tempDateline)):
                vocabularyWord[tempDateline] = vocabIndex
                vocabularyNum[vocabIndex] = tempDateline
                vocabIndex += 1

 
            body = documents[i].body
#            print "Body: " + body
            tempBody = ""
            #Go through the whole body to extract all the words in the body
            for w in range(len(body)):
              if (body[w] >= 'a' and body[w] <= 'z') or body[w] == "'" or body[w] == "-":
                tempBody += body[w]
              #if the character is capitalize, make it lower case
              elif(body[w] >= 'A' and body[w] <= 'Z'):
                tempBody += body[w].lower()
              #the word being built is finished
              elif body[w] == ' ' or body[w] == '\r' or body[w] == '\n' \
                   or body[w] == '\t' or body[w] == '/' or ((w + 1) >= len(body)):
                #the word is not empty and is not a simple word
                if tempBody != '' and len(tempBody) > 3:
                  wordsInTheDocuments[index1].addWord(tempBody)
                  #if the word is not already in the vocabulary, add it
                  if not(vocabularyWord.has_key(tempBody)):
                    vocabularyWord[tempBody] = vocabIndex
                    vocabularyNum[vocabIndex] = tempBody
                    vocabIndex += 1
                tempBody = '';
            #the word is not empty and is not a simple word
            if tempBody != '' and len(tempBody) > 3:
              wordsInTheDocuments[index1].addWord(tempBody)
              #if the word is not already in the vocabulary, add it
              if not(vocabularyWord.has_key(tempBody)):
                vocabularyWord[tempBody] = vocabIndex
                vocabularyNum[vocabIndex] = tempBody
                vocabIndex += 1
 
        index1 += 1
      j += 1

  #for i in range(len(vocabularyWord)):
  #  print str(vocabularyWord[vocabularyNum[i]]) + ":  " + vocabularyNum[i]

  return vocabularyWord, vocabularyNum, numDocs, numDocsInClass, wordsInTheDocuments

#################################################
# extract tokens from doc
#
#	A function which goes through all of the 
# documents that were read in. If the document
# is a test document and it has a tag that
# match one of the tags we are training for, then
# we extract the words from the document and put 
# them in a class along with the tag that 
# corresponds to the document.
#################################################
def extractTokensFromDoc(classes, documents, vocabularyWord):
  tokensInTheDocuments = []

  #iterate through all documents read in from the files
  for i in range(len(documents)):
    j = 0
    notFound = True
    #go through tags of documents to see if they match the tags we are training for
    #stop once the first set of matching tags has been found
    while j < len(documents[i].tags) and notFound:
      index1 = 0
<<<<<<< HEAD
      
      #go through classes we are training for to see if the tags match
      #stop once the first set of matching tags has been found
=======
>>>>>>> 95e29febe3ef2309a7004ac90f609eea38c73aad
      while index1 < len(classes) and notFound:
        if documents[i].tags[j] == classes[index1]:
          notFound = False
          if documents[i].lewisSplit == "TEST": 
            index = 0
            tempTokensDocument = wordsInDocument()
            tempTokensDocument.tag = classes[index1]
            title = documents[i].title
            tempTitle = ""
            #Go through the whole title to extract all the words in the title
            for w in range(len(title)):
              if (title[w] >= 'a' and title[w] <= 'z') or title[w] == "'" or title[w] == "-":
                tempTitle += title[w]
              #if the character is capitalize, make it lower case
              elif(title[w] >= 'A' and title[w] <= 'Z'):
                tempTitle += title[w].lower()
              #the word being built is finished
              elif title[w] == ' ' or title[w] == '\r' or title[w] == '\n' \
                   or title[w] == '\t' or title[w] == '/':
                #if the word is in the vocabulary, add it to the words in the doc
                if vocabularyWord.has_key(tempTitle):
                  tempTokensDocument.addWord(tempTitle)
                tempTitle = '';
            
            #if the word is in the vocabulary, add it to the words in the doc
            if vocabularyWord.has_key(tempTitle):
                tempTokensDocument.addWord(tempTitle)

            dateline = documents[i].dateline
            tempDateline = ""
            #Go through the whole dateline to extract all the words in the dateline
            for w in range(len(dateline)):
              if (dateline[w] >= 'a' and dateline[w] <= 'z') or dateline[w] == "'" \
                  or dateline[w] == "-":
                tempDateline += dateline[w]
              #if the character is capitalize, make it lower case
              elif(dateline[w] >= 'A' and dateline[w] <= 'Z'):
                tempDateline += dateline[w].lower()
              #the word being built is finished
              elif dateline[w] == ' ' or dateline[w] == '\r' or dateline[w] == '\n' \
                   or dateline[w] == '\t' or dateline[w] == '/' or ((w + 1) >= len(dateline)):
                #if the word is in the vocabulary, add it to the words in the doc   
                if vocabularyWord.has_key(tempDateline):
                  tempTokensDocument.addWord(tempDateline)
                tempDateline = '';
            #if the word is in the vocabulary, add it to the words in the doc
            if vocabularyWord.has_key(tempDateline):
              tempTokensDocument.addWord(tempDateline)
 
            body = documents[i].body
            tempBody = ""
            #Go through the whole body to extract all the words in the body
            for w in range(len(body)):
              if (body[w] >= 'a' and body[w] <= 'z') or body[w] == "'" or body[w] == "-":
                tempBody += body[w]
              #if the character is capitalize, make it lower case
              elif(body[w] >= 'A' and body[w] <= 'Z'):
                tempBody += body[w].lower()
              #the word being built is finished
              elif body[w] == ' ' or body[w] == '\r' or body[w] == '\n' \
                   or body[w] == '\t' or body[w] == '/' or ((w + 1) >= len(body)):
                #if the word is in the vocabulary, add it to the words in the doc 
                if vocabularyWord.has_key(tempBody):
                  tempTokensDocument.addWord(tempBody)
                tempBody = '';
            #if the word is in the vocabulary, add it to the words in the doc 
            if vocabularyWord.has_key(tempBody):
              tempTokensDocument.addWord(tempBody)
            
            tokensInTheDocuments.append(tempTokensDocument)
            
        index1 += 1
      j += 1

  return tokensInTheDocuments

#################################################
# count Tokens Of Term
#
#	A function goes th
#################################################
def countTokensOfTerm(wordsInDocuments, tempVocWord):
  count = 0
  for i in range(len(wordsInDocuments)):
    tempWord = wordsInDocuments[i]
    if tempWord == tempVocWord:
      count += 1

  return count

def trainMultinomialNB(classes, documents):
  prior = []
  Tct = []
  wordsInTheDocuments = [wordsInDocument() for i in range(len(classes))]
  vocabularyWord, vocabularyNum, numDocs, numDocsInClass, wordsInTheDocuments = \
      extractEverythingForTraining(classes, documents)
  
#  print "Length dict: " + str(len(vocabularyWord))
  
  condProb = [probability() for i in range(len(vocabularyNum))]
  
  for i in range(len(numDocsInClass)):
    print "processing class: " + str(i)
    priorVal = float(numDocsInClass[i])/float(numDocs)
    prior.append(priorVal)
    Tct = []
    TctSum = 0
    for j in range(len(vocabularyNum)):
      tempVocWord = vocabularyNum[j] 
      timesInDocs = countTokensOfTerm(wordsInTheDocuments[i].words, tempVocWord)
#      print "term1: " + tempVocWord + " times in doc: " + str(timesInDocs)
      Tct.append(timesInDocs)
      TctSum += (timesInDocs + 1)
      if j%100 == 0:
        print "100 words processed."

#    print "Tct Sum: " + str(TctSum)
      
    print "finshed counting word in class: " + str(i) + " now calculating cond prob."
    
    for j in range(len(vocabularyNum)):
      tempVal = (float(Tct[j]) + 1.0)/float(TctSum)
      
      condProb[j].vocabTerm = vocabularyNum[j]
      condProb[j].addProb(tempVal)
#      print "term: " + vocabularyNum[j] + " Prob: " + str(tempVal)
      
  return vocabularyWord, vocabularyNum, prior, condProb  



def applyMultinomialNB(classes, vocabularyWord, prior, condProb, documents):
  print "Now working on applying the multinomial."
  tokens = extractTokensFromDoc(classes, documents, vocabularyWord)
  
  highestScores = [maxScoreDoc() for i in range(len(tokens))]
  for i in range(len(tokens)):
    highestScores[i].actualTag = tokens[i].tag
  
  for i in range(len(tokens)):
    print "Processing doc: " + str(i) + " out of " + str(len(tokens))
    for j in range(len(classes)):
      tempPrior = prior[j]

      if tempPrior != 0:
        tempScore = math.log10(tempPrior)
      else:
        print "Error in applyMNB temp prior should not be 0."
        tempScore = 0
      score = tempScore

      for k in range(len(tokens[i].words)):
        tempWord = tokens[i].words[k]
        locWord = vocabularyWord[tempWord]
        if condProb[locWord].vocabTerm != tempWord:
          print "ERROR finding word in apply MNB! Fix code!!!"
        score += math.log10(condProb[locWord].prob[j])
      #print "class: " + classes[j] + " score: " + str(score)
      if j == 0:
        highestScores[i].score = score
        highestScores[i].guessedTag = classes[j]
      if score > highestScores[i].score:
        highestScores[i].score = score
        highestScores[i].guessedTag = classes[j]

  return highestScores

def main():
  classes = []
  fileName = "reuters21578-xml/tenLargestClasses.txt"
  fin = open(fileName, 'r')
  tempClassNames = fin.read()
  fin.close()
  className = ""
  for i in range(len(tempClassNames)):
    if(tempClassNames[i] == '\r' or tempClassNames[i] == '\n'):
      classes.append(className)
      className = ""  
    else:
      className += tempClassNames[i]
      
  #classes = []
  
  #classes.append("China")
  #classes.append("Japan")
  
  documents = []
  index = -1
  for i in range(22):
    fileName = "reuters21578-xml/reut2-" + str(i) + ".xml"
    #fileName = "reuters21578-xml/test2.xml"
    parser = xml.dom.minidom.parse(fileName)
    for node in parser.getElementsByTagName("REUTERS"):
      tempDoc = document()
      
      topics = node.getAttribute("TOPICS")
      tempDoc.topics = topics
      
      lewisSplit = node.getAttribute("LEWISSPLIT")
      tempDoc.lewisSplit = lewisSplit
      
      newId = node.getAttribute("NEWID")
      tempDoc.newId = newId
      
      L = node.getElementsByTagName("DATE")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            tempDoc.date = node3.data
             
      L = node.getElementsByTagName("AUTHOR")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            tempDoc.author = node3.data
    
      L = node.getElementsByTagName("DATELINE")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            tempDoc.dateline = node3.data
            
      L = node.getElementsByTagName("TITLE")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            tempDoc.title = node3.data
            
      L = node.getElementsByTagName("BODY")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            tempDoc.body = node3.data

      documents.append(tempDoc)
      
    tempIndex = index
    for node in parser.getElementsByTagName("PLACES"):
      tempIndex += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[tempIndex].addPlace(node3.data)
  
    tempIndex = index
    for node in parser.getElementsByTagName("PEOPLE"):
      tempIndex += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[tempIndex].addPeople(node3.data)

    tempIndex = index
    for node in parser.getElementsByTagName("ORGS"):
      tempIndex += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[tempIndex].addOrg(node3.data)

    tempIndex = index
    for node in parser.getElementsByTagName("EXCHANGES"):
      tempIndex += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[tempIndex].addExchange(node3.data)
  
  
    for node in parser.getElementsByTagName("TOPICS"):
      index += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[index].addTag(node3.data)
              
    print "Done processing file " + fileName

  vocabularyWord, vocabularyNum, prior, condProb = trainMultinomialNB(classes, documents)
  results = applyMultinomialNB(classes, vocabularyWord, prior, condProb, documents)
  
  count = 0
  for i in range(len(results)):
    if results[i].guessedTag == results[i].actualTag:
      count += 1
  
  print "Files: " + str(len(results)) + " count: " + str(count)
  
  tp = []
  fp = []
  fn = []
  
  p = []
  r = []
  f1 = []
  
  for j in range(len(classes)):
    tp.append(0.0)
    fp.append(0.0)
    fn.append(0.0)
    
    for i in range(len(results)):
      if classes[j] == results[i].actualTag and results[i].guessedTag == results[i].actualTag: #c = aT & aT = gT
        tp[j] += 1
      if classes[j] == results[i].guessedTag and results[i].guessedTag != results[i].actualTag: #c = gT & gT != aT
        fp[j] += 1
      if classes[j] != results[i].guessedTag and results[i].guessedTag != results[i].actualTag: #gT != c & gT != aT
        fn[j] += 1
        
    print "class: " + str(j) + " tp: " + str(tp[j]) + " fp: " + str(fp[j]) + " fn: " + str(fn[j])
    if tp[j]+fp[j] == 0:
      p.append( 0.0 )
      print "\tERROR: div by zero calculating precision"
    else:
      p.append( float(tp[j])/(float(tp[j])+float(fp[j])) )
    
    if tp[j]+fp[j] == 0:
      r.append( 0.0 )
      print "\tERROR: div by zero calculating recall"
    else:
      r.append( float(tp[j])/(float(tp[j])+float(fn[j])) )
    
    if p[j]+r[j] == 0:
      print "\tERROR: div by zero calculating f1 score"
      f1.append( 0.0 )
    else:
      f1.append( float(p[j])*float(r[j])*2/(float(p[j])+float(r[j])) )
    
    print "class: " + classes[j] + " f1 score: " + str(f1[j])

  for j in range(len(classes)):
    tp.append(0.0)
    fp.append(0.0)
    fn.append(0.0)
    
    for i in range(len(results)):
      if results[i].actualTag == classes[j] or results[i].guessedTag == classes[j]:
        if results[i].guessedTag == results[i].actualTag:
          tp[j] += 1.0
        elif classes[j] == results[i].guessedTag:
          fp[j] += 1.0
        else:
          fn[j] += 1.0
      
    print classes[j]
    print "\ttp: " + str(tp[j]) + " fp: " + str(fp[j]) + " fn: " + str(fn[j])

    if tp[j]+fp[j] == 0:
      p.append( 0.0 )
      print "\tERROR: div by zero calculating precision"
    else:
      p.append( tp[j]/(tp[j]+fp[j]) )
      
    if tp[j]+fp[j] == 0:
      r.append( 0.0 )
      print "\tERROR: div by zero calculating recall"
    else:
      r.append( tp[j]/(tp[j]+fn[j]) )
    
    if p[j]+r[j] == 0:
      print "\tERROR: div by zero calculating f1 score"
      f1.append( 0.0 )
    else:
      f1.append( p[j]*r[j]*2.0/(p[j]+r[j]) )
    
      print "\tf1 score: " + str(f1[j])


if __name__ == "__main__":
  main()
