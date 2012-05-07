#!/usr/bin/python

import sys
import math
import time
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node

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
    #self.unknown
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

class wordsInDocument:
  def __init__(self):
    self.tag = ""
    self.words = []
 
  def addWord(self, wordIn):
    self.words.append(wordIn)

class tokensInDocument:
  def __init__(self):
    self.tag = ""
    self.words = []
 
  def addWord(self, wordIn):
    self.words.append(wordIn)

class probability:
  def __init__(self):
    self.vocabTerm = ""
    self.prob = []
  def addProb(self, probIn):
    self.prob.append(probIn)

class maxScoreDoc:
  def __init__(self):
    self.actualTag = ""
    self.guessedTag = ""
    self.score = -1


#AN IMPROVEMENT COULD BE GETTING RID OF CAP AND 
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

  for i in range(len(documents)):
    j = 0
    notFound = True
    while j < len(documents[i].tags) and notFound:
      index1 = 0
      while index1 < len(classes) and notFound:
        if documents[i].tags[j] == classes[index1]:
          notFound = False
          if documents[i].lewisSplit == "TRAIN": 
            numDocs += 1
            numDocsInClass[index1] += 1
            title = documents[i].title
            tempTitle = ""
#            isNum = False
            for w in range(len(title)):
              if (title[w] >= 'a' and title[w] <= 'z') or title[w] == "'" or title[w] == "-":
                tempTitle += title[w]
#              elif (title[w] >= '0' and title[w] <= '9'): 
#                tempTitle += title[w]
#                isNum = True
#              elif (title[w] == '.' and isNum): 
#                tempTitle += title[w]
              #if the character is capitalize, make it lower case
              elif(title[w] >= 'A' and title[w] <= 'Z'):
                tempTitle += title[w].lower()
              #the word being built is finished
              elif title[w] == ' ' or title[w] == '\r' or title[w] == '\n' \
                   or title[w] == '\t' or title[w] == '/':
                #the word is not empty and is not a simple word
                if tempTitle != '' and len(tempTitle) > 3:
                  wordsInTheDocuments[index1].addWord(tempTitle)
                  if not(vocabularyWord.has_key(tempTitle)):
                    vocabularyWord[tempTitle] = vocabIndex
                    vocabularyNum[vocabIndex] = tempTitle
                    vocabIndex += 1
                tempTitle = '';
#                isNum = False
            if tempTitle != '' and len(tempTitle) > 3:
              wordsInTheDocuments[index1].addWord(tempTitle)
              if not(vocabularyWord.has_key(tempTitle)):
                vocabularyWord[tempTitle] = vocabIndex
                vocabularyNum[vocabIndex] = tempTitle
                vocabIndex += 1
                    
                     
            dateline = documents[i].dateline
            tempDateline = ""
#            isNum = False
            for w in range(len(dateline)):
              if (dateline[w] >= 'a' and dateline[w] <= 'z') or dateline[w] == "'" \
                  or dateline[w] == "-":
                tempDateline += dateline[w]
#              elif (dateline[w] >= '0' and dateline[w] <= '9'): 
#                tempDateline += dateline[w]
#                isNum = True
#              elif (dateline[w] == '.' and isNum): 
#                tempDateline += dateline[w]
              #if the character is capitalize, make it lower case
              elif(dateline[w] >= 'A' and dateline[w] <= 'Z'):
                tempDateline += dateline[w].lower()
              #the word being built is finished
              elif dateline[w] == ' ' or dateline[w] == '\r' or dateline[w] == '\n' \
                   or dateline[w] == '\t' or dateline[w] == '/' or ((w + 1) >= len(dateline)):
                #the word is not empty and is not a simple word
                if tempDateline != '' and len(tempDateline) > 3:
                  wordsInTheDocuments[index1].addWord(tempDateline)
                  if not(vocabularyWord.has_key(tempDateline)):
                    vocabularyWord[tempDateline] = vocabIndex
                    vocabularyNum[vocabIndex] = tempDateline
                    vocabIndex += 1
                tempDateline = '';
#                isNum = False
            if tempDateline != '' and len(tempDateline) > 3:
              wordsInTheDocuments[index1].addWord(tempDateline)
              if not(vocabularyWord.has_key(tempDateline)):
                vocabularyWord[tempDateline] = vocabIndex
                vocabularyNum[vocabIndex] = tempDateline
                vocabIndex += 1

 
            body = documents[i].body
#            print "Body: " + body
            tempBody = ""
#            isNum = False
            for w in range(len(body)):
              if (body[w] >= 'a' and body[w] <= 'z') or body[w] == "'" or body[w] == "-":
                tempBody += body[w]
#              elif (body[w] >= '0' and body[w] <= '9'): 
#                tempBody += body[w]
#                isNum = True
#              elif (body[w] == '.' and isNum): 
#                tempBody += body[w]
              #if the character is capitalize, make it lower case
              elif(body[w] >= 'A' and body[w] <= 'Z'):
                tempBody += body[w].lower()
              #the word being built is finished
              elif body[w] == ' ' or body[w] == '\r' or body[w] == '\n' \
                   or body[w] == '\t' or body[w] == '/' or ((w + 1) >= len(body)):
                #the word is not empty and is not a simple word
                if tempBody != '' and len(tempBody) > 3:
                  wordsInTheDocuments[index1].addWord(tempBody)
                  if not(vocabularyWord.has_key(tempBody)):
                    vocabularyWord[tempBody] = vocabIndex
                    vocabularyNum[vocabIndex] = tempBody
                    vocabIndex += 1
                tempBody = '';
