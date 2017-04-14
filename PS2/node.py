class Node:
    def __init__(self):
        self.label = None
        self.parent = None
        self.value = None
        self.children = {} 
        self.classVals = {}
        self.isLeaf = False
	# you may want to add additional fields here...

	def add_branch(self,label, subtree):
		self.children[label] = subtree

	def set_parent(self,par):
		self.parent = par