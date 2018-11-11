import nonogram
import util
import nonogen

def createPuzzle():
    lines   = [[2], 
               [9],
               [2,4,2],
               [1,3,1],
               [1,4,2],
               [10],
               [10],
               [1,1,1,1],
               [1,1],
               [10]]

    columns = [[5,1],
               [2,3,1],
               [1,2,2],
               [8,1],
               [7,1],
               [6,1],
               [2,3,1],
               [1,3,1],
               [2,3,2],
               [7,1]]

    rules  = nonogram.Rules(lines, columns)

    filledSquares = [(0,3),(0,4)] 
    filledSquares +=  [(1,i) for i in range(1,10)]
    filledSquares +=  [(2,i) for i in range(0,10) if i != 2 and i != 7]
    filledSquares +=  [(3,0)]+[(3,i) for i in range(3,6)]+[(3,9)]
    filledSquares +=  [(4,0)]+[(4,i) for i in range(3,7)]+[(4,8),(4,9)]
    filledSquares +=  [(j,i) for i in range(0,10) for j in range(5,7)]
    filledSquares +=  [(7,1),(7,3),(7,7),(7,9)]
    filledSquares +=  [(8,2),(8,8)]
    filledSquares +=  [(9,i) for i in range(0,10)]

    puzzle = nonogram.Game(nColumns=10, nLines=10, points=filledSquares)

    return puzzle, rules

def testSolution():
    puzzle, rules = createPuzzle()
    print(rules)
    print(puzzle)

    if nonogram.checkSolution(puzzle, rules):
        print("eh resposta")
    else:
        print("nao eh resposta")

def testRules():
    lines   = [[1,2,3], [], [2], [9]]
    columns = [[], [3,4,1], [2,2,2], [5]]
    rules  = nonogram.Rules(lines, columns)
    print(rules)

def testNonogram():
    filled = [(0, 0), (2,1), (3,5), (7, 7), (1,2), (5,3), (2,2)]
    ng     = nonogram.Game(nLines=8, nColumns=8, points=filled)
    print(ng)

def testSet():
    v1 = ['a','b','c','a']
    v2 = ['b','a','c']
    s1 = set(v1)
    s2 = set(v2)

    print(v1 == v2)
    print(s1 == s2)

def myGame(points=False):
    gamePoints  = [(0,i) for i in range(2,5)]
    gamePoints += [(1,i) for i in range(1,6)]
    gamePoints += [(2,0),(2,6)]
    gamePoints += [(3,i) for i in range(0,13) if i != 7]
    gamePoints += [(4,i) for i in range(0,7)]+[(4,8),(4,10),(4,12)]
    gamePoints += [(j,i) for j in range(5,8) for i in range(0,13) if i != 1 and i != 7]
    gamePoints += [(j,i) for j in range(8,12) for i in range(0,11) if (i != 1 and i != 7 and (j,i) != (10,9)) or ((j,i) == (11,1))]
    gamePoints += [(12,0),(12,6)]
    gamePoints += [(13,i) for i in range(1,6)]

    if points:
        return gamePoints

    game = nonogram.Game(nLines=14,nColumns=13,points=gamePoints)

    return game


def myGameFake(points=False):
    gamePoints  = [(1,i) for i in range(2,5)]
    gamePoints += [(3,i) for i in range(1,6)]
    gamePoints += [(4,0),(2,6)]
    gamePoints += [(2,i) for i in range(0,13) if i != 7]
    gamePoints += [(0,i) for i in range(0,7)]+[(4,8),(4,10),(4,12)]
    gamePoints += [(j,i) for j in range(5,8) for i in range(0,13) if i != 1 and i != 7]
    gamePoints += [(j,i) for j in range(8,12) for i in range(0,11) if (i != 1 and i != 7 and (j,i) != (10,9)) or ((j,i) == (11,1))]
    gamePoints += [(11,0),(12,6)]
    gamePoints += [(0,i) for i in range(1,6)]

    if points:
        return gamePoints

    game = nonogram.Game(nLines=14,nColumns=13,points=gamePoints)

    return game

def testReadFile():
    rules = util.readRulesFile('puzzles/i20902.txt')
    print(rules)

    game = myGame()
    print(game)
    print('ta certo' if nonogram.checkSolution(game=game, rules=rules) else 'ta errado')

def testFitness():
    rules = util.readRulesFile('puzzles/i20902.txt')
    constraints = util.createConstraints(rules, 10)

    print(nonogen.fitness(myGame(True), constraints))

def wrongFitness():
    rules = util.readRulesFile('puzzles/i20902.txt')
    constraints = util.createConstraints(rules, 10)
    print(nonogen.fitness(myGameFake(True), constraints))

def main():
    testRules()
    testNonogram()
    testSet()
    testSolution()
    testReadFile()
    testFitness()
    wrongFitness()

if __name__ == '__main__':
    main()

