from API import Common
from math import floor

class PackerHandler:
    heightOfShips = None
    layersOfContainers = []

    def __init__(self):
        self.layersOfContainers.append(None)

    def fillResourcesWithDataFromFile(self, inputFileName, resources):
        file = open(inputFileName, "r")
        for line in file:
            if line[0] == 'S':
                resources.getShip(line)
            elif line[0] == 'C':
                resources.getContainer(line)
            else:
                Common.terminateScript("Undefined ID")
        file.close()

    def packContainersToShips(self, resources, packer):
        for container in resources.containers:
            packer.add_rect(container.width, container.length)

        self.heightOfShips = resources.containers[0].height

        for ship in resources.ships:
            layers = floor(ship.height/self.heightOfShips)
            packer.add_bin(ship.width, ship.length, count=layers, bid=int(ship.id[1:]))
            self.layersOfContainers.append(layers)
        packer.pack()

    def executePacker(self, inputFileName, resources, packer):
        self.fillResourcesWithDataFromFile(inputFileName, resources)
        self.packContainersToShips(resources, packer)

