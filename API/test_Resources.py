import sys
sys.path.append('../')
from API.Resources import Resources
import unittest


class TestResources(unittest.TestCase):

    def test_getShipShouldAddShipsToArray(self):
        line = "S001,89,68,82"
        innerResources = Resources()
        innerResources.getShip(line)
        assert str(innerResources.ships[0]).replace('\n', '') == "S001,89,68,82"

    def test_getContainerShouldAddContainersToArray(self):
        line = "C001,11,5,30,1546057335"
        innerResources = Resources()
        innerResources.getContainer(line)
        assert str(innerResources.containers[0]).replace('\n', '') == "C001,11,5,30,1546057335"

    def test_timestampCompareFunctionShouldReturnTimestamp(self):
        line = "C024,14,16,30,1546024033"
        innerResources = Resources()
        innerResources.getContainer(line)
        assert str(innerResources.timestampCompareFunction(innerResources.containers[1])) == "1546024033"

if __name__ == '__main__':
    unittest.main()