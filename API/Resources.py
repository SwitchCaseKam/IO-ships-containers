from generator.containers import Container
from generator.ships import Ship

class Resources:        # class to storage data about ships and containers
    ships = []          # structure to store ships
    containers = []     # structure to store containers

    def getShip(self, line):                                        # add Ship to ships array of class Resources
        id, width, length, height = line.split(",")
        ship = Ship(id, int(width), int(length), int(height))
        self.ships.append(ship)

    def getContainer(self, line):                                   # add Container to containers array of class Resources
        id, width, length, height, timestamp = line.split(",")
        container = Container(id, int(width), int(length), int(height), int(timestamp))
        self.containers.append(container)

    def timestampCompareFunction(self, container):                  # retrun timestamp of current container
        return container.timestamp

    def sortContainersByTimestamp(self):                            # sort containers by timestamp (priority of container)
        self.containers.sort(key=self.timestampCompareFunction)

    def idCompareFunction(self, container):                         # return container id
        return container.id[1:]

    def sortContainersById(self):                                   # sort container by id
        self.containers.sort(key=self.idCompareFunction)
