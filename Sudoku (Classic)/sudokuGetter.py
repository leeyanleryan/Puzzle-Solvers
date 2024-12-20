import pygetwindow as gw
import pyautogui
import time
import os

class sudokuGetter:
    def __init__(self, directory):
        self.directory = directory
        self.puzzle_directory = ""
        self.sudoku_website = self.getSudokuWebsite()

    def getSudokuWebsite(self):
        sudoku_website = None
        for window in gw.getAllTitles():
            if (("Easy sudoku" in window) or
                ("Sudoku medium" in window) or
                ("Hard sudoku" in window) or
                ("Hardest sudoku" in window) or
                ("Sudoku Evil" in window) or
                ("Extreme Sudoku" in window) or
                ("Play Free Sudoku" in window)):
                sudoku_website = gw.getWindowsWithTitle(window)[0]
        if sudoku_website == None:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return
        return sudoku_website

    def getLatestPuzzleNumber(self):
        try:
            puzzles = os.listdir(self.directory)
            return len(puzzles)+1
        except FileNotFoundError:
            return "The directory does not exist."
        except PermissionError:
            return "You do not have permission to access this directory."

    def getSudokuScreenshot(self):
        print("Opening website to screenshot...")
        if not self.sudoku_website:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return
        self.sudoku_website.restore()
        self.sudoku_website.maximize()
        self.sudoku_website.activate()
        time.sleep(0.4)
        screenshot = pyautogui.screenshot()
        self.puzzle_directory = f"{self.directory}/puzzle{str(self.getLatestPuzzleNumber())}.png"
        screenshot.save(self.puzzle_directory)
        time.sleep(0.4)
        pyautogui.hotkey("alt", "tab")
        print("Website has been screenshotted!")
        print()