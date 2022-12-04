
class MObject:
    def __init__(self):
        self.callback = None

    def connect(self, function):
        self.callback = function
