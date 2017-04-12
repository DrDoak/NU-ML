class Node:
    def __init__(self):
        self.label = None
        self.children = {} 
	# you may want to add additional fields here...

	def add_branch(label, subtree):
		self.children[label] = subtree