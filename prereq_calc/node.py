class ClassNode():
    
    def __init__(self, class_name, class_prereqs, class_credits, class_period, class_required):
        self.name: str = class_name
        self.prereq_names: list[str] = class_prereqs
        self.credits = class_credits
        self.period = class_period
        self.required = True if class_required == 1 else False

    def expand_prereqs(self, data):
        for full_prereq in self.prereq_names:
            # e.g. full_prereq: {'relationship': 'OR', 'courses': ['CHEM101']}

            class_nodes_to_add = [] # have to save adding all these until after so that we're not modifying the list during its iteration
            classes_to_remove = [] # have to keep for the same reason as above
            for prereq in full_prereq["courses"]:
                # e.g. prereq: 'CHEM101'

                if (isinstance(prereq, ClassNode)): 
                    # if this has already been turned into a node, will happen if certain node has already been processed
                    # as a different course's prereq
                    break

                # remove the prereq name, it will be replaced by an actual node object
                classes_to_remove.append(prereq)

                # check if the prereq node was already made in data
                prereq_node = data.get(prereq, None)
                # if node was found in data
                if (prereq_node != None):
                    prereq_node.expand_prereqs(data) # recursively expand the other nodes
                    class_nodes_to_add.append(prereq_node)
                else:
                    # if prereq is not in data because it is not a class (e.g. "Senior standing")
                    class_nodes_to_add.append(ClassNode(prereq, [], None, None, 0))
            
            for course in classes_to_remove:
                full_prereq["courses"].remove(course)
            full_prereq["courses"].extend(class_nodes_to_add) # extend() to not have sublist (would happen with append())

    def go_through(self):
        to_process = self.get_prereqs() # start with first node's prereqs
        seen_prereqs = [] # keep track of unique prereqs

        while to_process: # while there are still nodes to process
            current = to_process.pop(0) # get the node to process
            # print(current.name)
            # print(current in seen_prereqs)

            if current not in seen_prereqs:
                # if current is unique
                seen_prereqs.append(current) # has now been "seen"

                # recursively go through the new node's prereqs to process
                for prereq in current.get_prereqs():
                    to_process.append(prereq)
        
        return seen_prereqs

    def get_prereqs(self, name = False):
        prereqs = {}
        for full_prereq in self.prereq_names:
            # e.g. full_prereq: {'relationship': 'OR', 'courses': ['CHEM101']}
            prereqs[full_prereq["relationship"]] = []
            for prereq in full_prereq["courses"]:
                # e.g. prereq: ClassNode
                prereqs[full_prereq["relationship"]].append(prereq.name if name else prereq)
        return prereqs
    
    def get_prereqs_rec(self):
        total = {self.name: {}}
        # for each combination of relationship and courses
        for relationship, courses in self.get_prereqs().items():
            for prereq in courses:
                if (relationship not in total[self.name]):
                    # if the relationship key needs to be made
                    total[self.name][relationship] = {}
                # pass onto the second stage recursive backbone. It will fill all the prereqs and their prereqs.
                total[self.name][relationship][prereq.name] = prereq.__get_prereqs_rec() 
        
        return total
    
    def __get_prereqs_rec(self):
        total = {}
        for relationship, courses in self.get_prereqs().items():
            for prereq in courses:
                if (len(courses) == 0):
                    # if next node has no prereqs
                    return prereq.name
                
                if (relationship not in total):
                    # if the realtionship key needs to be made
                    total[relationship] = {}
                total[relationship][prereq.name] = prereq.__get_prereqs_rec()

        return total
    
    def __eq__(self, rhs):
        if (isinstance(rhs, ClassNode)):
            # names are all that really matter for class nodes, so just compare that
            return self.name == rhs.name
        
        # otherwise this should be sufficient... not foolproof
        return self.name == rhs