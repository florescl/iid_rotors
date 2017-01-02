# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict

dim = 5
n_iters = 100
k = 150


def __MAIN__():

    print '#n_iters_item, n_sites_visited, n_iters_item/math.log(n_iters_item), pow(n_iters_item,0.667), n_excursions'

    rotor_matrix = [[[0 for z in xrange(-dim, dim)] for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]

    visited_matrix = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    print 'initializing mat'
    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    print 'done initializing'
    print(rotor_matrix)
    
    particle_x = 0
    particle_y = 0
    particle_z = 0
    
    n_iters_try = 0
    n_excursions = 0
    
    n_successive_visits = 0    
    n_sites_visited = 0

    
    while n_iters_try < n_iters:
            #update rotor move particle
        
        rotor_matrix[particle_x][particle_y][particle_z] = update_rotor_matrix(rotor_matrix, particle_x, particle_y, particle_z)
        print 'rotor', rotor_matrix[particle_x][particle_y][particle_z]

        particle_x, particle_y, particle_z = update_particle_position(rotor_matrix, particle_x, particle_y, particle_z)
     
        visited_matrix[particle_x][particle_y][particle_z]+=1
        print n_iters_try, particle_x, particle_y, particle_z
        
        if(visited_matrix[particle_x][particle_y][particle_z] == 1):
            n_sites_visited+=1

        if particle_x==0 and particle_y==0 and particle_z==0:
            n_successive_visits+=1
             
            if n_succesive_visits==6:
                n_excursions+=1
                n_successive_visits=0

        n_iters_try+=1
                        
        print n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.75), n_excursions
            
def isPower (num, base):
    if base == 1 and num != 1: return False
    if base == 1 and num == 1: return True
    if base == 0 and num != 1: return False
    power = int (math.log (num, base) + 0.5)
    return base ** power == num

def is_power2(num):

	'states if a number is a power of two'

        if (num != 0 and ((num & (num - 1)) == 0) ==True):
            return 1
        else:
            return 0


def update_particle_position(rotor_matrix, particle_x, particle_y, particle_z):
    #east
      if rotor_matrix[particle_x][particle_y][particle_z] == 0:
          particle_z+=1

      else:
          if rotor_matrix[particle_x][particle_y][particle_z] ==1:
              particle_y+=1
              
          else:
              if rotor_matrix[particle_x][particle_y][particle_z] == 2:
                  particle_x+=1
                  
              else:
                  if rotor_matrix[particle_x][particle_y][particle_z] ==3:
                      particle_z-=1
                      
                  else:
                      if rotor_matrix[particle_x][particle_y][particle_z] ==4:
                          particle_y-=1
                          
                      else:
                          if rotor_matrix[particle_x][particle_y][particle_z]==5:
                              particle_x-=1

      return particle_x, particle_y, particle_z


def update_rotor_matrix(rotor_matrix,x,y,z):
      
  rotor_matrix[x][y][z] = ((rotor_matrix[x][y][z]+1)% 6)
  return rotor_matrix[x][y][z]

def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
            for z_ind in range(-dim,dim):
                rotor_matrix[x_ind][y_ind][z_ind] = randrange(0,5)
            
    return rotor_matrix



if __name__ == '__main__':
  __MAIN__()
