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
import random
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
        def greed(action, bestAction, EF):
            BV3 = minimax_value(gameState.generateSuccessor(0, bestAction), 1, 3, -20000, 20000)
            V3 = minimax_value(gameState.generateSuccessor(0, action), 1, 3, -20000, 20000)
            V4 = minimax_value(gameState.generateSuccessor(0, action), 1, 4, -20000, 20000) - 5
            BV4 = minimax_value(gameState.generateSuccessor(0, action), 1, 4, -20000, 20000) - 5
            EF -= 2
            print(V3, BV3, EF, V4, BV4)
            if BV3 + EF == 2 * V3 and V4 > EF:
                print('111111111111111111111111111111')
                return 1
            if V3 + EF == 2 * BV3 and BV4 > EF:
                print('222222222222222222222222222222')
                return 2
            return 0

        def minimax_decision(gameState):
            legalActions = gameState.getLegalActions(0)
            legalActions.remove('Stop')
            bestAction = None
            bestValue = -math.inf
            worst = math.inf
            EF = self.evaluationFunction(gameState)
            q = True
            for action in legalActions:
                value = minimax_value(gameState.generateSuccessor(0, action), 1, 0, bestValue, worst)
                if value > EF:
                    q = False
                print(action, value)
                for i in range(5):
                    if i:
                        V = minimax_value(gameState.generateSuccessor(0, action), 1, i, bestValue, worst)
                        BV = minimax_value(gameState.generateSuccessor(0, bestAction), 1, i, bestValue, worst)
                        print(action, V, bestAction, BV)
                    else:
                        V = value
                        BV = bestValue
                    if V != BV:
                        if V > BV:
                            print('Changed')
                            bestValue = value
                            bestAction = action
                        break
                # if bestAction != None:
                #     g = greed(action, bestAction, EF)
                #     if g > 0:
                #         if g == 1:
                #             bestValue = value
                #             bestAction = action
                #         break
            if q:
                print('random')
                bestAction = random.choice(legalActions)
            print(bestAction)
            return bestAction

        def minimax_value(gameState, agentIndex, depth, bestsofar, worst):
            if gameState.isLose():
                return -20000
            if gameState.isWin():
                return 20000
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth, worst)
            return min_value(gameState, agentIndex, depth, bestsofar)

        def max_value(gameState, agentIndex, depth, worst):
            v = -math.inf
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                v = max(v, minimax_value(gameState.generateSuccessor(agentIndex, action), (agentIndex + 1) % gameState.getNumAgents(), depth + 1, v, worst))
                if v >= worst:
                    return v
            return v

        def min_value(gameState, agentIndex, depth, bestsofar):
            v = math.inf
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
                v = min(v, minimax_value(gameState.generateSuccessor(agentIndex, action), (agentIndex + 1) % gameState.getNumAgents(), depth, bestsofar, v))
                if v <= bestsofar:
                    return v
            return v
        return minimax_decision(gameState)