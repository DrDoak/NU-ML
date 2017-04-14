from node import Node
import math,copy

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  return ID3Helper(examples,default,None)
def ID3Helper(examples,default,parent):
  # print "+++++++ID3 start"
  # print examples
  finalTree = Node()
  finalTree.parent = parent
  if (not examples):
    # print "empty, returning default: " + str(default)
    finalTree.value = default
    finalTree.isLeaf = True
    propagate_ClassVal(finalTree,finalTree.value)
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
      propagate_ClassVal(finalTree,finalTree.value)
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
      subtree = ID3Helper(examplesI,mode(examples),finalTree)
      #finalTree.add_branch(vi,subtree)
      finalTree.children[vi] = subtree
  return finalTree


def propagate_ClassVal(node, classVal):
  if "Class" in node.classVals.keys():
    node.classVals[classVal] += 1
  else:
    node.classVals[classVal] = 1
  if (node.parent != None):
    propagate_ClassVal(node.parent, classVal)

def valueFinder(examples, attribute):
  '''
  Takes array of dictionaries, and returns all possible values for a specific attribute
  '''
  possibleValues = []
  for ex in examples:
    if ex[attribute] not in possibleValues:
      possibleValues.append(ex[attribute])
  return possibleValues

def choose_attribute(examples):
  # print "Choosing Attribute"
  attrs = examples[0]
  maxAttr = None
  maxGain = 0
  for k,v in attrs.iteritems():
    if k != "Class":
      testGain = gain(examples,k,valueFinder(examples,k))
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
    for key, subnode in node.children.iteritems():
      listLeaves += getLeaves(subnode)
  return listLeaves

def getMajorityClass():
  return None

def prune(oldTree, examples):
  # print oldTree
  listLeaves = getLeaves(oldTree)
  checked = []
  # print "Initial Accuracy: " + str(test(oldTree, examples))
  while(len(listLeaves) > 0):
    leaf = listLeaves[0]
    newTree,newLeaf = pruneHelper(copy.deepcopy(oldTree),leaf,checked)
    listLeaves.pop(0)
    # print "Old Accuracy: " + str(test(oldTree, examples))
    # print "New Accuracy: " + str(test(newTree,examples))
    if test(newTree,examples) > test(oldTree, examples): 
      oldTree = newTree
      listLeaves.append(newLeaf)
  return oldTree

def pruneHelper(node,leaf,checked):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if (leaf.parent != None and not leaf.parent in checked):
    totalMajority = {}
    for key, child in leaf.parent.children.iteritems():
      for className,number in child.classVals.iteritems():
        # print "ClassName: " + str(className) + " ClassNum: " + str(number)
        if not className in totalMajority.keys():
          totalMajority[className] = number
        else:
          totalMajority[className] += number
    #find out majority attribute
    majorityClass = None
    maxNum = 0
    totalVal = 0;
    # print "-----------"
    for className, classNum in totalMajority.iteritems():
      totalVal = totalVal + classNum
      # print "ClassName: " + str(className) + " ClassNum: " + str(classNum)
      if classNum > maxNum:
        maxNum = classNum 
        majorityClass = className
    # print "Majority attribute is :" + str(majorityClass)
    leaf.parent.value = majorityClass
    leaf.parent.isLeaf = True
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
    # print "evaluatedAns: " + str(testAnswer) + "Real Answer: " + str(testCase["Class"])
    if testAnswer == testCase["Class"]:
      numCorrect = numCorrect + 1
  return (numCorrect * 1.0)/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if (not node.isLeaf):
    for k,v in node.children.iteritems():
      #print str(k) + " : " + str(v)
      if (example[node.label] == k):
        return evaluate(v,example)
  else:
    # print "Final value is " + str(node.value)
    return node.value