from typing import List
import copy
from itertools import permutations
import random

class Sudoku:
    def __init__(self,n:int):
        self.n = n
        self.chances = 3
        self.size = self.n**2
        self.board = self.generate_sudoku()
        self.board_copy = copy.deepcopy(self.board)

    def is_valid(self,row:int, column:int, num:int)->bool:
        output:bool = True
        if row < self.size and column < self.size : 
            for i in range(0,(self.size)):
                if self.board[row][i] == num or self.board[i][column] == num:
                    output = False
            sq_row = row // self.n
            sq_column = column // self.n
            for i in range((sq_row * self.n), ((sq_row * self.n)+ self.n)):
                for j in range((sq_column * self.n), ((sq_column * self.n)+ self.n)):
                    if self.board[i][j] == num:
                        output = False
        else:
            output = False
        return output    
    
    def restore(self):
        self.chances = 3
        self.board = copy.deepcopy(self.board_copy)
    
    def chance(self)->int:
        return self.chances

    def make_move(self,row:int, column:int, value:int):
        self.board[row][column] = value

    def decrement_chance(self) -> int:
        self.chances -= 1
        return self.chances
    
    def check_winner(self):
        # output = False
        # for i in self.board:
            # output  = output or (0 in i)
        # return not output
        return ([i for i in self.board if 0 in i] == [])

    def generate_sudoku(self):
        board = [[0 for _ in range(self.size)]for _ in range(self.size)]
        self.board = board
        self.solver(board, 0, 0)
        return self.add_none(board)
 
    def solver(self, board, i, j):
        if i == self.size:
            return True
        if j == self.size:
            return self.solver(board, i+1, 0)
        if board[i][j] != 0:
            return self.solver(board, i, j+1) 
        values = random.choice(list(permutations(self.all_possible_values(i, j))))
        for k in range(0, len(values)):
            board[i][j] = values[k]
            if self.solver(board, i, j+1):
                return True
            board[i][j] = 0
        return False
    
    def all_possible_values(self, i, j):
        output = []
        for k in range(1,self.size+1):
            if self.is_valid(i, j, k):
                output.append(k)
        return output
    
    def add_none(self, board):
        value = random.choice(list(range(40,61)))
        counter = int((value / 100) * (self.size**2))
        while counter :
            row = random.randint(0,self.size-1)
            col = random.randint(0,self.size-1)
            if board[row][col] != 0:
                board[row][col] = 0
                counter -= 1
        return board

    
    def __str__(self)->str:
        return f'"size":{self.size},"board":{self.board}'