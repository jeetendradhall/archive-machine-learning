#!/usr/bin/env python
# coding: utf-8

# In[111]:


#imports
import enum
from random import randrange

#enumeration for X and Y marks, empty slots are called 'none'
class Mark (enum.Enum):
    none = None
    X = 'X'
    Y = 'Y'

#define a board
board = [Mark.none] * 9

#do we have a winner? Mark.X, Mark.Y, or none (Mark.none) yet
def winner ():
    #indexes of winning rows, columns, and diagonals
    l_win_ind = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    #check all winning stripes
    for win_ind in l_win_ind:
        #get a set of marks on the winning stripe
        marks = set([board[i] for i in win_ind])
        #if there is only one type of mark, and it is not None
        if len(marks) == 1 and None not in marks:
            return marks.pop () #we got a winner
    return None

#play a move, Mark.X or Mark.Y passed in as a parameter
def play_a_move (mark):
    #if there is no empty spot 
    if Mark.none not in board:
        return False #could not play
    
    #get a list of empty spots
    l_empty = [i for i, x in enumerate(board) if x == Mark.none]
    #select an empty spot
    idx_select = randrange (len(l_empty))
    #play the move
    board [l_empty[idx_select]] = mark

    return True #played a move


# In[112]:


print(play_a_move (Mark.X))
board

