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

            while ruleIndex < rulesQtt and countSegment != rules.lines[lineIndex][ruleIndex]:
                ruleIndex += 1
                count     -= 1

            if ruleIndex < rulesQtt and countSegment == rules.lines[lineIndex][ruleIndex]:
                ruleIndex += 1
                count     += 1

        while ruleIndex < rulesQtt:
            count     -= 1
            ruleIndex += 1

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

            while ruleIndex < rulesQtt and rules.columns[columnIndex][ruleIndex] != countSegment:
                ruleIndex += 1
                count     -= 1

            if ruleIndex < rulesQtt and rules.columns[columnIndex][ruleIndex] == countSegment:
                ruleIndex += 1
                count     += 1

        while ruleIndex < rulesQtt:
            count     -= 1
            ruleIndex += 1

    return count

def fitnessInEdgesAgainWithWeigth(sol, constraints):
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

            while ruleIndex < rulesQtt and countSegment != rules.lines[lineIndex][ruleIndex]:
                count     -= rules.lines[lineIndex][ruleIndex]
                ruleIndex += 1

            if ruleIndex < rulesQtt and countSegment == rules.lines[lineIndex][ruleIndex]:
                count     += rules.lines[lineIndex][ruleIndex]
                ruleIndex += 1

        while ruleIndex < rulesQtt:
            count     -= rules.lines[lineIndex][ruleIndex]
            ruleIndex += 1

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

            while ruleIndex < rulesQtt and rules.columns[columnIndex][ruleIndex] != countSegment:
                count     -= rules.columns[columnIndex][ruleIndex]
                ruleIndex += 1

            if ruleIndex < rulesQtt and rules.columns[columnIndex][ruleIndex] == countSegment:
                count     += rules.columns[columnIndex][ruleIndex]
                ruleIndex += 1

        while ruleIndex < rulesQtt:
            count     -= rules.columns[columnIndex][ruleIndex]
            ruleIndex += 1

    return count

def fitnessMatchEnhanced(sol, constraints):
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

        while columnIndex < nColumns or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while columnIndex < nColumns and not board[lineIndex][columnIndex]:
                columnIndex += 1

            while columnIndex < nColumns and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex += 1

            count -= min(1,currRule)*abs(countSegment - currRule)
            ruleIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex][columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= min(1,currRule)*abs(countSegment - currRule)
            ruleIndex += 1

    return count

def fitnessMatch(sol, constraints):
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

        while columnIndex < nColumns or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while columnIndex < nColumns and not board[lineIndex][columnIndex]:
                columnIndex += 1

            while columnIndex < nColumns and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex += 1

            count -= abs(countSegment - currRule)
            ruleIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex][columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    return count


def fitnessMatchWithEdges(sol, constraints):
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

        while columnIndex < nColumns or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while columnIndex < nColumns and not board[lineIndex][columnIndex]:
                columnIndex += 1

            while columnIndex < nColumns and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex += 1

            count -= abs(countSegment - currRule)
            ruleIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex][columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    # Count in lines in descending order
    for lineIndex in range(nLines-1, -1, -1):
        rulesQtt = len(rules.lines[lineIndex])

        columnIndex = nColumns-1
        ruleIndex   = rulesQtt-1

        while columnIndex >= 0 or ruleIndex >= 0:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex >= 0 else 0

            while columnIndex >= 0 and not board[lineIndex][columnIndex]:
                columnIndex -= 1

            while columnIndex >= 0 and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex  -= 1

            count -= abs(countSegment - currRule)
            ruleIndex -= 1

    # Count in columns in descending order
    for columnIndex in range(nColumns-1, -1, -1):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = nLines-1
        ruleIndex = rulesQtt-1

        while lineIndex >= 0 or ruleIndex >= 0:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex >= 0 else 0

            while lineIndex >= 0 and not board[lineIndex][columnIndex]:
                lineIndex -= 1

            while lineIndex >= 0 and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    -= 1

            count     -= abs(countSegment - currRule)
            ruleIndex -= 1

    return count
def fitnessMatchWithoutEdges(sol, constraints):
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

        while columnIndex < nColumns or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while columnIndex < nColumns and not board[lineIndex][columnIndex]:
                columnIndex += 1

            while columnIndex < nColumns and board[lineIndex][columnIndex]:
                countSegment += 1
                columnIndex += 1

            count -= abs(countSegment - currRule)
            ruleIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex][columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex][columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    return count
