from csv import reader
from node import ClassNode
from tree import PreReqTree
from sys import argv

CSVNAME = "classNodes.csv"

class PreReqCalc():
    def __init__(self, target_class: str, csv_path: str, **kwargs):
        '''kwags:
        has_headers: true for ignoring csv headers'''
        self.target: ClassNode
        self.data: dict[str,ClassNode] = dict[str,ClassNode]()
        with open(csv_path, 'r', newline='') as f:
            class_nodes_info = reader(f)

            # skip one row if the data has headers
            if kwargs.get("has_headers", False): next(class_nodes_info, None) 

            for row in class_nodes_info:

                # set up the prereq relationships (AND/OR) in json format
                prereqs = [] # this will replace the 2nd row later on
                for orCourse in row[2].split(" OR "):
                    split_courses = orCourse.split(" AND ")
                    if (len(split_courses) > 1):
                        # if there are courses that have to be taken together
                        prereqs.append({"relationship" : "AND", "courses" : split_courses})
                    else:
                        # does not have to take both (OR)
                        prereqs.append({"relationship" : "OR", "courses" : split_courses})
                
                # make the node
                name: str = row[0] + row[1]
                node: ClassNode = ClassNode(name, prereqs, row[3], row[4], row[5])

                # if the node is the target
                if name == target_class:
                    self.target = node

                # add node to the bunch of nodes
                self.data[name] = node
        
        self.tree = PreReqTree(self.target, self.data)
        self.tree.generate_report()
    
if __name__ == "__main__":
    prc = PreReqCalc(argv[1], CSVNAME, has_headers = True)