#                isNum = False
            if tempBody != '' and len(tempBody) > 3:
              wordsInTheDocuments[index1].addWord(tempBody)
              if not(vocabularyWord.has_key(tempBody)):
                vocabularyWord[tempBody] = vocabIndex
                vocabularyNum[vocabIndex] = tempBody
                vocabIndex += 1
 
        index1 += 1
      j += 1

  #for i in range(len(vocabularyWord)):
  #  print str(vocabularyWord[vocabularyNum[i]]) + ":  " + vocabularyNum[i]

  return vocabularyWord, vocabularyNum, numDocs, numDocsInClass, wordsInTheDocuments

def extractTokensFromDoc(classes, documents, vocabularyWord):
  tokensInTheDocuments = []

  for i in range(len(documents)):
    j = 0
    notFound = True
    while j < len(documents[i].tags) and notFound:
      index1 = 0
      while index1 < len(classes) and notFound:
        if documents[i].tags[j] == classes[index1]:
          notFound = False
          if documents[i].lewisSplit == "TEST": 
            index = 0
            tempTokensDocument = tokensInDocument()
            tempTokensDocument.tag = classes[index1]
            title = documents[i].title
            tempTitle = ""
            for w in range(len(title)):
              if (title[w] >= 'a' and title[w] <= 'z') or title[w] == "'" or title[w] == "-":
                tempTitle += title[w]
              #if the character is capitalize, make it lower case
              elif(title[w] >= 'A' and title[w] <= 'Z'):
                tempTitle += title[w].lower()
              #the word being built is finished
              elif title[w] == ' ' or title[w] == '\r' or title[w] == '\n' \
                   or title[w] == '\t' or title[w] == '/':
                if vocabularyWord.has_key(tempTitle):
                  tempTokensDocument.addWord(tempTitle)
                tempTitle = '';
            if vocabularyWord.has_key(tempTitle):
                tempTokensDocument.addWord(tempTitle)

                    
                     
            dateline = documents[i].dateline
            tempDateline = ""
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
                if vocabularyWord.has_key(tempDateline):
                  tempTokensDocument.addWord(tempDateline)
                tempDateline = '';
            if vocabularyWord.has_key(tempDateline):
              tempTokensDocument.addWord(tempDateline)
 
            body = documents[i].body
            tempBody = ""
            for w in range(len(body)):
              if (body[w] >= 'a' and body[w] <= 'z') or body[w] == "'" or body[w] == "-":
                tempBody += body[w]
              #if the character is capitalize, make it lower case
              elif(body[w] >= 'A' and body[w] <= 'Z'):
                tempBody += body[w].lower()
              #the word being built is finished
              elif body[w] == ' ' or body[w] == '\r' or body[w] == '\n' \
                   or body[w] == '\t' or body[w] == '/' or ((w + 1) >= len(body)):
                if vocabularyWord.has_key(tempBody):
                  tempTokensDocument.addWord(tempBody)
                tempBody = '';
            if vocabularyWord.has_key(tempBody):
              tempTokensDocument.addWord(tempBody)
            
            tokensInTheDocuments.append(tempTokensDocument)
            
        index1 += 1
      j += 1

  return tokensInTheDocuments
  
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
    tp.append(0)
    fp.append(0)
    fn.append(0)
    
    
    for i in range(len(results)):
      if classes[j] == results[i].actualTag and results[i].guessedTag == results[i].actualTag: #c = aT & aT = gT
        tp[j] += 1
      if classes[j] == results[i].guessedTag and results[i].guessedTag != results[i].actualTag: #c = gT & gT != aT
        fp[j] += 1
      if classes[j] != results[i].guessedTag and results[i].guessedTag != results[i].actualTag: #gT != c & gT != aT
        fn[j] += 1
        
    print "class: " + str(j) + " tp: " + str(tp[j]) + " fp: " + str(fp[j]) + " fn: " + str(fn[j])
    if fp[j] == 0 and tp[j] == 0:
      p.append(0.0)
    else:
      p.append( float(tp[j])/(float(tp[j])+float(fp[j])) )
    
    if fn[j] == 0 and tp[j] == 0:
      r.append(0.0)
    else:
      r.append( float(tp[j])/(float(tp[j])+float(fn[j])) )
    
    if p[j] == 0 or r[j] == 0:
      f1 = 0
    else:
      f1.append( float(p[j])*float(r[j])*2/(float(p[j])+float(r[j])) )
    
    print "class: " + classes[j] + " f1 score: " + str(f1[j])

#class maxScoreDoc:
#  def __init__(self):
#    self.actualTag = ""
#    self.guessedTag = ""
#    self.score = -1


"""  for i in range(len(documents)):
    print "topics: " + documents[i].topics
    print "lewisSplit: " + documents[i].lewisSplit
    print "newID: " + documents[i].newId
    print "date: " + documents[i].date

    print "tags: ",
    for j in range(len(documents[i].tags)):
      print documents[i].tags[j] + ", ",

    print ""
    print "places: ",
    for j in range(len(documents[i].places)):
      print documents[i].places[j] + ", ",

    print ""
    print "people: ",
    for j in range(len(documents[i].people)):
      print documents[i].people[j] + ", ",

    print ""
    print "orgs: ",
    for j in range(len(documents[i].orgs)):
      print documents[i].orgs[j] + ", ",

    print ""
    print "exchanges: ",
    for j in range(len(documents[i].exchanges)):
      print documents[i].exchanges[j] + ", ",
    print ""

    print "author: " + documents[i].author
    print "dateline: " + documents[i].dateline
    print "title: " + documents[i].title
    print "body: " + documents[i].body"""


if __name__ == "__main__":
  main()
