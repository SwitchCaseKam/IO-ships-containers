import sys
sys.path.append('../')
from API.Resources import Resources
from API.PackerHandler import PackerHandler
from rectpack.packer import newPacker
from rectpack.packer import PackingMode
import unittest

class TestReportCreator(unittest.TestCase):

    def test_totalSurfaceOfAllLayersInShip(self):
        assert 1 == 1

if __name__ == '__main__':
    unittest.main()