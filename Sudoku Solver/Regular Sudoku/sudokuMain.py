from sudokuReader import sudokuReader
from sudokuSolver import sudokuSolver

def main():
    sr = sudokuReader("Puzzles/puzzle5.png")
    sr.readGrid("Numbers")
    ss = sudokuSolver(sr.sudoku)
    ss.solve()
    ss.printSolution()

if __name__ == "__main__":
    main()