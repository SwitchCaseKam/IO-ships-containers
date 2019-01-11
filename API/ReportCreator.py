from API.Resources import Resources
from rectpack.packer import newPacker
from API.ShipVisualizer import ShipVisualizer
from API.PackerHandler import PackerHandler
from API import Common
from rectpack.packer import PackingMode
from API.OutputFileCreator import OutputFileCreator

class ReportCreator:
    def __init__(self, _inputFileName , _algorithmName):
        self.resources = Resources()
        self.inputFileName = _inputFileName
        self.algorithmName = _algorithmName
        self.packer = newPacker(mode=PackingMode.Online, pack_algo=self.getAlgotithmClass())
        self.packerHandler = PackerHandler()
        self.shipVisualizer = ShipVisualizer(_algorithmName)

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


    def start(self):
        self.packerHandler.executePacker(self.inputFileName, self.resources, self.packer)
        self.shipVisualizer.VisualizeOfAllContainersOnShip(self.packer, self.packerHandler.layersOfContainers)
        outputFileCreator = OutputFileCreator(self.resources, self.packer, self.packerHandler, self.shipVisualizer.containersPerShip)
        outputFileCreator.saveRaport()
