# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 19:32:34 2021

@author: ann_1
"""

import numpy as np
import networkx as nx

global n_city #Number of city
global n_road #Number of road
global city_x
global city_y

#fn: Input detail of Number of city, Number of road, city_x, city_y
def input_data():
    detail = input("")
    global n_city
    global n_road
    global city_x
    global city_y
    n_city = int(detail.split(" ")[0])
    n_road = int(detail.split(" ")[1])
    city_x = int(detail.split(" ")[2])
    city_y = int(detail.split(" ")[3])
    
    if n_road > 0:
        matrix_t = np.zeros((n_city+1, n_city+1)) #time t
        matrix_k = np.zeros((n_city+1, n_city+1)) #time k
        
        for i in range(0,n_road):
            railroad = input("")
            matrix_t[int(railroad.split(" ")[0])][int(railroad.split(" ")[1])] = int(railroad.split(" ")[2])
            matrix_t[int(railroad.split(" ")[1])][int(railroad.split(" ")[0])] = int(railroad.split(" ")[2])
            matrix_k[int(railroad.split(" ")[0])][int(railroad.split(" ")[1])] = int(railroad.split(" ")[3])
            matrix_k[int(railroad.split(" ")[1])][int(railroad.split(" ")[0])] = int(railroad.split(" ")[3])
        
        return matrix_t, matrix_k
    else:
        return -1
#fn: Check connected gragh or not?    
def connected_graph(matrix_t):
    
    temp_m = np.delete(matrix_t, (0), axis=0)
    temp_m = np.delete(temp_m, (0), axis=1)
    temp_m = nx.from_numpy_matrix(temp_m)
    return nx.is_connected(temp_m)
    
#fn: find earliest time
def earliest(matrix_t, matrix_k):
    
    d_min = [10**9] * (n_city + 1) # time from city_startpoint to city...
    d_mark = [0] * (n_city + 1) # mark visited  
    d_min[0] = 0
    d_mark[0] = 1
    
    i_transfer = 0 # number of times (transfer)
    previous_point = city_x # previous visited city
    start_point = city_x # start point (from city ... to city...)
    d_min[start_point] = 0 # start at time 0
    d_mark[start_point] = 1 # start point (visited)
     
    while(1):
        i_transfer = i_transfer + 1 # number of times (transfering from A to B)
        temp_d = 10**9 # time for checking all neighbor (to finding the earliest time)
        temp_mark = start_point # neighbor city that is earliest time
        
        #visit the all neighbor city
        possible_r = np.where(matrix_t[start_point] != 0)[0] # list of possible neighbor to reach Ex.[a, b, ...]
        possible_r = np.delete(possible_r, np.where(possible_r == previous_point))
            
        for i in range(0,len(possible_r)):
            city_visit = possible_r[i] 
            
            if i_transfer == 1: #first transfer 
                
                #calculate the time (time for transfering) 
                d = matrix_t[start_point][city_visit]
                
                if d_min[city_visit] > d:
                    d_min[city_visit] = d
                    #d_mark[city_visit] = 1
            
            else: #more than 1 transfer
                #calculate the time (time for transfering)
                if d_min[start_point]%matrix_k[start_point][city_visit] == 0: # (d_min%k)+ t
                    d = (d_min[start_point]%matrix_k[start_point][city_visit]) + matrix_t[start_point][city_visit]
                    d = d + d_min[start_point]
                else: # (k-(d_min%k)) + t
                    d = (matrix_k[start_point][city_visit] - (d_min[start_point]%matrix_k[start_point][city_visit])) + matrix_t[start_point][city_visit]
                    d = d + d_min[start_point]                  
                    
                # update earliest time
                if d_min[city_visit] > d:
                    d_min[city_visit] = d

                elif (d_min[city_visit] < d) & (d_mark[city_visit] == 0):
                    d = d_min[city_visit]
                    
            if temp_d > d:
                temp_d = d
                temp_mark = city_visit
        
        # update city 
        d_mark[temp_mark] = 1 # mark city to visited 
        previous_point = start_point
        start_point = temp_mark
        
        # all() >>> d_mark: all-nonzero > True
        # all() >>> d_mark: all-somezero > False
        if all(d_mark) & (d_min[city_y] != [10**9]):
            #print("d_mark: ", d_mark)
            return d_min
        
try:
    matrix_t, matrix_k = input_data() # input data
    if connected_graph(matrix_t): # check graph
        d_min = earliest(matrix_t, matrix_k) # find earliest time
        #print(d_min)
        print(int(d_min[city_y]))
    else:
        print("-1")

except:
    print("-1")
    
#print(earliest(matrix_t, matrix_k, city_x, city_y, n_city))
