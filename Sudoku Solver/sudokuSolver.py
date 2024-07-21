def findNextEmpty(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return (i, j)
    return ()

def getValidNumbers(sudoku, row, col):
    valid = [1 for i in range(10)]
    for i in range(9):
        valid[sudoku[row][i]] = 0
        valid[sudoku[i][col]] = 0
        valid[sudoku[row//3*3 + i//3][col//3*3 + i%3]] = 0
    return valid

def printSolution(sudoku):
    for i in range(9):
        print(sudoku[i])

def sudokuSolver(sudoku):
    changed = []
    stack = [(-1, -1, -1, 0)]
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
        valid = getValidNumbers(sudoku, next_row, next_col)
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

puzzle1 = [[9,5,0,  0,0,2,  0,6,7], 
           [4,7,2,  0,0,0,  1,0,3],
           [0,3,8,  9,0,0,  0,2,4],

           [0,0,7,  2,0,0,  0,3,5],
           [3,0,0,  5,8,1,  0,7,0],
           [0,0,0,  0,0,3,  9,0,0],

           [0,2,0,  8,0,0,  0,0,0],
           [0,8,9,  0,7,0,  0,1,2],
           [0,0,6,  0,2,0,  3,5,8]]

answer1 = [[9,5,1,  4,3,2,  8,6,7],
           [4,7,2,  6,5,8,  1,9,3],
           [6,3,8,  9,1,7,  5,2,4],

           [8,1,7,  2,9,6,  4,3,5],
           [3,9,4,  5,8,1,  2,7,6],
           [2,6,5,  7,4,3,  9,8,1],

           [1,2,3,  8,6,5,  7,4,9],
           [5,8,9,  3,7,4,  6,1,2],
           [7,4,6,  1,2,9,  3,5,8]]

my_ans1 = sudokuSolver(puzzle1)
printSolution(my_ans1)
print(f"Solution is same as answer: {my_ans1 == answer1}")

# puzzle2 = [[8,0,0,  0,1,0,  0,7,0],
#            [0,0,4,  0,5,0,  0,0,2],
#            [0,0,9,  0,0,4,  0,3,0],

#            [0,5,0,  2,0,0,  0,0,0],
#            [0,0,0,  0,0,0,  6,8,0],
#            [9,0,0,  0,6,3,  0,0,0],

#            [0,0,0,  0,0,0,  3,4,0],
#            [7,0,0,  5,2,0,  0,0,1],
#            [0,8,0,  0,0,0,  0,0,0]]

# answer2 = [[8,6,5,  3,1,2,  4,7,9],
#            [3,7,4,  9,5,8,  1,6,2],
#            [1,2,9,  6,7,4,  5,3,8],

#            [6,5,8,  2,4,7,  9,1,3],
#            [4,3,2,  1,9,5,  6,8,7],
#            [9,1,7,  8,6,3,  2,5,4],

#            [2,9,6,  7,8,1,  3,4,5],
#            [7,4,3,  5,2,6,  8,9,1],
#            [5,8,1,  4,3,9,  7,2,6]]

# my_ans2 = sudokuSolver(puzzle2)
# printSolution(my_ans2)
# print(f"Solution is same as answer: {my_ans2 == answer2}")

# printSolution(sudokuSolver([[0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,8,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0]]))