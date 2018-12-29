from generator.containers import Container
from generator.ships import Ship

class Resources:
    ships = []
    containers = []

    def getShip(self, line):
        id, width, length, height = line.split(",")
        ship = Ship(id, int(width), int(length), int(height))
        self.ships.append(ship)

    def getContainer(self, line):
        id, width, length, height, timestamp = line.split(",")
        container = Container(id, int(width), int(length), int(height), int(timestamp))
        self.containers.append(container)


