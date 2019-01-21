import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import Counter, defaultdict

class ShipVisualizer:
    fig = plt.figure(figsize=(15, 15))
    figCols = 0
    fig_rows = 1
    numOfProcessedLayer = 0
    layersOfContainers = {}
    numberOfPackedContainers = 0
    numberOfPlotedContainers = 0
    containersPerShip=defaultdict(list)

    def __init__(self, algorithmName):      # init algorithm name and delete results if exists
        self.algorithmName = algorithmName
        if not os.path.exists("results"):
            os.makedirs("results")

    def setLayersPerShip(self, packer):     # count layers (levels) of the ship
        self.layersPerShip = Counter(packer)

    def setFigCols(self, id):               # set figure columns
        self.figCols = self.layersOfContainers[id]

    def setNumberOfPackedContainers(self,packer):   # set number of all packet containers to ships
        self.numberOfPackedContainers = len(packer.rect_list())

    def saveFigure(self, shipId):               # save file .png with location of containers in ships
        self.numOfProcessedLayer = 0
        pathToImg = "results/" + self.algorithmName + "_" + str(shipId) + ".png"
        self.fig.savefig(pathToImg, dpi=144, bbox_inches='tight')
        self.fig = plt.figure(figsize=(15, 15))

    def prepareSubAxis(self, layerId):      # function returns axis on which containers will be drawn
        self.setFigCols(layerId)
        self.numOfProcessedLayer += 1
        return self.fig.add_subplot(self.fig_rows, self.figCols, self.numOfProcessedLayer, aspect='equal')

    def fillSubAxisWithRectangles(self, layer, subAxis): # function is drawing containers in each layer of ship
        for container in layer:
            self.numberOfPlotedContainers += 1
            plt.axis([0, layer.width, 0, layer.height])

            subAxis.add_patch(Rectangle((container.x, container.y),  # create rectangle in the .png file
                                        container.width,
                                        container.height,
                                        facecolor="green",
                                        edgecolor="black",
                                        linewidth=3))

            subAxis.annotate(container.rid,                         # create label at rectangle
                             (container.x+container.width/2, container.y+container.height/2),
                             color='w',
                             weight='bold',
                             fontsize=6,
                             ha='center',
                             va='center')
            self.containersPerShip[layer.bid].append(str(container.rid))

        subAxis.set_title("Ship id: " + str(layer.bid) + ", Level " + str(self.numOfProcessedLayer))        # title of picture with rectangles

    def prepareFigureOfContainersOnSpecificShip(self, layer):           # create list with containers assign to ships
        subAxis = self.prepareSubAxis(layer.bid)
        self.fillSubAxisWithRectangles(layer, subAxis)
        if (self.numOfProcessedLayer == self.figCols) or \
           (self.numberOfPlotedContainers == self.numberOfPackedContainers):
            self.saveFigure(layer.bid)          # if all containers are drawn save figure

    def VisualizeOfAllContainersOnShip(self, packer, layersOfContainers):       # executable function of class ShipVisualizer
        self.setLayersPerShip(packer)
        self.layersOfContainers = layersOfContainers
        self.setNumberOfPackedContainers(packer)
        for layer in packer:
            self.prepareFigureOfContainersOnSpecificShip(layer)
