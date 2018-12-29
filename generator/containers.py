class Container:
    def __init__(self, id, width, length, height, timestamp=None):
        self.id = id
        self.width = width
        self.length = length
        self.height = height
        self.timestamp = timestamp

    def __str__(self):
        return str(self.id)+","+str(self.width)+","+str(self.length)+","+str(self.height)+","+str(self.timestamp)+"\n"
