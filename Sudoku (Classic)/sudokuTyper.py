import pyautogui

class sudokuTyper:
    def __init__(self, sudoku, sudoku_website):
        self.sudoku = sudoku
        self.sudoku_website = sudoku_website

    def openWebsite(self):
        if not self.sudoku_website:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return False
        self.sudoku_website.restore()
        self.sudoku_website.maximize()
        self.sudoku_website.activate()
        return True
    
    def resetStartingPosition(self):
        for _ in range(9):
            pyautogui.press("up")
            pyautogui.press("left")

    def inputSolution(self):
        print("Inputting solution...")
        if not self.openWebsite():
            return
        self.resetStartingPosition()
        for i in range(9):
            direction = "right" if i%2 == 0 else "left"
            for j in range(9):
                if direction == "right":
                    pyautogui.press(f"{str(self.sudoku[i][j])}")
                elif direction == "left":
                    pyautogui.press(f"{str(self.sudoku[i][8-j])}")
                pyautogui.press(direction)
            pyautogui.press("down")
        print("Solution has been inputted!")