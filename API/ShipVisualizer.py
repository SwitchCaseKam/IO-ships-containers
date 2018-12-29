import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import Counter

class ShipVisualizer:
    fig = plt.figure(figsize=(15, 15))
    fig_cols = 0
    fig_rows = 1
    numOfProcessedLayer = 0
    layersOfContainers = []

    def __init__(self, algorithmName):
        self.algorithmName = algorithmName
        if not os.path.exists("results"):
            os.makedirs("results")

    def setLayersPerShip(self, packer):
        self.layersPerShip = Counter(packer)

    def setFigCols(self, id):
        self.fig_cols = self.layersOfContainers[id]

    def saveFigureIfAllLayerProcessed(self, shipId):
        if self.numOfProcessedLayer == self.fig_cols:
            self.numOfProcessedLayer = 0
            pathToImg = "results/" + self.algorithmName + "_Ship" + str(shipId) + ".png"
            self.fig.savefig(pathToImg, dpi=144, bbox_inches='tight')
            self.fig = plt.figure(figsize=(15, 15))

    def prepareFigureOfContainersOnSpecificShip(self, layer):
        self.setFigCols(layer.bid)
        self.numOfProcessedLayer += 1
        subAxis = self.fig.add_subplot(self.fig_rows, self.fig_cols, self.numOfProcessedLayer, aspect='equal')

        for container in layer:
            plt.axis([0, layer.width, 0, layer.height])
            subAxis.add_patch(
                Rectangle((container.x, container.y), container.width, container.height,
                           facecolor="green", edgecolor="black", linewidth=3))

        subAxis.set_title("Ship num: " + str(layer.bid) + ", Level " + str(self.numOfProcessedLayer))
        self.saveFigureIfAllLayerProcessed(layer.bid)

    def VisualizeOfAllContainersOnShip(self, packer, layersOfContainers):
        self.setLayersPerShip(packer)
        self.layersOfContainers = layersOfContainers
        all_rects = packer.rect_list()
        i = 0
        for rect in all_rects:
            i += 1
        print(i)
        for layer in packer:
            self.prepareFigureOfContainersOnSpecificShip(layer)




