import cv2
import sys
import os

class sudokuReader:
    def __init__(self, image):
        self.name = image
        self.image = cv2.imread(self.name)
        self.height, self.width, self.channels = self.image.shape
        self.sudoku = []
        self.initial_position = ()
        self.border_rgb = [97, 72, 52]
        self.cropImage()

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
        print("Reading screenshot...")
        top_left, bottom_right = self.getBorderCoordinates()
        if top_left == bottom_right == (-1, -1):
            print("Invalid Image")
            return
        self.image = self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
        self.height, self.width, self.channels = self.image.shape
        self.saveImage(self.name, self.image)
        print("Sudoku has been extracted from the screenshot!")
        print()
    
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
                self.initial_position = (top_left[0]+25, top_left[1]+25)
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

    def setDataRow(self, index, number_image):
        row = []
        row.append(f"{str(index)},")
        for i in range(number_image.shape[0]):
            for j in range(number_image.shape[1]):
                if self.getRGBAt(number_image, i, j) != [255, 255, 255]:
                    row.append(f"({str(i)},{str(j)})")
        row = ",".join(row)
        return row

    def saveNumbers(self, folder):
        print("Saving numbers from the Sudoku...")
        start = [2, 58, 113, 168, 223, 278, 334, 388, 443]
        change = [54, 53, 52, 53, 53, 53, 52, 53, 54]
        data_empty = False
        try:
            number_data = os.listdir(folder)
        except FileNotFoundError:
            return "The directory does not exist."
        except PermissionError:
            return "You do not have permission to access this directory."
        index = len(number_data)
        if index == 1:
            data_empty = True
        data = []
        for i in range(9):
            for j in range(9):
                number_image = self.resizeNumberImage(start, change, i, j)
                number_image, is_empty = self.removeExtraColor(number_image)
                if not is_empty:
                    self.saveImage(f"{folder}/{str(index)}.png", number_image)
                    data.append(self.setDataRow(index, number_image))
                    index += 1
        with open(f"{folder}/data.txt", "a") as f:
            if not data_empty:
                f.write("\n")
            for i in range(len(data)-1):
                f.write(f"{data[i]}\n")
            f.write(f"{data[-1]}")
        print("Numbers from the sudoku has been saved!")
        print()
    
    def getNumbersData(self, folder):
        output = []
        with open(f"{folder}/data.txt", "r") as f:
            for line in f:
                line = line.rstrip().split(",")
                new_line = [int(line[0]), int(line[1])]
                for i in range(2, len(line), 2):
                    new_line.append((int(line[i][1:]), int(line[i+1][:-1])))
                output.append(new_line)
        return output

    def readGrid(self, folder):
        print("Reading Sudoku...")
        sys.setrecursionlimit(10000)
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
        print("Sudoku has been read!")
        print()

    def convertNumberImageToBinary(self, number_image):
        output, coords = [], []
        for i in range(number_image.shape[0]):
            row = []
            for j in range(number_image.shape[1]):
                if self.getRGBAt(number_image, i, j) == [255, 255, 255]:
                    row.append(0)
                else:
                    row.append(1)
                    coords.append((i, j))
            output.append(row)
        return output, coords
    
    def printNumber(self, binary_image):
        for row in binary_image:
            print("".join([str(x) for x in row]))
    
    def readNumber(self, number_image, numbers_data):
        binary_image, binary_coords = self.convertNumberImageToBinary(number_image)
        number_distances = []
        for number in numbers_data:
            number_coords = number[2:]
            total_distance = 0
            for binary_coord in binary_coords:
                x1 = binary_coord[0]
                y1 = binary_coord[1]
                min_distance = 5001
                for number_coord in number_coords:
                    x2 = number_coord[0]
                    y2 = number_coord[1]
                    if (x2-x1)**2 + (y2-y1)**2 < min_distance:
                        min_distance = (x2-x1)**2 + (y2-y1)**2
                total_distance += min_distance
            number_distances.append([number[1], total_distance])
        number_distances = sorted(number_distances, key = lambda x: x[-1])[:1]
        #self.printNumber(binary_image)
        #print(number_distances)
        #print()
        number = number_distances[0][0]
        if number == 3 or number == 8:
            return 8 if self.hasClosedLoop(binary_image) else 3
        return number
    
    def hasClosedLoop(self, binary_image):
        total = 0
        for i in range(len(binary_image)):
            for j in range(len(binary_image[0])):
                if binary_image[i][j] == 0:
                    total += 1
        bi_copy = [row.copy() for row in binary_image]
        bi_copy[0][0] = 1
        visited = [(0,0)]
        self.floodFill(bi_copy, 0, 0, visited)
        return len(visited) != total

    def floodFill(self, binary_image, row, col, visited):
        # up
        if row-1 > -1:
            if binary_image[row-1][col] == 0:
                binary_image[row-1][col] = 1
                visited.append((row-1, col))
                self.floodFill(binary_image, row-1, col, visited)
        # down
        if row+1 < len(binary_image):
            if binary_image[row+1][col] == 0:
                binary_image[row+1][col] = 1
                visited.append((row+1, col))
                self.floodFill(binary_image, row+1, col, visited)
        # left
        if col-1 > -1:
            if binary_image[row][col-1] == 0:
                binary_image[row][col-1] = 1
                visited.append((row, col-1))
                self.floodFill(binary_image, row, col-1, visited)
        # right
        if col+1 < len(binary_image[0]):
            if binary_image[row][col+1] == 0:
                binary_image[row][col+1] = 1
                visited.append((row, col+1))
                self.floodFill(binary_image, row, col+1, visited)