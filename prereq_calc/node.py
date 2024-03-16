class ClassNode():
    
    def __init__(self, class_name, class_prereqs, class_credits, class_period, class_required):
        self.name: str = class_name
        self.prereq_names: list[str] = class_prereqs
        self.prereqs: list[ClassNode] = list[ClassNode]()
        self.credits = class_credits
        self.period = class_period
        self.required = True if class_required == 1 else False
    
    # def expand_prereqs(self, data):
    #     for full_prereq in self.prereq_names:
    #             for prereq in full_prereq.split("+"):
                
    #                 # check if the prereq node was already made in data
    #                 prereq_node = data.get(prereq, None)
    #                 # if node was found in data
    #                 if (prereq_node != None):
    #                     prereq_node.expand_prereqs(data) # recursively expand the other nodes
    #                     self.prereqs.append(prereq_node)
    #                 else:
    #                     # if prereq is not in data because it is not a class (e.g. "Senior standing")
    #                     self.prereqs.append(ClassNode(prereq, [], None, None, 0))

    def expand_prereqs(self, data):
        for full_prereq in self.prereq_names:
                for prereq in full_prereq.split("+"):
                
                    # check if the prereq node was already made in data
                    prereq_node = data.get(prereq, None)
                    # if node was found in data
                    if (prereq_node != None):
                        prereq_node.expand_prereqs(data) # recursively expand the other nodes
                        self.prereqs.append(prereq_node)
                    else:
                        # if prereq is not in data because it is not a class (e.g. "Senior standing")
                        self.prereqs.append(ClassNode(prereq, [], None, None, 0))

    def go_through(self):
        to_process = self.prereqs.copy() # start with first node's prereqs
        seen_prereqs = [] # keep track of unique prereqs

        while to_process: # while there are still nodes to process
            current = to_process.pop(0) # get the node to process
            # print(current.name)
            # print(current in seen_prereqs)

            if current not in seen_prereqs:
                # if current is unique
                seen_prereqs.append(current)

                # structure of prereq path:
                # each list in the main list is a collection of classes that *can* be taken
                # that is, a sublist is an OR path
                # AND paths are indistinguishable from a block of classes
                # because really they are just more qualified blocks of classes

                for prereq in current.prereqs:
                    to_process.append(prereq)
            
        return seen_prereqs

    def get(self):
        return self.name

    # def __str__(self):
    #     final = f"{{ \"target\" : \"{self.name}\", "
    #     i = 0
    #     for prereq in self.go_through():
    #         final +=  f"\"prereq{i}\" : \"{prereq.get()}\", "
    #         i += 1
    #     return f"{final[:-2]} }}" # slice to -1 to remove last comma and space

    def __str__(self):
        final = ""
        for prereq in self.prereq_names:
            final += prereq
        
        for preNode in self.go_through():
            for req in preNode.prereq_names:
                final += req
        return final
    
    def __eq__(self, rhs):
        if (isinstance(rhs, ClassNode)):
            # names are all that really matter for class nodes, so just compare that
            return self.name == rhs.name
        
        # otherwise this should be sufficient... not foolproof
        return self.name == rhs

# if __name__ == "__main__":
#     n = ClassNode("CS232", ["CS112", "ENGR220"])
#     assert(n.name == "CS232")
#     assert(n.prereqs[0] == "CS112")
#     print("All tests passed!")