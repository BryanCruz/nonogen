class Game:
    def __init__(self, nLines, nColumns, points):
        self.nLines   = nLines
        self.nColumns = nColumns
        self.board = []

        for _ in range(self.nLines):
            aux = []
            for _ in range(self.nColumns):
                aux += [False]
            self.board += [aux]

        self.fill(points, nLines, nColumns)

    def fill(self, points, nLines, nColumns):
        for i, v in enumerate(points):
            self.board[int(i/nColumns)][i%nColumns] = v

    def __str__(self):
        result = '=' * ((self.nColumns)*2+2) + '\n'

        for l in self.board:
            result += '|'
            for s in l:
                result += (chr(9608) if not s else ' ')*2
            result += '|\n'

        result += '=' * ((self.nColumns)*2+2)
        return result

class Rules:
    # example: lines = [[1,2,3], [], [2], [9]]
    def __init__(self, lines, columns):
        self.lines   = lines
        self.columns = columns

    def __str__(self):
        result = 'lines:\n'
        for l in self.lines:
            for n in l:
                result += str(n)
                result += ' '
            result += '\n'

        result += 'columns:\n'
        for c in self.columns:
            for n in c:
                result += str(n)
                result += ' '
            result += '\n'
        return result[:-1]

def checkSolution(game, rules):
    board    = game.board
    nLines   = game.nLines
    nColumns = game.nColumns

    # Check lines
    for lineIndex in range(nLines):
        rulesQtt = len(rules.lines[lineIndex])

        columnIndex = 0
        ruleIndex   = 0

        # Check if all rules are being fulfilled
        while columnIndex < nColumns and ruleIndex < rulesQtt:
            countSegment = 0

            while(columnIndex < nColumns and not board[lineIndex][columnIndex]):
                columnIndex += 1

            while(columnIndex < nColumns and board[lineIndex][columnIndex]):
                countSegment += 1
                columnIndex  += 1

            currRule = rules.lines[lineIndex][ruleIndex]
            if(countSegment != currRule):
                return False

            ruleIndex += 1

        # Check if there isn't any remaining rule
        if ruleIndex < rulesQtt:
            return False

        # Check if there isn't any additional square after last rule
        while(columnIndex < nColumns):
            if(board[lineIndex][columnIndex]):
                return False
            columnIndex += 1

    # Check columns
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex   = 0

        # Check if all rules are being fulfilled
        while lineIndex < nLines and ruleIndex < rulesQtt:
            countSegment = 0

            while(lineIndex < nLines and not board[lineIndex][columnIndex]):
                lineIndex += 1

            while(lineIndex < nLines and board[lineIndex][columnIndex]):
                countSegment += 1
                lineIndex  += 1

            currRule = rules.columns[columnIndex][ruleIndex]
            if(countSegment != currRule):
                return False

            ruleIndex += 1

        # Check if there isn't any remaining rule
        if ruleIndex < rulesQtt:
            return False

        # Check if there isn't any additional square after last rule
        while(lineIndex < nLines):
            if(board[lineIndex][columnIndex]):
                return False
            lineIndex += 1

    return True
