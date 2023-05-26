class Cell(object):
    index: int
    cell_type: int
    resources: int
    neighbors: list[int]
    my_ants: int
    opp_ants: int

    def __init__(
        self,
        index: int,
        cell_type: int,
        resources: int,
        neighbors: list[int],
        my_ants: int,
        opp_ants: int,
    ):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants


def find_nearest_resources_and_distance(base, cells):
    visited = set()
    queue = [(base, 0)]
    while len(queue) > 0:
        cell, distance = queue.pop(0)
        if cell.resources > 0:
            return cell, distance
        visited.add(cell.index)
        for neighbor in cell.neighbors:
            if neighbor not in visited:
                queue.append((cells[neighbor], distance + 1))
    return None, None


def total_ants(cells):
    return sum([cell.my_ants + cell.opp_ants for cell in cells])


##################################################################
## Load Initalization inputs
cells: list[Cell] = []

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    inputs = [int(j) for j in input().split()]
    cell_type = inputs[0]  # 0 for empty, 1 for eggs, 2 for crystal
    initial_resources = inputs[1]  # the initial amount of eggs/crystals on this cell
    neigh_0 = inputs[2]  # the index of the neighbouring cell for each direction
    neigh_1 = inputs[3]
    neigh_2 = inputs[4]
    neigh_3 = inputs[5]
    neigh_4 = inputs[6]
    neigh_5 = inputs[7]
    cell: Cell = Cell(
        index=i,
        cell_type=cell_type,
        resources=initial_resources,
        neighbors=list(
            filter(
                lambda id: id > -1,
                [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5],
            )
        ),
        my_ants=0,
        opp_ants=0,
    )
    cells.append(cell)
number_of_bases = int(input())
my_bases: list[int] = []
for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)
opp_bases: list[int] = []
for i in input().split():
    opp_base_index = int(i)
    opp_bases.append(opp_base_index)

##################################################################
# game loop
while True:
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0]  # the current amount of eggs/crystals on this cell
        my_ants = inputs[1]  # the amount of your ants on this cell
        opp_ants = inputs[2]  # the amount of opponent ants on this cell

        cells[i].resources = resources
        cells[i].my_ants = my_ants
        cells[i].opp_ants = opp_ants

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    actions = []

    # TODO: choose actions to perform and push them into actions
    for base in my_bases:
        cell, distance = find_nearest_resources_and_distance(cells[base], cells)
        if cell is not None:
            actions.append(
                f"LINE {base} {cell.index} {min(cell.resources ,total_ants(cells) // distance)}"
            )

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    if len(actions) == 0:
        print("WAIT")
    else:
        print(";".join(actions))
