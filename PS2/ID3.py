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
      return examples[0].Class
    if (allEmpty):
      print "error: should terminate classification"
      return False
    best = choose_attribute(examples)
    tree = Node()

    for vi in best:
      examplesI = []
      for val in examples:
        if (val[best] && val[best] == vi)
          examplesI.append(newDict)
      subtree = ID3(examplesI,mode(examples)):
      finalTree.add_branch(vi,subtree)
      
  return finalTree

def choose_attribute(examples):
  return []

def gain(S, A):
  ent = entropy(S)
  sumA = 0
  for v in A:
    Sv = {}
    for val in S:
      if (val[A] && val[A] == v)
        Sv.append(val)
    sumA += (len(Sv)/len(S)) * entropy(Sv)
  return ent - sumA

def entropy(examples):
  ent = 0
  attri_frequencies = {}
  for key, val in examples.iteritems():
  for val in attri_frequencies:
    ent += (-val/len(examples)) * math.log((val/len(examples)),2)

  def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq     = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]]  = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy

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
  checked = []
  oldTreeValidation = test(node, examples) #test oldTree
  #foreach leaf:
  #   go to parent, put parent in checked
  #   if parent unchecked: 
  #      for children of parent:
  #         find majority value of attribute 
  #      for children of parent:
  #         change all to majority value 
  #
  #   newTreeValidation = test(node, examples)
  #   if newTreeValidation > oldTreeValidation:
  #      oldTreeValidation = newTreeValidation
  #      remove parent and children, replace with majority value
  #   else:
  #      revert tree back to how it was
  
  
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
