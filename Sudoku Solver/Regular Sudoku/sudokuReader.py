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
            top_left = (-1, -1)
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
        coords = []
        start = [2, 58, 113, 168, 223, 278, 334, 388, 443]
        change = [54, 53, 52, 53, 53, 53, 52, 53, 54]
        for i in range(9):
            curr_row = []
            for j in range(9):
                top_left = (start[i], start[j])
                bottom_right = (top_left[0]+change[i], top_left[1]+change[j])
                curr_row.append([top_left, bottom_right])
                number_image = self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
                cv2.imwrite(f"Numbers/{str(i*9+j+1)}.png", number_image)
            coords.append(curr_row)
        print(coords)
        
sr = sudokuReader("Puzzles/puzzle3.png")