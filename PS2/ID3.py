from node import Node
import math,copy

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  posAns = {}
  for k in examples[0]:
    posAns[k] = valueFinder(examples,k)
  return ID3Helper(examples,default,posAns, None)

def ID3Helper(examples,default,posAns, parent):
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

    bestAttr = choose_attribute(examples,posAns)
    # print "split on label: " + str(bestAttr)
    finalTree.label = bestAttr

    for vi in posAns[finalTree.label]:
      # print "grade: " + str(vi)
      examplesI = []
      for val in examples:
        # print "my grade: " + str(vi) + "|| example attr: " + str(val[bestAttr])
        if (val[bestAttr] == vi):
          # print "appending a new thing"
          examplesI.append(val)
      potMode = default
      if (mode(examples) != None):
        potMode = mode(examples)
      subtree = ID3Helper(examplesI,potMode,posAns,finalTree)
      #finalTree.add_branch(vi,subtree)
      finalTree.children[vi] = subtree
  return finalTree


def propagate_ClassVal(node, cv):
  if cv in node.classVals.keys():
    node.classVals[cv] += 1
  else:
    node.classVals[cv] = 1
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

def choose_attribute(examples,options):
  # print "Choosing Attribute"
  maxAttr = None
  maxGain = 0
  # print "---"
  for k,v in options.iteritems():
    if k != "Class":
      testGain = gain(examples,k,options[k])
      # print "attr: " + str(k) + " diff: " + str(testGain - maxGain) + " new: " + str(testGain) + " max: " + str(maxGain) + str(testGain - maxGain)
      if testGain > maxGain:
        # print "testGain for attr: " + str(k) + " is: " + str(testGain) + " maxis: " + str(maxGain)
        maxGain = testGain
        maxAttr = k
  # attrAns = []
  # for v in examples:
  #   if (maxAttr != None) and not v[maxAttr] in attrAns:
  #     attrAns.append(v[maxAttr])
  return maxAttr

def gain(S, A, options):
  ent = entropy(S)
  sumA = 0
  # print "_-----" + str(len(S)) + " At: " + str(A)
  for v in options:
    Sv = []
    for val in S:
      if (val[A] == v):
        Sv.append(val)
    # print "len1: " + str(len(Sv)) + " len2: " + str(len(S)) + " entSm: " + str(entropy(Sv))
    sumA = sumA + ((len(Sv) * 1.0)/len(S)) * entropy(Sv)
    # print "lS: " + str(len(Sv)) + " ent: " + str(entropy(Sv)) + " add: " + str((len(Sv) * 1.0)/len(S)) + " sum: " + str(sumA)
  # print "startEnt: " + str(ent) + "sum A: " + str(sumA) + " gain: " + str(ent - sumA)

  return ent - sumA

def entropy(examples):
  ent = 0
  countList = {}
  for att in examples:
    # print "___" + str(att)
    if att["Class"] in countList.keys():
      # print att["Class"]
      countList[att["Class"]] += 1.0
    else:
      countList[att["Class"]] = 1.0
  for key,val in countList.iteritems():
    # print "found: " + str(val * 1.0)
    # print "total: " + str(len(examples) * 1.0)
    # print "ratio: " + str((val*1.0) / (len(examples)*1.0))
    ent += (-val/len(examples)) * math.log((val/len(examples)),2)
    # print str(key) + " l: " + str(val) + " e: " + str(ent)
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
  if node.pruned:
    return []
  if node.isLeaf:
    return [node]
  else:
    for key, subnode in node.children.iteritems():
      listLeaves += getLeaves(subnode)
  return listLeaves

def prune(oldTree, examples):
  oldTree.children = pruneH(oldTree,examples).children

def pruneH(oldTree, examples):
  checked = []
  previousBest = test(oldTree, examples)
  # print "Now pruning: Initial Accuracy: " + str(previousBest) 
  testTree = copyTree(oldTree,None)
  listLeaves = getLeaves(testTree)
  while(len(listLeaves) > 1):
    leaf = listLeaves[0]
    newTree,newLeaf = pruneHelper(testTree,leaf,checked)
    listLeaves.pop(0)
    newScore = test(newTree,examples)
    # print "newScore: " + str(newScore)

    if newScore > previousBest: 
      oldTree = newTree
      # print "PRUNE: New accuracy is: " + str(newScore) + " Over old: " + str(previousBest) + " diff: "+  str(newScore - previousBest)
      previousBest = newScore
    otherList = getLeaves(oldTree)
    otherList[0].pruned = True
    testTree = copyTree(oldTree,None)
    listLeaves = getLeaves(testTree)
    # print "len: " + str(len(listLeaves))


  return oldTree

def copyTree(oNode,parent):
  newNode = Node()
  newNode.label = oNode.label
  newNode.parent = parent
  newNode.value = oNode.value
  newNode.children = {}
  newNode.pruned = oNode.pruned
  for k,c in oNode.children.iteritems():
   newNode.children[k] = copyTree(c,newNode)
  newNode.classVals = copy.deepcopy(oNode.classVals)
  newNode.isLeaf = oNode.isLeaf
  return newNode

def pruneHelper(node,leaf,checked):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if (leaf.parent != None and not leaf.parent.label in checked):
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
    leaf.pruned = True
    leaf.parent.isLeaf = True
    leaf.parent.classVals = {majorityClass: totalVal}
  checked.append(leaf.parent.label)

  return node ,leaf.parent  

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
    else:
      pass
      # print "test case: " + str(testCase)
      # print "evaluatedAns: " + str(testAnswer) + " Real Answer: " + str(testCase["Class"])
  return (numCorrect * 1.0)/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if (not node.isLeaf):
    for k,v in node.children.iteritems():
      if (example[node.label] == k):
        return evaluate(v,example)
  else:
    # print "Final value is " + str(node.value)
    return node.value