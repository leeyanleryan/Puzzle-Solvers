class sudokuSolver:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def findNextEmpty(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    return (i, j)
        return ()

    def getValidNumbers(self, row, col):
        valid = [1 for i in range(10)]
        for i in range(9):
            valid[self.sudoku[row][i]] = 0
            valid[self.sudoku[i][col]] = 0
            valid[self.sudoku[row//3*3 + i//3][col//3*3 + i%3]] = 0
        return valid

    def printSolution(self):
        for i in range(9):
            row = ""
            for j in range(9):
                row += str(self.sudoku[i][j])
                if (j+1)%3 == 0:
                    row += "  "
            print(row)
            if (i+1)%3 == 0 and i != 8:
                print()

    def solve(self):
        print("Solving Sudoku...")
        changed = []
        stack = [(-1, -1, -1, 0)]
        while len(stack) != 0:
            coord = stack.pop()
            row, col, num, depth = coord[0], coord[1], coord[2], coord[3]
            if (row, col, num, depth) != (-1, -1, -1, 0):
                self.sudoku[row][col] = num
                changed.append((row, col, num, depth))
            next_coord = self.findNextEmpty()
            if not next_coord:
                print("Sudoku has been solved!")
                print("The solution is: ")
                return self.sudoku
            next_row, next_col, next_depth = next_coord[0], next_coord[1], depth+1
            valid = self.getValidNumbers(next_row, next_col)
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
                    self.sudoku[remove_row][remove_col] = 0
                    changed.pop()
        print("Sudoku has been solved!\n")
        print("The solution is: ")
        return self.sudoku