from node import ClassNode
from json import dumps

class PreReqTree():

    def __init__(self, headNode: ClassNode, data: dict[str,ClassNode]):
        self.head: ClassNode = headNode

        # recursively construct the rest of the nodes based on head's prereqs
        self.head.expand_prereqs(data)

    def generate_report(self):
        print(dumps(self.head.get_prereqs_rec())) # json dump the to stdin
        
        pass