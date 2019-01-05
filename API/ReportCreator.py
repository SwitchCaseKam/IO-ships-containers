from API.Resources import Resources
from rectpack.packer import newPacker
from API.ShipVisualizer import ShipVisualizer
from API.PackerHandler import PackerHandler
from API import Common
from rectpack.packer import PackingMode
from math import floor
from operator import truediv
import os

class ReportCreator:
    def __init__(self, _inputFileName , _algorithmName):
        self.resources = Resources()
        self.inputFileName = _inputFileName
        self.algorithmName = _algorithmName
        self.packer = newPacker(mode=PackingMode.Online, pack_algo=self.getAlgotithmClass())
        self.packerHandler = PackerHandler()
        self.shipVisualizer = ShipVisualizer(_algorithmName)
        self.surfacesOfShips = {}
        self.surfacesOfContainersOnShip = {}
        self.numberOfContainersInEachShip = {}

    def getAlgotithmClass(self):
        if self.algorithmName == "Guillotine":
            from rectpack import GuillotineBssfMaxas
            return GuillotineBssfMaxas
        elif self.algorithmName == "MaxRects":
            from rectpack import MaxRectsBssf
            return MaxRectsBssf
        elif self.algorithmName == "Skyline":
            from rectpack import SkylineMwfl
            return SkylineMwfl
        else:
            Common.terminateScript("Undefined algorithm")

    def saveUnusedResourcesToFile(self):

        percentageOfFilledSurface = self.calculatePercentageOfFilledSurface()
        print(percentageOfFilledSurface)
        idOfFullShip = []
        idOfNotFullShips = []

        for key, val in percentageOfFilledSurface.items():
            if val > 0.60:
                idOfFullShip.append(key)
            else:
                idOfNotFullShips.append(key)

        self.deletePreparedShipToSetOff(idOfFullShip)
        self.deletePackedContainersFromResources(idOfNotFullShips)

        if os.path.exists("resourcesLegacy.txt"):
            os.remove("resourcesLegacy.txt")

        self.resources.sortContainersById()
        file = open("resourcesLegacy.txt", "w")

        for ship in self.resources.ships:
            file.write(str(ship))

        for container in self.resources.containers:
            file.write(str(container))

        file.close()

        if os.path.exists("summary.txt"):
            os.remove("summary.txt")

        file = open("summmary.txt", "w")
        file.write("SHIP PACKER REPORT\n")
        file.write("\n")
        file.write("Initial resources:\n")
        file.write("Amount of ships: " + str(len(percentageOfFilledSurface)) + "\n")
        file.write("Amount of containers: " + str(self.packerHandler.amountOfContainersInResources) + "\n")
        file.write("\n")
        file.write("\n")
        file.write("Results: \n")
        file.write("\n")
        file.write("Number of ships ready to set off: " + str(len(idOfFullShip)) + "\n")
        file.write("Number of packed containers: " + str(self.packerHandler.amountOfContainersInResources-len(self.resources.containers)) + "\n")
        file.write("\n")
        file.write("Number of left ships: " + str(len(self.resources.ships)) + "\n")
        file.write("Number of left containers: " + str(len(self.resources.containers)) + "\n")
        file.close()

    def calculateSurfaceOfLayerMadeByContainers(self, layer):
        containersSurfaceOnLayer = 0
        for container in layer:
            containersSurfaceOnLayer += container.width * container.height
        return containersSurfaceOnLayer

    def totalSurfaceOfAllLayersInShip(self):
        for ship in self.resources.ships:
            layers = floor(ship.height / self.heightOfContainer)
            self.surfacesOfShips[ship.id] = layers * ship.width * ship.length

    def totalSurfaceOfAllPackedContainers(self):
        for ship in self.resources.ships:
            self.surfacesOfContainersOnShip[ship.id] = 0
            self.numberOfContainersInEachShip[ship.id] = 0
        for layer in self.packer:
            self.surfacesOfContainersOnShip[layer.bid] += self.calculateSurfaceOfLayerMadeByContainers(layer)
            self.numberOfContainersInEachShip[layer.bid] += 1

    def calculatePercentageOfFilledSurface(self):
        self.heightOfContainer = self.packerHandler.heightOfContainer
        self.totalSurfaceOfAllLayersInShip()
        self.totalSurfaceOfAllPackedContainers()
        result = {key: self.surfacesOfContainersOnShip.get(key, 0) / self.surfacesOfShips.get(key, 0)
                  for key in set(self.surfacesOfContainersOnShip) | set(self.surfacesOfShips)}
        return result

    def deletePackedContainersFromResources(self, idOfNotFullShips):
        for layer in self.packer:
            if layer.bid in idOfNotFullShips:
                continue
            for container in layer:
                self.resources.containers = \
                    [cont for cont in self.resources.containers if cont.id != container.rid]

    def deletePreparedShipToSetOff(self, idsOfShipsReadyToSetOff):
        for id in idsOfShipsReadyToSetOff:
            self.resources.ships = [ship for ship in self.resources.ships if ship.id != id]

    def start(self):
        self.packerHandler.executePacker(self.inputFileName, self.resources, self.packer)
        self.shipVisualizer.VisualizeOfAllContainersOnShip(self.packer, self.packerHandler.layersOfContainers)
        self.saveUnusedResourcesToFile()
