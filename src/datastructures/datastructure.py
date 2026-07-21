import heapq
from collections import deque
from itertools import count


class Node:

    """
    Node implementation for(BFS-DFS).

    :param state: node state (x, y)
    :type state: tuple
    :param parent: Node instance
    :type parent: Node
    """

    def __init__(self, state: tuple, parent):
        self.state = state
        self.parent = parent

class WeightNode(Node):
    """
    Node object containing distance from start
    """

    def __init__(self, state: tuple, parent, g: int):
        super().__init__(state, parent)
        self.g = g


class ASNode(WeightNode):

    """
    A* Node implementation for(A*)

    child :: (Node)
    """

    def __init__(self, state: tuple, parent, g: int = 0, h: int = 0):
        super().__init__(state, parent, g)
        self.h = h
        self.f = self.g + self.h


class Stack:

    """
    Stack implementation.
    """

    def __init__(self):
        self.list = deque([])

    def add(self, node: Node):
        """
        Add new element into list.

        :param node: Node object to add
        :type node: Node
        """
        self.list.append(node)

    def remove(self) -> Node:
        """
        Remove and return element from list.

        :returns: last in element
        :rtype: Node
        """
        return self.list.pop()

    def isempty(self) -> bool:
        """
        Is the list empty?

        :returns: True if the list is empty otherwise False
        :rtype: bool
        """
        return len(self.list) == 0

    def isexist(self, state: int) -> bool:
        """
        Is the state exist on the list?

        :param state: state to check
        :type state: int
        :returns: True if exist otherwise False
        :rtype: bool
        """
        return any(node.state == state for node in self.list)


class Queue(Stack):

    """
    Queue implementation.

    child :: (Stack)
    """

    def remove(self) -> Node:
        """
        Remove and return element from list.

        :returns: last in element
        :rtype: Node
        """
        return self.list.popleft()


class OpenList:

    """
    Open list implementation.

    Backed by a binary min-heap (heapq), keyed on node.g, so the
    lowest-cost node always sits at index 0 and both add/remove run
    in O(log n) instead of the O(n) linear scan a plain list would need.
    """

    def __init__(self):
        self.list = []
        # tie-breaker so heapq never has to compare WeightNode instances
        # (which don't define __lt__) when two nodes share the same g
        self._counter = count()

    def add(self, node: WeightNode):
        """
        Add new element into list.

        :param node: Node object to add
        :type node: Node
        """
        heapq.heappush(self.list, (node.g, next(self._counter), node))

    def front(self) -> WeightNode:
        """
        Return list front element.

        The heap invariant guarantees this is always the lowest-cost node.

        :returns: front node element
        :rtype: WeightNode
        """
        return self.list[0][2]

    def pop(self) -> WeightNode:
        """
        Remove and return the lowest-cost (front) node.

        :returns: lowest-cost node element
        :rtype: WeightNode
        """
        return heapq.heappop(self.list)[2]

    def isempty(self) -> bool:
        """
        Is the list empty?

        :returns: True if the list is empty otherwise False
        :rtype: bool
        """
        return len(self.list) == 0

    def isexist(self, state: int, g: int) -> bool:
        """
        Is the state exist on the list?

        :param state: state to check
        :type state: int
        :param g: g value
        :type g: int
        :returns: True if exist otherwise False
        :rtype: bool
        """
        return any(node.state == state for _, _, node in self.list if g > node.g)
