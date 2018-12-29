from random import randint, SystemRandom
from containers import Container
from ships import Ship
import time

class DataGenerator:
    def __init__(self, ships_num, containers_num, timestamps_num ):
        self.containers_num = containers_num
        self.ships_num = ships_num
        self.timestamps_num = timestamps_num

        self.ships = []
        self.containers = []
        self.timestamps = []

        self.ships_min_width = 50
        self.ships_max_width = 100
        self.ships_min_length = 50
        self.ships_max_length = 100
        self.ships_min_height = 50
        self.ships_max_height = 100

        self.containers_min_width = 1
        self.containers_max_width = 40
        self.containers_min_length = 1
        self.containers_max_length = 40
        self.containers_min_height = 1
        self.containers_max_height = 40

    def generate_timestamps(self):
        for timestamp in range(1, self.timestamps_num):
            self.timestamps.append(int(time.time())-randint(100, 100000))

    def generate_ships(self):
        ids = ["S" +str(id+1).zfill(3) for id in range(0, self.ships_num)]
        for id in ids:
            self.ships.append(Ship(id,
                                randint(self.ships_min_width, self.ships_max_width),
                                randint(self.ships_min_length, self.ships_max_length),
                                randint(self.ships_min_height, self.ships_max_height)))

    def generate_containers(self):
        ids = ["C" +str(id+1).zfill(3) for id in range(0, self.containers_num)]
        height = randint(self.containers_min_height, self.containers_max_height)
        for id in ids:
            self.containers.append(Container(id,
                                        randint(self.containers_min_width, self.containers_max_width),
                                        randint(self.containers_min_length, self.containers_max_length),
                                        height,
                                        SystemRandom().choice(self.timestamps)))


    def write_to_file(self, filename):
        self.generate_timestamps()
        self.generate_ships()
        self.generate_containers()
        with open(filename, "w") as f:
            for ship in self.ships:
                f.write(str(ship))
            for container in self.containers:
                f.write(str(container))

if __name__ == "__main__":
    a = DataGenerator(5, 200, 10)
    a.write_to_file("../input")