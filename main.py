from transformation import *
from objects import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import threading


def rotateScreen():
    keystate = pygame.key.get_pressed()
    if keystate[K_DOWN]:
        glRotatef(-1, 1, 0, 0)
    elif keystate[K_UP]:
        glRotatef(1, 1, 0, 0)
    elif keystate[K_LEFT]:
        glRotatef(-1, 0, 1, 0)
    elif keystate[K_RIGHT]:
        glRotatef(1, 0, 1, 0)


def Animate3D(verticies, nextvert, edges, surfaces, colors):
    anivert = np.copy(verticies)
    for n in range(60):
        for i in range(int(verticies.size/3)):
            dx = nextvert[i][0] - verticies[i][0]
            dy = nextvert[i][1] - verticies[i][1]
            dz = nextvert[i][2] - verticies[i][2]
            temp = translate3D(np.array([anivert[i]]), dx/60, dy/60, dz/60)
            anivert[i] = temp[0]
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rotateScreen()
        ShadowCube(verticies, edges, surfaces)
        Cube(anivert, edges, surfaces, colors)
        Sumbu3D()
        pygame.display.flip()
        pygame.time.wait(50)
    return


def Animate2D(verticies, nextvert):
	anivert = np.copy(verticies)
	for n in range(60):
		for i in range(int(verticies.size/2)):
			dx = nextvert[i][0] - verticies[i][0]
			dy = nextvert[i][1] - verticies[i][1]
			temp = translate2D(np.array([anivert[i]]), dx/60, dy/60)
			anivert[i] = temp[0]
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		rotateScreen()
		ShadowShape(verticies)
		Shape(anivert)
		Sumbu2D()
		pygame.display.flip()
		pygame.time.wait(50)
	return


class getCommand (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cmd
        global commandexist
        global multicmd
        while cmd != 'exit':
            cmd = input("Masukan command : ")
            temp = cmd.split(' ')
            if temp[0] == 'multiple':
                for n in range(int(temp[1])):
                    multicmd.append(input('>> Masukan command ke-' + str(n+1) + ' : '))
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
            verticies = np.append(verticies, vertex, axis=0)
    return verticies


def main():

    print("Pilih Mode:\n1. 2D\n2. 3D")
    mode = int(input("Masukan pilihan : "))
    while mode != 1 and mode != 2:
        print("Masukan salah!")
        mode = int(input("Masukan pilihan : "))
    if mode == 1:
        main2D()
    else:
        main3D()
    pygame.display.quit
    pygame.quit


def main3D():
    verticies = np.array([
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
        [0, 1],
        [0, 3],
        [0, 4],
        [2, 1],
        [2, 3],
        [2, 7],
        [6, 3],
        [6, 4],
        [6, 7],
        [5, 1],
        [5, 4],
        [5, 7]
    ])

    surfaces = np.array([
        [0, 1, 2, 3],
        [3, 2, 7, 6],
        [6, 7, 5, 4],
        [4, 5, 1, 0],
        [1, 5, 7, 2],
        [4, 0, 3, 6]
    ])
    colors = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 1, 1]
    ])
    initvert = np.copy(verticies)
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Transformation")
    gluPerspective(45, (display[0]/display[1]), 0.1, 4000.0)
    glTranslatef(0.0, 0.0, -1500.0)
    glRotatef(30, 1, 1, 1)
    global cmd
    global commandexist
    global multicmd
    cmd = ""
    commandexist = False
    multicmd = []
    threadcmd = getCommand()
    threadcmd.start()
    while cmd != 'exit':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rotateScreen()
        if commandexist:
            arg = cmd.split(' ')
            if arg[0] == 'translate':
                dx = float(arg[1])
                dy = float(arg[2])
                dz = float(arg[3])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = translate3D(nextvert, dx/60, dy/60, dz/60)
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies, edges, surfaces)
                    Cube(nextvert, edges, surfaces, colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = translate3D(verticies, dx, dy, dz)
            elif arg[0] == 'dilate':
                k = float(arg[1])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = dilate3D(nextvert, k**(1./60))
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies, edges, surfaces)
                    Cube(nextvert, edges, surfaces, colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = dilate3D(verticies, k)
            elif arg[0] == 'rotate':
                a = float(arg[1])
                b = float(arg[2])
                c = float(arg[3])
                degree = float(arg[4])
                nextvert = np.copy(verticies)
                for n in range(60):
                      nextvert = rotate3D(nextvert, a, b, c, degree/60)
                      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                      ShadowCube(verticies, edges, surfaces)
                      Cube(nextvert, edges, surfaces, colors)
                      Sumbu3D()
                      pygame.display.flip()
                      pygame.time.wait(round(3000/60))
                verticies = rotate3D(verticies,a,b,c,degree)
            elif arg[0] == 'shear':
                param1 = (arg[1])
                param2 = (arg[2])
                k = float(arg[3])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = shear3D(nextvert,param1,param2,(k/60))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = shear3D(verticies,param1,param2,k)
            elif arg[0] == 'stretch' :
                param = (arg[1])
                k = float(arg[2])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = stretch3D(nextvert,param,(k**(1./60)))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowCube(verticies,edges,surfaces)
                    Cube(nextvert,edges,surfaces,colors)
                    Sumbu3D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = stretch3D(verticies,param,k)
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
                nextvert = np.copy(verticies)
                verticies = custom3D(verticies,a,b,c,d,e,f,g,h,i)
                Animate3D(nextvert,verticies,edges,surfaces,colors)
            elif arg[0] == 'reflect' :
                param = arg[1]
                Animate3D(verticies, reflect3D(verticies, param), edges, surfaces, colors)
                verticies = reflect3D(verticies,param)
            elif arg[0] == 'reset':
                Animate3D(verticies,initvert,edges,surfaces,colors)
                verticies = np.copy(initvert)
            elif arg[0] == 'multiple':
                for cmd in multicmd:
                    arg = cmd.split(' ')
                    if arg[0] == 'translate':
                        dx = float(arg[1])
                        dy = float(arg[2])
                        dz = float(arg[3])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = translate3D(nextvert, dx/60, dy/60, dz/60)
                            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            ShadowCube(verticies, edges, surfaces)
                            Cube(nextvert, edges, surfaces, colors)
                            Sumbu3D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = translate3D(verticies, dx, dy, dz)
                    elif arg[0] == 'dilate':
                        k = float(arg[1])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = dilate3D(nextvert, k**(1./60))
                            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            ShadowCube(verticies, edges, surfaces)
                            Cube(nextvert, edges, surfaces, colors)
                            Sumbu3D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = dilate3D(verticies, k)
                    elif arg[0] == 'rotate':
                        a = float(arg[1])
                        b = float(arg[2])
                        c = float(arg[3])
                        degree = float(arg[4])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = rotate3D(nextvert, a, b, c, degree/60)
                            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            ShadowCube(verticies, edges, surfaces)
                            Cube(nextvert, edges, surfaces, colors)
                            Sumbu3D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = rotate3D(verticies,a,b,c,degree)
                    elif arg[0] == 'shear':
                        param1 = (arg[1])
                        param2 = (arg[2])
                        k = float(arg[3])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = shear3D(nextvert,param1,param2,(k/60))
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowCube(verticies,edges,surfaces)
                            Cube(nextvert,edges,surfaces,colors)
                            Sumbu3D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = shear3D(verticies,param1,param2,k)
                    elif arg[0] == 'stretch' :
                        param = (arg[1])
                        k = float(arg[2])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = stretch3D(nextvert,param,(k**(1./60)))
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowCube(verticies,edges,surfaces)
                            Cube(nextvert,edges,surfaces,colors)
                            Sumbu3D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = stretch3D(verticies,param,k)
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
                        nextvert = np.copy(verticies)
                        verticies = custom3D(verticies,a,b,c,d,e,f,g,h,i)
                        Animate3D(nextvert,verticies,edges,surfaces,colors)
                    elif arg[0] == 'reflect' :
                        param = arg[1]
                        Animate3D(verticies, reflect3D(verticies, param), edges, surfaces, colors)
                        verticies = reflect3D(verticies,param)
                    elif arg[0] == 'reset':
                        Animate3D(verticies,initvert,edges,surfaces,colors)
                        verticies = np.copy(initvert)
                multicmd = []
            commandexist = False
        Cube(verticies,edges,surfaces,colors)
        Sumbu3D()
        pygame.display.flip()
        pygame.time.wait(1)

def main2D():
    global N
    verticies = inputVerticies()
    initvert = verticies
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("2D Transformation")
    gluPerspective(45, (display[0]/display[1]), 0.1, 4000.0)
    glTranslatef(0.0,0.0, -1500.0)
    global cmd
    global commandexist
    global multicmd
    cmd = ""
    commandexist = False
    multicmd = []
    threadcmd = getCommand()
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
                dx = float(arg[1])
                dy = float(arg[2])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = translate2D(nextvert,dx/60,dy/60)
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowShape(verticies)
                    Shape(nextvert)
                    Sumbu2D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = translate2D(verticies,dx,dy)
            elif arg[0] == 'dilate':
                k = float(arg[1])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = dilate2D(nextvert,k**(1./60))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowShape(verticies)
                    Shape(nextvert)
                    Sumbu2D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = dilate2D(verticies,k)
            elif arg[0] == 'rotate':
                degree = float(arg[1])
                x = float(arg[2])
                y = float(arg[3])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = rotate2D(nextvert,(degree/60), x, y)
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowShape(verticies)
                    Shape(nextvert)
                    Sumbu2D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = rotate2D(verticies, degree, x, y)
            elif arg[0] == 'shear' :
                param = (arg[1])
                k = float(arg[2])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = shear2D(nextvert,param,(k/60))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowShape(verticies)
                    Shape(nextvert)
                    Sumbu2D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = shear2D(verticies,param,k)
            elif arg[0] == 'stretch' :
                param = (arg[1])
                k = float(arg[2])
                nextvert = np.copy(verticies)
                for n in range(60):
                    nextvert = stretch2D(nextvert,param,(k**(1./60)))
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    ShadowShape(verticies)
                    Shape(nextvert)
                    Sumbu2D()
                    pygame.display.flip()
                    pygame.time.wait(round(3000/60))
                verticies = stretch2D(verticies,param,k)
            elif arg[0] == 'custom' :
                a = float(arg[1])
                b = float(arg[2])
                c = float(arg[3])
                d = float(arg[4])
                Animate2D(verticies, custom2D(verticies,a,b,c,d))
                verticies = custom2D(verticies,a,b,c,d)
            elif arg[0] == 'reflect' :
                param = arg[1]
                Animate2D(verticies,reflect2D(verticies, param))
                verticies = reflect2D(verticies, param)
            elif arg[0] == 'reset':
                Animate2D(verticies, initvert)
                verticies = initvert
            elif arg[0] == 'multiple':

                #Start Multiple

                for cmd in multicmd:
                    arg = cmd.split(' ')
                    if arg[0] == 'translate':
                        dx = float(arg[1])
                        dy = float(arg[2])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = translate2D(nextvert,dx/60,dy/60)
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowShape(verticies)
                            Shape(nextvert)
                            Sumbu2D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = translate2D(verticies,dx,dy)
                    elif arg[0] == 'dilate':
                        k = float(arg[1])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = dilate2D(nextvert,k**(1./60))
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowShape(verticies)
                            Shape(nextvert)
                            Sumbu2D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = dilate2D(verticies,k)
                    elif arg[0] == 'rotate':
                        degree = float(arg[1])
                        x = float(arg[2])
                        y = float(arg[3])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = rotate2D(nextvert,(degree/60), x, y)
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowShape(verticies)
                            Shape(nextvert)
                            Sumbu2D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = rotate2D(verticies, degree, x, y)
                    elif arg[0] == 'shear' :
                        param = (arg[1])
                        k = float(arg[2])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = shear2D(nextvert,param,(k/60))
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowShape(verticies)
                            Shape(nextvert)
                            Sumbu2D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = shear2D(verticies,param,k)
                    elif arg[0] == 'stretch' :
                        param = (arg[1])
                        k = float(arg[2])
                        nextvert = np.copy(verticies)
                        for n in range(60):
                            nextvert = stretch2D(nextvert,param,(k**(1./60)))
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            ShadowShape(verticies)
                            Shape(nextvert)
                            Sumbu2D()
                            pygame.display.flip()
                            pygame.time.wait(round(3000/60))
                        verticies = stretch2D(verticies,param,k)
                    elif arg[0] == 'custom' :
                        a = float(arg[1])
                        b = float(arg[2])
                        c = float(arg[3])
                        d = float(arg[4])
                        Animate2D(verticies, custom2D(verticies,a,b,c,d))
                        verticies = custom2D(verticies,a,b,c,d)
                    elif arg[0] == 'reflect' :
                        param = arg[1]
                        Animate2D(verticies,reflect2D(verticies, param))
                        verticies = reflect2D(verticies, param)
                    elif arg[0] == 'reset':
                        Animate2D(verticies, initvert)
                        verticies = initvert
                multicmd = []
                #End Multiple

            commandexist = False
        Shape(verticies)
        Sumbu2D()
        pygame.display.flip()
        pygame.time.wait(1)

main()
