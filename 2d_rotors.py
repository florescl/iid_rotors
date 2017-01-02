# -*- coding: utf-8 -*-
#from __future__ import print_function

import itertools
import random
import math
import numpy as np
import random

from random import randrange
from collections import defaultdict
import Image


dim = 400
experiments = 1000000
k=100

n_iters_try =10000000

#random.seed(1234)

def __MAIN__():

    exp = 0
    
    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]
    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    sites_visits = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    unique = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]

    #u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,300)]
    set_a = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    particle_x = 0
    particle_y = 0

    n_iters = 0
    n_succesive_visits = 0
    n_sites_visited = 0
    
    n_excursions = 0
    length_f_exc = 0

    while n_iters < n_iters_try:
        #while n_excursions < 10:
        rotor_matrix[particle_x][particle_y] = update_rotor_matrix(rotor_matrix, particle_x, particle_y)
        particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y)
        unique[particle_x][particle_y] = 1
        
        if set_a[particle_x][particle_y] == 0:
            set_a[particle_x][particle_y] = n_excursions

        sites_visits[particle_x][particle_y]+=1

        if sites_visits[particle_x][particle_y] ==1:
            n_sites_visited+=1
                 
        if particle_x==0 and particle_y==0:
            n_succesive_visits+=1
                
            if n_succesive_visits==4:

                n_excursions+=1
                print n_excursions, n_iters, n_sites_visited
                n_succesive_visits=0

        n_iters+=1

        #print n_sites_vis
        #print n_iters_try, n_excursions*4

        #print(set_a)
        #draw_sets(set_a)

def draw_an(unique):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(255,255,255),(255,0,0)][unique[x][y]]

    im.save("set_an" + ".png")


def draw_sets(set_a):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(255,255,255),(1,1,15), (10,10,25), (20,20,35), (30,30,45), (40,40,55),(50,50,65), (60,60,75), (70,70,85), (80,80,95), (90,90,105)][set_a[x][y]]
    im.save("sets_new" + ".png")


def draw_pic(u_func,n_excursions):
    #from PIL import Image
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-dim,dim):
        for y in xrange(-dim,dim):
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][u_func[n_excursions][x][y]]

    im.save("2dexc" + str(n_excursions) + ".png")


def draw_unicycle(rotor_matrix, n_excursions):
    im = Image.new('RGB',(2*dim,2*dim))
    pix=im.load()

    for x in xrange(-k,k):
        for y in xrange(-k,k):
            pix[x+dim,y+dim]=[(250,250,250),(255,0,0),(0,255,0),(0,0,255)][rotor_matrix[x][y]]

    im.save("unicycle" + str(n_excursions) + ".png")


def latex_export_blob(f1, k, u_func,n_excursions):
    for i_ind in range(-k,k):
        for j_ind in range(-k,k):
            if u_func[n_excursions][i_ind][j_ind] == 0:
              f1.write(r'\node[blackdot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
              f1.write('\n')
            else:
                if u_func[n_excursions][i_ind][j_ind] == 1:
                    f1.write(r'\node[reddot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
                    f1.write('\n')
                else:
                    if u_func[n_excursions][i_ind][j_ind] == 2:
                        f1.write(r'\node[yellowdot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
                        f1.write('\n')
                    else:
                        if u_func[n_excursions][i_ind][j_ind] == 3:
                            f1.write(r'\node[greendot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
                            f1.write('\n')
                        else:
                            if u_func[n_excursions][i_ind][j_ind] == 4:
                                f1.write(r'\node[bluedot] (1) at (' + str(i_ind) + ',' + str(j_ind) + ') {};') 
                                f1.write('\n')





def latex_export_unicycles(f1, k, rotor_matrix):

    for i_ind in range(-k,k):
        for j_ind in range(-k,k):
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

def update_particle_position(rotor_matrix, particle_x, particle_y):
    #east
      if rotor_matrix[particle_x][particle_y] == 0:
          particle_x+=1
      else:
          if rotor_matrix[particle_x][particle_y] ==1:
              particle_y+=1
          else:
              if rotor_matrix[particle_x][particle_y] == 2:
                  particle_x-=1
              else:
                  if rotor_matrix[particle_x][particle_y] ==3:
                      particle_y-=1

      return particle_x, particle_y


def update_rotor_matrix(rotor_matrix,x,y):
      
  rotor_matrix[x][y] = ((rotor_matrix[x][y]+1)% 4)
  return rotor_matrix[x][y]

def initialize_rotor_matrix(rotor_matrix):
    for x_ind in range(-dim,dim):
        for y_ind in range(-dim,dim):
            rotor_matrix[x_ind][y_ind] = randrange(0,4)
            
    return rotor_matrix


if __name__ == '__main__':
  __MAIN__()
