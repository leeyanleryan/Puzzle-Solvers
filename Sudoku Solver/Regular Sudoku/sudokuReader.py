import cv2
import os.path

class sudokuReader:
    def __init__(self, image):
        self.name = image
        self.modified_name = self.getCroppedName()
        self.getImage()
        self.modified_image = self.image
        self.height, self.width, self.channels = self.image.shape
        self.sudoku = []
        self.border_rgb = [97, 72, 52]
        self.divider_rgb = [228, 217, 209]
        self.cropImage()

    def getImage(self):
        if os.path.isfile(self.modified_name):
            self.image = cv2.imread(self.modified_name)
        else:
            self.image = cv2.imread(self.name)

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

    def getRGBAt(self, image, row, col):
        return [value for value in image[row, col]]

    def changeRGBAt(self, image, row, col, rgb):
        image[row, col] = rgb
    
    def saveImage(self, name, image):
        cv2.imwrite(name, image)
    
    def cropImage(self):
        top_left, bottom_right = self.getBorderCoordinates()
        if top_left == bottom_right == (-1, -1):
            print("Invalid Image")
            return
        self.image = self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
        self.modified_image = self.image
        self.height, self.width, self.channels = self.image.shape
        self.saveImage(self.modified_name, self.image)
    
    def getBorderCoordinates(self):
        top_left = (-1, -1)
        for i in range(self.height):
            top_left = (-1, -1)
            for j in range(self.width):
                if self.getRGBAt(self.image, i, j) == self.border_rgb:
                    top_left = (i, j)
                    break
            if top_left == (-1, -1):
                continue
            if top_left[0]+499 >= self.height or top_left[1]+499 >= self.width:
                continue
            top_left_rgb = self.getRGBAt(self.image, top_left[0], top_left[1])
            bottom_left_rgb = self.getRGBAt(self.image, top_left[0]+499, top_left[1])
            top_right_rgb = self.getRGBAt(self.image, top_left[0], top_left[1]+499)
            bottom_right_rgb = self.getRGBAt(self.image, top_left[0]+499, top_left[1]+499)
            if top_left_rgb == bottom_left_rgb == top_right_rgb == bottom_right_rgb:
                return top_left, (top_left[0]+499, top_left[1]+499)
        return (-1, -1), (-1, -1)
    
    def removeExtraColor(self, number_image):
        is_empty = True
        for k in range(number_image.shape[0]):
            for l in range(number_image.shape[1]):
                rgb = self.getRGBAt(number_image, k, l)
                if rgb == [255,255,255]:
                    continue
                if rgb == self.border_rgb:
                    is_empty = False
                    continue
                self.changeRGBAt(number_image, k, l, [255,255,255])
        return number_image, is_empty
    
    def resizeNumberImage(self, start, change, i, j):
        height, width = change[i], change[j]
        
        if height == 54 and width == 54:
            top_left = (start[i]+2, start[j]+2)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 54 and width == 53:
            top_left = (start[i]+2, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 54 and width == 52:
            top_left = (start[i]+2, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)

        elif height == 53 and width == 54:
            top_left = (start[i]+1, start[j]+2)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 53 and width == 53:
            top_left = (start[i]+1, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 53 and width == 52:
            top_left = (start[i]+1, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)

        elif height == 52 and width == 54:
            top_left = (start[i]+1, start[j]+2)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 52 and width == 53:
            top_left = (start[i]+1, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)
        elif height == 52 and width == 52:
            top_left = (start[i]+1, start[j]+1)
            bottom_right = (top_left[0]+49, top_left[1]+49)

        return self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    def saveNumbers(self, folder):
        start = [2, 58, 113, 168, 223, 278, 334, 388, 443]
        change = [54, 53, 52, 53, 53, 53, 52, 53, 54]
        data_empty = False
        with open(f"{folder}/data.txt", "r") as f:
            last = ""
            for line in f:
                last = line
        if last == "":
            data_empty = True
            curr = 1
        else:
            curr = int(last.split(",")[0])+1
        data = []
        for i in range(9):
            for j in range(9):
                number_image = self.resizeNumberImage(start, change, i, j)
                number_image, is_empty = self.removeExtraColor(number_image)
                if not is_empty:
                    self.saveImage(f"{folder}/{str(curr)}.png", number_image)
                    binary_image = self.convertNumberImageToBinary(number_image)
                    sp_forward, sp_backward = self.getSumProduct(binary_image)
                    data.append((str(curr), str(sp_forward), str(sp_backward)))
                    curr += 1
        with open(f"{folder}/data.txt", "a") as f:
            if not data_empty:
                f.write("\n")
            for i in range(len(data)-1):
                f.write(f"{data[i][0]},{data[i][1]},{data[i][2]},\n")
            f.write(f"{data[len(data)-1][0]},{data[len(data)-1][1]},{data[len(data)-1][2]},")
    
    def getNumbersData(self, folder):
        output = []
        with open(f"{folder}/data.txt", "r") as f:
            for line in f:
                line = line.rstrip().split(",")
                line = [int(x) for x in line]
                output.append(line)
        return output

    def readGrid(self, folder):
        start = [2, 58, 113, 168, 223, 278, 334, 388, 443]
        change = [54, 53, 52, 53, 53, 53, 52, 53, 54]
        numbers_data = self.getNumbersData(folder)
        for i in range(9):
            row = []
            for j in range(9):
                number_image = self.resizeNumberImage(start, change, i, j)
                number_image, is_empty = self.removeExtraColor(number_image)
                if is_empty:
                    number = 0
                else:
                    number = self.readNumber(number_image, numbers_data)
                row.append(number)
            self.sudoku.append(row)

    def convertNumberImageToBinary(self, number_image):
        output = []
        for i in range(number_image.shape[0]):
            row = []
            for j in range(number_image.shape[1]):
                if self.getRGBAt(number_image, i, j) == [255, 255, 255]:
                    row.append(0)
                else:
                    row.append(1)
            output.append(row)
        return output
    
    def getSumProduct(self, binary_image):
        forward = 0
        multiplier = 1
        for i in range(len(binary_image)):
            has_ones = False
            for j in range(len(binary_image[0])):
                if binary_image[i][j] == 1:
                    has_ones = True
                    forward += multiplier**3
            if has_ones:
                multiplier += 1
        backward = 0
        multiplier = 1
        for i in range(len(binary_image)-1, -1, -1):
            has_ones = False
            for j in range(len(binary_image[0])-1, -1, -1):
                if binary_image[i][j] == 1:
                    has_ones = True
                    backward += multiplier**3
            if has_ones:
                multiplier += 1
        return forward, backward
    
    def printNumber(self, binary_image):
        for row in binary_image:
            pass
            print("".join([str(x) for x in row]))
    
    def readNumber(self, number_image, numbers_data):
        binary_image = self.convertNumberImageToBinary(number_image)
        sp_forward, sp_backward = self.getSumProduct(binary_image)
        nd_copy = [row.copy() for row in numbers_data]
        print(sp_forward, sp_backward)
        for row in nd_copy:
            row[1] = abs(row[1]-sp_forward)
            row[2] = abs(row[2]-sp_backward)
        nd_copy.sort(key = lambda x: x[1])
        print(nd_copy)
        #self.printNumber(binary_image)
        print()
        return 0
        
sr = sudokuReader("Puzzles/puzzle9.png")
sr.saveNumbers("Numbers")