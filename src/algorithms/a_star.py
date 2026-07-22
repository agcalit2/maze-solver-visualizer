from time import sleep

# local import
from src.algorithms.base import BaseAlgorithm
from src.datastructures.datastructure import ASNode, ASOpenList
from src.gui.dialog import ConfigurationDialog as report


class AStar(BaseAlgorithm):

    """
    A* algorithm implementation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_shortest_path(self, show: bool) -> list:
        """
        Find shortest path (A*).

        :param show: if True, the algorithm will run with delay
        :type show: bool
        :returns: sulution list (positions) OR None if there's no solution
        :rtype: list
        """
        # create init node
        start_node = ASNode(state=self.start, parent=None, g=0, h=self.euclidean_distance(self.start, self.target))
        # init distances dict: start to every position, all infinity except start
        distances = {
            (x, y): float("inf")
            for x in range(self.grid_len)
            for y in range(self.grid_len)
        }
        distances[self.start] = 0
        # init open list
        open_list = ASOpenList()
        open_list.add(start_node)
        # track frontier set
        frontier = {start_node.state}
        # init explored list
        explored_list = set()

        # start A* searching
        while not open_list.isempty() and self.run:

            # show sleep
            if show:
                sleep(0.03)

            # pop the lowest-cost node from the open list, add to explored list
            current_node = open_list.pop()
            if current_node.state in explored_list:
                continue
            frontier.remove(current_node.state)
            explored_list.add(current_node.state)

            # mark as explored
            self.set_value(current_node.state, 3)

            # found the goal
            if current_node.state == self.target:
                # recolor start and target
                self.set_value(self.target, 5)
                self.set_value(self.start, 5)
                # init solution list
                solution = []
                # skip target node
                current_node = current_node.parent
                # backtrack to get the solution list
                while current_node.parent is not None:
                    # store solution tuple (movie_id, actor_id)
                    solution.append(current_node.state)
                    # mark solution path
                    self.set_value(current_node.state, 4)
                    # show sleep
                    if show:
                        sleep(0.03)
                    # move to the next parent
                    current_node = current_node.parent
                # reverse the solution
                solution.reverse()
                # total traversal cost of the path
                path_cost = sum(self.get_cost(pos) for pos in solution) + self.get_cost(self.target)
                # distance report
                report.show_report(len(solution), path_cost)
                # return the solution
                return solution

            # search for neighors
            for neighbor in self.get_neighbors(current_node.state):
                # if neighbor is already explored, skip it
                if neighbor in explored_list:
                    continue

                # tentative cost to reach neighbor via current_node
                tentative_g = current_node.g + self.get_cost(neighbor)

                # if not already in the frontier, add it to the frontier
                if neighbor not in frontier:
                    node = ASNode(state=neighbor, parent=current_node, g=tentative_g, h=self.euclidean_distance(neighbor, self.target))
                    open_list.add(node)
                    frontier.add(neighbor)
                    continue

                if neighbor in frontier and distances[neighbor] > tentative_g:
                    # update the node's cost + parent, and distances[neighbor]
                    node = ASNode(state=neighbor, parent=current_node, g=tentative_g, h=self.euclidean_distance(neighbor, self.target))
                    open_list.add(node)
                    distances[neighbor] = tentative_g
                    continue

        # no solution
        # distance report
        if open_list.isempty():
            report.show_report(0)
        return None
