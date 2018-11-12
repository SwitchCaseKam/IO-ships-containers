from random import randint
import sys

def generate_ships(amount, file_name):
    ids = ["S" +str(id+1).zfill(3) for id in range(0, amount)]
    ships = []
    for id in ids:
        ships.append({"id": id, "width": randint(50, 100), "length": randint(50, 100), "height": randint(50, 100)})

    with open(file_name, "w") as file:
        file.writelines("id,width,length,height,\n");
        for ship in ships:
            file.write(str(ship['id'])+','+str(ship['width'])+','+str(ship['length'])+','+str(ship['height'])+',\n')
    print("--> Ships generated")


def generate_containers(amount, file_name):
    ids = ["C" + str(id + 1).zfill(3) for id in range(0, amount)]
    containers = []
    height = randint(1, 40)
    for id in ids:
        containers.append({"id": id, "width": randint(1, 40), "length": randint(1, 40), "height": height})

    with open(file_name, "w") as file:
        file.writelines("id,width,length,height,\n");
        for container in containers:
            file.write(str(container['id']) + ',' + str(container['width']) + ',' + str(container['length']) + ',' + str(container['height']) + ',\n')
    print("--> Containers generated")


def generator():
    if(len(sys.argv) == 5):
        generate_ships(int(sys.argv[1]), sys.argv[2])
        generate_containers(int(sys.argv[3]), sys.argv[4])
    elif (len(sys.argv) == 4):
        if(str(sys.argv[3]) == "S"):
            print("Ships only will be generated")
            generate_ships(int(sys.argv[1]), sys.argv[2])
        elif (str(sys.argv[3]) == "C"):
            print("Containers only will be generated")
            generate_containers(int(sys.argv[1]), sys.argv[2])
    else:
        print("Number of arguments incorrect - need 2, 4")


generator()