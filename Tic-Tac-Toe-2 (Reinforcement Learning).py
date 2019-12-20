#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import random
from random import randrange


# In[2]:


#tic-tac-toe class to encapsulate the following:
#1. state (a 3x3 board), get_start_board
#2. reward (state) (1.0 for an X stripe,
#    0.0 for O stripe, 0.5 by default,
#    learnt rewards from value function) get_value ()
#3. action - play_a_random_move,
#            play_an_explore_exploit_move,
#           play_a_greedy_move
#4. value function - a map from state to its long-term value
#5. stride (game) - a sequence of states leading to the end of a game
#6. episodes/learn - a set of strides (games) played 
#               to learn the value function
#7. helper functions:
#    get_value () - goal state value of 1.0 or 0.0;
#                   value function;
#                   default value
#    backpropagate_values () - of states in a stride in reverse order
#    get_winner () - do we have a winner? X, O, or None yet
#8. winning stripes - set of 8 stripes of 
#                      row or column or diagonal of size 3
#9. explore_exploit percentage
#10. learning_rate
class TicTacToe:
    def __init__ (self):
        #also see helper get_start_board (), init_start_board ()
        #self.board = [None] * 9
        self.value_function = {}
        self.reward_default = 0.5
        self.reward_x = 1.0
        self.reward_o = 0.0
        #indexes of winning rows, columns, and diagonals
        self.winning_stripes = [[0,1,2], [3,4,5], [6,7,8], [0,3,6]                                , [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        #percentage of exploration
        self.explore_exploit = 0.3
        self.learning_rate = 0.1
    
    #helper to initialize the start board
    # at the beginning of every stride
    #def init_start_board (self):
        #self.board = self.get_start_board ()
        
    def print_value_function (self, cutoff = 0.0, num_moves = 0):
        print ('Value Function:')
        for state, value in self.value_function.items ():
            
            #if we have a state value above cutoff and
            # if there are at least 'num_moves' moves made
            if value >= cutoff and             state.count ('None') <= (9 - num_moves):
                print (state, value)
    
    #empty 3x3 tic-tac-toe board
    def get_start_board (self):
        return [None] * 9
    
    #do we have a winner? X, O, or None yet
    def get_winner (self, board):
        #check all winning stripes
        for stripe in self.winning_stripes:
            #get a set of marks on the winning stripe
            marks = set([board[i] for i in stripe])
            #if there is only one type of mark, and it is not None
            if len(marks) == 1 and None not in marks:
                return marks.pop () #we got a winner
        return None
    
    def get_value (self, board):
        winner = self.get_winner (board)
        #'X' won, so we won, so value = 1.0
        if winner == 'X':
            #print ('got X winner value for ', board)
            return self.reward_x
        #'O' won, we lost, so value = 0.0
        elif winner == 'O':
            #print ('got O winner value for ', board)
            return self.reward_o
        #no winner yet
        else:
            #if we have a non-default (0.5) value
            if str (board) in self.value_function.keys ():
                #print ('got from value function, value ',\
                #       self.value_function [str(board)], ' for ', board)
                return self.value_function [str(board)]
            else:
                #default value of a state
                # P(equally probable to win or lose) = 0.5
                #print ('got default value ', 0.5, ' for ', board)
                return self.reward_default
    
    #called only for non-winning, and non-default values
    #so, add/update the (state, value) map in the value function
    def set_value (self, board, value):
        self.value_function [str(board)] = value
        
    #update the value of the board (state) by
    # a learning rate fraction of the value of
    # the next state in the stride
    def learn_value (self, this_board, next_board):
        next_state_value = self.get_value (next_board)
        this_state_value = self.get_value (this_board)
        this_state_value += (self.learning_rate * next_state_value)
        self.set_value (this_board, this_state_value)
    
    #NO. stride function - updates member variable board
    
    #play a random move, X or O (mostly) passed in as a 'mark' parameter
    #return ('played a move yes/no')
    def play_a_random_move (self, board, mark):
        #if there is no empty spot 
        if None not in board:
            return board, False #could not play

        #get a list of empty spots
        l_empty = [i for i, x in enumerate(board) if x == None]
        #randomly select an empty spot
        idx_select = randrange (len(l_empty))
        #play the move
        board [l_empty[idx_select]] = mark

        #return (board, 'played a move yes/no')
        return board, True
    
    #get next greedy state and its value
    def get_next_greedy_state (self, board, mark):
        #if there is no empty spot 
        if None not in board:
            return None, -1 #(no next state, invalid value)

        #get a list of empty spots
        l_empty = [i for i, x in enumerate(board) if x == None]
        
        #initialize the next state to transition to,
        # along with its value
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
            candidate_next_state_value =             self.get_value (candidate_next_state)
            #keep track of which next-state has maximum value
            if candidate_next_state_value > next_state_value_max:
                next_state_max = candidate_next_state
                next_state_value_max = candidate_next_state_value
                
        return next_state_max, next_state_value_max
    
    #NO - stride function - updates member variable board
    
    #play a greedy move, X (mostly) or O passed in as a 'mark' parameter
    #return (board, 'played a move yes/no')
    def play_a_greedy_move (self, board, mark):
        #if there is no empty spot 
        if None not in board:
            return board, False #could not play
        
        #get the next state greedily
        next_state_max, next_state_value_max =         self.get_next_greedy_state (board, mark)
        #play the move
        board = next_state_max
        
        #we are not making use of next_state_value_max.
        #we will store the moves in a stripe.
        #we will backpropagate through the stripe 
        # and update the state values.
        
        #return 'played a move yes/no'
        return board, True 

    #play an explore/exploit move, X (mostly) or O passed in
    # as a 'mark' parameter
    #return (board, 'played a move yes/no')
    def play_an_explore_exploit_move (self, board, mark):
        #if there is no empty spot 
        if None not in board:
            return board, False #could not play
        
        #we have a chance of explore or exploit ?
        chance = random.random ()
        if chance <= self.explore_exploit:
            return self.play_a_random_move (board, mark)
        else:
            return self.play_a_greedy_move (board, mark)
    
    #the last state is usually a 'X' win or a 'O' win state
    # or a 'draw' state
    #backpropagate, starting from the last state and
    # percolating the value backwards towards the previous
    # state by a learning factor
    def backpropagate_values (self, boards):
        #index of the last board
        n = len (boards) - 1
        #iterate from last to second board,
        # and update the value of the previous board using this board
        for i in range (n, 0, -1): #n, n-1, ...1
            self.learn_value (boards[i-1], boards[i])

    #play a game (after having learnt)
    #return who won the game
    def play (self, naive_adversary = True):
        #start a fresh game
        board = self.get_start_board ()
        #the player could make a move
        can_play = True
        #who won the game?
        winner = None
        
        #while there are more moves
        while (can_play):
            #X plays
            #we are greedy
            board, can_play = self.play_a_greedy_move (board, 'X')
            #break if no more moves possible
            if can_play == False:
                break
            #break if won
            winner = self.get_winner (board)
            if winner != None:
                break
                
            #O plays
            #if adversary is naive
            if naive_adversary:
                board, can_play = self.play_a_random_move (board, 'O')
            #if adversary is greedy
            else:
                board, can_play = self.play_a_greedy_move (board, 'O')
            #break if no more moves possible
            if can_play == False:
                break
            #break if won
            winner = self.get_winner (board)
            if winner != None:
                break
        
        #return who won the game
        return winner
    
    #play a game (while learning)
    #play while exploring yes/no
    #play against a naive or a greedy advisory
    #TODO: with a separate play() defined,
    # we now do not need the 'explore' flag
    def play_a_stride (self, explore = True, naive_adversary = True):
        #start a fresh game
        board = self.get_start_board ()
        
        #list of boards (states) in the stripe
        stripe_states = []
        
        #the player could make a move
        can_play = True
        
        #while there are more moves
        while (can_play):

            #X plays

            #if we are exploring and exploiting
            if explore:
                board, can_play =                 self.play_an_explore_exploit_move (board, 'X')
            #if we are greedy
            else:
                board, can_play = self.play_a_greedy_move (board, 'X')
                
            #save a copy of the board (state) after making the move
            stripe_states.append (board.copy ())
            
            #break if no more moves possible
            if can_play == False:
                break
            #break if won
            if self.get_winner (board) != None:
                break
                
            #O plays
            
            #if adversary is naive
            if naive_adversary:
                board, can_play = self.play_a_random_move (board, 'O')
            #if adversary is greedy
            else:
                board, can_play = self.play_a_greedy_move (board, 'O')
            
            #save a copy of the board (state) after making the move
            stripe_states.append (board.copy ())
            #break if no more moves possible
            if can_play == False:
                break
            #break if won
            if self.get_winner (board) != None:
                break
                
        #backpropagate the learning
        self.backpropagate_values (stripe_states)
    
    #learn by playing n number of strides
    # (exploratory 'X' and naive 'O')
    def learn (self, num_strides):
        for i in range (num_strides):
            self.play_a_stride ()
            


# In[33]:


#test learn() (exploratory 'X' and naive 'O')
ttt = TicTacToe ()
ttt.learn (10)
#print states with (value_cutoff, num_moves cutoff)
ttt.print_value_function (2, 5)


# In[36]:


#test play() (greedy 'X' and naive 'O')
#ttt = TicTacToe () #use ttt instance with the learnt value function
for i in range (25): 
    print (ttt.play (), ' won!!')


# In[49]:


#test play() (greedy 'X' and greedy 'O')
#ttt = TicTacToe () #use ttt instance with the learnt value function
for i in range (25):
    print (ttt.play (True), ' won!!')


# In[ ]:


#test play_a_stride for exploratory 'X' and naive 'O'
ttt = TicTacToe ()
ttt.play_a_stride ()
ttt.print_value_function ()


# In[ ]:


#test play_a_stride for exploratory 'X' and greedy 'O'
ttt = TicTacToe ()
ttt.play_a_stride (True, False)
ttt.print_value_function ()


# In[ ]:


#test play_a_stride for greedy 'X' and naive 'O'
ttt = TicTacToe ()
ttt.play_a_stride (False, True)
ttt.print_value_function ()


# In[ ]:


#test play_a_stride for greedy 'X' and greedy 'O'
ttt = TicTacToe ()
ttt.play_a_stride (False, False)
ttt.print_value_function ()


# In[ ]:


#test get_winner
ttt = TicTacToe ()
board = ttt.get_start_board()
board [0] = board [4] = board [8] = 'X'
print (ttt.get_winner (board)) #X


# In[ ]:


#test get_value
ttt = TicTacToe ()
board = ttt.get_start_board()
board [0] = board [4] = board [8] = 'X'
print (ttt.get_value (board)) #1.0
board [8] = None
print (ttt.get_value (board)) #0.5


# In[ ]:


#test play_a_random_move
ttt = TicTacToe ()
board = ttt.get_start_board()
print (ttt.play_a_random_move (board, 'O')) #board [...O...], True
print (ttt.play_a_random_move (board, 'X')) #board [...O...X...], True
board = ['O'] * 9
print (ttt.play_a_random_move (board, 'X')) #board [O...O], False


# In[ ]:


#test get_next_greedy_state
ttt = TicTacToe ()
board = ttt.get_start_board()
next_board, value = ttt.get_next_greedy_state (board, 'X')
print (next_board, value) #board [X..], 0.5
next_board, value = ttt.get_next_greedy_state (next_board, 'X')
print (next_board, value) #board [X X...], 0.5


# In[ ]:


#test play_a_greedy_move
ttt = TicTacToe ()
board = ttt.get_start_board()
next_board, value = ttt.play_a_greedy_move (board, 'X')
print (next_board, value) #board [X...], True
next_board, value = ttt.play_a_greedy_move (next_board, 'X')
print (next_board, value) #board [X X...], True


# In[ ]:


#test play_an_explore_exploit_move
ttt = TicTacToe ()
board = ttt.get_start_board()
next_board, value = ttt.play_an_explore_exploit_move (board, 'X')
print (next_board, value) #board [X...], True
next_board, value = ttt.play_an_explore_exploit_move (next_board, 'X')
print (next_board, value) #board [X X...], True
ttt.explore_exploit = 0.7
next_board, value = ttt.play_an_explore_exploit_move (next_board, 'X')
print (next_board, value) #board [X X...X...], True
next_board, value = ttt.play_an_explore_exploit_move (next_board, 'X')
print (next_board, value) #board [X X...X...X...], True


# In[ ]:


#test learn_value
ttt = TicTacToe ()

board_this = ttt.get_start_board() #the first 'key' in value_function
board_next = ttt.get_start_board()
board_next [0] = board_next [4] = board_next [8] = 'X'
ttt.learn_value (board_this, board_next)
print (ttt.value_function) #[0.51]

board_this = ttt.get_start_board()
board_this [0] = 'X' #just to have another 'key' in value_function
board_next = ttt.get_start_board()
board_next [0] = board_next [4] = board_next [8] = 'O'
ttt.learn_value (board_this, board_next)
ttt.print_value_function () #[0.51, 0.5]


# In[ ]:


#test backpropagate_values for 'X' win
ttt = TicTacToe ()
board = ttt.get_start_board()

#winning stripe of 'X'
#first column of 3 'X's [0,3,6],
# second column has 2 'O's [1,4]
stripe_moves = [(0, 'X'), (1, 'O'), (3, 'X'), (4, 'O'), (6, 'X')]

#list of boards (states) in the stripe
stripe_states = []

for i, mark in stripe_moves:
    #make a move
    board [i] = mark
    #save a copy of the board (state) after making the move
    stripe_states.append (board.copy ())
    
ttt.backpropagate_values (stripe_states)
ttt.print_value_function ()# [0.51, 0.5051, 0.505051, 0.50505051]


# In[ ]:


#test backpropagate_values for 'O' win
ttt = TicTacToe ()
board = ttt.get_start_board()

#winning stripe of 'O'
#first column of 3 'O's [0,3,6],
# second column has 2 'X's [1,4]
stripe_moves = [(0, 'O'), (1, 'X'), (3, 'O'), (4, 'X'), (6, 'O')]

#list of boards (states) in the stripe
stripe_states = []

for i, mark in stripe_moves:
    #make a move
    board [i] = mark
    #save a copy of the board (state) after making the move
    stripe_states.append (board.copy ())
    
ttt.backpropagate_values (stripe_states)
ttt.print_value_function ()# [0.5, 0.505, 0.50505, 0.5050505]

