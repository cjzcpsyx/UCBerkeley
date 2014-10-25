# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        alpha = float("-infinity")
        beta = float("infinity")
        agentNum = gameState.getNumAgents() #Number of Agents
        depth = 1 * agentNum
        agent = 0
        legalMoves = gameState.getLegalActions(agent)
        # Choose one of the best actions
        scores = []
        for action in legalMoves:
          v = self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta)
          alpha = max(alpha, v)
          scores.append(v)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluate(self, gameState, action, depth, agent, alpha, beta):
      agentNum = gameState.getNumAgents() #Number of Agents
      legalMoves = gameState.getLegalActions(agent)
      if depth == 0 or len(legalMoves) == 0:
        return self.getFeatures(gameState) * self.getWeights(gameState)
      elif agent == 0:
        v = float("-infinity")
        for action in legalMoves:
          v = max(v, self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta))
          if v > beta:
            return v
          alpha = max(alpha, v)
        return v
      else:
        v = float("infinity")
        for action in legalMoves:
          v = min(v, self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta))
          if v < alpha:
            return v
          beta = min(beta, v)
        return v

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        if currentGameState.isLose():
          return float('-infinity')
        if currentGameState.isWin():
          return float('infinity')
        features = self.getFeatures(currentGameState)
        weights = self.getWeights(currentGameState)
        return features * weights

    def getFeatures(self, currentGameState):
      features = util.Counter()
      position = currentGameState.getPacmanPosition()
      foods = currentGameState.getFood().asList()
      PowerPellets = currentGameState.getCapsules()
      newGhostStates = currentGameState.getGhostStates()

      score = currentGameState.getScore()
      features['currentScore'] = score

      if len(foods) > 0:
        minDistance = min([manhattanDistance(position, food) for food in foods])
        features['distanceToFood'] = minDistance
        
      ghosts, scaredGhost = [], []
      for ghostState in newGhostStates:
        if ghostState.scaredTimer == 0:
          ghosts.append(ghostState)
        else:
          scaredGhost.append(ghostState)

      if len(ghosts) > 0:
        distanceToGhost = min([manhattanDistance(position, ghostState.getPosition()) for ghostState in ghosts])
      else:
        distanceToGhost = float('infinity')
      distanceToGhost = max(distanceToGhost, 5)
      features['improvedDistanceToGhost'] = 1.0/distanceToGhost

      distanceToScaredGhosts = 0
      if len(scaredGhost) > 0:
        distanceToScaredGhosts = min([manhattanDistance(position, ghostState.getPosition()) for ghostState in scaredGhost])
      else:
        distaceToScaredGhost = 0
      features['distanceToScaredGhost'] = distanceToScaredGhosts

      features['powerPelletsLeft'] = len(PowerPellets)
      
      features['foodLeft'] = len(foods)

      return features

    def getWeights(self, currentGameState):
      return {'currentScore':0.8, 'distanceToFood':-0.5, 'improvedDistanceToGhost':-1, 'distanceToScaredGhosts':2, 'powerPelletsLeft':-20, 'foodLeft':-4}


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents() #Number of Agents
        depth = self.depth * agentNum
        agent = self.index
        legalMoves = gameState.getLegalActions(agent)
        # Choose one of the best actions
        scores = [self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluate(self, gameState, action, depth, agent):
      agentNum = gameState.getNumAgents() #Number of Agents
      legalMoves = gameState.getLegalActions(agent)
      if depth == 0 or len(legalMoves) == 0:
        return self.evaluationFunction(gameState)
      elif agent == 0:
        return max([self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum) for action in legalMoves])
      else:
        return min([self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum) for action in legalMoves])



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-infinity")
        beta = float("infinity")
        agentNum = gameState.getNumAgents() #Number of Agents
        depth = self.depth * agentNum
        agent = self.index
        legalMoves = gameState.getLegalActions(agent)
        # Choose one of the best actions
        scores = []
        for action in legalMoves:
          v = self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta)
          alpha = max(alpha, v)
          scores.append(v)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluate(self, gameState, action, depth, agent, alpha, beta):
      agentNum = gameState.getNumAgents() #Number of Agents
      legalMoves = gameState.getLegalActions(agent)
      if depth == 0 or len(legalMoves) == 0:
        return self.evaluationFunction(gameState)
      elif agent == 0:
        v = float("-infinity")
        for action in legalMoves:
          v = max(v, self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta))
          if v > beta:
            return v
          alpha = max(alpha, v)
        return v
      else:
        v = float("infinity")
        for action in legalMoves:
          v = min(v, self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum, alpha, beta))
          if v < alpha:
            return v
          beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents() #Number of Agents
        depth = self.depth * agentNum
        agent = self.index
        legalMoves = gameState.getLegalActions(agent)
        # Choose one of the best actions
        scores = [self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluate(self, gameState, action, depth, agent):
      agentNum = gameState.getNumAgents() #Number of Agents
      legalMoves = gameState.getLegalActions(agent)
      if depth == 0 or len(legalMoves) == 0:
        return self.evaluationFunction(gameState)
      elif agent == 0:
        return max([self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum) for action in legalMoves])
      else:
        expects = []
        for action in legalMoves:
          expects.append(self.evaluate(gameState.generateSuccessor(agent, action), action, depth - 1, (agent + 1) % agentNum))
        return sum(expects) / float(len(expects))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isLose():
      return float('-infinity')
    if currentGameState.isWin():
      return float('infinity')
    features = getFeatures(currentGameState)
    weights = getWeights(currentGameState)
    return features * weights

def getFeatures(currentGameState):
  features = util.Counter()
  position = currentGameState.getPacmanPosition()
  foods = currentGameState.getFood().asList()
  PowerPellets = currentGameState.getCapsules()
  newGhostStates = currentGameState.getGhostStates()

  score = currentGameState.getScore()
  features['currentScore'] = score

  minDistance = min([manhattanDistance(position, food) for food in foods])
  features['distanceToFood'] = minDistance
    
  ghosts, scaredGhost = [], []
  for ghostState in newGhostStates:
    if ghostState.scaredTimer == 0:
      ghosts.append(ghostState)
    else:
      scaredGhost.append(ghostState)

  if len(ghosts) > 0:
    distanceToGhost = min([manhattanDistance(position, ghostState.getPosition()) for ghostState in ghosts])
  else:
    distanceToGhost = float('infinity')
  distanceToGhost = max(distanceToGhost, 5)
  features['improvedDistanceToGhost'] = 1.0/distanceToGhost

  distanceToScaredGhosts = 0
  if len(scaredGhost) > 0:
    distanceToScaredGhosts = min([manhattanDistance(position, ghostState.getPosition()) for ghostState in scaredGhost])
  else:
    distaceToScaredGhost = 0
  features['distanceToScaredGhost'] = distanceToScaredGhosts

  features['powerPelletsLeft'] = len(PowerPellets)
  
  features['foodLeft'] = len(foods)

  return features

def getWeights(currentGameState):
  return {'currentScore':0.8, 'distanceToFood':-0.5, 'improvedDistanceToGhost':-1, 'distanceToScaredGhosts':2, 'powerPelletsLeft':-20, 'foodLeft':-4}

# Abbreviation
better = betterEvaluationFunction

