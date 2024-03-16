from node import ClassNode

class PreReqTree():

    def __init__(self, headNode: ClassNode, data: dict[str,ClassNode]):
        self.head: ClassNode = headNode

        # recursively construct the rest of the nodes based on head's prereqs
        self.head.expand_prereqs(data)

    def generate_report(self):
        #res = self.head.go_through()
        #print(f"\n\n{[req.name for req in res]}")
        print(self.head)