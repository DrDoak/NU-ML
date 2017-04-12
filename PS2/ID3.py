from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  finalTree = Node()
  if (not examples):
    return default
  else:
    sameClassifcation = True
    lastClassification = False
    allEmpty = True
    for att in examples:
      if lastClassification and att.Class != lastClassification:
        sameClassifcation = False
      else:
        lastClassification = att.Class

    if (sameClassifcation):
      return mode(examples)
    if (allEmpty):
      return False
    best = choose_attribute(examples)
    tree = Node()
    examplesI
    for val in examples:
      if examples == val:

    for val in best:
      
      subtree = ID3(examples,default,mode(examples)):
      finalTree.add_branch(val,subtree)
      
  return finalTree

def choose_attribute(examples):
  return []

def mode(examples):
  countList = []
  maxCount = 0
  maxClass
  for att in examples:
    if countList[att.Class]:
      countList[att.Class] = countList[att]
      if countList[att.Class] > maxCount:
        maxCount = countList[att.Class]
        maxClass = att.Class
    else:
      countList[att.Class] = 1
      if maxCount == 0:
        maxCount = 1
        maxClass = att.Class
  return maxClass

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
