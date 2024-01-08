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
import time
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
        def minimax_decision(gameState):
            Start = time.time()
            legalActions = gameState.getLegalActions(0)
            legalActions.remove('Stop')
            bestAction = None
            bestValue = -math.inf
            worst = math.inf
            EF = self.evaluationFunction(gameState)
            q = True
            v = [0, 0, 0]
            bv = [0, 0, 0]
            for action in legalActions:
                v[0] = minimax_value(gameState.generateSuccessor(0, action), 1, 2, bestValue, worst)
                v[1] = minimax_value(gameState.generateSuccessor(0, action), 1, 3, bestValue, worst)
                v[2] = minimax_value(gameState.generateSuccessor(0, action), 1, 4, bestValue, worst)
                if(v[1] - EF == 8 and v[2] - EF == 9):
                    bestAction = action
                    q = False
                    break
                if(v[0] - EF == 7 and v[1] - EF == 8 and v[2] - EF == -1):
                    bestAction = action
                    q = False
                    break
                if(v[0] - EF == 17 and v[1] - EF == 18):
                    bestAction = action
                    q = False
                    break
                value = minimax_value(gameState.generateSuccessor(0, action), 1, 0, bestValue, worst)
                if value != EF - 5:
                    q = False
                    
                print('each legal action with its values:', action, value)

                for i in range(5):
                    if i:
                        if i > 1:
                            V = v[i - 2]
                            BV = bv[i - 2]
                        else:
                            V = minimax_value(gameState.generateSuccessor(0, action), 1, i, bestValue, worst)
                            BV = minimax_value(gameState.generateSuccessor(0, bestAction), 1, i, bestValue, worst)
                            print(action, V, bestAction, BV)
                    else:
                        V = value
                        BV = bestValue

                    if V != BV:
                        if V > BV:
                            print('best Value Updated')
                            bestValue = value
                            bv = v
                            bestAction = action
                        break
            if q:
                print('Random action picked')
                bestAction = random.choice(legalActions)
            print('chosenAction:', bestAction)
            print(time.time() - Start)
            return bestAction

        def minimax_value(gameState, agentIndex, depth, bestsofar, worst):
            if gameState.isLose():
                return self.evaluationFunction(gameState) - 2000
            if gameState.isWin():
                return self.evaluationFunction(gameState) + 2000
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