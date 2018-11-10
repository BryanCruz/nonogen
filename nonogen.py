import random
from nonogram import Game, Rules, checkSolution
from util     import readRulesFile, printSol, createConstraints, fitnessInEdgesAgain as evaluateFitness

# points = [(x, y), ...] => Filled squares in nonogram
# constraints = (rules, nLines, nColumns, nPoints, nPopulation)

class Solution:
    def __init__(self, points, constraints):
        self.points  = sortedPoints(points)
        self.fitness = evaluateFitness(points, constraints)

def main(puzzleName = 'i20902', nPopulation = 1000):
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
        PP  = crossover(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)
        print(P[0])
        print(P[0].fitness)
        printSol(P[0], constraints)
        # printSol(P[1], constraints)
        # printSol(P[2], constraints)
        # printSol(P[500], constraints)
        printSol(P[999], constraints)

    return best(P)

def sortedPoints(points):
    return sorted(points, key = lambda p : (p[0]+p[1]))

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
        if P[i].fitness != P[i+1].fitness:
            return False
    return True

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    P      = sorted(P, key = lambda s: s.fitness, reverse=True)
    weights=[i for i in range(nPopulation, 0, -1)]

    while count < nPopulation:
        childPoints = []
        while len(set(childPoints)) != nPoints:
            parent1 = 0
            parent2 = 0
            while parent1 == parent2:
                parent1, parent2 = random.choices(P, weights=weights, k=2)

            r = random.randint(0, nPoints-1)
            childPoints = parent1.points[:r] + parent2.points[r:]
        PP    += [Solution(childPoints, constraints)]
        count += 1

    return PP

def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        # mutate with a prob of p
        p = 0.25
        mutate = random.random()
        if mutate < p:
            PP += [sol]
            continue

        # Change a point to a new one that isn't in the points
        oldPoint = sol.points[random.randint(0,nPoints-1)]

        newPoint  = oldPoint
        while newPoint in sol.points:
            newPoint = (random.randint(0,nLines-1), random.randint(0,nColumns-1))

        newPoints =  sorted([p for p in sol.points if p != oldPoint] + [newPoint])
        PP += [Solution(newPoints, constraints)]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PPP    = P + PP
    auxPPP = sorted(PPP, key = lambda s : s.fitness, reverse = True)
    bestN  = auxPPP[0:nPopulation]

    return bestN

def best(P):
    # All population is equal, because of converge function
    return P[0]

if __name__ == '__main__':
    main()
