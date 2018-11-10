import random
from nonogram import Game, Rules, checkSolution
from util     import readRulesFile, createConstraints, fitnessInEdges as fitness

# points = [(x, y), ...] => Filled squares in nonogram
# constraints = (rules, nLines, nColumns, nPoints, nPopulation)

def main(puzzleName = 'i20902', nPopulation = 1000):
    rules       = readRulesFile('puzzles/' + puzzleName + '.txt')
    constraints = createConstraints(rules, nPopulation)
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    mySol = GA(constraints)
    print(Game(nLines,  nColumns, mySol))

def GA(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = randomSolutions(constraints)
    while not converge(P, constraints):
        PP  = crossover(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)
        print(fitness(P[0], constraints))
        print(Game(nLines, nColumns, P[0]))
       # print(len(P[0]))
  #      print(Game(nLines, nColumns, P[1]))
   #     print(Game(nLines, nColumns, P[2]))
    #    print(Game(nLines, nColumns, P[3]))

    return best(P)

def sortedSolution(sol):
    return sorted(sol, key = lambda p : p[0]+p[1])

def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    allPoints = [(i,j) for i in range(nLines) for j in range(nColumns)]
    solutions = []

    for _ in range(nPopulation):
        random.shuffle(allPoints)
        solution  = sortedSolution(allPoints[:nPoints])
        solutions += [solution]

    return solutions

def converge(P, constraints):
    for i in range(len(P)-1):
        if fitness(P[i], constraints) != fitness(P[i+1], constraints):
            return False
    return True

def printFitnessPopulation(P, constraints):
    for s in P:
        print(fitness(s, constraints))

def printPopulation(P):
    for s in P:
        print('='*20)
        print(s)
        print('='*20)

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []
    count = 0

    while count < nPopulation:
        child = []

        while len(set(child)) != nPoints:
            parent1 = P[random.randint(0, nPopulation-1)]
            parent2 = parent1
            while parent2 == parent1:
                parent2 = P[random.randint(0, nPopulation-1)]

            r = random.randint(1, nPoints-2)
            child = parent1[:r] + parent2[r:]
        PP    += [sortedSolution(child)]
        count += 1

    return PP

def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for sol in P:
        mutate = random.randint(1, 100)
        if mutate <= 75:
            PP += [sol]
            continue

        changeLine = random.randint(1, 100) <= 50
        newSol = []
        if(changeLine):
            lineIndex = random.randint(0, nLines-1)
            newSol  = [p for p in sol if p[0] != lineIndex]

            oldLine = [p for p in sol if p[0] == lineIndex]
            newLine = []

            for _ in range(len(oldLine)):
                newPoint = (lineIndex, random.randint(0, nColumns-1))
                while newPoint in newLine:
                    newPoint = (lineIndex, random.randint(0, nColumns-1))
                newLine += [newPoint]

            newSol += newLine
        else:
            columnIndex = random.randint(0, nColumns-1)
            newSol  = [p for p in sol if p[1] != columnIndex]

            oldColumn = [p for p in sol if p[1] == columnIndex]
            newColumn = []

            for _ in range(len(oldColumn)):
                newPoint = (random.randint(0, nLines-1), columnIndex)
                while newPoint in newColumn:
                    newPoint = (random.randint(0, nLines-1), columnIndex)
                newColumn += [newPoint]

            newSol += newColumn

        PP += [newSol]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PPP    = P + PP
    auxPPP = sorted(PPP, key = lambda s : fitness(s, constraints), reverse = True)
    bestN  = auxPPP[0:nPopulation]

    return bestN

def best(P):
    # All population is equal, because of converge function
    return P[0]

if __name__ == '__main__':
    main()
