import cv2
import sys

class sudokuReader:
    def __init__(self, image):
        sys.setrecursionlimit(10000)
        self.name = image
        self.image = cv2.imread(self.name)
        self.height, self.width, self.channels = self.image.shape
        self.sudoku = []
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
        top_left, bottom_right = self.getBorderCoordinates()
        if top_left == bottom_right == (-1, -1):
            print("Invalid Image")
            return
        self.image = self.image[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
        self.height, self.width, self.channels = self.image.shape
        self.saveImage(self.name, self.image)
    
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
        start = [2, 58, 113, 168, 223, 278, 334, 388, 443]
        change = [54, 53, 52, 53, 53, 53, 52, 53, 54]
        data_empty = False
        with open(f"{folder}/latest.txt", "r") as f:
            index = int(f.readline())
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
        with open(f"{folder}/latest.txt", "w") as f:
            f.write(str(index))
        with open(f"{folder}/data.txt", "a") as f:
            if not data_empty:
                f.write("\n")
            for i in range(len(data)-1):
                f.write(f"{data[i]}\n")
            f.write(f"{data[-1]}")
    
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
    
    def printNumber(self, binary_image):
        for row in binary_image:
            print("".join([str(x) for x in row]))
    
    def readNumber(self, number_image, numbers_data):
        binary_image = self.convertNumberImageToBinary(number_image)
        sp_forward, sp_backward = self.getSumProduct(binary_image)
        nd_copy = [row.copy() for row in numbers_data]
        for row in nd_copy:
            row[1] = abs(row[1]-sp_forward)
            row[2] = abs(row[2]-sp_backward)
            if (row[1], row[2]) == (0, 0):
                return row[3]
        nd_copy = sorted(sorted(nd_copy, key = lambda x: x[2])[:16], key = lambda x: x[1])[:5]
        print(sp_forward, sp_backward)
        print(nd_copy)
        self.printNumber(binary_image)
        print()
        return 0
    
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

sr = sudokuReader("Puzzles/puzzle17.png")
#sr.saveNumbers("Numbers")
sr.readGrid("Numbers")

# for i in range(9):
#     row = ""
#     for j in range(9):
#         row += str(sr.sudoku[i][j])
#         if (j+1)%3 == 0:
#             row += "  "
#     print(row)
#     if (i+1)%3 == 0:
#         print()

# def getRGBAt(image, row, col):
#     return [value for value in image[row, col]]

# output = []
# with open("Numbers/data.txt", "r") as f:
#     for line in f:
#         line = line.split(",")
#         row = []
#         row.append(line[0])
#         row.append(line[-1].rstrip())
#         number_image = cv2.imread(f"Numbers/{line[0]}.png")
#         for i in range(number_image.shape[0]):
#             for j in range(number_image.shape[1]):
#                 if getRGBAt(number_image, i, j) != [255, 255, 255]:
#                     row.append(f"({str(i)},{str(j)})")
#         row[-1] = row[-1] + "\n"
#         row = ",".join(row)
#         output.append(row)

# with open("Numbers/data.txt", "w") as f:
#     for row in output:
#         f.write(row)