#!/usr/bin/python

import sys
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
  
  documents = []
  index = -1
  for i in range(22):
    fileName = "reuters21578-xml/reut2-" + str(i) + ".xml"
    #fileName = "reuters21578-xml/test.xml"
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

    #Training
    for j in range(len(documents[i].tags)):
      for k tagin range(len(classes)):
        if documents[i].tags[j] == classes[k]:              
          if documents[i].lewisSplit == "TRAIN":

#          elif documents[i].lewisSplit == "TEST":

    #Testing
    for j in range(len(documents[i].tags)):
      for k tagin range(len(classes)):
        if documents[i].tags[j] == classes[k]:              
          if documents[i].lewisSplit == "TEST":

#          elif documents[i].lewisSplit == "TEST":


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
