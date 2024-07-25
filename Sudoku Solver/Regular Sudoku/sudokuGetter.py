import pygetwindow as gw
import pyautogui
import time

class sudokuGetter:
    def __init__(self, directory):
        self.directory = directory
        self.puzzle_directory = ""
        self.sudoku_website = self.getSudokuWebsite()

    def getSudokuWebsite(self):
        sudoku_website = None
        for window in gw.getAllTitles():
            if "Sudoku" in window and "free" in window:
                sudoku_website = gw.getWindowsWithTitle(window)[0]
        if sudoku_website == None:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return
        return sudoku_website

    def getLatestPuzzleNumber(self):
        with open(f"{self.directory}/latest.txt", "r") as f:
            puzzle_number = int(f.readline().rstrip())
        with open(f"{self.directory}/latest.txt", "w") as f:
            f.write(f"{str(puzzle_number+1)}")
        return puzzle_number

    def getSudokuScreenshot(self):
        if not self.sudoku_website:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return
        time.sleep(0.5)
        self.sudoku_website.restore()
        self.sudoku_website.maximize()
        self.sudoku_website.activate()
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        self.puzzle_directory = f"{self.directory}/puzzle{str(self.getLatestPuzzleNumber())}.png"
        screenshot.save(self.puzzle_directory)
        time.sleep(0.5)
        pyautogui.hotkey("alt", "tab")