import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import Counter, defaultdict

class ShipVisualizer:
    fig = plt.figure(figsize=(15, 15))
    fig_cols = 0
    fig_rows = 1
    numOfProcessedLayer = 0
    layersOfContainers = {}
    numberOfPackedContainers = 0
    numberOfPlotedContainers = 0
    containersPerShip=defaultdict(list)

    def __init__(self, algorithmName):
        self.algorithmName = algorithmName
        if not os.path.exists("results"):
            os.makedirs("results")

    def setLayersPerShip(self, packer):
        self.layersPerShip = Counter(packer)

    def setFigCols(self, id):
        self.fig_cols = self.layersOfContainers[id]

    def setNumberOfPackedContainers(self,packer):
        self.numberOfPackedContainers = len(packer.rect_list())

    def saveFigure(self, shipId):
        self.numOfProcessedLayer = 0
        pathToImg = "results/" + self.algorithmName + "_" + str(shipId) + ".png"
        self.fig.savefig(pathToImg, dpi=144, bbox_inches='tight')
        self.fig = plt.figure(figsize=(15, 15))

    def prepareSubAxis(self, layerId):
        self.setFigCols(layerId)
        self.numOfProcessedLayer += 1
        return self.fig.add_subplot(self.fig_rows, self.fig_cols, self.numOfProcessedLayer, aspect='equal')

    def fillSubAxisWithRectangles(self, layer, subAxis):
        for container in layer:
            self.numberOfPlotedContainers += 1
            plt.axis([0, layer.width, 0, layer.height])

            subAxis.add_patch(
                Rectangle((container.x, container.y), container.width, container.height,
                          facecolor="green", edgecolor="black", linewidth=3))
            subAxis.annotate(container.rid, (container.x+container.width/2, container.y+container.height/2), color='w', weight='bold',
                        fontsize=6, ha='center', va='center')
            self.containersPerShip[layer.bid].append(str(container.rid))

        subAxis.set_title("Ship id: " + str(layer.bid) + ", Level " + str(self.numOfProcessedLayer))

    def prepareFigureOfContainersOnSpecificShip(self, layer):
        subAxis = self.prepareSubAxis(layer.bid)
        self.fillSubAxisWithRectangles(layer, subAxis)
        if (self.numOfProcessedLayer == self.fig_cols) or \
           (self.numberOfPlotedContainers == self.numberOfPackedContainers):
            self.saveFigure(layer.bid)

    def VisualizeOfAllContainersOnShip(self, packer, layersOfContainers):
        self.setLayersPerShip(packer)
        self.layersOfContainers = layersOfContainers
        self.setNumberOfPackedContainers(packer)
        for layer in packer:
            self.prepareFigureOfContainersOnSpecificShip(layer)
