# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict
#import Image

dim = 100
n_iters = 15000
k = 150


def __MAIN__():

    print '#n_iters_item, n_sites_visited, pow(n_iters_item,0.667), n_excursions, n_excursions, math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))'

    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]

    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    global_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,10)]
     
    print 'initializing mat'
    rotor_matrix = ust_matrix(rotor_matrix)

    '''
    for i in range(-dim,dim):
        for j in range(-dim,dim):
            print 'doing', i, j
            rotor_matrix, global_matrix = ust_matrix(rotor_matrix, i,j,global_matrix)
            #print(global_matrix)
            #add_sites_to_global_matrix
    '''
    
    print 'done initializing'
    f = open('ust.tex','w')
    #print(rotor_matrix)
    
    latex_export_ust(f,rotor_matrix)
    
    particle_x = 0
    particle_y = 0
    particle_z = 0
    
    n_iters_try = 0
    n_excursions = 0
    
    n_succesive_visits = 0    
    n_sites_visited = 0

    with open('ust.csv','wb') as csvfile:
        
        while n_iters_try < n_iters:
            #update rotor move particle
        
            rotor_matrix[particle_x][particle_y] = update_rotor_matrix(rotor_matrix, particle_x, particle_y)

            #print rotor_matrix[particle_x][particle_y]
            
            particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)
            #print particle_x, particle_y
            visited_matrix[particle_x][particle_y]+=1
            u_func[n_excursions][particle_x][particle_y]+=1

            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1

            if particle_x==0 and particle_y==0:
                n_succesive_visits+=1
             
            if n_succesive_visits==4:
                n_excursions+=1
                n_successive_visits=0

            n_iters_try+=1

            if n_iters_try % 100==0:
                print n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))
                #draw_pic(u_func,n_excursions,n_iters_try)
                #cw = csv.writer(csvfile, dialect='excel')
                #cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))])


def draw_pic(u_func,n_excursions,n_iters_try):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("ust" + str(n_iters_try) + ".png")
            
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
      if rotor_matrix[particle_x][particle_y] == 0:
          particle_y+=1
      else:
          if rotor_matrix[particle_x][particle_y] ==1:
              particle_x-=1
          else:
              if rotor_matrix[particle_x][particle_y] == 2:
                  particle_y-=1
              else:
                  if rotor_matrix[particle_x][particle_y] ==3:
                      particle_x+=1

      return particle_x, particle_y


def update_rotor_matrix(rotor_matrix,x,y):
      
  rotor_matrix[x][y] = ((rotor_matrix[x][y]+1)%4)
  return rotor_matrix[x][y]


def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
          rotor_matrix[x_ind][y_ind] = randrange(0,2)
            
    return rotor_matrix

def ust_matrix(rotor_matrix, site_x, site_y, global_matrix):
    #wilson's algorithm:

    #then set the rotors as the direction of random walk

    
    this_mat = [[0 for x in xrange(-dim,dim)] for y in xrange(-dim,dim)]
    
    #start random walk at site

    particle_x,particle_y = site_x, site_y
    global_matrix[particle_x][particle_y] = 1
    stack_sites_x = [0 for x in range(0,2*dim)]
    stack_sites_y = [0 for x in range(0,2*dim)]
    
    stack_sites_x[0] = site_x
    stack_sites_y[0] = site_y

    i=1
    #either reach the boundary or another path
    
    while particle_x!=dim or particle_y!=dim or particle_x!=-dim or particle_y!=-dim or global_matrix[particle_x][particle_y] ==0:
        print 'i', i
        rotor_matrix[particle_x][particle_y] = randrange(0,4)
        print 'rotor', rotor_matrix[particle_x][particle_y]
        
        while check_self_loop(rotor_matrix, particle_x, particle_y)==1:
            print 'try again'
            rotor_matrix[particle_x][particle_y] = randrange(0,4)
            #print '
        
        particle_x,particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)
        print 'loc', particle_x, particle_y
        stack_sites_x[i] = particle_x
        stack_sites_y[i] = particle_y

        if this_mat[particle_x][particle_y] == 1:
            prev = find_prev_xy(particle_x,particle_y, stack_sites_x, stack_sites_y)
            
            for ind in range(prev, i):
                rotor_matrix[stack_sites_x[ind]][stack_sites_y[ind]] = 0
                this_mat[stack_sites_x[ind]][stack_sites_y[ind]] = 0

        else:
            this_mat[particle_x][particle_y] =1
            i+=1

        #this adds the path found to the global matrix
        global_matrix = add_stuff_to_global_matrix(global_matrix, stack_sites_x, stack_sites_y)
        
    return rotor_matrix, global_matrix
    # if visited again, then remove the rotors at the previously visited sites
    
    #now i have from the origin to

def check_self_loop(rotor_matrix, particle_x, particle_y):
    ok = 0
    if rotor_matrix[particle_x][particle_y] == 0 and rotor_matrix[particle_x][particle_y+1] == 2:
        ok == 1
    else:
        if rotor_matrix[particle_x][particle_y] == 1 and rotor_matrix[particle_x-1][particle_y] == 3:
            ok == 1
        else:
            if rotor_matrix[particle_x][particle_y] == 2 and rotor_matrix[particle_x][particle_y-1] == 0:
                ok == 1
            else:
                if rotor_matrix[particle_x][particle_y] == 3 and rotor_matrix[particle_x+1][particle_y] == 1:
                    ok == 1

    return ok

def latex_export_ust(f1, rotor_matrix):

    for i_ind in range(-dim,dim):
        for j_ind in range(-dim,dim):
            f1.write(r'\node[reddot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
            f1.write('\n')
            
            if rotor_matrix[i_ind][j_ind] == 0:
                f1.write(r'\draw[color=black] (' + str(i_ind) + ',' + str(j_ind) + ') -- (' + str(i_ind) + ',' + str(j_ind+1) +');')
                f1.write('\n')

            else:
                if rotor_matrix[i_ind][j_ind] == 1:
                    f1.write(r'\draw[color=black] (' + str(i_ind) + ',' + str(j_ind) + ') -- (' + str(i_ind-1) + ',' + str(j_ind) + ');')
                    f1.write('\n')

                else:
                    if rotor_matrix[i_ind][j_ind] == 2:
                        f1.write(r'\draw[color=black] (' + str(i_ind) + ',' + str(j_ind) + ') -- (' + str(i_ind) + ',' + str(j_ind-1) + ');')
                        f1.write('\n')

                    else:
                        if rotor_matrix[i_ind][j_ind] == 3:
                            f1.write(r'\draw[color=black] (' + str(i_ind) + ',' + str(j_ind) + ') -- (' + str(i_ind+1) + ',' + str(j_ind) + ');')
                            f1.write('\n')



def ust_matrix(rotor_matrix):
    

