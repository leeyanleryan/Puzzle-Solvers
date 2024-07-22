import cv2
import numpy as np

class sudokuReader:
    def __init__(self, image):
        self.image = cv2.imread(image)
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.sudoku = []
        self.height, self.width = self.getSize()
        #self.cropImage()

    def displayImage(self):
        cv2.imshow('Sudoku', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getRGBAt(self, row, col):
        return [value for value in self.image[row, col]]

    def getHSVAt(self, row, col):
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return [value for value in self.hsv_image[row, col]]

    def changeRGBAt(self, row, col, rgb):
        self.image[row, col] = rgb
        cv2.imwrite('Modified/ss puzzle3 modified.png', self.image)

    def getSize(self):
        height, width, channels = self.image.shape
        return height, width
    
    def cropImage(self):
        if (self.height, self.width) == (500, 500):
            return
        top_left = (-1, -1)
        for i in range(self.height):
            for j in range(self.width):
                if self.getRGBAt(i, j) == [97, 72, 52]:
                    top_left = (i, j)
                    break
            if top_left == (-1, -1):
                continue
            if top_left[0]+1 < self.height and top_left[0]+1 < self.width:

        return top_left
        
sr = sudokuReader("Puzzles/ss puzzle3.png")
#print(sr.cropImage())
print(sr.getRGBAt(3+499, 5+499))