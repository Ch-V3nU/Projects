#!/usr/bin/py2

import cv2
import imutils
import numpy as np
from solver import Solver
from Recognizer import OCR
from skimage.segmentation import clear_border
from imutils.perspective import four_point_transform


class Sudoku(object):
	def __init__(self, image):
		self.image = image
		self.gray = None
		

	def initialize_image(self):

		self.image = cv2.imread(self.image)
		self.image = imutils.resize(self.image, width=600)

		return 


	def fetch_rectangle(self):

		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(self.gray, (7, 7), 3)

		thresh = cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
		thresh = cv2.bitwise_not(thresh)


		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

		puzzleCnt = None

		for c in cnts:

			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)

			if len(approx) == 4:
				puzzleCnt = approx
				break

		return puzzleCnt


	def extract_sudoku_board(self,board):

		original_image = four_point_transform(self.image, board.reshape(4, 2))
		gray_image = four_point_transform(self.gray, board.reshape(4, 2))


		return gray_image

	def split_board(self,board):

		return board.shape[1] // 9, board.shape[0] // 9

	def extract_digit(self,cell):

		thresh = cv2.threshold(cell, 0, 255,
			cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		thresh = clear_border(thresh)


		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		if len(cnts) == 0:
			return None

		c = max(cnts, key=cv2.contourArea)
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)

		(h, w) = thresh.shape
		percentFilled = cv2.countNonZero(mask) / float(w * h)

		if percentFilled < 0.03:
			return None

		digit = cv2.bitwise_and(thresh, thresh, mask=mask)

		return digit

	def process_cells(self,stepX,stepY,board):

		ocr = OCR()

		sudoku_array = np.zeros((9, 9), dtype="int")

		cellLocs = []
		boolean = True

		for y in range(0, 9):

			row = []
			for x in range(0, 9):

				startX = x * stepX
				startY = y * stepY
				endX = (x + 1) * stepX
				endY = (y + 1) * stepY

				row.append((startX, startY, endX, endY))

				cell = board[startY:endY, startX:endX]
				digit = self.extract_digit(cell)

				if (digit is not None):
					cv2.imwrite("img-"+str(y)+str(x)+".png",digit)
					sudoku_array[y][x] = ocr.prediction(digit)


		return sudoku_array


	def solve(self):

		self.initialize_image()
		board = self.fetch_rectangle()

		if board is None:
			return 

		board = self.extract_sudoku_board(board)
		x,y = self.split_board(board)
		final_board = self.process_cells(x,y,board)

		return final_board

def manipulate(board):

	canShow = True

	while (canShow):

		decision = raw_input("\nWanna make any corrections to the board? Press y if yes:-")

		if (decision and decision[0].lower() == "y"):
			canShow = False
			break

		values = raw_input("\nEnter Row,Column and Value. Ex: 2,2,3: ").split(",")

		try:

			row,col,val = list(map(int,values[:3]))

			check = lambda x:  x>0 and x<10

			if (all([check(i) for i in [row,col,val]])):

				board[row-1][col-1] = val
				print("\nUpdated Board\n")
				print(board)

			else:
				print("\nInvalid input")

		except:
			print("\nInvalid input")

	return board



sudoku_board = Sudoku("Images/sudoku.jpg").solve()
print(sudoku_board)
updated_board = manipulate(sudoku_board)
Solver().solution(updated_board)
