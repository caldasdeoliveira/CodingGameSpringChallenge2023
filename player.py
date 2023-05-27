from typing import List, Tuple, Dict


class Cell(object):
    index: int
    cell_type: int
    resources: int
    neighbors: List[int]
    my_ants: int
    opp_ants: int

    def __init__(
        self,
        index: int,
        cell_type: int,
        resources: int,
        neighbors: List[int],
        my_ants: int,
        opp_ants: int,
    ):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants

    def __str__(self):
        return f"Cell(index={self.index}, cell_type={self.cell_type}, resources={self.resources}, neighbors={self.neighbors}, my_ants={self.my_ants}, opp_ants={self.opp_ants})"

    def __repr__(self):
        return self.__str__()


##################################################################
## Helper functions


def get_my_number_ants(cells: List[Cell]) -> List[Cell]:
    return sum(map(lambda cell: cell.my_ants, cells))


def best_resource_path(base: Cell, cells: List[Cell]) -> List[Tuple[Cell, int]]:
    """
    Returns the best path to a resource. The best path is the one that has the most resources on the way.
    It is calculated by going through all the cells and calculating the value of each cell.
    The value is calculated by adding the resources of the cell to the value of the previous cell.
    The value of the base cell is 0.


    Args:
        base (Cell): The base cell
        cells (List[Cell]): The list of all cells

    Returns:
        List[Tuple[Cell, int]]: The list of cells to go through to get to the resource
    """
    visited: List[
        Dict[Cell, Cell, int, int]
    ] = []  # [{"cell": cell, "previous": cell, "distance": distance, "value": value}]
    queue: List[Dict[Cell, Cell, int, int]] = [
        {"cell": base, "previous": None, "distance": 1, "value": 0}
    ]

    while len(queue) > 0:
        current = queue.pop(0)

        if visited:
            if current["cell"].index in [v["cell"].index for v in visited]:
                continue

        visited.append(current)

        if current["distance"] < get_my_number_ants(cells):
            for neighbor in current["cell"].neighbors:
                if visited:
                    if cells[neighbor].index in [v["cell"].index for v in visited]:
                        continue
                queue.append(
                    {
                        "cell": cells[neighbor],
                        "previous": current["cell"],
                        "distance": current["distance"] + 1,
                        "value": current["value"] + cells[neighbor].resources - 1,
                    }
                )

        queue.sort(key=lambda cell: cell["value"], reverse=True)
    return visited


##################################################################
## Load Initalization inputs
cells: List[Cell] = []

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
my_bases: List[int] = []
for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)
opp_bases: List[int] = []
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
        visited = best_resource_path(cells[base], cells)
        max_value = max(visited, key=lambda cell: cell["value"])
        strength = get_my_number_ants(cells) // max_value["distance"]

        while True:
            actions.append(f"BEACON {max_value['cell'].index} {strength}")
            if max_value["previous"] is None:
                break
            max_value = visited[
                [v["cell"].index for v in visited].index(max_value["previous"].index)
            ]

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    if len(actions) == 0:
        print("WAIT")
    else:
        print(";".join(actions))
