#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import gym
import random
from IPython.core.debugger import set_trace


# In[2]:


env = gym.make ('FrozenLake-v0')
env.render ()
action_size = env.action_space.n
state_size = env.observation_space.n
print ('Action Size:', action_size, ' State Size:', state_size)


# In[3]:


qtable = np.zeros ((state_size, action_size))
#print (qtable[0:5])


# In[4]:


#hyperparameters
total_episodes = 50000
#total_test_episodes = 100
max_steps = 99

learning_rate = 0.8
gamma = 0.95 #discounting rate

#exploration parameters
epsilon = 1.0
max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.005 #exponential decay rate for exploration


# In[5]:


# List of rewards
rewards = []

#play episodes
for episode in range (total_episodes):
    #start state
    state = env.reset ()
    total_rewards = 0
    
    #has the passenger reached destination?
    done = False
    
    #iterate upto maximum steps in an episode
    for step in range (max_steps):
        
        #set_trace ()
        
        #explore or exploit
        exp_exp_tradeoff = random.uniform (0, 1)
        #if we exploit
        if exp_exp_tradeoff > epsilon:
            action = np.argmax (qtable [state, :])
        #else, we explore by randomly sampling the action space
        else:
            action = env.action_space.sample ()
            
        #take the action, and observe the outcome state and reward
        new_state, reward, done, info = env.step (action)
        
        #update the Q-Table
        qtable [state, action] = qtable [state, action] +        learning_rate * (reward + gamma*np.max(qtable[new_state, :])                         - qtable [state, action])
        
        #move to the next state
        state = new_state
        
        total_rewards += reward
        
        #has the passenger reached destination?
        if done:
            break
            
        #print(qtable[state])
    
    #reduce exploration with increasing episodes
    epsilon = min_epsilon + (max_epsilon - min_epsilon)    * np.exp (-decay_rate * episode)
    
    #record rewards for this episode
    rewards.append (total_rewards)
    
print ("Score over time: " +  str(sum(rewards)/total_episodes))
print(qtable)


# In[6]:


env.reset()

for episode in range(10):
    state = env.reset()
    step = 0
    done = False
    print("****************************************************")
    print("EPISODE ", episode)

    for step in range(max_steps):
        
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(qtable[state,:])
        
        new_state, reward, done, info = env.step(action)
        
        if done:
            # Here, we decide to only print the last state (to see if our agent is on the goal or fall into an hole)
            env.render()
            
            # We print the number of step it took.
            print("Number of steps", step)
            break
        state = new_state
env.close()


# In[ ]:




