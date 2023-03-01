import time

POS_FILE = "./data/positions.xyz"

def cube(pos, distance):
    """Get the three indices for the cube containing the given position."""
    [x,y,z] = pos
    return (int(x//distance), int(y//distance), int(z//distance))


def dist(p1, p2):
    """Geometrical distance between two points."""
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**.5


def pos_to_cubes(positions, distance):
    """Returns a dictionary {(index_x, index_y, index_z): [pos1, pos2, ... ], ... } with the points contained in each cube."""

    cubes = {(0,0,0): []}

    for pos in positions:

        # Get the cube that the particle belongs to:
        cube_indices = cube(pos, distance)

        if cube_indices in cubes:
            cubes[cube_indices].append(pos)
        else:
            cubes[cube_indices] = [pos]

    return cubes


def num_pairs(cubes, distance):
    """Determine the number of pairs within the given distance."""

    num = 0

    for i,j,k in cubes:

        for _ in range(len(cubes[(i,j,k)])):
            # For each point we need to check the 27 cubes with indices (i-1,j-1,k-1), ... , (i,j,k), ... , (i+1,j+1,k+1):

            p1 = cubes[(i,j,k)].pop()

            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    for dk in [-1, 0, 1]:

                        indices = (i+di, j+dj, k+dk)
                        
                        if indices in cubes:
                            for p2 in cubes[indices]:
                                if dist(p1,p2) < distance:
                                    num += 1

    return num


def main():
    """Main function to get number of pairs within the distance d = .05 m"""

    start = time.time()

    distance = .05

    with open(POS_FILE, 'r', encoding='UTF-8') as file:
        data = file.readlines()

    # Positions in format [[x1,y1,z1], [x2,y2,z2], ...]:
    positions = [[float(coord) for coord in pos.split()] for pos in data]

    cubes = pos_to_cubes(positions, distance)

    num = num_pairs(cubes, distance)

    print("There are", num, "pairs within a distance of", distance, "m from each other")

    end = time.time()

    print("Processed in", round(end-start, 3), "s.")


if __name__ == '__main__':
    main()
