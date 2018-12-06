class Ship:
    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

    def __str__(self):
        return str(self.id)+","+str(self.width)+","+str(self.length)+","+str(self.height)+"\n"
