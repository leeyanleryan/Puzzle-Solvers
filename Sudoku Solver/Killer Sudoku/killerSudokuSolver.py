def findNextEmpty(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return (i, j)
    return ()

def getValidNumbers(sudoku, graph, row, col):
    valid = [1 for i in range(10)]
    section = graph[(row, col)]
    highest = section[0]
    count = 0
    for i in range(1, len(section)):
        coord = section[i]
        num = sudoku[coord[0]][coord[1]]
        if num == 0:
            count += 1
        highest -= num
    if count == 1 and highest <= 9:
        valid = [0 for i in range(10)]
        valid[highest] = 1
    elif count == 1 and highest >= 10:
        return [0 for i in range(10)]
    for i in range(9):
        valid[sudoku[row][i]] = 0
        valid[sudoku[i][col]] = 0
        valid[sudoku[row//3*3 + i//3][col//3*3 + i%3]] = 0
        if i > highest:
            valid[i] = 0
    return valid

def printSolution(sudoku):
    for i in range(9):
        print(sudoku[i])

def preprocess(sudoku, sections):
    graph = {}
    for i in range(len(sections)):
        count, index, total = 0, 0, 0
        for j in range(1, len(sections[i])):
            coord = sections[i][j]
            if sudoku[coord[0]][coord[1]] == 0:
                count += 1
                index = j
            total += sudoku[coord[0]][coord[1]]
            graph[(coord[0], coord[1])] = sections[i]
        if count == 1:
            coord = sections[i][index]
            sudoku[coord[0]][coord[1]] = sections[i][0] - total
    return sudoku, graph

def killerSudokuSolver(sudoku, sections):
    sudoku, graph = preprocess(sudoku, sections)
    stack = [(-1, -1, -1, 0)]
    changed = []
    while len(stack) != 0:
        coord = stack.pop()
        row, col, num, depth = coord[0], coord[1], coord[2], coord[3]
        if (row, col, num, depth) != (-1, -1, -1, 0):
            sudoku[row][col] = num
            changed.append((row, col, num, depth))
        next_coord = findNextEmpty(sudoku)
        if not next_coord:
            return sudoku
        next_row, next_col, next_depth = next_coord[0], next_coord[1], depth+1
        valid = getValidNumbers(sudoku, graph, next_row, next_col)
        backtrack = True
        for next_num in range(9, 0, -1):
            if valid[next_num] == 0:
                continue
            stack.append((next_row, next_col, next_num, next_depth))
            backtrack = False
        if len(stack) == 0:
            break
        if backtrack:
            for i in range(len(changed)-1, -1, -1):
                remove_row, remove_col, remove_depth = changed[i][0], changed[i][1], changed[i][3]
                backtrack_depth = stack[-1][3]
                if remove_depth == backtrack_depth:
                    break
                sudoku[remove_row][remove_col] = 0
                changed.pop()
    return sudoku

# puzzle1 = [[0,0,5,  7,4,0,  1,0,0], 
#            [0,0,0,  0,0,0,  0,9,8],
#            [0,1,0,  3,0,0,  7,0,4],

#            [5,0,0,  1,0,3,  0,2,7],
#            [0,9,7,  0,2,0,  0,8,0],
#            [0,0,0,  0,6,0,  9,0,0],

#            [0,0,6,  0,0,0,  0,7,1],
#            [8,5,0,  2,0,6,  0,0,0],
#            [0,7,0,  0,8,0,  0,0,6]]

# sections1 = [[6, (0,0)], 
#              [8, (0,1)],
#              [25, (0,2), (0,3), (1,2), (2,2)],
#              [5, (0,4), (1,4)],
#              [9, (0,5)],
#              [4, (0,6), (0,7)],
#              [19, (0,8), (1,7), (1,8)],
#              [13, (1,0), (1,1), (2,0), (2,1)],
#              [10, (1,3), (2,3), (3,3)],
#              [7, (1,5), (1,6)],
#              [20, (2,4), (2,5), (2,6)],
#              [23, (2,7), (3,5), (3,6), (3,7), (4,7)],
#              [14, (2,8), (3,8), (4,8)],
#              [6, (3,0), (4,0)],
#              [14, (3,1), (3,2)],
#              [21, (3,4), (4,4), (4,5), (5,4)],
#              [13, (4,1), (5,1)],
#              [22, (4,2), (4,3), (5,2), (5,3)],
#              [6, (4,6)],
#              [20, (5,0), (6,0), (7,0)],
#              [16, (5,5), (5,6)],
#              [6, (5,7), (5,8)],
#              [14, (6,1), (7,1), (8,1)],
#              [13, (6,2), (6,3), (6,4)],
#              [19, (6,5), (6,6), (7,5)],
#              [14, (6,7), (7,6), (7,7)],
#              [16, (6,8), (7,8), (8,8)],
#              [3, (7,2), (7,3)],
#              [7, (7,4)],
#              [4, (8,0)],
#              [20, (8,2), (8,3), (8,4)],
#              [8, (8,5), (8,6), (8,7)]]

# answer1 = [[6,8,5,  7,4,9,  1,3,2],
#            [7,3,4,  6,1,2,  5,9,8],
#            [2,1,9,  3,5,8,  7,6,4],
           
#            [5,6,8,  1,9,3,  4,2,7],
#            [1,9,7,  5,2,4,  6,8,3],
#            [3,4,2,  8,6,7,  9,1,5],
           
#            [9,2,6,  4,3,5,  8,7,1],
#            [8,5,1,  2,7,6,  3,4,9],
#            [4,7,3,  9,8,1,  2,5,6]]

# my_ans1 = killerSudokuSolver(puzzle1, sections1)
# printSolution(my_ans1)
# print(f"Solution is same as answer: {my_ans1 == answer1}")

puzzle2 = [[0,0,0,  0,0,0,  0,0,0], 
           [0,0,0,  0,0,0,  0,0,0],
           [0,0,0,  0,0,0,  0,0,0],

           [0,0,0,  0,0,0,  0,0,0],
           [0,0,0,  0,0,0,  0,0,0],
           [0,0,0,  0,0,0,  0,0,0],

           [0,0,0,  0,0,0,  0,0,0],
           [0,0,0,  0,0,0,  0,0,0],
           [0,0,0,  0,0,0,  0,0,0]]

sections2 = [[2, (0,0)],
             [19, (0,1), (1,1), (1,2)],
             [20, (0,2), (0,3), (0,4), (1,4)],
             [8, (0,5), (1,5)],
             [1, (0,6)],
             [25, (0,7), (0,8), (1,6), (1,7), (1,8)],
             [19, (1,0), (2,0), (3,0)],
             [13, (1,3), (2,3)],
             [4, (2,1), (2,2)],
             [5, (2,4), (3,4)],
             [14, (2,5), (2,6), (3,5)],
             [14, (2,7), (2,8)],
             [17, (3,1), (4,1), (4,2)],
             [8, (3,2), (3,3)],
             [21, (3,6), (4,5), (4,6)],
             [8, (3,7)],
             [12, (3,8), (4,7), (4,8)],
             [21, (4,0), (5,0), (5,1), (6,0)],
             [15, (4,3), (5,2), (5,3)],
             [15, (4,4), (5,4)],
             [13, (5,5), (6,5)],
             [23, (5,6), (6,6), (7,6), (8,6)],
             [10, (5,7), (5,8)],
             [11, (6,1), (7,1)],
             [14, (6,2), (7,2), (7,3)],
             [14, (6,3), (6,4), (7,4)],
             [6, (6,7), (6,8)],
             [12, (7,0), (8,0), (8,1)],
             [7, (7,5), (8,5)],
             [9, (7,7), (8,7)],
             [9, (7,8), (8,8)],
             [16, (8,2), (8,3), (8,4)]]

answer2 = [[2, 4, 5, 6, 8, 3, 1, 9, 7],
           [6, 7, 8, 9, 1, 5, 3, 4, 2],
           [9, 3, 1, 4, 2, 7, 5, 6, 8],
           [4, 9, 7, 1, 3, 2, 6, 8, 5],
           [1, 2, 6, 5, 9, 8, 7, 3, 4],
           [5, 8, 3, 7, 6, 4, 2, 1, 9],
           [7, 6, 2, 3, 4, 9, 8, 5, 1],
           [3, 5, 4, 8, 7, 1, 9, 2, 6],
           [8, 1, 9, 2, 5, 6, 4, 7, 3]]

my_ans2 = killerSudokuSolver(puzzle2, sections2)
printSolution(my_ans2)
print(f"Solution is same as answer: {my_ans2 == answer2}")