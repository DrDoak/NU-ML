class Node:
    def __init__(self):
        self.label = None
        self.parent = None
        self.value = None
        self.children = {} 
	# you may want to add additional fields here...

	def add_branch(label, subtree):
		self.children[label] = subtree

	def set_parent(par):
		self.parent = par