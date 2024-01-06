# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent
from pacman import GameState


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn="scoreEvaluationFunction", depth="2", time_limit="6"):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.time_limit = int(time_limit)
class AIAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        def minimax_decision(gameState):
            legalActions = gameState.getLegalActions(0)
            bestAction = None
            bestValue = -math.inf
            for action in legalActions:
                value = minimax_value(gameState.generateSuccessor(0, action), 1, 0)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
            return bestAction

        def minimax_value(gameState, agentIndex, depth):
            if gameState.isWin() or gameState.isLose() or depth == 4:
                return self.evaluationFunction

            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth)
            else:
                return min_value(gameState, agentIndex, depth)

        def max_value(gameState, agentIndex, depth):
            v = -math.inf
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                v = max(v, minimax_value(gameState.generateSuccessor(agentIndex, action), (agentIndex + 1) % gameState.getNumAgents(), depth + 1))
            return v

        def min_value(gameState, agentIndex, depth):
            v = math.inf
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                v = min(v, minimax_value(gameState.generateSuccessor(agentIndex, action), (agentIndex + 1) % gameState.getNumAgents(), depth))
            return v
        return minimax_decision(gameState)