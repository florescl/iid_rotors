# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict
import Image

#random.seed(1234)

dim = 90
n_iters = 1000000
k = 10


def __MAIN__():

    
    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]

    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    unique_vis_mat = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    set_a = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]

    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,300)]

    rotor_matrix = initialize_rotor_matrix(rotor_matrix)

    #print(rotor_matrix)

    particle_x = 0
    particle_y = 0

    n_iters_try = 0
    n_excursions = 0

    n_successive_visits = 0    
    n_sites_visited = 0
    
    with open('comb.csv','wb') as csvfile:
                    
        while n_iters_try < n_iters and n_excursions < 21:
            rotor_matrix[particle_x][particle_y] = update_rotor_matrix(rotor_matrix, particle_x, particle_y)
            
            particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)

            if set_a[particle_x][particle_y] == 0:
                set_a[particle_x][particle_y] = n_excursions
            
            u_func[n_excursions][particle_x][particle_y]+=1
            visited_matrix[particle_x][particle_y]+=1
            unique_vis_mat[particle_x][particle_y] = 1

            #print n_iters_try, particle_x, particle_y, rotor_matrix[particle_x][particle_y]
            if particle_x > dim or particle_x < -dim or particle_y > dim or particle_y < -dim:
                break

            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1

            if particle_x==0 and particle_y==0:
                n_successive_visits+=1
             
                if n_successive_visits % 4 == 0:
                    n_excursions+=1
                    n_successive_visits=0
                    
            n_iters_try+=1
            
            #if n_iters_try % 100000==0:
            # draw_pic(u_func,n_excursions)
            # draw_pic2(unique_vis_mat, n_excursions)
                
                print 'exc', n_iters_try, n_sites_visited, n_sites_visited/(pow(n_iters_try,0.5)*math.log(n_iters_try)), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), particle_x, particle_y, math.log(math.sqrt(pow(max_horizontal(unique_vis_mat),2.0)+pow(max_vertical(unique_vis_mat),2.0)))

                #print 'max x', max_horizontal(unique_vis_mat)
                #print 'max y', max_vertical(unique_vis_mat)

                cw = csv.writer(csvfile, dialect='excel')
                cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/(pow(n_iters_try,0.5)*math.log(n_iters_try)), n_excursions, math.log(n_iters_try), math.log(n_sites_visited),math.log(n_iters_try),  math.log(math.sqrt(pow(max_horizontal(unique_vis_mat),2.0)+pow(max_vertical(unique_vis_mat),2.0)))])
        
    draw_sets(set_a)



def draw_sets(set_a):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255),(250,250,20),(255,80,0),(80,255,0),(0,80,255), (200,250,250),(55,0,0),(0,55,0),(0,0,55),(20,20,20),(25,0,0),(0,25,0),(0,0,25),(100,100,100),(98,76,200),(70,64,109),(87,234,200),(76,54,12),(87,12,90)][set_a[x][y]]

    im.save("sets_comb" + ".png")
   
def print_odometer(u_func, n_excursions):
    for i in range(-dim,dim):
        for j in range(-dim,dim):
            print u_func[n_excursions][i][j]

def draw_pic(u_func,n_excursions):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):                
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("combpic1" + str(n_excursions) + ".png")

  
def draw_pic2(unique_vis_mat,n_excursions):
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):    
            #print x,y, visited_matrix[x][y]
            pix[x+dim,y+dim]=[(250,250,250),(123,112,0),(89,80,0), (0,0,255), (89,76,0), (76,23,12), (0,1,255), (120,120,120)][unique_vis_mat[x][y]]

    im.save("combpic" + str(n_excursions) + ".png")

def max_horizontal(unique_vis_mat):
    max = 0
    for i in range(0, dim):
        if unique_vis_mat[0][i-1] == 1 and unique_vis_mat[0][i] == 0:
            max = i

    return max

def max_vertical(unique_vis_mat):
    max = 0
    for i in range(0, dim):
        if unique_vis_mat[i-1][0] == 1 and unique_vis_mat[i][0] == 0:
            max = i

    return max

          
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
    
    if particle_y == 0:
        if rotor_matrix[particle_x][particle_y] == 0:
            particle_y+=1
        else:
            if rotor_matrix[particle_x][particle_y] ==1:
              particle_x+=1
            else:
                if rotor_matrix[particle_x][particle_y] == 2:
                    particle_y-=1
                else:
                    if rotor_matrix[particle_x][particle_y] ==3:
                        particle_x-=1
    else:
        if rotor_matrix[particle_x][particle_y] == 0:
            particle_y+=1
        else:
            particle_y-=1
             
    return particle_x, particle_y

def update_rotor_matrix(rotor_matrix,x,y):
      
    if y==0:
        rotor_matrix[x][y] = (rotor_matrix[x][y]+1)%4
    else:
        rotor_matrix[x][y] = ((rotor_matrix[x][y]+1)%2)
    return rotor_matrix[x][y]


def initialize_rotor_matrix(rotor_matrix):

    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
          rotor_matrix[x_ind][y_ind] = randrange(0,2)

    for i in range(-dim,dim):
        for j in range(-dim,dim):
            if j==0:
                rotor_matrix[i][j]=randrange(0,4)
            
    return rotor_matrix



if __name__ == '__main__':
  __MAIN__()
