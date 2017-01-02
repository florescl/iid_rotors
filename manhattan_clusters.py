# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict

dim = 50
n_iters = 100000
k = 150


def __MAIN__():

    print '#n_iters_item, n_sites_visited, pow(n_iters_item,0.667), n_excursions, n_excursions, math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))'

    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]
    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,300)]

    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    
    print 'initializing mat'
    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    print 'done initializing'
    #print(rotor_matrix)
    
    particle_x = site_x
    particle_y = site_y
    
    n_iters_try = 0
    n_excursions = 0
    
    n_successive_visits = 0    
    n_sites_visited = 0

    with open('manhattan.csv','wb') as csvfile:

        while n_successive_visits <2:

            rotor_matrix[particle_x][particle_y] = update_rotor_matrix(rotor_matrix, particle_x, particle_y)
            #print 'rotor', rotor_matrix[particle_x][particle_y]
            particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)
            #print 'pos', particle_x, particle_y
            visited_matrix[particle_x][particle_y]+=1
            
            u_func[n_excursions][particle_x][particle_y]+=1

        
            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1
                
            if particle_x==0 and particle_y==0:
                n_successive_visits+=1
             
          

            n_iters_try+=1

            if n_iters_try % 1000000==0:
                print n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))
            
                cw = csv.writer(csvfile, dialect='excel')
                cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))])

def update_particle_position(rotor_matrix,particle_x, particle_y):

    #odd col odd row
    if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 1) and (particle_y %2 ==1)):
          particle_x = particle_x-1
          particle_y = particle_y
          
    else:
        if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 1) and (particle_y %2 ==1)):
          particle_y = particle_y+1
          particle_x = particle_x
          
        else:
            #even col even row
            if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 0) and (particle_y %2 ==0)):
                particle_y = particle_y-1
                particle_x = particle_x
                
            else:
                 if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 0) and (particle_y %2 ==0)):
                     particle_x = particle_x+1
                     particle_y = particle_y

                 else:
                     #odd row even col
                     if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 0) and (particle_y %2 ==1)):
                         particle_x= particle_x-1
                         particle_y = particle_y
                         
                     else:
                         if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 0) and (particle_y %2 ==1)):
                             particle_y = particle_y-1
                             particle_x = particle_x

                         else:
                             #even row odd col
                             if  rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 1) and (particle_y %2 ==0)):
                                 particle_x = particle_x
                                 particle_y = particle_y+1
                                
                             else:
                                 if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 1) and (particle_y %2 ==0)):
                                     particle_y=particle_y
                                     particle_x = particle_x+1

        
                
    return particle_x, particle_y

#def move_particle_visbef(prev_particle_x, prev_particle_y, rotor_matrix):

def draw_pic(u_func,n_excursions):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):                
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("manh" + str(n_excursions) + ".png")
    
            
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


def percolation_cluster(rotor_matrix, site_x, site_y)
    #do rotor walk starting from the site
    #and set a function to be 1 if a site has been visited 4 times and 0 otherwise
    # plot accordingly

    
    


'''
def update_particle_position(rotor_matrix, particle_x, particle_y):
    #depending on the type of line and column and the rotor

      if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 1) and (particle_y %2 ==1)):
          particle_x+=1

      else:
          if rotor_matrix[particle_x][particle_y] ==0 and ((particle_x % 2 == 1) and (particle_y %2 ==1)):
              particle_y+=1
              
          else:
              if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 1) and (particle_y %2 ==0)):
                  particle_x+=1
              else:
                  if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 1) and (particle_y %2 ==0)):
                      particle_y-=1
  
                  else:
                      if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 0) and (particle_y %2 ==1)):
                          particle_y+=1
                      else:
                          if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 0) and (particle_y %2 ==1)):
                              particle_x-=1

                          else:
                              if rotor_matrix[particle_x][particle_y] == 1 and ((particle_x % 2 == 0) and (particle_y %2 ==0)):
                                  particle_y-=1
                              else:
                                  if rotor_matrix[particle_x][particle_y] == 0 and ((particle_x % 2 == 0) and (particle_y %2 ==0)):
                                      particle_x-=1
                          
                          
                          
                      
      return particle_x, particle_y
'''

def update_rotor_matrix(rotor_matrix,x,y):
      
  rotor_matrix[x][y] = ((rotor_matrix[x][y]+1)%2)
  return rotor_matrix[x][y]

def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
          rotor_matrix[x_ind][y_ind] = randrange(0,2)
            
    return rotor_matrix



if __name__ == '__main__':
  __MAIN__()
