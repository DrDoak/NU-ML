import ID3, parse, random, copy

def testID3AndEvaluate():
  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
  tree = ID3.ID3(data, 0)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=1, b=0))
    print "final-ans"
    print ans
    if ans != 1:
      print "ID3 test failed."
    else:
      print "ID3 test succeeded."
  else:
    print "ID3 test failed -- no tree returned"

def testPruning():
  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=0, b=1, Class=0), dict(a=0, b=0, Class=1)]
  validationData = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1), dict(a=0, b=0, Class=0), dict(a=0, b=0, Class=0)]
  tree = ID3.ID3(data, 0)
  ID3.prune(tree, validationData)
  print tree.children
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=0))
    print "FInal answer: " + str(ans)
    if ans != 0:
      print "pruning test failed."
    else:
      print "pruning test succeeded."
  else:
    print "pruning test failed -- no tree returned."

def testID3AndTest():
  trainData = [dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1), 
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]

  testData = [dict(a=1, b=0, c=1, Class=1), dict(a=1, b=1, c=1, Class=1), 
  dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)]
  
  tree = ID3.ID3(trainData, 0)
  fails = 0
  if tree != None:
    # print "label: " + str(tree.label) + "| children: " + str(tree.children)
    acc = ID3.test(tree, trainData)
    print "final result: " + str(acc)
    if acc == 1.0:
      print "testing on train data succeeded."
    else:
      print "testing on train data failed."
      fails = fails + 1
    acc = ID3.test(tree, testData)
    if acc == 0.75:
      print "testing on test data succeeded."
    else:
      print "testing on test data failed."
      fails = fails + 1
    if fails > 0:
      print "Failures: ", fails
    else:
      print "testID3AndTest succeeded."
  else:
    print "testID3andTest failed -- no tree returned."

# inFile - string location of the house data file
def testPruningOnHouseData(inFile):
  data = parse.parse(inFile)
  
  for tSize in [10,25,50,100,150,200]:
    withPruning = []
    print "testing size: " + str(tSize)
    withoutPruning = []
    for i in range(100):
      random.shuffle(data)
      # train = copy.deepcopy(data[0:tSize])
      # random.shuffle(data)
      # valid = copy.deepcopy(data[0:(tSize/2)])
      # random.shuffle(data)
      # test = copy.deepcopy(data[0:(tSize/2)])
      
      train = data[:len(data)/2]
      valid = data[len(data)/2:3*len(data)/4]
      test = data[3*len(data)/4:]
      
      train = data[:tSize]
      valid = data[tSize:(tSize + tSize/2)]
      test = data[(tSize + tSize/2):]

      tree = ID3.ID3(train, 'democrat')
      acc = ID3.test(tree, train)
      # print "training accuracy: ",acc
      acc = ID3.test(tree, valid)
      # print "validation accuracy: ",acc
      acc = ID3.test(tree, test)
      # print "test accuracy: ",acc
      
      ID3.prune(tree, valid)
      acc = ID3.test(tree, train)
      # print "pruned tree train accuracy: ",acc
      acc = ID3.test(tree, valid)
      # print "pruned tree validation accuracy: ",acc
      acc = ID3.test(tree, test)
      # print "pruned tree test accuracy: ",acc
      withPruning.append(acc) 
      tree = ID3.ID3(train+valid, 'democrat')
      
      # tree = ID3.ID3(train, 'democrat')
      acc = ID3.test(tree, test)
      # print "no pruning test accuracy: ",acc
      withoutPruning.append(acc)
      """print withPruning 
      print "---" 
      print withoutPruning"""
      # print str(len(withPruning))
      # print str(len(withoutPruning))
    print "average with pruning " + str(sum(withPruning)/len(withPruning)) + " without: " + str(sum(withoutPruning)/len(withoutPruning))
  