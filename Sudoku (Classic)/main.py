from sudokuGetter import sudokuGetter
from sudokuReader import sudokuReader
from sudokuSolver import sudokuSolver
from sudokuTyper import sudokuTyper

def main():
    automated()
    #manual()

def automated():
    sg = sudokuGetter("Puzzles")
    sg.getSudokuScreenshot()
    sr = sudokuReader(sg.puzzle_directory)
    sr.readGrid("Numbers")
    ss = sudokuSolver(sr.sudoku)
    ss.solve()
    st = sudokuTyper(sg.sudoku_website, sr.initial_position, ss.sudoku)
    st.inputSolution()

def manual():
    sudoku = [[0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]]
    ss = sudokuSolver(sudoku)
    ss.solve()
    ss.printSolution()

if __name__ == "__main__":
    main()