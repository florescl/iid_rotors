# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict

dim = 1000
n_iters = 10000000
k = 150


def __MAIN__():

    print '#n_iters_item, n_sites_visited, n_iters_item/math.log(n_iters_item), pow(n_iters_item,0.667), n_excursions'

    rotor_matrix = [[0 for y in range(-dim, dim)] for x in range(-dim,dim)]
    print len(rotor_matrix)
    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,100)]

    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    print 'initializing mat'
    
    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    print 'done initializing'
    #print(rotor_matrix)
    
    particle_x = 0
    particle_y = 0
    particle_z = 0
    
    n_iters_try = 0
    n_excursions = 0
    
    n_successive_visits = 0    
    n_sites_visited = 0

    with open('triangle.csv','wb') as csvfile:
        while n_iters_try < n_iters:
            #update rotor move particle
        
            rotor_matrix[particle_x][particle_y] = update_rotor_matrix(rotor_matrix, particle_x, particle_y)
            u_func[n_excursions][particle_x][particle_y]+=1
            particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)
     
            visited_matrix[particle_x][particle_y]+=1
        
            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1
                
            if particle_x==0 and particle_y==0:
                n_successive_visits+=1
             
                if n_successive_visits==6:
                    print n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions
                #draw_pic(u_func,n_excursions)
                    n_excursions+=1
                    n_successive_visits=0

            n_iters_try+=1
            #print n_iters_try, particle_x, particle_y
            if particle_x == 0  and particle_y == 0:
                print 'origin'
                
            if n_iters_try % 100000==0:

                cw = csv.writer(csvfile, dialect='excel')
                cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))])
                check_u_func(u_func,n_excursions)
                
def check_u_func(u_func, n_excursions):
    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            if u_func[n_excursions][x][y] > 6:
                print 'not ok'


def draw_pic(u_func,n_excursions):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("triangle" + str(n_excursions) + ".png")

            
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


def update_particle_position(rotor_matrix, particle_x, particle_y):
    #east
      if rotor_matrix[particle_x][particle_y]== 0:
          particle_y+=1

      else:
          if rotor_matrix[particle_x][particle_y] ==1:
              particle_x-=1
          else:
              if rotor_matrix[particle_x][particle_y] == 2:
                  particle_x-=1
                  particle_y-=1
                  
              else:
                  if rotor_matrix[particle_x][particle_y] ==3:
                      particle_y-=1
                      
                  else:
                      if rotor_matrix[particle_x][particle_y] ==4:
                          particle_x+=1
                          
                      else:
                          if rotor_matrix[particle_x][particle_y]==5:
                              particle_x+=1
                              particle_y+=1

      return particle_x, particle_y


def update_rotor_matrix(rotor_matrix,x,y):
      
  rotor_matrix[x][y] = ((rotor_matrix[x][y]+1)% 6)
  return rotor_matrix[x][y]

def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
            rotor_matrix[x_ind][y_ind] = randrange(0,6)
            
    return rotor_matrix



if __name__ == '__main__':
  __MAIN__()
