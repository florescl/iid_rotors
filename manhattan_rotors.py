# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict

dim = 10
n_iters = 20
k = 10


def __MAIN__():

    print '#n_iters_item, n_sites_visited, pow(n_iters_item,0.667), n_excursions, n_excursions, math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0))'

    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]
    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,300)]
    mirror_matrix = [[0 for y in range(-dim,dim)] for x in xrange(-dim,dim)]

    mirror_matrix = assign_probabilities(mirror_matrix)
    
    #print mirror_matrix
    
    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    
    f2 = open('initial_mirrors_manh.tex','w')

    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    
    initial_mirrors(f2, mirror_matrix)
    
    particle_x = 0
    particle_y = 0

    visited_matrix[0][0] =1
    prev_particle_x = 0
    prev_particle_y = 0

    prev_prev_particle_x = 0
    prev_prev_particle_y = 0
    
    n_iters_try = 0
    n_excursions = 0
    
    f1 = open('mirror_manh'+str(n_excursions) + '.tex','w')
        
    n_successive_visits = 0    
    n_sites_visited = 0
    n_bdry = 0

    with open('manhattan.csv','wb') as csvfile:
        
        while n_iters_try < n_iters:
            print 'rotor', rotor_matrix[prev_particle_x][prev_particle_y], mirror_matrix[prev_particle_x][prev_particle_y], visited_matrix[prev_particle_x][prev_particle_y]
            
            if visited_matrix[prev_particle_x][prev_particle_y] == 1:
                print 'not seen'
                particle_x, particle_y = update_pp_first(rotor_matrix, particle_x, particle_y, prev_particle_x, prev_particle_y, mirror_matrix,prev_prev_particle_x, prev_prev_particle_y)
                set_rotor(rotor_matrix,particle_x,particle_y, prev_particle_x, prev_particle_y)
                #depending on where it went, set rotor
                
            else:
                print 'seen before'
                particle_x, particle_y = update_particle_position(rotor_matrix,particle_x, particle_y, prev_particle_x,prev_particle_y)

            print 'loc', particle_x, particle_y, prev_particle_x, prev_particle_y, prev_prev_particle_x, prev_prev_particle_y

            add_mirror(f1, f2, rotor_matrix,particle_x, prev_particle_x, particle_y, prev_particle_y)

            rotor_matrix[prev_particle_x][prev_particle_y] = update_rotor_matrix(rotor_matrix, prev_particle_x, prev_particle_y)

            prev_prev_particle_x = prev_particle_x
            prev_prev_particle_y = prev_particle_y

            visited_matrix[particle_x][particle_y]+=1


            prev_particle_x = particle_x
            prev_particle_y = particle_y
          
            u_func[n_excursions][particle_x][particle_y]+=1

            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1

            if particle_x > dim or particle_x < -dim or particle_y> dim or particle_y < -dim:
                break
            
            if particle_x==0 and particle_y==0:
                n_successive_visits+=1
             
                if n_successive_visits==2:
                    n_excursions+=1
                    n_successive_visits=0

            n_iters_try+=1
            if n_iters_try % 1000==0:
                print n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0)), particle_x, particle_y
            
                cw = csv.writer(csvfile, dialect='excel')
                cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0)), math.log(n_sites_visited)])

def set_rotor(rotor_matrix,particle_x,particle_y, prev_particle_x, prev_particle_y):
    if prev_particle_y %2 == 0 and prev_particle_x %2 == 0 and particle_x - prev_particle_x == 1:
        rotor_matrix[prev_particle_x][prev_particle_y] = 0
    else:
        if prev_particle_y %2 == 0 and prev_particle_x %2 == 0 and particle_y - prev_particle_y == -1:
            rotor_matrix[prev_particle_x][prev_particle_y] =1
        else:
            if prev_particle_x % 2==0 and prev_particle_x %2==1 and particle_x - prev_particle_x == 1:
                rotor_matrix[prev_particle_x][prev_particle_y] = 0
            else:
                if prev_particle_y % 2==0 and prev_particle_x %2==1 and particle_y - prev_particle_y == 1:
                    rotor_matrix[prev_particle_x][prev_particle_y] = 1
                else:
                    if prev_particle_y % 2==1 and prev_particle_x %2==0 and particle_x - prev_particle_x == -1:
                        rotor_matrix[prev_particle_x][prev_particle_y] = 0
                    else:
                         if prev_particle_y % 2==1 and prev_particle_x %2==0 and particle_y - prev_particle_y == -1:
                             rotor_matrix[prev_particle_x][prev_particle_y] = 1
                         else:
                             if prev_particle_y % 2==1 and prev_particle_x %2==1 and particle_x - prev_particle_x == -1:
                                 rotor_matrix[prev_particle_x][prev_particle_y] = 0
                             else:
                                 if prev_particle_y % 2==1 and prev_particle_x %2==1 and particle_y - prev_particle_y == 1:
                                     rotor_matrix[prev_particle_x][prev_particle_y] = 1
                                            
        

