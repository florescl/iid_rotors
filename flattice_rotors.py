# -*- coding: utf-8 -*-

import itertools
import random
import math
import numpy as np
import random
import csv
from random import randrange
from collections import defaultdict
import png
#import Image

random.seed(1234)

dim = 100
n_iters = 20
k = 10


def __MAIN__():


    f = open('fl.tex','w')
    g = open('manh.tex','w')
    
    #draw_lattice(f)
    draw_lattice1(g)
    '''
    rotor_matrix = [[0 for y in xrange(-dim, dim)] for x in xrange(-dim,dim)]

    visited_matrix = [[0 for y in xrange(-dim,dim)] for x in xrange(-dim,dim)]
    u_func = [[[0 for z in xrange(-dim,dim)] for y in xrange(-dim,dim)] for x in xrange(0,300)]

    rotor_matrix = initialize_rotor_matrix(rotor_matrix)
    f2 = open('initialmirrors_fl.tex','w')
    initial_mirrors(f2, rotor_matrix)

    particle_x = 0
    particle_y = 0

    prev_particle_x = 0
    prev_particle_y = 0
    
    n_iters_try = 0
    n_excursions = 0
    f1 = open('mirrorfl'+str(n_excursions) + '.tex','w')

    n_successive_visits = 0    
    n_sites_visited = 0
    
    with open('flattice.csv','wb') as csvfile:
                    
        while n_iters_try < n_iters:
            
            particle_x, particle_y = update_particle_position(rotor_matrix, particle_x, particle_y,prev_particle_x,prev_particle_y)
            rotor_matrix[prev_particle_x][prev_particle_y] = update_rotor_matrix(rotor_matrix, prev_particle_x, prev_particle_y)
            
            #ADD a mirror in the NW or NE direction
            add_mirror(f1, f2, rotor_matrix,particle_x, prev_particle_x, particle_y, prev_particle_y)
            
            u_func[n_excursions][particle_x][particle_y]+=1

            print 'u', n_iters_try, particle_x, particle_y
            #, u_func[n_excursions][particle_x][particle_y], n_excursions
            
            visited_matrix[particle_x][particle_y]+=1
            if particle_x > dim or particle_x < -dim or particle_y > dim or particle_y < -dim:
                break

            if(visited_matrix[particle_x][particle_y] == 1):
                n_sites_visited+=1

            if particle_x==0 and particle_y==0:
                n_successive_visits+=1
             
                if n_successive_visits % 2 == 0:
                    n_excursions+=1
                    n_successive_visits=0
                    
            n_iters_try+=1
            
            if n_iters_try % 1000==0:
            #draw_pic(u_func,n_excursions)
                n_bdry = boundary(visited_matrix)
                print 'exc', n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0)), particle_x, particle_y, math.log(boundary(visited_matrix))
                 
                cw = csv.writer(csvfile, dialect='excel')
                cw.writerow([n_iters_try, n_sites_visited, n_sites_visited/pow(n_iters_try,0.667), n_excursions, math.log(n_iters_try), math.log(n_sites_visited), math.sqrt(pow(particle_x,2.0)+pow(particle_y,2.0)), particle_x, particle_y, math.log(n_sites_visited), math.log(boundary(visited_matrix))])

            prev_particle_x = particle_x
            prev_particle_y = particle_y
   '''

def draw_lattice(f):

    for j in range(-2,2):
        for i in range(-2,2):
            if j % 2 == 0 and i<2:
                f.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i+1) + ',' + str(j) +');')
            else:
                if j %2 == 1 and i>-2:
                    f.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i-1) + ',' + str(j) +');')

    for ii in range(-2,2):
       for ji in range(-2,2):
            if ii % 2==0 and ji <2:
                f.write(r'\draw[color=black] (' + str(ii) + ',' + str(ji) + ') -- (' + str(ii) + ',' + str(ji+1) +');')
            else:
                if ii % 2==1 and ji > -2:
                   f.write(r'\draw[color=black] (' + str(ii) + ',' + str(ji) + ') -- (' + str(ii) + ',' + str(ji-1) +');')

def draw_lattice1(g):
    for j in range(-2,2):
        for i in range(-2,2):
            if ((i+j) % 2 == 0) and i<2 and j<2:
                g.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i) + ',' + str(j+1) +');')
                g.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i) + ',' + str(j-1) +');')
            else:
                g.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i+1) + ',' + str(j) +');')
                g.write(r'\draw[color=black] (' + str(i) + ',' + str(j) + ') -- (' + str(i-1) + ',' + str(j) +');')
                   
    
def boundary(visited_matrix):
    n_bdry = 0
    for i in xrange(-dim,dim):
        for j in xrange(-dim, dim):
            if visited_matrix[i][j] > 0 and (visited_matrix[i+1][j] == 0 or visited_matrix[i-1][j] == 0 or visited_matrix[i][j-1] == 0 or visited_matrix[i][j+1] == 0):
                n_bdry+=1

    return n_bdry


