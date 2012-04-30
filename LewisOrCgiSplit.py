#!/usr/bin/python

import sys
import time
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node

class document:
  def __init__(self):
    self.cgiSplit = ""
    self.lewisSplit = ""
    self.tags = []
  def addTag(self, tagIn):
    self.tags.append(tagIn)
  def getNumOfTags(self):
    return len(self.tags)

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
  
  cgiTrain = []
  cgiTest = []
  lewisTrain = []
  lewisTest = []
  
  for i in range(len(classes)):
    cgiTrain.append(0)
    cgiTest.append(0)
    lewisTrain.append(0)
    lewisTest.append(0)
  
  documents = []
  index = -1
  for i in range(22):
    fileName = "reuters21578-xml/reut2-" + str(i) + ".xml"
    parser = xml.dom.minidom.parse(fileName)
    #index = len(documents)
    for node in parser.getElementsByTagName("REUTERS"):
      tempDoc = document()
      lewisSplit = node.getAttribute("LEWISSPLIT")
      tempDoc.lewisSplit = lewisSplit
      cgiSplit = node.getAttribute("CGISPLIT")
      tempDoc.cgiSplit = cgiSplit
      documents.append(tempDoc)
    
    for node in parser.getElementsByTagName("TOPICS"):
      index += 1
      L = node.getElementsByTagName("D")
      for node2 in L:
        for node3 in node2.childNodes:
          if node3.nodeType == Node.TEXT_NODE:
            documents[index].addTag(node3.data)
            
    print "Done processing file " + fileName

  print "Size: " + str(len(documents))

  for i in range(len(documents)):
    for j in range(len(documents[i].tags)):
      for k in range(len(classes)):
        if documents[i].tags[j] == classes[k]:
          if documents[i].cgiSplit == "TRAINING-SET":
            cgiTrain[k] += 1
          elif documents[i].cgiSplit == "PUBLISHED-TESTSET":
            cgiTest[k] += 1
          else:
            print "UNKNOWN CGI SPLIT: " + documents[i].cgiSplit
              
          if documents[i].lewisSplit == "TRAIN":
            lewisTrain[k] += 1
          elif documents[i].lewisSplit == "TEST":
            lewisTest[k] += 1
          elif documents[i].lewisSplit == "NOT-USED":
            la = 0
          else:
            print "UNKNOWN LEWIS SPLIT: " + documents[i].lewisSplit
              
    
  for i in range(len(classes)):
    print "CGI " + classes[i] + ": " + str(cgiTrain[i]) + "    " + str(cgiTest[i])
    print "LEWIS " + classes[i] + ": " + str(lewisTrain[i]) + "    " + str(lewisTest[i])


if __name__ == "__main__":
  main()
