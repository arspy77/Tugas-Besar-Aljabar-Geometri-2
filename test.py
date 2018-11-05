import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
'''
verticies = [] 

for i in range(0,8):
    a = int(input("a : "))
    b = int(input("b : "))
    c = int(input("c : "))
    l = []
    l.append(a)
    l.append(b)
    l.append(c)
    verticies.append(l)
print (verticies)


verticies =  np.array([
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
])
edges = np.array([
    [0,1],
    [0,3],
    [0,4],
    [2,1],
    [2,3],
    [2,7],
    [6,3],
    [6,4],
    [6,7],
    [5,1],
    [5,4],
    [5,7]
])
'''


def shear(verticies, param, k):
    if param == 'x':
        tfMat = np.array([
            [1,k,k,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
    elif param == 'y':
        tfMat = np.array([
            [1,0,0,0],
            [k,1,k,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
    elif param == 'z':
        tfMat = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [k,k,1,0],
            [0,0,0,1]
        ]) 
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV


def custom(verticies, a, b, c, d, e, f, g, h, i):
    tfMat = np.array([
        [a,b,c,0],
        [d,e,f,0],
        [g,h,i,0],
        [0,0,0,1]
    ])
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV

def stretch(verticies, param, k):
    if param == 'x':
        tfMat = np.array([
            [k,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
    elif param == 'y':
        tfMat = np.array([
            [1,0,0,0],
            [0,k,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
    elif param == 'z':
        tfMat = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,k,0],
            [0,0,0,1]
        ]) 
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV



def translate(verticies, dx, dy, dz):
    tfMat = np.array([
        [1,0,0,dx],
        [0,1,0,dy],
        [0,0,1,dz],
        [0,0,0,1]
    ]) 
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV 

def dilate(verticies, k):
    tfMat = np.array([
        [k,0,0,0],
        [0,k,0,0],
        [0,0,k,0],
        [0,0,0,1]
    ]) 
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV 

def rotate(verticies, degreeX, degreeY, degreeZ, x, y, z):
    translateToZeroMat = np.array([
        [1,0,0,-x],
        [0,1,0,-y],
        [0,0,1,-z],
        [0,0,0,1]
    ]) 
    xRotateMat = np.array([
        [1,0,0,0],
        [0,np.math.cos((degreeX/360)*2*np.pi),-(np.math.sin((degreeX/360)*2*np.pi)),0],
        [0,np.math.sin((degreeX/360)*2*np.pi),np.math.cos((degreeX/360)*2*np.pi),0],
        [0,0,0,1]
    ]) 
    yRotateMat = np.array([
        [np.math.cos((degreeY/360)*2*np.pi),0,np.math.sin((degreeY/360)*2*np.pi),0],
        [0,1,0,0],
        [-(np.math.sin((degreeY/360)*2*np.pi)),0,np.math.cos((degreeY/360)*2*np.pi),0],
        [0,0,0,1]
    ]) 
    zRotateMat = np.array([
        [np.math.cos((degreeZ/360)*2*np.pi),-(np.math.sin((degreeZ/360)*2*np.pi)),0,0],
        [np.math.sin((degreeZ/360)*2*np.pi),np.math.cos((degreeZ/360)*2*np.pi),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ]) 
    translateBackMat = np.array([
        [1,0,0,x],
        [0,1,0,y],
        [0,0,1,z],
        [0,0,0,1]
    ]) 
    tfMat = np.matmul(translateBackMat, np.matmul(xRotateMat, np.matmul(yRotateMat, np.matmul(zRotateMat, translateToZeroMat))))
    newV = np.empty((0,3), float)
    for vertex in verticies:
        vertex = np.append(vertex , [1])
        temp = np.matmul(tfMat,vertex.T)
        keep = [True,True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV 


def Cube(verticies,edges,surfaces,colors):
    

    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    
    glVertex3fv([-1000,0,0])
    glVertex3fv([1000,0,0])
    glVertex3fv([0,-1000,0])
    glVertex3fv([0,1000,0])
    glVertex3fv([0,0,-1000])
    glVertex3fv([0,0,1000])
    for i in range(-500,500,10):    
        glVertex3fv([500,0,i])
        glVertex3fv([-500,0,i])
        glVertex3fv([0,500,i])
        glVertex3fv([0,-500,i])
        glVertex3fv([500,i,0])
        glVertex3fv([-500,i,0])
        glVertex3fv([0,i,500])
        glVertex3fv([0,i,-500])
        glVertex3fv([i,500,0])
        glVertex3fv([i,-500,0])
        glVertex3fv([i,0,500])
        glVertex3fv([i,0,-500])
    glEnd()

def main():
    verticies =  np.array([
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, -1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ])
    edges = np.array([
        [0,1],
        [0,3],
        [0,4],
        [2,1],
        [2,3],
        [2,7],
        [6,3],
        [6,4],
        [6,7],
        [5,1],
        [5,4],
        [5,7]
    ])
    
    surfaces = np.array([
        [0,1,2,3],
        [3,2,7,6],
        [6,7,5,4],
        [4,5,1,0],
        [1,5,7,2],
        [4,0,3,6]
    ])
    colors = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [0,1,0],
    [1,1,1],
    [0,1,1],
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [1,0,0],
    [1,1,1],
    [0,1,1]
    ])
    
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -10)
    state = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                '''
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rxp = True
                elif event.key == pygame.K_LEFT:
                    rym = True
                elif event.key == pygame.K_RIGHT:
                    ryp = True
                elif event.key == pygame.K_DOWN:
                    rxm = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rxp = False
                elif event.key == pygame.K_LEFT:
                    rym = False
                elif event.key == pygame.K_RIGHT:
                    ryp = False
                elif event.key == pygame.K_DOWN:
                    rxm = False
            if rxp == True:
                glRotatef(1,1,0,0)
            elif rym == True:
                glRotatef(-1,0,1,0)
            elif ryp == True:
                glRotatef(1,0,1,0)
            elif rxm == True:
                glRotatef(-1,1,0,0)
                '''
        keystate = pygame.key.get_pressed()
        if keystate[K_DOWN]:
            glRotatef(-1,1,0,0)
        if keystate[K_UP]:
            glRotatef(1,1,0,0)
        if keystate[K_LEFT]:
            glRotatef(-1,0,1,0)
        if keystate[K_RIGHT]:
            glRotatef(1,0,1,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube(verticies,edges,surfaces,colors)
        pygame.display.flip()
        '''
        if (np.absolute(verticies[0][0]) >= 10): 
            state = 2
        elif(np.absolute(verticies[0][0]) <= 1):
            state = 1
        if state == 1:
            verticies = dilate(verticies,1.01)
        else:
            verticies = dilate(verticies,0.99)
        '''
    
        verticies = rotate(verticies,0,0.6,0,1,0,1)
        '''
        if (np.absolute(verticies[0][0]) >= 5) and (state == 1):
            state = 2
        elif (np.absolute(verticies[0][0]) < 1) and (state == 2):
            state = 3
        elif (np.absolute(verticies[0][1]) >= 5) and (state == 3):
            state = 4
        elif (np.absolute(verticies[0][1]) < 1) and (state == 4):
            state = 5
        elif (np.absolute(verticies[0][2]) >= 5) and (state == 5):
            state = 6
        elif (np.absolute(verticies[0][2]) < 1) and (state == 6):
            state = 1
        if state == 1:
            verticies = shear(verticies, 'x', 0.01)
        elif state == 2:
            verticies = shear(verticies, 'x', -0.01)
        elif state == 3:
            verticies = shear(verticies, 'y', 0.01)
        elif state == 4:
            verticies = shear(verticies, 'y', -0.01)
        elif state == 5:
            verticies = shear(verticies, 'z', 0.01)
        elif state == 6:
            verticies = shear(verticies, 'z', -0.01)
            '''
        print(verticies)
        pygame.time.wait(1)



main()