def initial_mirrors(f2, mirror_matrix):

    
    for a in xrange(-k,k):
        for b in xrange(-k,k):
            
            if ((a+b) % 2 == 1) and math.fabs(mirror_matrix[a][b]) >0:
                f2.write(r'\draw[color=black] (' + str(a+0.5) + ',' + str(b+0.5) + ') -- (' + str(a-0.5) + ',' + str(b-0.5) +');')
                f2.write('\n')

            else:
                if ((a+b) % 2 == 0) and math.fabs(mirror_matrix[a][b]) >0:
                  f2.write(r'\draw[color=black] (' + str(a-0.5) + ',' + str(b+0.5) + ') -- (' + str(a+0.5) + ',' + str(b - 0.5) +');')
                  f2.write('\n')
                else:
                    continue
                                      
def add_mirror(f1, f2, rotor_matrix, particle_x, prev_particle_x, particle_y, prev_particle_y):


    f2.write(r'\draw[color=green] (' + str(prev_particle_x) + ',' + str(prev_particle_y) + ') {} -- (' + str(particle_x) + ',' + str(particle_y) +') {}[->];')

   
def update_particle_position(rotor_matrix,particle_x, particle_y, prev_particle_x,prev_particle_y):

    if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_x % 2 == 1) and (prev_particle_y %2 ==1)):
          particle_x = prev_particle_x-1
          particle_y = prev_particle_y
          
    else:
        if rotor_matrix[prev_particle_x][prev_particle_y] == 1 and ((prev_particle_x % 2 == 1) and (prev_particle_y %2 ==1)):
          particle_y = prev_particle_y+1
          particle_x = prev_particle_x
          
        else:
            #even col even row
            if rotor_matrix[prev_particle_x][prev_particle_y] == 1 and ((prev_particle_x % 2 == 0) and (prev_particle_y %2 ==0)):
                particle_y = prev_particle_y-1
                particle_x = prev_particle_x
                
            else:
                 if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_x % 2 == 0) and (prev_particle_y %2 ==0)):
                     particle_x = prev_particle_x+1
                     particle_y = prev_particle_y

                 else:
                     #odd row even col
                     if rotor_matrix[prev_particle_x][prev_particle_y] == 1 and ((prev_particle_y % 2 == 0) and (prev_particle_x %2 ==1)):
                         particle_x= prev_particle_x
                         particle_y = prev_particle_y+1
                         
                     else:
                         if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_y % 2 == 0) and (prev_particle_x %2 ==1)):
                             particle_y = prev_particle_y
                             particle_x = prev_particle_x+1

                         else:
                             #even row odd col
                             if  rotor_matrix[prev_particle_x][prev_particle_y] == 1 and ((prev_particle_y % 2 == 1) and (prev_particle_x %2 ==0)):
                                 particle_x = prev_particle_x
                                 particle_y = prev_particle_y-1
                                
                             else:
                                 if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_y % 2 == 1) and (prev_particle_x % 2 ==0)):
                                     particle_y=prev_particle_y
                                     particle_x = prev_particle_x-1

        
                
    return particle_x, particle_y

