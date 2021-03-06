from model.Neighbourhoods.NeighbourhoodBase import NeighbourhoodBase


class HexagonalRight(NeighbourhoodBase):

    def _set_neighbours(self):
        self._append_neighbour(-1, 0)
        self._append_neighbour(-1, 1)
        self._append_neighbour(0, -1)
        self._append_neighbour(0, 0)
        self._append_neighbour(0, 1)
        self._append_neighbour(1, -1)
        self._append_neighbour(1, 0)
