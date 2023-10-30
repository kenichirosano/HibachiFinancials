# Class of each concept defined in DTS (taxonomy schema files)
class Instance:
    def __init__(self, element):
        self.name = element.localName
        self.value = element.nodeValue