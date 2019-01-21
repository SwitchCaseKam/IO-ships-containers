from API.Resources import Resources
from rectpack.packer import newPacker
from API.ShipVisualizer import ShipVisualizer
from API.PackerHandler import PackerHandler
from API import Common
from rectpack.packer import PackingMode
from API.OutputFileCreator import OutputFileCreator

'''
Script is responsible for creating raports.
'''



class ReportCreator:
    def __init__(self, _inputFileName , _algorithmName): # init bacis structures
        self.resources = Resources()
        self.inputFileName = _inputFileName
        self.algorithmName = _algorithmName
        self.packer = newPacker(mode=PackingMode.Online, pack_algo=self.getAlgotithmClass())
        self.packerHandler = PackerHandler()
        self.shipVisualizer = ShipVisualizer(_algorithmName)

    def getAlgotithmClass(self):                 # select packing algorithm
        if self.algorithmName == "Guillotine":
            """
            Implements Best Short Side Fit (BSSF) section selection criteria for 
            Guillotine algorithm.
            Implements Max Area Axis Split (MAXAS) selection rule for Guillotine
            algorithm. Maximize the larger area == minimize the smaller area.
            Tries to make the rectangles more even-sized.
            """
            from rectpack import GuillotineBssfMaxas
            return GuillotineBssfMaxas

        elif self.algorithmName == "MaxRects":
            """Best Sort Side Fit minimize short leftover side"""
            from rectpack import MaxRectsBssf
            return MaxRectsBssf

        elif self.algorithmName == "Skyline":
            """
            Implements Min Waste fit with low profile heuritic, minimizing the area
            wasted below the rectangle, at the same time it tries to keep the height
            minimal.
            """
            from rectpack import SkylineMwfl
            return SkylineMwfl

        else:
            Common.terminateScript("Undefined algorithm")


    def start(self):
        self.packerHandler.executePacker(self.inputFileName, self.resources, self.packer)   # handling packer object
        self.shipVisualizer.VisualizeOfAllContainersOnShip(self.packer, self.packerHandler.layersOfContainers) # visualize results
        outputFileCreator = OutputFileCreator(self.resources, self.packer, self.packerHandler, self.shipVisualizer.containersPerShip)
        outputFileCreator.saveRaport()
