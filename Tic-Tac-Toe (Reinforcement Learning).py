#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import enum
from random import randrange

#enumeration for X and Y marks, empty slots are called 'none'
class Mark (enum.Enum):
    none = None
    X = 'X'
    Y = 'Y'

#define a board
board = [None] * 9

#value function is a map of states to their value
value_function = {}

#indexes of winning rows, columns, and diagonals
l_win_ind = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7],             [2,5,8], [0,4,8], [2,4,6]]

#do we have a winner? X, Y, or None yet
def get_winner (board):

    #check all winning stripes
    for win_ind in l_win_ind:
        #get a set of marks on the winning stripe
        marks = set([board[i] for i in win_ind])
        #if there is only one type of mark, and it is not None
        if len(marks) == 1 and None not in marks:
            return marks.pop () #we got a winner
    return None

#play a move, X or Y passed in as a parameter
def play_a_random_move (mark):
    #if there is no empty spot 
    if None not in board:
        return False #could not play
    
    #get a list of empty spots
    l_empty = [i for i, x in enumerate(board) if x == None]
    #select an empty spot
    idx_select = randrange (len(l_empty))
    #play the move
    board [l_empty[idx_select]] = mark

    return True #played a move

def get_value_of_state (board):
    winner = get_winner (board)
    #'X' won, so we won, so value = 1.0
    if winner == 'X':
        print ('got X winner value for ', board)
        return 1.0
    #'Y' won, we lost, so value = 0.0
    elif winner == 'Y':
        print ('got Y winner value for ', board)
        return 0.0
    #no winner yet
    else:
        #if we have a non-default (0.5) value
        if str (board) in value_function.keys ():
            print ('got from value function, value ', value_function [str(board)], ' for ', board)
            return value_function [str(board)]
        else:
            #default value of a state
            # P(equally probable to win or lose) = 0.5
            #print ('got default value ', 0.5, ' for ', board)
            return 0.5
        
def play_a_greedy_move (mark):    
    #we refer the global board as the present state
    global board
    
    #if there is no empty spot 
    if None not in board:
        return False #could not play

    this_state = board
    #default value of a state
    # P(equally probable to win or lose) = 0.5
    this_state_value = 0.5
    #if this state has a non-default value
    if str(this_state) in value_function.keys ():
        this_state_value = value_function [str(this_state)]

    #get possible move indices
    l_empty = [i for i, x in enumerate(board) if x == None]
    
    #initialize the next state to transition to, along with its value
    next_state_max = []
    next_state_value_max = -1
    
    #try a move for every possible move index
    #find which next-state has maximum value
    for i in l_empty:
        #create a copy of the present board state
        candidate_next_state = board.copy ()
        
        #make a move
        candidate_next_state [i] = mark
        
        #get value of the board state after the move
        candidate_next_state_value = get_value_of_state (candidate_next_state)

        #default value of a state
        # P(equally probable to win or lose) = 0.5
        #candidate_next_state_value = 0.5
        
        #if this state has a non-default value
        #if str(candidate_next_state) in value_function.keys ():
            #candidate_next_state_value = value_function [str(candidate_next_state)]

        #keep track of which next-state has maximum value
        if candidate_next_state_value > next_state_value_max:
            next_state_max = candidate_next_state
            next_state_value_max = candidate_next_state_value

    #store state if value is not 0.5
    #if next_state_value_max != 0.5:
        #value_function [str(next_state_max)] = next_state_value_max
        
    #update value of this state, and store it in the value function
    #print ('this state', this_state, 'value', get_value_of_state(this_state))
    this_state_value += (0.1*next_state_value_max)
    #print ('new value', this_state_value)
    value_function [str(this_state)] = this_state_value
    
    #make the move
    board = next_state_max
    
    return True #played a move 


# In[2]:


#episodes - play some games
for i in range (1000):
    board = [None] * 9
    played = True
    while played:
        played = play_a_greedy_move ('X')
        if get_winner (board) is not None:
            break
        if (played):
            played = play_a_random_move ('Y')
        if get_winner (board) is not None:
            break


# In[3]:


for k, v in value_function.items ():
    print (k, v)


# #set up values for winning and losing states
# #value = 1.0 for winning states, value = 0.0 for losing states
# def init_win_lose_states ():
#     #create a no-moves board
#     no_move_board = [None] * 9
# 
#     #iterate over winning stripes
#     for stripe in l_win_ind:
#         #create an X winning and Y winning board each for this stripe
#         board_state_x_win = no_move_board.copy ()
#         board_state_y_win = no_move_board.copy ()
#         #set the marks at the winning indices
#         for j in stripe:
#             board_state_x_win [j] = 'X'
#             board_state_y_win [j] = 'Y'
#         #add this X winning and Y winning board to the value function
#         # and assign values
#         #str is used to convert a non-hashable list to a hashable string
#         value_function [str(board_state_x_win)] = 1.0
#         value_function [str(board_state_y_win)] = 0.0

# In[4]:


from IPython.core.debugger import set_trace
board = [None] * 9
played = True
while played:
    played = play_a_greedy_move ('X')
    print (board)
    if get_winner (board) is not None:
        break
    if (played):
        index = -1
        set_trace ()
        board [index] = 'Y'
        played = True#play_a_random_move ('Y')
    if get_winner (board) is not None:
        break
print (get_winner (board), ' won !!!')


# In[ ]:




