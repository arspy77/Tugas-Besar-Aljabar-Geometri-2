import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import threading

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
def reflect(verticies, a, b, c) :

    ab = a*b
    ac = a*c
    bc = b*c
    tfMat = np.array([
        [1-(2*a*a),-2*ab,-2*ac,0],
        [-2*ab,1-(2*b*b),-2*bc,0],
        [-2*ac,-2*bc,1-(2*c*c),0],
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

def rot(verticies, a, b, c, degree) :
    degree = degree*np.pi/180
    cosa = np.math.cos(degree)
    sina = np.math.sin(degree)
    ab = a*b
    bc = b*c
    ac = a*c
    tfMat = np.array([
        [1,0,0,0],
        [a,1,0,0],
        [b,0,1,0],
        [0,0,0,1]
    ])
    tfMat = np.array([
        [cosa+((a**2)*(1-cosa)),ab*(1-cosa)-(c*sina),ac*(1-cosa)+(b*sina),0],
        [ab*(1-cosa)+(c*sina),cosa+((b**2)*(1-cosa)),bc*(1-cosa)-(a*sina),0],
        [ac*(1-cosa)-(b*sina),bc*(1-cosa)+(a*sina),cosa+((c**2)*(1-cosa)),0],
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
    glEnd()

def Shape(verticies):
    glBegin(GL_POLYGON)
    
    glColor3fv([255,0,0])
    for i in range(int(verticies.size/2)):
        glVertex2fv(verticies[i])
    '''
    glEnd()

    glBegin(GL_LINES)
    '''
    glColor3fv([255,255,255])
    for i in range(int(verticies.size/2)):
        '''
        if i == 0:
            glVertex2fv(verticies[int(verticies.size/2)-1])
            glVertex2fv(verticies[i])
        else:
            glVertex2fv(verticies[i-1])
            '''
        glVertex2fv(verticies[i])


    glEnd()


def ShadowCube(verticies,edges,surfaces):

    '''
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor4fv(np.append(colors[x],[0.1]))
            glVertex3fv(verticies[vertex])
    glEnd()
    '''
    glBegin(GL_LINES)
    glColor3fv([255,255,255])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Sumbu3D():  
    glBegin(GL_LINES)  
    glColor3fv([255,255,255])
    glVertex3fv([-500,0,0])
    glVertex3fv([0,0,0])
    glColor3fv([0,255,0])
    glVertex3fv([0,0,0])
    glVertex3fv([500,0,0])

    glColor3fv([255,255,255])
    glVertex3fv([0,-500,0])
    glVertex3fv([0,0,0])
    glColor3fv([0,0,255])
    glVertex3fv([0,0,0])
    glVertex3fv([0,500,0])

    glColor3fv([255,255,255])
    glVertex3fv([0,0,-500])
    glVertex3fv([0,0,0])
    glColor3fv([255,0,0])
    glVertex3fv([0,0,0])
    glVertex3fv([0,0,500])
    glEnd()

def Sumbu2D():  
    glBegin(GL_LINES)  
    glColor3fv([255,255,255])
    glVertex2fv([-500,0])
    glVertex2fv([0,0])
    glColor3fv([0,255,0])
    glVertex2fv([0,0])
    glVertex2fv([500,0])

    glColor3fv([255,255,255])
    glVertex2fv([0,-500])
    glVertex2fv([0,0])
    glColor3fv([0,0,255])
    glVertex2fv([0,0])
    glVertex2fv([0,500])
    glEnd()

def rotateScreen():
    keystate = pygame.key.get_pressed()
    if keystate[K_DOWN]:
        glRotatef(-1,1,0,0)
    elif keystate[K_UP]:
        glRotatef(1,1,0,0)
    elif keystate[K_LEFT]:
        glRotatef(-1,0,1,0)
    elif keystate[K_RIGHT]:
        glRotatef(1,0,1,0)

def Animate(verticies, nextvert, edges, surfaces, colors):
    anivert = np.copy(verticies)
    for n in range(60):
        for i in range(int(verticies.size/3)):
            dx = nextvert[i][0] - verticies[i][0]
            dy = nextvert[i][1] - verticies[i][1]
            dz = nextvert[i][2] - verticies[i][2]
            temp = translate(np.array([anivert[i]]),dx/60,dy/60,dz/60)
            anivert[i] = temp[0]
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        rotateScreen()
        ShadowCube(verticies,edges,surfaces)
        Cube(anivert,edges,surfaces,colors)
        Sumbu3D()
        pygame.display.flip()
        pygame.time.wait(50)
    return


class getCommand (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global cmd
        global commandexist
        while True:
            cmd = input("Masukan command : ")
            commandexist = True

def inputVerticies():
    global N
    N = int(input("Masukan Jumlah Titik : "))
    while N < 1:
        print("Masukan salah")
        N = int(input("Masukan Jumlah Titik : "))
    for i in range(N):
        print("Masukan titik ke-" + str(i) + " (format : x y): ")
        vertex = (input().split(' '))
        x = int(vertex[0])
        y = int(vertex[1])
        vertex[0] = x
        vertex[1] = y
        vertex = np.array([vertex])
        if i == 0:
            verticies = vertex
        else:
            verticies = np.append(verticies,vertex,axis = 0)
    return verticies

def main():
    
    print("Pilih Mode:\n1. 2D\n2.3D")
    mode = int(input("Masukan pilihan : "))
    while mode != 1 and mode != 2:
        print("Masukan salah!")
        mode = int(input("Masukan pilihan : "))
    if mode == 1:
        main2D()
    else:
        main3D()

def main2D():
    global N
    verticies = inputVerticies()
    initvert = verticies
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 4000.0)
    glTranslatef(0.0,0.0, -1500.0)
    global cmd
    global commandexist
    threadcmd = getCommand()
    cmd = ""
    commandexist = False
    threadcmd.start()
    while cmd != 'exit':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if commandexist:
            arg = cmd.split(' ')
            if arg[0] == 'translate':
                print("wip")
            elif arg[0] == 'dilate':
                verticies = dilate(verticies,k)
            elif arg[0] == 'reset':
                verticies = initvert
            commandexist = False
            
        
        
        Shape(verticies)
        Sumbu2D()

        pygame.display.flip()
        
        pygame.time.wait(1)

def main3D():
    verticies =  np.array([
        [50, -50, -50],
        [50, 50, -50],
        [-50, 50, -50],
        [-50, -50, -50],
        [50, -50, 50],
        [50, 50, 50],
        [-50, -50, 50],
        [-50, 50, 50]
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
    initvert = np.copy(verticies)
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 4000.0)
    glTranslatef(0.0,0.0, -1500.0)
    glRotatef(30,1,1,1)
    global cmd
    global commandexist
    threadcmd = getCommand()
    cmd = ""
    commandexist = False
    threadcmd.start()
    while cmd != 'exit':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        rotateScreen()
        if commandexist:
            arg = cmd.split(' ')
            if arg[0] == 'translate':
                dx = float(arg[1])
                dy = float(arg[2])
                dz = float(arg[3])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = translate(nextvert,dx/60,dy/60,dz/60)
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = translate(verticies,dx,dy,dz)
            elif arg[0] == 'dilate':
                k = float(arg[1])
                nextvert = verticies
                for n in range(60):
                    nextvert = dilate(nextvert,k**(1./60))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = dilate(verticies,k)
           elif arg[0] == 'rotate' :
                  a = float(arg[1])
                  b = float(arg[2])
                  c = float(arg[3])
                  degree = float(arg[4])
                  nextvert = verticies
                  for n in range(60):
                      nextvert = rot(nextvert,a,b,c,degree/60)
                      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                      rotateScreen()
                      ShadowCube(verticies,edges,surfaces)
                      Cube(nextvert,edges,surfaces,colors)
                      Sumbu3D()
                      pygame.display.flip()
                      pygame.time.wait(round(3000/60))
                  verticies = rot(verticies,a,b,c,degree)
                param = (arg[1])
                k = float(arg[2])
                nextvert = verticies
                for n in range(60):
                    nextvert = shear(nextvert,param,(k/60))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    rotateScreen()
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = shear(verticies,param,k)
            elif arg[0] == 'stretch' :
                param = (arg[1])
                k = float(arg[2])
                nextvert = verticies
                for n in range(60):
                    nextvert = stretch(nextvert,param,(k**(1./60)))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    rotateScreen()
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = stretch(verticies,param,k)
            elif arg[0] == 'custom' :
                a = float(arg[1])
                b = float(arg[2])
                c = float(arg[3])
                d = float(arg[4])
                e = float(arg[5])
                f = float(arg[6])
                g = float(arg[7])
                h = float(arg[8])
                i = float(arg[9])
                nextvert = verticies
                verticies = custom(verticies,a,b,c,d,e,f,g,h,i)
                Animate(nextvert,verticies,edges,surfaces,colors)
            elif arg[0] == 'reflect' :
                a = float(arg[1])
                b = float (arg[2])
                c = float (arg[3])
                if not(a == 0.0 and b == 0.0 and c == 0.0) :
                    mag = (a*a+b*b+c*c)**(1.0/2.0)
                    aa = a/mag
                    bb = b/mag
                    cc = c/mag
                    nextvert = reflect(verticies,aa,bb,cc)
                    Animate(verticies,nextvert,edges,surfaces,colors)
                    verticies = nextvert
            elif arg[0] == 'reset':
                Animate(verticies,initvert,edges,surfaces,colors)
                verticies = np.copy(initvert)
            commandexist = False
            
        
        
        Cube(verticies,edges,surfaces,colors)
        Sumbu3D()

        pygame.display.flip()
        
        pygame.time.wait(1)

main()


