import pygetwindow as gw
import pyautogui
import time

class sudokuTyper:
    def __init__(self, sudokuWebsite):
        self.sudokuWebsite = self.getSudokuWebsite()

    def getSudokuWebsite(self):
        for window in gw.getAllTitles():
            if "Sudoku" in window and "free" in window:
                sudokuWebsite = gw.getWindowsWithTitle(window)[0]
        return sudokuWebsite

    def inputSudokuWebsite(self, solution):
        if not self.sudokuWebsite:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return
        
        self.sudokuWebsite.activate()
        for i in range(5):
            pyautogui.press("right")