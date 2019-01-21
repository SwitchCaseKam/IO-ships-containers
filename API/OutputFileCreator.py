from math import floor
import os

class OutputFileCreator:

    surfacesOfShips = {}
    surfacesOfContainersOnShip = {}
    numberOfContainersInEachShip = {}

    def __init__(self, resources, packer, packerHandler, containersPerShip):
        self.resources = resources
        self.packer = packer
        self.packerHandler = packerHandler
        self.percentageOfFilledSurface = self.calculatePercentageOfFilledSurface()
        print(self.percentageOfFilledSurface)
        self.containersPerShip = containersPerShip

    def calculatePercentageOfFilledSurface(self):           # calculate percentage fill of the surface of the ship
        self.heightOfContainer = self.packerHandler.heightOfContainer
        self.totalSurfaceOfAllLayersInShip()
        self.totalSurfaceOfAllPackedContainers()
        result = {key: self.surfacesOfContainersOnShip.get(key, 0) / self.surfacesOfShips.get(key, 0)
                  for key in set(self.surfacesOfContainersOnShip) | set(self.surfacesOfShips)}
        return result

    def deletePackedContainersFromResources(self, idOfNotFullShips):    # delete containers from resurces, that are packed in ship
        for layer in self.packer:
            if layer.bid in idOfNotFullShips:
                continue
            for container in layer:
                self.resources.containers = \
                    [cont for cont in self.resources.containers if cont.id != container.rid]

    def deletePreparedShipToSetOff(self, idsOfShipsReadyToSetOff):      # delete ships which are packed
        for id in idsOfShipsReadyToSetOff:
            self.resources.ships = [ship for ship in self.resources.ships if ship.id != id]


    def calculateSurfaceOfLayerMadeByContainers(self, layer):       # return sum of container surfaces on each level
        containersSurfaceOnLayer = 0
        for container in layer:
            containersSurfaceOnLayer += container.width * container.height
        return containersSurfaceOnLayer

    def totalSurfaceOfAllLayersInShip(self):                # calculate all possible surface in current ship
        for ship in self.resources.ships:
            layers = floor(ship.height / self.heightOfContainer)        # count layers number
            self.surfacesOfShips[ship.id] = layers * ship.width * ship.length

    def totalSurfaceOfAllPackedContainers(self):            # calculate surface of all packed containers in current ship
        for ship in self.resources.ships:
            self.surfacesOfContainersOnShip[ship.id] = 0
            self.numberOfContainersInEachShip[ship.id] = 0
        for layer in self.packer:
            self.surfacesOfContainersOnShip[layer.bid] += self.calculateSurfaceOfLayerMadeByContainers(layer)
            self.numberOfContainersInEachShip[layer.bid] += 1

    def createContainersWithIdOfFullAndNotFullShips(self): # returns two list. First contains id of ships ready to set off, second which are not
        idsOfFullShips = []
        idsOfNotFullShips = []
        for key, val in self.percentageOfFilledSurface.items():
            if val > 0.60:
                idsOfFullShips.append(key)
            else:
                idsOfNotFullShips.append(key)
        self.numOfFullShips = len(idsOfFullShips)
        return idsOfFullShips, idsOfNotFullShips

    def removeUsedResources(self):      # remove used ships and containers
        fullShips, notFullShips = self.createContainersWithIdOfFullAndNotFullShips()
        self.deletePreparedShipToSetOff(fullShips)
        self.deletePackedContainersFromResources(notFullShips)

    def saveResourcesLegacy(self):          # save all containers and ships that left in harbour
        if os.path.exists("resourcesLegacy.txt"):
            os.remove("resourcesLegacy.txt")

        self.resources.sortContainersById()
        file = open("resourcesLegacy.txt", "w")

        for ship in self.resources.ships:
            file.write(str(ship))

        for container in self.resources.containers:
            file.write(str(container))

        file.close()

    def saveSummary(self):      # save summary report
        if os.path.exists("summary.txt"):
            os.remove("summary.txt")

        file = open("summmary.txt", "w")
        file.write("SHIP PACKER REPORT\n")
        file.write("\n")
        file.write("Initial resources:\n")
        file.write("Amount of ships: " + str(len(self.percentageOfFilledSurface)) + "\n")
        file.write("Amount of containers: " + str(self.packerHandler.amountOfContainersInResources) + "\n")
        file.write("\n")
        file.write("\n")
        file.write("Results: \n")
        file.write("\n")
        file.write("Number of ships ready to set off: " + str(self.numOfFullShips) + "\n")
        file.write("Number of packed containers: " + str(
            self.packerHandler.amountOfContainersInResources-len(self.resources.containers)) + "\n")
        file.write("\n")
        file.write("Number of left ships: " + str(len(self.resources.ships)) + "\n")
        file.write("Number of left containers: " + str(len(self.resources.containers)) + "\n")

        file.close()

    def saveContainersOnFullShipReport(self):   # save report with containers in each ship
        with open("containersOnFullShips", 'w') as overallReport:
            overallReport.write("*** OVERALL REPORT *** \n\n")
            for ship in self.containersPerShip:
                overallReport.write("Containers to ship: " + str(ship)+"\n")
                for container in self.containersPerShip[ship]:
                    overallReport.write(container+"\n")
                overallReport.write("\n")

    def saveRaport(self):       # save all reports
        self.removeUsedResources()
        self.saveResourcesLegacy()
        self.saveSummary()
        self.saveContainersOnFullShipReport()


