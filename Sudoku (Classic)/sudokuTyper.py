import pyautogui
import time

class sudokuTyper:
    def __init__(self, sudoku_website, initial_position, sudoku):
        self.sudoku_website = sudoku_website
        self.initial_position = initial_position
        self.sudoku = sudoku

    def openWebsite(self):
        if not self.sudoku_website:
            print("Sudoku website not found. Please ensure it is the only tab open.")
            return False
        self.sudoku_website.restore()
        self.sudoku_website.maximize()
        try:
            self.sudoku_website.activate()
        except Exception as e:
            print(f"Warning: Could not activate window ({e}). Continuing anyway.")
        return True
    
    def resetStartingPosition(self):
        pyautogui.moveTo(self.initial_position[1], self.initial_position[0])
        time.sleep(0.4)
        pyautogui.click()

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