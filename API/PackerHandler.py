from API import Common
from math import floor

class PackerHandler:
    heightOfContainer = None
    layersOfContainers = {}
    amountOfContainersInPacker = 0
    amountOfContainersInResources = 0

    def fillResourcesWithDataFromFile(self, inputFileName, resources):                  # insert data about ships and containers to arrays of class Resources
        file = open(inputFileName, "r")                                                 # read input file
        for line in file:
            if line[0] == 'S':
                resources.getShip(line)                                                 # insert ship to ships array in Resources class
            elif line[0] == 'C':
                resources.getContainer(line)                                            # insert container to containers array in Resources class
            else:
                Common.terminateScript("Undefined ID")
        file.close()

    def packContainersToShipsOffline(self, resources, packer):                          # pack ship to ship in Resources class - offline = no wait for containers, immediate packing
        self.heightOfContainer = resources.containers[0].height                         # all containers have the same height, so only need to get value of one container

        for container in resources.containers:
            packer.add_rect(container.width, container.length)                          # add container to containers to pack pool

        for ship in resources.ships:
            layers = floor(ship.height / self.heightOfContainer)                        # calculate how many floor of containers is possible to create in current ship
            packer.add_bin(ship.width, ship.length, count=layers, bid=ship.id)          # add ships to ships pool
            self.layersOfContainers[ship.id] = layers
        packer.pack()

        self.amountOfContainersInPacker = len(packer.rect_list())
        self.amountOfContainersInResources = len(resources.containers)

    def packContainersToShipsOnline(self, resources, packer):                           # pack ship to ship in Resources class - online = wait for containers
        resources.sortContainersByTimestamp()
        self.heightOfContainer = resources.containers[0].height                         # all containers have the same height, so only need to get value of one container

        for ship in resources.ships:
            layers = floor(ship.height / self.heightOfContainer)                        # calculate how many floor of containers is possible to create in current ship
            packer.add_bin(ship.width, ship.length, count=layers, bid=ship.id)          # add ships to ships pool
            self.layersOfContainers[ship.id] = layers

        for container in resources.containers:
            packer.add_rect(container.width, container.length, rid=container.id)        # add container to containers to pack pool

        self.amountOfContainersInPacker = len(packer.rect_list())
        self.amountOfContainersInResources = len(resources.containers)

    def executePacker(self, inputFileName, resources, packer):                          # executable function of class PackerHandler
        self.fillResourcesWithDataFromFile(inputFileName, resources)                    # fill input data from file to structure
        self.packContainersToShipsOnline(resources, packer)                             # pack containers to ship
