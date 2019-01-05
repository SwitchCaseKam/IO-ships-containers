import sys
sys.path.append('../')
from API.Resources import Resources
from API.PackerHandler import PackerHandler
from rectpack.packer import newPacker
from rectpack.packer import PackingMode
import unittest


class TestPackerHandler(unittest.TestCase):

    def test_fillResourcesWithDataFromFileFunctionShouldFillResourcesData(self):
        packerHandler = PackerHandler()
        resources = Resources()
        packerHandler.fillResourcesWithDataFromFile("../test_input", resources)
        ships_pattern = ["S001,89,68,82", "S002,94,88,82"]
        containers_pattern = ["C001,11,5,30,1546057335", "C002,39,14,30,1546042255"]
        self.assertEqual(str(resources.ships[0]).replace("\n", ""), ships_pattern[0])
        self.assertEqual(str(resources.ships[1]).replace("\n", ""), ships_pattern[1])
        self.assertEqual(str(resources.containers[0]).replace("\n", ""), containers_pattern[0])
        self.assertEqual(str(resources.containers[1]).replace("\n", ""), containers_pattern[1])


if __name__ == '__main__':
    unittest.main()