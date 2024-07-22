from sudokuReader import sudokuReader
from sudokuSolver import sudokuSolver

if __name__ == "__main__":
    # Using screenshots
    sr = sudokuReader("Puzzles/ss puzzle3.png")
    ss = sudokuSolver(sr.sudoku)
    ss.solve()
    ss.printSolution()

    # Manually Typing
    # puzzle1 = [[9,5,0,  0,0,2,  0,6,7], 
    #            [4,7,2,  0,0,0,  1,0,3],
    #            [0,3,8,  9,0,0,  0,2,4],

    #            [0,0,7,  2,0,0,  0,3,5],
    #            [3,0,0,  5,8,1,  0,7,0],
    #            [0,0,0,  0,0,3,  9,0,0],

    #            [0,2,0,  8,0,0,  0,0,0],
    #            [0,8,9,  0,7,0,  0,1,2],
    #            [0,0,6,  0,2,0,  3,5,8]]

    # answer1 = [[9,5,1,  4,3,2,  8,6,7],
    #            [4,7,2,  6,5,8,  1,9,3],
    #            [6,3,8,  9,1,7,  5,2,4],

    #            [8,1,7,  2,9,6,  4,3,5],
    #            [3,9,4,  5,8,1,  2,7,6],
    #            [2,6,5,  7,4,3,  9,8,1],

    #            [1,2,3,  8,6,5,  7,4,9],
    #            [5,8,9,  3,7,4,  6,1,2],
    #            [7,4,6,  1,2,9,  3,5,8]]

    # ss = sudokuSolver(puzzle1)
    # my_ans1 = ss.solve()
    # ss.printSolution()
    # print(f"Solution is same as answer: {my_ans1 == answer1}")

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

    # ss.sudoku = puzzle2
    # my_ans2 = ss.solve()
    # ss.printSolution()
    # print(f"Solution is same as answer: {my_ans2 == answer2}")