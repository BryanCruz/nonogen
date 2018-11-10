import nonogram

def printSol(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    print(nonogram.Game(nLines,  nColumns, sol.points))

def readRulesFile(fileName):
    with open(fileName) as rulesFile:
        readingLines = True
        lines   = []
        columns = []

        for fileLine in rulesFile:
            if(fileLine == '-\n'):
                readingLines = False
                continue

            rulesInFileLine = [[int(rule) for rule in fileLine.split()]]
            if(readingLines):
                lines   += rulesInFileLine
            else:
                columns += rulesInFileLine

    return nonogram.Rules(lines=lines, columns=columns)

def createConstraints(rules, nPopulation):
    nLines   = len(rules.lines)
    nColumns = len(rules.columns)
    nPoints  = 0

    # Count total number of points
    for line in rules.lines:
        for rule in line:
            nPoints += rule

    return (rules, nLines, nColumns, nPoints, nPopulation)

def fitnessInEdgesAgain(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    # Count how many rules it is following
    count = 0
    game  = nonogram.Game(nLines, nColumns, sol)
    board = game.board

    # Count in lines in ascending order
    for lineIndex in range(nLines):
        rulesQtt = len(rules.lines[lineIndex])

        columnIndex = 0
        ruleIndex   = 0

        while columnIndex < nColumns and ruleIndex < rulesQtt:
            countSegment = 0

            while columnIndex < nColumns and not board[lineIndex][columnIndex]:
                    columnIndex += 1

            while columnIndex < nColumns and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex += 1

            currRule = rules.lines[lineIndex][ruleIndex]
            if countSegment == currRule:
                ruleIndex += 1
            else:
                count -= countSegment

        while columnIndex < nColumns:
            if board[lineIndex][columnIndex]:
                count   -= 1
            columnIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines and ruleIndex < rulesQtt:
            countSegment = 0

            while lineIndex < nLines and not board[lineIndex][columnIndex]:
                    lineIndex += 1

            while lineIndex < nLines and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    += 1

            currRule = rules.columns[columnIndex][ruleIndex]
            if countSegment == currRule:
                ruleIndex += 1
            else:
                count -= countSegment

        while lineIndex < nLines:
            if board[lineIndex][columnIndex]:
                count   -= 1
            lineIndex += 1

    return count
