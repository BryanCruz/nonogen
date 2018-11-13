import numpy as np
from numpy import random
from nonogram import Game, Rules, checkSolution
from util     import readRulesFile, printSol, createConstraints, fitness as evaluateFitness

class Solution:
    def __init__(self, points, constraints):
        self.points  = points
        self.fitness = evaluateFitness(points, constraints)
# i21021
# i21128
# i20902
# i20941
# i21303
# i1118

def main(puzzleName = 'i1118', nPopulation = 50):
    rules       = readRulesFile('puzzles/' + puzzleName + '.txt')
    constraints = createConstraints(rules, nPopulation)
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    constraints = rules, nLines, nColumns, nLines*nColumns, nPopulation

    mySol = GA(constraints)
    print(checkSolution(Game(nLines, nColumns, mySol.points), rules))
    printSol(mySol, constraints)

iterations = 0
def GA(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = randomSolutions(constraints)
    while not converge(P, constraints):
        PP  = crossover(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)
        global iterations
        iterations += 1

        print(iterations)
        print(P[0].fitness)
        printSol(P[0], constraints)

    return best(P, constraints)

def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    S = []

    print()
    for _ in range(nPopulation):
        s = []
        for _ in range(nPoints):
            if random.random() <= 0.5:
                s += [True]
            else:
                s += [False]
        S += [Solution(s, constraints)]
    return S

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []

    P = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    for _ in range(nPopulation):
        child1Points = []
        child2Points = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        for i in range(nPoints):
            if random.random() <= 0.5:
                child1Points += [parent1.points[i]]
                child2Points += [parent2.points[i]]
            else:
                child1Points += [parent2.points[i]]
                child2Points += [parent1.points[i]]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]

    return PP

def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for s in P:
        prob = 0.4/100

        newPoints = []

        for p in s.points:
            if random.random() > prob:
                newPoints += [p]
            else:
                newPoints += [not p]

        PP += [Solution(newPoints, constraints)]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = sorted(P, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    nParents  = int(2*nPopulation/10)+1
    nChildren = int(5*nPopulation/10)+1
    nRandom = nPopulation - nChildren - nParents

    bestOnes = P[:nParents] + PP[:nChildren]
    others   = P[nParents:] + PP[nChildren:]

    nextP = bestOnes + np.ndarray.tolist(random.choice(others, size=nRandom, replace=False))

    return nextP

def converge(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    for s in P:
        if s.fitness == 0:
            return True

    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False

    return True

def best(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    for s in P:
        if s.fitness == 0:
            return s
    return P[0]

if __name__ == '__main__':
    main()
