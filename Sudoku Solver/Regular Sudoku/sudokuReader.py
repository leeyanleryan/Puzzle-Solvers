import cv2
import numpy as np

class sudokuReader:
    def __init__(self, image):
        self.name = image
        self.modified_name = self.getCroppedName()
        self.image = cv2.imread(image)
        self.modified_image = self.image
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.height, self.width, self.channels = self.getSize()
        self.sudoku = []
        self.border_rgb = [97, 72, 52]
        self.divider_rgb = [228, 217, 209]
        self.cropImage()
        self.readNumber()

    def getCroppedName(self):
        lst = self.name.split("/")
        temp = lst[-1].split(".")
        temp[0] = temp[0] + "_cropped"
        lst[-1] = ".".join(temp)
        return "/".join(lst)

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
        cv2.imwrite(self.modified_name, self.image)

    def getSize(self):
        return self.image.shape
    
    def cropImage(self):
        top_left, bottom_right = self.getBorderCoordinates()
        if top_left == bottom_right == (-1, -1):
            print("Invalid Image")
            return
        self.image = self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
        self.modified_image = self.image
        self.height, self.width, self.channels = self.getSize()
        cv2.imwrite(self.modified_name, self.image)
    
    def getBorderCoordinates(self):
        top_left = (-1, -1)
        for i in range(self.height):
            for j in range(self.width):
                if self.getRGBAt(i, j) == self.border_rgb:
                    top_left = (i, j)
                    break
            if top_left == (-1, -1):
                continue
            if top_left[0]+499 >= self.height or top_left[0]+499 >= self.width:
                continue
            top_left_rgb = self.getRGBAt(top_left[0], top_left[1])
            bottom_left_rgb = self.getRGBAt(top_left[0]+499, top_left[1])
            top_right_rgb = self.getRGBAt(top_left[0], top_left[1]+499)
            bottom_right_rgb = self.getRGBAt(top_left[0]+499, top_left[1]+499)
            if top_left_rgb == bottom_left_rgb == top_right_rgb == bottom_right_rgb:
                return top_left, (top_left[0]+499, top_left[1]+499)
        return (-1, -1), (-1, -1)
    
    def readNumber(self):
        for i in range(self.height):
            for j in range(self.width):
                rgb = self.getRGBAt(i, j)
                if rgb == self.border_rgb:
                    self.modified_image[i, j] = rgb
        
sr = sudokuReader("Puzzles/puzzle3.png")