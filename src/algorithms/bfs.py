from time import sleep

# local import
from src.algorithms.base import BaseAlgorithm
from src.datastructures.datastructure import Queue, Node
from src.gui.dialog import ConfigurationDialog as report


class BFS(BaseAlgorithm):

    """
    Breadth First Search algorithm implementation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_shortest_path(self, show: bool) -> list:
        """
        Find shortest path (BFS).

        :param show: if True, the algorithm will run with delay
        :type show: bool
        :returns: sulution list (positions) OR None if there's no solution
        :rtype: list
        """
        # create init node
        start_node = Node(state=self.start, parent=None)
        # init frontier (QUEUE)
        frontier = Queue()
        frontier.add(start_node)
        # frontier set for faster time complexity
        frontierSet = set({start_node.state})
        # init explored nodes set
        explored = set()

        # start BFS
        while not frontier.isempty() and self.run:

            # dequeue node from frontier and remove from set
            node = frontier.remove()
            frontierSet.remove(node.state)

            # mark as explored
            self.set_value(node.state, 3)
            # show sleep
            if show:
                sleep(0.03)

            # check if the node state equals target
            if node.state == self.target:
                # recolor start and target
                self.set_value(self.target, 5)
                self.set_value(self.start, 5)
                # init solution list
                solution = []
                # skip target node
                node = node.parent
                # backtrack to get the solution list
                while node.parent is not None:
                    # store solution tuple (movie_id, actor_id)
                    solution.append(node.state)
                    # mark solution path
                    self.set_value(node.state, 4)
                    # show sleep
                    if show:
                        sleep(0.03)
                    # move to the next parent
                    node = node.parent
                # reverse the solution
                solution.reverse()
                # total traversal cost of the path
                path_cost = sum(self.get_cost(pos) for pos in solution) + self.get_cost(self.target)
                # distance report
                report.show_report(len(solution), path_cost)
                # return the solution
                return solution

            # mark as explored
            explored.add(node.state)

            # search for neighbors
            for neighbor in self.get_neighbors(node.state):
                if neighbor not in explored and neighbor not in frontierSet:
                    # add the node to the frontier
                    frontier.add(Node(state=neighbor, parent=node))
                    frontierSet.add(neighbor)
                    

        # no solution
        # distance report
        if frontier.isempty():
            report.show_report(0)
        return None
