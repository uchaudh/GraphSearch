#!/usr/bin/env python

import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2

#constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 3000
RADIUS=20
start_locx = 200
start_locy = 100
start_loc = (start_locx,start_locy)
goal_locx = 600
goal_locy = 100
goal_loc = (goal_locx,goal_locy)

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

#def isinobstacle(ranx,rany):


def chooseParent(nn,newnode,nodes):
    for p in nodes:
        if dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and p.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y]):
            nn = p
    newnode.cost=nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y])
    newnode.parent=nn
    return newnode,nn

def reWire(nodes,newnode,pygame,screen):
    white = 255, 240, 200
    black = 20, 20, 40
    for i in range(len(nodes)):
        p = nodes[i]
        if p!=newnode.parent and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < p.cost:
            pygame.draw.line(screen,white,[p.x,p.y],[p.parent.x,p.parent.y])  
            p.parent = newnode
            p.cost=newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) 
            nodes[i]=p  
            pygame.draw.line(screen,black,[p.x,p.y],[newnode.x,newnode.y])                    
    return nodes

def drawSolutionPath(start,goal,nodes,pygame,screen):
    pink = 200, 20, 240
    nn = nodes[0]
    solx = []
    soly = []
    for p in nodes:
        if dist([p.x,p.y],[goal.x,goal.y]) < dist([nn.x,nn.y],[goal.x,goal.y]):
            nn = p
    while nn!=start:
        pygame.draw.line(screen,pink,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)  
        nn=nn.parent
        solx.append(nn.x)
        soly.append(nn.y)

    #print(solx)
    #print(soly)


class Node:
    x = 0
    y = 0
    cost=0  
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def main():
    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRTstar')
    white = 255, 240, 200
    black = 20, 20, 40
    blue = 0, 0, 255
    green = 0, 255, 0
    red = 255, 0, 0
    screen.fill(white)

    pygame.draw.circle(screen,red,start_loc,5)
    pygame.draw.circle(screen,green,goal_loc,5)
    pygame.draw.rect(screen,blue,[XDIM/4,YDIM/3,300,100])
    pygame.draw.rect(screen,blue,[(XDIM/4)+250,(YDIM/3)-200,50,200])

    nodes = []
    
    #nodes.append(Node(XDIM/2.0,YDIM/2.0)) # Start in the center
    nodes.append(Node(start_locx, start_locy)) # Start in the corner
    start=nodes[0]
    goal=Node(goal_locx, goal_locy)
    for i in range(NUMNODES):
        rand = Node(random.random()*XDIM, random.random()*YDIM)

        if (rand.x >= XDIM/4 and rand.x <= (XDIM/4)+300 and rand.y >= YDIM/3 and rand.y <= (YDIM/3)+100) or (rand.x >= (XDIM/4)+250 and rand.x <=(XDIM/4)+300 and rand.y <= (YDIM/3)):
            continue

        nn = nodes[0]
        for p in nodes:
            if dist([p.x,p.y],[rand.x,rand.y]) < dist([nn.x,nn.y],[rand.x,rand.y]):
                nn = p
        interpolatedNode= step_from_to([nn.x,nn.y],[rand.x,rand.y])

        newnode = Node(interpolatedNode[0],interpolatedNode[1])
        if (newnode.x >= XDIM/4 and newnode.x <= (XDIM/4)+300 and newnode.y >= YDIM/3 and newnode.y <= (YDIM/3)+100) or (newnode.x >= (XDIM/4)+250 and newnode.x <=(XDIM/4)+300 and newnode.y <= (YDIM/3)):
            continue

        [newnode,nn]=chooseParent(nn,newnode,nodes)
       
        nodes.append(newnode)
        pygame.draw.line(screen,black,[nn.x,nn.y],[newnode.x,newnode.y])
        nodes=reWire(nodes,newnode,pygame,screen)
        pygame.display.update()
        #print i, "    ", nodes

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")

    drawSolutionPath(start,goal,nodes,pygame,screen)
    pygame.display.update()

# if python says run, then we should run
if __name__ == '__main__':
    main()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



