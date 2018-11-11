import random
from nonogram import Game, Rules, checkSolution
from util     import readRulesFile, printSol, createConstraints, fitnessMatch as evaluateFitness

# points = [(x, y), ...] => Filled squares in nonogram
# constraints = (rules, nLines, nColumns, nPoints, nPopulation)

class Solution:
    def __init__(self, points, constraints):
        self.points  = sortedPoints(points)
        self.fitness = evaluateFitness(points, constraints)

def main(puzzleName = 'i20902', nPopulation = 500):
    rules       = readRulesFile('puzzles/' + puzzleName + '.txt')
    constraints = createConstraints(rules, nPopulation)
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    mySol = GA(constraints)
    print(checkSolution(Game(nLines, nColumns, mySol.points), rules))
    printSol(mySol, constraints)

def GA(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = randomSolutions(constraints)
    while not converge(P, constraints):
        PP  = crossoverTest(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)
        print(P[0].fitness)
        printSol(P[0], constraints)

    return best(P)

def sortedPoints(points):
    return points
    return sorted(points, key = lambda p : (p[0]+p[1], p[0], p[1]))

def sortedSolutions(P):
    return sorted(P, key = lambda s : (s.fitness, random.random()))

def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    allPoints = [(i,j) for i in range(nLines) for j in range(nColumns)]
    solutions = []

    for _ in range(nPopulation):
        random.shuffle(allPoints)
        points     = allPoints[:nPoints]
        solutions += [Solution(points, constraints)]

    return solutions

def converge(P, constraints):
    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False
    return True

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sortedSolutions(P)
    weights=[i for i in range(1, nPopulation+1)]

    while count < nPopulation:
        childPoints = []
        while len(set(childPoints)) != nPoints:
            parent1 = 0
            parent2 = 0
            while parent1 == parent2:
                parent1, parent2 = random.choices(P, weights=weights, k=2)
                # parent1, parent2 = random.choices(P, weights=weights, k=2)

            r = random.randint(0, nPoints-1)
            childPoints = parent1.points[:r] + parent2.points[r:]
        PP    += [Solution(childPoints, constraints)]
        count += 1

    return PP

def crossoverTest(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sortedSolutions(P)
    weights=[i for i in range(1, nPopulation+1)]

    while count < nPopulation:
        childPoints = []

        parent1 = 0
        parent2 = 0
        while parent1 == parent2:
            parent1, parent2 = random.choices(P, weights=weights, k=2)

            r = random.randint(0, nPoints)
            child1Points = parent1.points[r:] + parent2.points[:r]
            child2Points = parent1.points[:r] + parent2.points[r:]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP


def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sortedSolutions(P)
    weights=[i for i in range(1, nPopulation+1)]

    while count < nPopulation:
        childPoints = []

        # while len(set(childPoints)) != nPoints or len(set(childPoints)) != nPoints:
        parent1 = 0
        parent2 = 0
        while parent1 == parent2:
            parent1, parent2 = random.choices(P, weights=weights, k=2)

        r = random.randint(0, nPoints-1)
        child1Points = parent1.points[:r] + parent2.points[r:]
        child2Points = parent1.points[r:] + parent2.points[:r]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]
        count += 1

    return PP

def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.8
        mutate = random.random()
        if mutate < p:
            # PP += [sol]
            PP += [Solution(sol.points, constraints)]
            continue

        # Change a point to a new one that isn't in the points
        oldPoint = sol.points[random.randint(0,nPoints-1)]

        newPoint  = oldPoint
        while newPoint in sol.points:
            newPoint = (random.randint(0,nLines-1), random.randint(0,nColumns-1))

        newPoints =  sorted([p for p in sol.points if p != oldPoint] + [newPoint])
        PP += [Solution(newPoints, constraints)]

    return PP

def mutationLine(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.85
        mutate = random.random()
        if mutate < p:
            PP += [sol]
            continue

        # Change a line or column
        oldPoints = []

        lineIndex = random.randint(0, nLines-1)

        oldPoints = [p for p in sol.points if p[0] != lineIndex]
        oldLine   = [p for p in sol.points if p[0] == lineIndex]

        newPoints = []
        while len(newPoints) != len(oldLine):
            newPoint = (lineIndex, random.randint(0,nColumns-1))
            if newPoint not in newPoints:
                newPoints += [newPoint]

        columnIndex = random.randint(0, nColumns-1)

        oldPoints = [p for p in sol.points if p[1] != columnIndex]
        oldColumn = [p for p in sol.points if p[1] == columnIndex]

        newPoints = []
        while len(newPoints) != len(oldColumn):
            newPoint = (random.randint(0,nLines-1), columnIndex)
            if newPoint not in newPoints:
                newPoints += [newPoint]

        PP += [Solution(oldPoints+newPoints, constraints)]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PPP = P+PP
    offset = 1-min(PPP, key = lambda s : s.fitness).fitness

    bestN  = random.choices(PPP, weights=[(s.fitness+offset) for s in PPP], k=nPopulation)
    return bestN

def best(P):
    # All population is equal, because of converge function
    return P[0]

if __name__ == '__main__':
    main()
