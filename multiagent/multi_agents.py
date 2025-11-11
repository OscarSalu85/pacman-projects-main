# multi_agents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattan_distance
from game import Directions, Actions
from pacman import GhostRules
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghostState.scared_timer for ghostState in new_ghost_states]
        
        "*** YOUR CODE HERE ***"
        food_list = new_food.as_list()
        score = 0
        """
        for food in food_list:
            score -= manhattan_distance(food, new_pos)
            print(food)
        """
        return score

def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.get_score()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, eval_fn='score_evaluation_function', depth='2'):
        super().__init__()
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth) 

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action from the current game_state using self.depth
        and self.evaluation_function.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
        Returns a list of legal actions for an agent
        agent_index=0 means Pacman, ghosts are >= 1

        game_state.generate_successor(agent_index, action):
        Returns the successor game state after an agent takes an action

        game_state.get_num_agents():
        Returns the total number of agents in the game

        game_state.is_win():
        Returns whether or not the game state is a winning state

        game_state.is_lose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        """ Initialize variables 
        Pacment agent max player 
        Ghost min player
        """

        #minmax function with recursion
        def minmax(depth,state,agent_index):
            if state.is_win() or state.is_lose() or self.depth == depth: #Base case
                return self.evaluation_function(state)
            
            legal_action = state.get_legal_actions(agent_index)
            if not legal_action : # if there are no legal actions then return what we have now
                return self.evaluation_function(state)
            
            num_agents = state.get_num_agents() #num of agents
            next_agent_index = (agent_index+1) % num_agents
            next_depth = depth  # by defalut we assume that a ply has not been completed
            if(next_agent_index ==0 ): # check if we are have finsihed the ply
                next_depth = depth +1

            if agent_index == 0: #max player --> PACMAN
                max_score = float('-inf')
                for i in legal_action:
                    next_state = state.generate_successor(agent_index, i)
                    max_score = max(minmax(next_depth,next_state,next_agent_index), max_score)
                return max_score
            
            else: #min player --> GHOSTS
                min_score = float('inf')
                for i in legal_action:
                    next_state = state.generate_successor(agent_index, i)
                    min_score = min(minmax(next_depth,next_state,next_agent_index), min_score)
                return min_score


        best_action = None
        best_score = float('-inf')
        agent_index = self.index

        for action in game_state.get_legal_actions(agent_index):
            #we start by checking to the next states
            next_game_state = game_state.generate_successor(agent_index, action)
            #assuming that we start with agent_index equal to 0 so we start by the next agent which is ghost and 
            #the minmax will try with other ghosts and states
            score = minmax(0,next_game_state,1)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action 
        #util.raise_not_defined()
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluation_function
        """
        "*** YOUR CODE HERE ***"
        def max_value(state, alpha, beta, agent_index, depth):
            if state.is_win() or state.is_lose() or self.depth == depth: #Base case
                return self.evaluation_function(state)
            
            legal_action = state.get_legal_actions(agent_index)
            if not legal_action : # if there are no legal actions then return what we have now
                return self.evaluation_function(state)

            value = float('-inf')
            num_agents = state.get_num_agents() #num of agents
            next_agent_index = (agent_index+1) % num_agents
            next_depth = depth  # by defalut we assume that a ply has not been completed
            if(next_agent_index ==0 ): # check if we are have finsihed the ply
                next_depth = depth +1

            for action in legal_action: 
                next_state = state.generate_successor(agent_index,action)
                if next_agent_index == 0: #completed a ply hence max node
                    value = max(value, max_value(next_state, alpha, beta, next_agent_index, next_depth))
                else: #middle of ply hence min node 
                    value = max(value, min_value(next_state, alpha, beta, next_agent_index, next_depth))
                if value>beta:
                    return value
                alpha = max(alpha, value)
            return value
        
        def min_value(state,alpha,beta, agent_index, depth):
            if state.is_win() or state.is_lose() or self.depth == depth: #Base case
                return self.evaluation_function(state)
            
            legal_action = state.get_legal_actions(agent_index)
            if not legal_action : # if there are no legal actions then return what we have now
                return self.evaluation_function(state)
            
            value= float('inf')

            num_agents = state.get_num_agents() #num of agents
            next_agent_index = (agent_index+1) % num_agents
            next_depth = depth  # by defalut we assume that a ply has not been completed
            if(next_agent_index ==0 ): # check if we are have finsihed the ply
                next_depth = depth +1

            for action in legal_action:
                successor_state = state.generate_successor(agent_index,action)
                if next_agent_index !=0: #min node
                    value = min(value, min_value(successor_state, alpha, beta, next_agent_index, next_depth))
                else: #max node
                    value = min(value,max_value(successor_state, alpha, beta, next_agent_index, next_depth))

                if value<alpha:
                    return value
                beta = min(beta, value)
            return value
        
        best_action = None
        best_score = float('-inf')
        agent_index = self.index
        alpha = float('-inf')
        beta = float('inf')
        value = float('-inf')

        for action in game_state.get_legal_actions(agent_index):
            #we start by checking to the next states
            next_game_state = game_state.generate_successor(agent_index, action)
            #we start by the next ghost which 1 and we are still at depth 0
            value = min_value(next_game_state, alpha, beta, 1, 0)
            #update best score and action
            if value > best_score:
                best_score = value
                best_action = action
            #update alpha at the root
            alpha = max(alpha, best_score)
        return best_action
        #util.raise_not_defined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluation_function

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raise_not_defined()

def better_evaluation_function(current_game_state):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()
    


# Abbreviation
better = better_evaluation_function