def update_pp_first(rotor_matrix, particle_x, particle_y, prev_particle_x, prev_particle_y, mirror_matrix, prev_prev_particle_x, prev_prev_particle_y):
    #send a particle based on the mirrors first time I reach a site

    if mirror_matrix[prev_particle_x][prev_particle_y] == 0:
        if prev_prev_particle_x == prev_particle_x and prev_particle_y - prev_prev_particle_y ==1:           
            particle_x = prev_particle_x
            particle_y = prev_particle_y+1
        else:
            if prev_prev_particle_x == prev_particle_x and prev_particle_y - prev_prev_particle_y ==-1:           
                particle_x = prev_particle_x
                particle_y = prev_particle_y-1

            else:
                if prev_prev_particle_y == prev_particle_y and prev_particle_x - prev_prev_particle_x ==1:
                    particle_x = prev_particle_x+1
                    particle_y = prev_particle_y
                else:
                    if prev_prev_particle_y == prev_particle_y and prev_particle_x - prev_prev_particle_x ==-1:
                        particle_x = prev_particle_x-1
                        particle_y = prev_particle_y
                    

    else:
        if mirror_matrix[prev_particle_x][prev_particle_y] == 1:
            if prev_particle_x == prev_prev_particle_x and prev_particle_y - prev_prev_particle_y == 1:             
                particle_x = prev_particle_x+1
                particle_y = prev_particle_y
                
            else:
                if prev_particle_x == prev_prev_particle_x and prev_particle_y - prev_prev_particle_y == -1:
                    particle_x = prev_particle_x-1
                    particle_y = prev_particle_y

                else:
                    if prev_particle_y == prev_prev_particle_y and prev_particle_x - prev_prev_particle_x == 1:
                      particle_x = prev_particle_x
                      particle_y = prev_particle_y+1

                    else:
                        if prev_particle_y == prev_prev_particle_y and prev_particle_x - prev_prev_particle_x == -1:
                            particle_x = prev_particle_x
                            particle_y = prev_particle_y-1

        else:
            if mirror_matrix[prev_particle_x][prev_particle_y] == -1:
                if prev_particle_x == prev_prev_particle_x and prev_particle_y - prev_prev_particle_y == 1:             
                    particle_x = prev_particle_x-1
                    particle_y = prev_particle_y
                
                else:
                    if prev_particle_x == prev_prev_particle_x and prev_particle_y - prev_prev_particle_y == -1:
                        particle_x = prev_particle_x+1
                        particle_y = prev_particle_y

                    else:
                        if prev_particle_y == prev_prev_particle_y and prev_particle_x - prev_prev_particle_x == 1:
                            particle_x = prev_particle_x
                            particle_y = prev_particle_y-1

                        else:
                            if prev_particle_y == prev_prev_particle_y and prev_particle_x - prev_prev_particle_x == -1:
                                particle_x = prev_particle_x
                                particle_y = prev_particle_y+1
            

    return particle_x, particle_y

    

def draw_pic(u_func,n_excursions):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):                
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("manh" + str(n_excursions) + ".png")

def is_power2(num):

	'states if a number is a power of two'

        if (num != 0 and ((num & (num - 1)) == 0) ==True):
            return 1
        else:
            return 0

'''
def boundary(visited_matrix):
    n_bdry = 0
    for i in xrange(-dim,dim):
        for j in xrange(-dim, dim):
            if visited_matrix[i][j] > 0 and (visited_matrix[i+1][j] == 0 or visited_matrix[i-1][j] == 0 or visited_matrix[i][j-1] == 0 or visited_matrix[i][j+1] == 0):
                n_bdry+=1

    return n_bdry
'''

def update_rotor_matrix(rotor_matrix,x,y):
      
  rotor_matrix[x][y] = (rotor_matrix[x][y]+1) %2
  return rotor_matrix[x][y]

def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
           #if prob_matrix[x_ind][y_ind]
          rotor_matrix[x_ind][y_ind] = randrange(0,2)
            
    return rotor_matrix

def assign_probabilities(mirror_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
            if ((x_ind + y_ind) % 2==0):
                mirror_matrix[x_ind][y_ind] = randrange(-1,1)
            else:
                mirror_matrix[x_ind][y_ind] = randrange(0,2)

    
    return mirror_matrix

if __name__ == '__main__':
  __MAIN__()
