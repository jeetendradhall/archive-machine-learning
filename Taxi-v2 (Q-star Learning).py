#!/usr/bin/env python
# coding: utf-8

# In[47]:


#imports
import numpy as np
import gym
import random
from IPython.core.debugger import set_trace


# In[48]:


#gym environment
env = gym.make ("Taxi-v2")
env.render ()

#state and action dimensions, and Q-Table
#action
action_size = env.action_space.n
print ('Action Size:', action_size)
#state
state_size = env.observation_space.n
print ('State Size:', state_size)
#Q-Table
qtable = np.zeros ((state_size, action_size))
print (qtable)


# In[49]:


#hyperparameters
total_episodes = 50000
total_test_episodes = 100
max_steps = 99

learning_rate = 0.7
gamma = 0.618 #discounting rate

#exploration parameters
epsilon = 1.0
max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.01 #exponential decay rate for exploration


# In[50]:


# List of rewards
#rewards = []

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
        
        #total_rewards += reward
        
        #has the passenger reached destination?
        if done:
            break
            
        #print(qtable[state])
    
    #reduce exploration with increasing episodes
    epsilon = min_epsilon + (max_epsilon - min_epsilon)    * np.exp (-decay_rate * episode)
    
#print ("Score over time: " +  str(sum(rewards)/total_episodes))
print(qtable)


# In[59]:


env.reset ()
rewards = [] #list of rewards in episodes
for episode in range (total_test_episodes):
    state = env.reset () #begin the episode with a fresh state
    done = False
    step = 0 #how many steps completed in this iteration
    total_rewards = 0 #rewards collected in this episode
    for step in range (max_steps):
        action = np.argmax(qtable [state, :]) #greedy action
        #take the action
        new_state, reward, done, info = env.step (action)
        #accumulate the reward
        total_rewards += reward
        #has the passenger reached destination?
        if done:
            rewards.append (total_rewards)
            break #move to the next episode
        #if passenger hasn't reached destination
        # move to the next state
        state = new_state
env.close ()
print ('average rewards', str(sum(rewards)/total_test_episodes))


# In[ ]:




