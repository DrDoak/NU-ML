from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  # print "+++++++ID3 start"
  # print examples
  finalTree = Node()
  if (not examples):
    # print "empty, returning default: " + str(default)
    finalTree.value = default
    finalTree.isLeaf = True
    return finalTree
  else:
    sameClassification = True
    lastClassification = None
    allEmpty = True
    for att in examples:
      allEmpty = False
      # print "bool: " + str(lastClassification != None) + " bool2: " + str(att["Class"] != lastClassification)
      if (lastClassification != None) and att["Class"] != lastClassification:
        # print "l: " + str(lastClassification) + "| n: " + str(att["Class"])
        # print "values are different, no longer sameClassification"
        sameClassification = False
      else:
        lastClassification = att["Class"]
    if (sameClassification):
      finalTree.value = lastClassification
      finalTree.isLeaf = True
      # print "-----"
      # print examples
      # print "returning last class: " + str(lastClassification)
      return finalTree
    if (allEmpty):
      finalTree.value = default
      return finalTree
    bestAttr,potentialAnswers = choose_attribute(examples)
    # print "split on label: " + str(bestAttr)
    finalTree.label = bestAttr
    for vi in potentialAnswers:
      # print "grade: " + str(vi)
      examplesI = []
      for val in examples:
        # print "my grade: " + str(vi) + "|| example attr: " + str(val[bestAttr])
        if (val[bestAttr] == vi):
          # print "appending a new thing"
          examplesI.append(val)
      subtree = ID3(examplesI,mode(examples))
      #finalTree.add_branch(vi,subtree)
      finalTree.children[vi] = subtree
  return finalTree

def choose_attribute(examples):
  # print "Choosing Attribute"
  attrs = examples[0]
  maxAttr = None
  maxGain = 0
  for k,v in attrs.iteritems():
    if k != "Class":
      testGain = gain(examples,k,[0,1])
      # print "testGain for attr: " + str(k) + " is: " + str(testGain) + " maxis: " + str(maxGain)
      if testGain > maxGain:
        maxGain = testGain
        maxAttr = k
  attrAns = []
  for v in examples:
    if (maxAttr != None) and not v[maxAttr] in attrAns:
      attrAns.append(v[maxAttr])
  return maxAttr, attrAns

def gain(S, A, options):
  ent = entropy(S)
  sumA = 0
  for v in options:
    Sv = []
    for val in S:
      if (val[A] == v):
        Sv.append(val)
    # print "len1: " + str(len(Sv)) + " len2: " + str(len(S)) + " entSm: " + str(entropy(Sv))
    sumA += (len(Sv)/len(S)) * entropy(Sv)
  # print "startEnt: " + str(ent) + "sum A: " + str(sumA)
  return ent - sumA

def entropy(examples):
  ent = 0
  countList = {}
  for att in examples:
    # print "___" + str(att)
    if att["Class"] in countList.keys():
      countList[att["Class"]] += 1
    else:
      countList[att["Class"]] = 1
  for key,val in countList.iteritems():
    val = val * 1.0    
    # print val * 1.0
    # print len(examples) * 1.0
    # print str((val*1.0) / (len(examples)*1.0))
    ent += (-val/len(examples)) * math.log((val/len(examples)),2)
  # Entropy = - p(a)*log(p(a)) - p(b)*log(p(b))
  return ent

def mode(examples):
  countList = {}
  maxCount = 0
  maxClass = None
  for att in examples:
    # print att["Class"]
    if att["Class"] in countList.keys():
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

def getLeaves(node):
  listLeaves = []
  if node.isLeaf:
    return [node]
  else:
    for subnode in node.children:
      listLeaves += getLeaves(subnode)
  return listLeaves

def getMajorityClass():
  return None

def prune(oldTree, examples):
  listLeaves = getLeaves(oldTree)
  checked = []

  while(len(listLeaves) > 0):
    leaf = listLeaves[0]
    newTree,newLeaf = pruneHelper(deepcopy(oldTree),leaf,checked)
    listLeaves.pop(0)
    if test(newTree,examples) > test(oldTree, examples): 
      oldTree = newTree
      listLeaves.insert(newLeaf)
  return oldTree

def pruneHelper(node,leaf):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if (not leaf.parent in checked):
    totalMajority = {}
    for child in leaf.parent.children:
      for className,number in child.classVals.iteritems():
        if not className in totalMajority.keys():
          totalMajority[className] = number
        else:
          totalMajority[className] += number
    #find out majority attribute
    majorityClass = None
    maxNum = 0
    totalVal = 0;
    for className, classNum in totalMajority.iteritems():
      totalVal = totalVal + classNum
      if classNum > maxNum:
        maxNum = classNum 
        majorityClass = className

    leaf.parent.value = majorityClass
    leaf.parent.classVals = {majorityClass: totalVal}
  checked.append(leaf.parent)

  return node ,leaf.parent  

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  numCorrect = 0
  for testCase in examples:
    testAnswer = evaluate(node,testCase)
    print "evaluatedAns: " + str(testAnswer) + "Real Answer: " + str(testCase["Class"])
    if testAnswer == testCase["Class"]:
      numCorrect = numCorrect + 1
  return (numCorrect * 1.0)/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if (node.children):
    for k,v in node.children.iteritems():
      #print str(k) + " : " + str(v)
      if (example[node.label] == k):
        return evaluate(v,example)
  else:
    # print "Final value is " + str(node.value)
    return node.value