def add_mirror(f1, f2, rotor_matrix, particle_x, prev_particle_x, particle_y, prev_particle_y):


    f1.write(r'\draw[color=green] (' + str(prev_particle_x) + ',' + str(prev_particle_y) + ') -- (' + str(particle_x) + ',' + str(particle_y) +');')

    f2.write(r'\draw[color=green] (' + str(prev_particle_x) + ',' + str(prev_particle_y) + ') -- (' + str(particle_x) + ',' + str(particle_y) +');')
    
    if prev_particle_x == particle_x:
        if particle_y - prev_particle_y == 1:
            if rotor_matrix[particle_x][particle_y] == 0:
                f1.write(r'\draw[color=black] (' + str(particle_x+0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x-0.2) + ',' + str(particle_y - 0.2) +');')
                f1.write('\n')

            else:
                if rotor_matrix[particle_x][particle_y] == 1:
                    f1.write(r'\draw[color=black] (' + str(particle_x-0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x+0.2) + ',' + str(particle_y - 0.2) +');')
                    f1.write('\n')
                
        else:
            if particle_y - prev_particle_y == -1:
                if rotor_matrix[particle_x][particle_y] == 0:
                    f1.write(r'\draw[color=black] (' + str(particle_x+0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x-0.2) + ',' + str(particle_y - 0.2) +');')
                    f1.write('\n')

                else:
                    if rotor_matrix[particle_x][particle_y] == 1:
                        f1.write(r'\draw[color=black] (' + str(particle_x-0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x+0.2) + ',' + str(particle_y - 0.2) +');')
                        f1.write('\n')


    else:
        if prev_particle_y == particle_y:
            if particle_x - prev_particle_x == 1:
                if rotor_matrix[particle_x][particle_y] == 0:
                    f1.write(r'\draw[color=black] (' + str(particle_x+0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x-0.2) + ',' + str(particle_y - 0.2) +');')
                    f1.write('\n')

                else:
                    if rotor_matrix[particle_x][particle_y] == 1:
                        f1.write(r'\draw[color=black] (' + str(particle_x-0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x+0.2) + ',' + str(particle_y - 0.2) +');')
                        f1.write('\n')


            if particle_x - prev_particle_x == -1:
                if rotor_matrix[particle_x][particle_y] == 1:
                    f1.write(r'\draw[color=black] (' + str(particle_x+0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x-0.2) + ',' + str(particle_y - 0.2) +');')
                    f1.write('\n')

                else:
                    if rotor_matrix[particle_x][particle_y] == 0:
                        f1.write(r'\draw[color=black] (' + str(particle_x-0.2) + ',' + str(particle_y+0.2) + ') -- (' + str(particle_x+0.2) + ',' + str(particle_y - 0.2) +');')
                        f1.write('\n')
                        

#def perc_cluster(rotor_matrix):
#   for i in range(

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

    im.save("flattice" + str(n_excursions) + ".png")

            
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


def update_particle_position(rotor_matrix, particle_x, particle_y, prev_particle_x, prev_particle_y):
    #depending on the type of site and the rotor
    
      if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_x + prev_particle_y) % 2 == 0):
          particle_y = prev_particle_y+1

      else:
          if rotor_matrix[prev_particle_x][prev_particle_y] ==1 and ((prev_particle_x + prev_particle_y) % 2 == 1):
              particle_x = prev_particle_x-1
              
          else:
              if rotor_matrix[prev_particle_x][prev_particle_y] == 0 and ((prev_particle_x + prev_particle_y) % 2 == 1):
                  particle_x = prev_particle_x+1
                  
              else:
                  if rotor_matrix[prev_particle_x][prev_particle_y] == 1 and ((prev_particle_x + prev_particle_y) % 2 == 0):
                      particle_y=prev_particle_y-1
                      
      return particle_x, particle_y


def initial_mirrors(f2, rotor_matrix):

    for a in xrange(-k,k):
        for b in xrange(-k,k):
            if rotor_matrix[a][b] == 0 and (a+b) % 2 == 0:
                f2.write(r'\draw[color=black] (' + str(a+0.2) + ',' + str(b+0.2) + ') -- (' + str(a-0.2) + ',' + str(b-0.2) +');')
                f2.write('\n')

            else:
                if rotor_matrix[a][b] == 1 and (a+b) % 2 == 0:
                  f2.write(r'\draw[color=black] (' + str(a-0.2) + ',' + str(b+0.2) + ') -- (' + str(a+0.2) + ',' + str(b - 0.2) +');')
                  f2.write('\n')

                else:
                    if rotor_matrix[a][b] == 0 and (a+b) % 2 == 1:
                        f2.write(r'\draw[color=black] (' + str(a+0.2) + ',' + str(b+0.2) + ') -- (' + str(a-0.2) + ',' + str(b - 0.2) +');')
                        f2.write('\n')
                    else:
                        if rotor_matrix[a][b] == 1 and (a+b) % 2 == 1:
                            f2.write(r'\draw[color=black] (' + str(a-0.2) + ',' + str(b+0.2) + ') -- (' + str(a+0.2) + ',' + str(b - 0.2) +');')
                            f2.write('\n')


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
