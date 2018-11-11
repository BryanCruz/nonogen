import numpy as np
from numpy import random
from nonogram import Game, Rules, checkSolution
from util     import readRulesFile, printSol, createConstraints, fitnessMatchWithoutEdges as evaluateFitness

# points = [(x, y), ...] => Filled squares in nonogram
# constraints = (rules, nLines, nColumns, nPoints, nPopulation)

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

def main(puzzleName = 'i20941', nPopulation = 2500):
    rules       = readRulesFile('puzzles/' + puzzleName + '.txt')
    constraints = createConstraints(rules, nPopulation)
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    mySol = GA(constraints)
    print(checkSolution(Game(nLines, nColumns, mySol.points), rules))
    printSol(mySol, constraints)

iterations = 0
def GA(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = randomSolutions(constraints)
    while not converge(P, constraints):
        PP  = crossoverRandomBoard(P, constraints)
        PPP = mutationInLineN(PP, constraints)
        P   = selectBestChildren(P, PPP, constraints)

        global iterations
        iterations += 1

        print(P[nPopulation-1].fitness)
        printSol(P[nPopulation-1], constraints)

        print(iterations)
        print(P[0].fitness)
        printSol(P[0], constraints)

    return best(P, constraints)

def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    allPoints = [(i,j) for i in range(nLines) for j in range(nColumns)]
    solutions = []

    print()
    for _ in range(nPopulation):
        random.shuffle(allPoints)
        r = random.randint(0,nLines*nColumns+1)
        r = nPoints
        points     = allPoints[:r]
        solutions += [Solution(points, constraints)]

    return solutions

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < nPopulation:
        childPoints = []
        while len(set(childPoints)) != nPoints:
            parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

            r = random.randint(0, nPoints)
            childPoints = parent1.points[:r] + parent2.points[r:]
        PP    += [Solution(childPoints, constraints)]
        count += 1

    return PP

def crossoverRandomBoard(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < nPopulation:
        child1Points = []
        child2Points = []
        # parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)
        parent1, parent2 = random.choice(P, replace=False, size=2)

        if random.random() <= 0.5: # cut vertical
            r = random.randint(0, nColumns+1)

            child1Points = [p for p in parent1.points if p[1] < r]+[p for p in parent2.points if p[1] >= r]
            child2Points = [p for p in parent2.points if p[1] < r]+[p for p in parent1.points if p[1] >= r]
        else: # cut horizontal
            r = random.randint(0, nLines+1)

            child1Points = [p for p in parent1.points if p[0] < r]+[p for p in parent2.points if p[0] >= r]
            child2Points = [p for p in parent2.points if p[0] < r]+[p for p in parent1.points if p[0] >= r]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP

def crossoverHalfBoard(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < nPopulation:
        child1Points = []
        child2Points = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        if random.random() <= 0.5: # cut vertical
            r = nColumns/2

            child1Points = [p for p in parent1.points if p[1] < r]+[p for p in parent2.points if p[1] >= r]
            child2Points = [p for p in parent2.points if p[1] < r]+[p for p in parent1.points if p[1] >= r]
        else: # cut horizontal
            r = nLines/2

            child1Points = [p for p in parent1.points if p[0] < r]+[p for p in parent2.points if p[0] >= r]
            child2Points = [p for p in parent2.points if p[0] < r]+[p for p in parent1.points if p[0] >= r]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP


def crossoverRandomBoard2(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < 2*nPopulation:
        child1Points = []
        child2Points = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        c = random.randint(1, nColumns)
        l = random.randint(1, nLines)

        child1Points = [p for p in parent1.points if p[0] < l and p[1] < c]+[p for p in parent2.points if p[0] >= l or p[1] >= c]
        child2Points = [p for p in parent2.points if p[0] < l and p[1] < c]+[p for p in parent1.points if p[0] >= l or p[1] >= c]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP

def crossoverRandomBoard4(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < 2*nPopulation:
        parent1, parent2, parent3, parent4 = random.choice(P, p=prob, replace=False, size=4)

        c = random.randint(1, nColumns)
        l = random.randint(1, nLines)

        child1Points = [p for p in parent1.points if p[0] < l and p[1] < c]+[p for p in parent2.points if p[0] >= l and p[1] >= c] + [p for p in parent3.points if p[0] >= l and p[1] < c] + [p for p in parent4.points if p[0] < l and p[1] >= c]

        PP    += [Solution(child1Points, constraints)]
        count += 1

    return PP

def crossoverRandom(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    while count < nPopulation:
        childPoints = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        r = random.randint(0, nPoints)
        child1Points = parent1.points[:r] + parent2.points[r:]
        child2Points = parent2.points[:r] + parent1.points[r:]
        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP


def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        if random.random() > p:
            PP += [sol]
            continue

        # Change a point to a new one that isn't in the points
        oldPoint = sol.points[random.randint(0,len(sol.points))]

        newPoint  = oldPoint
        while newPoint in sol.points:
            newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

        newPoints =  [p for p in sol.points if p != oldPoint] + [newPoint]
        PP += [Solution(newPoints, constraints)]

    return PP

def mutationRandom(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        if random.random() > p:
            PP += [sol]
            continue

        # make n changes (max 5%)
        maxN = int(nLines*nColumns/10)
        n = random.randint(1, maxN)

        newPoints = sol.points

        for _ in range(n):

            # Add a point with a prob of pAdd
            pAdd = 0.5
            if random.random() < pAdd and len(newPoints)<=nLines*nColumns:
                newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

                if newPoint not in sol.points:
                    newPoints += [newPoint]
            elif len(newPoints)>0:
                # Remove a point with a prob of 1-pAdd
                newPoints.pop(0)

        PP += [Solution(newPoints, constraints)]

    return PP

def mutationFlipRandom(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.4
        if random.random() > p:
            PP += [sol]
            continue

        newPoints = sol.points

        if  len(newPoints)<nLines*nColumns:
            newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

            while newPoint in newPoints:
                newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

            newPoints += [newPoint]

            newPoints.pop(random.randint(len(newPoints)))

        PP += [Solution(newPoints, constraints)]

    return PP

def mutationFlipRandomN(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        if random.random() > p:
            PP += [sol]
            continue

        newPoints = sol.points

        n = random.randint(0, int(nLines*nColumns/10))+1
        # n = int(nLines*nColumns/4)
        # Add a point with a prob of pAdd
        for _ in range(n):
            pAdd = 0.51
            if random.random() < pAdd and len(newPoints)<=nLines*nColumns:
                newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

                while newPoint in newPoints:
                    newPoint = (random.randint(0,nLines), random.randint(0,nColumns))

                newPoints += [newPoint]
            elif len(newPoints) > 0:
                newPoints.pop(random.randint(len(newPoints)))

        PP += [Solution(newPoints, constraints)]

    return PP

def mutationInLine(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.35
        if random.random() > p or len(sol.points) == 0:
            PP += [sol]
            continue

        newPoints = sol.points

        newPoint = newPoints.pop(random.randint(len(newPoints)))

        moveInLine = random.random()
        if moveInLine <= 0.5:
            newPoint = (newPoint[0], random.randint(0,nColumns))
        else:
            newPoint = (random.randint(0,nLines), newPoint[1])

        newPoints += [newPoint]

        PP += [Solution(newPoints, constraints)]

    return PP

def mutationInLineN(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    boardSize = nLines*nColumns

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        if random.random() > p or len(sol.points) < 0:
            PP += [sol]
            continue

        n = random.randint(1, int(/10))

        newPoints = sol.points
        for _ in range(n):
            newPoint = None
            if random.random() <= 0.66:
                if len(newPoints) < 1:
                    continue

                newPoint = newPoints.pop(random.randint(len(newPoints)))

                if random.random() <= 0.5:
                    continue

                moveInLine = random.random()
                if moveInLine <= 0.5:
                    newPoint = (newPoint[0], random.randint(nColumns))
                    while newPoint in newPoints:
                        newPoint = (newPoint[0], random.randint(nColumns))

                else:
                    newPoint = (random.randint(nLines), newPoint[1])
                    while newPoint in newPoints:
                        newPoint = (random.randint(nLines), newPoint[1])
            else:
                if len(newPoints) == nLines*nColumns:
                    continue
                newPoint = (random.randint(nLines), random.randint(nColumns))
                while newPoint in newPoints:
                    newPoint = (random.randint(nLines), random.randint(nColumns))

            newPoints += [newPoint]

        PP += [Solution(newPoints, constraints)]

    return PP


def mutationFlip(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    allPoints = [(i,j) for i in range(nLines) for j in range(nColumns)]

    for sol in P:
        # mutate with a prob of p
        p = 0.15
        if random.random() > p:
            PP += [sol]
            continue

        # make n changes
        maxN = int(nLines*nColumns/10)
        n = random.randint(1, maxN)

        random.shuffle(allPoints)

        pointsToFlip = allPoints[:n]
        newPoints = [p for p in pointsToFlip if p not in sol.points] + [p for p in sol.points if p not in pointsToFlip]

        PP += [Solution(newPoints, constraints)]

    return PP

def mutationFlip1(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    allPoints = [(i,j) for i in range(nLines) for j in range(nColumns)]

    for sol in P:
        # mutate with a prob of p
        p = 0.15
        if random.random() > p:
            PP += [sol]
            continue

        # make n changes
        point1ToFlip = (random.randint(0,nLines), random.randint(0,nColumns))
        point2ToFlip = point1ToFlip
        while point2ToFlip == point1ToFlip:
            point2ToFlip = (random.randint(0,nLines), random.randint(0,nColumns))

        pointsToFlip = [point1ToFlip, point2ToFlip]
        newPoints = [p for p in sol.points if p not in pointsToFlip] + [p for p in pointsToFlip if p not in sol.points]

        PP += [Solution(newPoints, constraints)]

    return PP


def mutationProportional(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        if random.random() > p:
            PP += [sol]
            continue

        # make n changes (max 5%)
        maxN = int(nLines*nColumns/10)
        n = random.randint(1, maxN)

        newPoints = sol.points

        for _ in range(n):

            # Add a point with a prob of pAdd
            if len(newPoints) <= nLines*nColumns:
                pAdd = min(0.75, len(newPoints)/nPoints)

                if random.random() < pAdd:
                    newPoint = (random.randint(0,nLines), random.randint(0,nColumns))
                    if newPoint not in sol.points:
                        newPoints += [newPoint]

            if(len(newPoints) > 0):
                pRem = min(0.75, nPoints/len(newPoints))

                if random.random() < pRem:
                    # Remove a point with a prob of 1-pAdd
                    newPoints.pop(0)

        PP += [Solution(newPoints, constraints)]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PPP = sorted(P+PP, key = lambda s : (s.fitness, random.random()))

    size = len(PPP)
    n = (size*(size+1))/2
    prob=[i/n for i in range(1, size+1)]

    bestN = random.choice(PPP, p=prob, replace=False, size=nPopulation)
    bestN = np.ndarray.tolist(bestN)
    return bestN

def selectBestChildren(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    nChildren = int(2*nPopulation/3)+1
    nRandom = nPopulation - nChildren

    bestOnes = PP[:nChildren]
    others   = PP[nChildren:]
    sizeOthers = len(others)
    nOthers = (sizeOthers*(sizeOthers+1))/2

    bestN = bestOnes + np.ndarray.tolist(random.choice(others, p=[i/nOthers for i in range(sizeOthers, 0, -1)], size=nRandom, replace=False))

    return bestN


def selectYinYang(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = sorted(PP, key = lambda s : (s.fitness, random.random()))

    nChildren = int(3*nPopulation/4)+1
    nRandom = nPopulation - nChildren

    bestOnes  = PP[-nChildren:]
    worstOnes = PP[:nRandom]

    bestN = bestOnes + worstOnes

    return bestN


def selectBestOfAll(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    nParents  = int(nPopulation/3)+1
    nChildren = int(nPopulation/2)+1
    nChildren = nPopulation-nParents
    nRandom   = nPopulation - nParents - nChildren
    nRandom   = 0

    P = sorted(P, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    bestN = P[:nParents] + PP[:nChildren] + np.ndarray.tolist(random.choice(P[nParents:]+PP[nChildren:], size=nRandom, replace=False))
    return bestN


def selectRandom(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    nParents  = int(nPopulation/3)
    nChildren = nPopulation - nParents

    PPP = [{"elements": P, "tbChosen": nParents}, {"elements": PP, "tbChosen": nChildren}]

    for population in PPP:
        population["elements"] = sorted(population["elements"], key = lambda s : (s.fitness, random.random()))
        size                   = len(population["elements"])
        n                      = (size*(size+1))/2
        population["prob"]     = [i/n for i in range(1, size+1)]

    bestN = []
    for population in PPP:
        bestN += np.ndarray.tolist(random.choice(population["elements"], p=population["prob"], replace=False, size=population["tbChosen"]))

    return bestN

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
        if checkSolution(Game(nLines, nColumns, s.points), rules):
            return s
    return P[0]

if __name__ == '__main__':
    main()
