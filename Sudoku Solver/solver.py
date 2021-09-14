class Solver():
	def __init__(self):
		self.solved_board = None

	def solve(self,board):

	    find = self.find_empty(board)

	    if not find:
	        return True
	    else:
	        row, col = find

	    for i in range(1,10):
	        if self.valid(board, i, (row, col)):
	            board[row][col] = i

	            if self.solve(board):
	                return True

	            board[row][col] = 0

	    self.solved_board = board

	    return False


	def valid(self,board, num, pos):

	    for i in range(len(board[0])):
	        if board[pos[0]][i] == num and pos[1] != i:
	            return False

	    for i in range(len(board)):
	        if board[i][pos[1]] == num and pos[0] != i:
	            return False

	    box_x = pos[1] // 3
	    box_y = pos[0] // 3

	    for i in range(box_y*3, box_y*3 + 3):
	        for j in range(box_x * 3, box_x*3 + 3):
	            if board[i][j] == num and (i,j) != pos:
	                return False

	    return True



	def find_empty(self,bo):
	    for i in range(len(bo)):
	        for j in range(len(bo[0])):
	            if bo[i][j] == 0:
	                return (i, j)  

	    return None		

	def solution(self,board):
		value = self.solve(board)
		if (value):
			print("\nSolution:\n")
			print(self.solved_board)
		else:
			print("\nCan't Find Solution")
