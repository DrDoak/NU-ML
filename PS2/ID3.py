from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  print "starting ID3"
  finalTree = Node()
  if (not examples):
    print "No Example returning default"
    finalTree.value = default
    return finalTree
  else:
    print "====not EMPTY starting classification"
    sameClassification = True
    lastClassification = None
    allEmpty = True
    for att in examples:
      allEmpty = False
      if lastClassification and  att["Class"] != lastClassification:
        sameClassification = False
      else:
        lastClassification = att["Class"]
    if (sameClassification):
      finalTree.value = lastClassification
      return finalTree
    if (allEmpty):
      print "all Empty, returning"
      finalTree.value = default
      return finalTree
    bestAttr,potentialAnswers = choose_attribute(examples)
    tree = Node()

    for vi in potentialAnswers:
      examplesI = []
      for val in examples:
        if (val[bestAttr] and val[bestAttr] == vi):
          examplesI.append(newDict)
      subtree = ID3(examplesI,mode(examples))
      finalTree.add_branch(vi,subtree)

  print "Returning tree: " + str(finalTree)
  return finalTree

def choose_attribute(examples):
  print "Choosing Attribute"
  attrs = examples[0]
  maxAttr = None
  maxGain = 0
  for k,v in attrs.iteritems():
    if k != "Class":
      testGain = gain(examples,k)
      if testGain > maxGain:
        maxGain = testGain
        maxAttr = k
  attrAns = []
  for v in examples:
    if not v[maxAttr] in attrAns:
      attrAns.append(v[maxAttr])
  return maxAttr, attrAns

def gain(S, A):
  ent = entropy(S)
  sumA = 0
  for v in A:
    Sv = {}
    for val in S:
      if (val[A] and val[A] == v):
        Sv.append(val)
    sumA += (len(Sv)/len(S)) * entropy(Sv)
  return ent - sumA

def entropy(examples):
  ent = 0
  countList = {}
  for att in examples:
    if att["Class"] in countList.keys():
      countList[att["Class"]] += 1
    else:
      countList[att["Class"]] = 1
  for key,val in countList.iteritems():
    val = val * 1.0
    
    print val * 1.0
    print len(examples) * 1.0
    print str((val*1.0) / (len(examples)*1.0))
    ent += (-val/len(examples)) * math.log((val/len(examples)),2)
  return ent

def mode(examples):
  countList = []
  maxCount = 0
  maxClass = None
  for att in examples:
    if countList[att["Class"]]:
      countList[att["Class"]] += 1
      if countList[att["Class"]] > maxCount:
        maxCount = countList[att["Class"]]
        maxClass = att["Class"]
    else:
      countList[att["Class"]] = 1
      if maxCount == 0:
        maxCount = 1
        maxClass = att["Class"]
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
  numCorrect = 0
  for testCase in examples:
    testAnswer = evaluate(node,testCase)
    if testAnswer == testCase["Class"]:
      numCorrect = numCorrect + 1
  return (numCorrect * 1.0)/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if (node.children):
    for k,v in node.children:
      if (example[node.label] == k):
        evaluate(v,example)
  else:
    return node.value
