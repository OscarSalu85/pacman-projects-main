# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in obj-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# def addSuccessors(problem, addCost=True):

class SearchNode:
    def __init__(self, parent, node_info):
        """
            parent: parent SearchNode.

            node_info: tuple with three elements => (coord, action, cost)

            coord: (x,y) coordinates of the node position

            action: Direction of movement required to reach node from
            parent node. Possible values are defined by class Directions from
            game.py

            cost: cost of reaching this node from the starting node.
        """

        self.__state = node_info[0]
        self.action = node_info[1]
        self.cost = node_info[2] if parent is None else node_info[2] + parent.cost
        self.parent = parent

    # The coordinates of a node cannot be modified, se we just define a getter.
    # This allows the class to be hashable.
    @property
    def state(self):
        return self.__state

    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        path.reverse()
        return path
    
    # Consider 2 nodes to be equal if their coordinates are equal (regardless of everything else)
    def __eq__(self, __o: object) -> bool:
         if (type(__o) is SearchNode):
             return self.__state == __o.__state
         return False

    def __hash__(self) -> int:
         return hash(self.__state)

def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    
    startSucc = problem.get_successors(problem.get_start_state())
    #get the start node
    startNode = SearchNode(None,(problem.get_start_state(),"",1))
    #inizilize the frontier which is stack in dfs
    frontier = util.Stack()
    #inziliaze the expaneded nodes
    expandedNodes = []
    #we will save the path in order return
    path = []
    #print(problem.get_start_state())

    #add the first node and its sucessors to frontier
    for succ in startSucc:
        node = SearchNode(startNode,succ)
        frontier.push(node)

    #check if frontier is not empty or not
    while not frontier.is_empty():
        #get the current node
        currentNode = frontier.pop()
        #add to expandednode
        expandedNodes.append(currentNode)
        #check if this node is the goal
        if(problem.is_goal_state(currentNode.state)):
            path = currentNode.get_path()
            #print(path)
            #return the path for the solution
            return path
        #get the next sucessors
        nextSucc = problem.get_successors(currentNode.state)
        for succ in nextSucc:
            nextNode = SearchNode(currentNode,succ)
            frontier.push(nextNode)
            for exp in expandedNodes:
                #if already expanded then take out of the frontier
                if(exp.state == nextNode.state):
                    #print(succ)
                    frontier.pop()  
    util.raise_not_defined()



def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    startSucc = problem.get_successors(problem.get_start_state())
    startNode = SearchNode(None,(problem.get_start_state(),"",0))
    #inziliaze the frontier which is queue in bfs
    frontier = util.Queue()
    #inizialize the expanded nodes
    expandedNodes = []
    # inizialize the path
    path = []
    #print(problem.get_start_state())
    expandedNodes.append(startNode)
    #add the first node and its sucessors to frontier
    for succ in startSucc:
        node = SearchNode(startNode,succ)
        frontier.push(node)

     #check if frontier is not empty or not
    while not frontier.is_empty():
        #variable to determine if a node is already expanded or not
        expanded = False
        #get the current node
        currentNode = frontier.pop()
        #check if the node is alredy expanded or not
        for exp in expandedNodes:
                if(exp == currentNode):
                    expanded = True
        #if node already not expanded
        if(not expanded):
            #add to the expandednode
            expandedNodes.append(currentNode)
            #check if this node is the goal node
            if(problem.is_goal_state(currentNode.state)):
                path = currentNode.get_path()
                #print(path)
                # return the path to the solution
                return path
            nextSucc = problem.get_successors(currentNode.state)
            # get the sucessors of current node and add to the frontier
            for succ in nextSucc:
                nextNode = SearchNode(currentNode,succ)
                frontier.push(nextNode)
       
    util.raise_not_defined()

def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    startSucc = problem.get_successors(problem.get_start_state())
    startNode = SearchNode(None,(problem.get_start_state(),"",0))
    #initialize the frontier which is prority queue
    frontier = util.PriorityQueue()
    #initialize the expanded node
    expandedNodes = []
    expandedNodes.append(startNode)
    path = []
    #print(problem.get_start_state())

    #add the first node and its sucessors to frontier
    for succ in startSucc:
        node = SearchNode(startNode,succ)
        frontier.push(node,succ[2])
    
    #while frontier not empty
    while not frontier.is_empty():
        #bool to analyze if node is already expanded or not
        expanded = False
        #get the current node
        currentNode = frontier.pop()
        for exp in expandedNodes:
                  #check if the node is alredy expanded or not
                if(exp == currentNode):
                    expanded = True
        #if node already not expanded
        if(not expanded):
            #add to expanded node
            expandedNodes.append(currentNode)
             #check if this node is the goal node
            if(problem.is_goal_state(currentNode.state)):
                path = currentNode.get_path()
                #print(path)
                return path
            # get the sucessors of current node and add to the frontier
            nextSucc = problem.get_successors(currentNode.state)
            for succ in nextSucc:
                nextNode = SearchNode(currentNode,succ)
                expanded = False
                for exp in expandedNodes:
                    if(exp.state == nextNode.state):
                        #check if already expanded or not
                        expanded = True
                if(not expanded):
                    #push the prority queue taking into account the cost
                    frontier.push(nextNode,nextNode.cost)
    util.raise_not_defined()

def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def a_star_search(problem, heuristic=null_heuristic):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"
        startSucc = problem.get_successors(problem.get_start_state())
        startNode = SearchNode(None,(problem.get_start_state(),"",0))
        #inziliaze the frontier
        frontier = util.PriorityQueue()
        #inizilize the expandednodes
        expandedNodes = []
        expandedNodes.append(startNode)
        path = []
        #print(problem.get_start_state())

        #put the first node and their sucessors in the frontier with the cost and heurisitic
        for succ in startSucc:
            node = SearchNode(startNode,succ)
            frontier.push(node,node.cost+ heuristic(node.state, problem))

        #while frontier not empty
        while not frontier.is_empty():
            #varable used to check if a node has been expanded or not
            expanded = False
            currentNode = frontier.pop()
            for exp in expandedNodes:
                    ##check if the node is alredy expanded or not
                    if(exp == currentNode):
                        expanded = True
            #if not expanded
            if(not expanded):
                #add to the expanded
                expandedNodes.append(currentNode)
                #check if this is node is the goal node
                if(problem.is_goal_state(currentNode.state)):
                    path = currentNode.get_path()
                    #print(path)
                    #return the solution path
                    return path
                #get the node sucessors
                nextSucc = problem.get_successors(currentNode.state)
                #add the sucessors to the frontier with the cost and heuristic
                for succ in nextSucc:
                    nextNode = SearchNode(currentNode,succ)
                    frontier.push(nextNode,nextNode.cost + heuristic(nextNode.state,problem))
        util.raise_not_defined()

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
