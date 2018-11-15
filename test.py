import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import threading

def shear2d(verticies, param, k):
	if param == 'x':
		tfMat = np.array([
			[1,k,0],
			[0,1,0],
			[0,0,1]
		])
	elif param == 'y':
		tfMat = np.array([
			[1,0,0],
			[k,1,0],
			[0,0,1]
		])
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV

def custom2d(verticies, a, b, c, d):
	tfMat = np.array([
		[a,b,0],
		[c,d,0],
		[0,0,1]
	])
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV

def stretch2d(verticies, param, k):
	if param == 'x':
		tfMat = np.array([
			[k,0,0],
			[0,1,0],
			[0,0,1]
		])
	elif param == 'y':
		tfMat = np.array([
			[1,0,0],
			[0,k,0],
			[0,0,1]
		])
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV

def translate2d(verticies, dx, dy):
	tfMat = np.array([
		[1,0,dx],
		[0,1,dy],
		[0,0,1]
	])
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV

def dilate2d(verticies, k):
	tfMat = np.array([
		[k,0,0],
		[0,k,0],
		[0,0,1]
	])
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV

def rotate2d(verticies, degree, x, y):
	translateToZeroMat = np.array([
		[1,0,-x],
		[0,1,-y],
		[0,0,1]
	])
	RotateMat = np.array([
		[np.math.cos((degree/360)*2*np.pi),-(np.math.sin((degree/360)*2*np.pi)),0],
		[np.math.sin((degree/360)*2*np.pi),np.math.cos((degree/360)*2*np.pi),0],
		[0,0,1]
	])
	translateBackMat = np.array([
		[1,0,x],
		[0,1,y],
		[0,0,1]
	])
	tfMat = np.matmul(translateBackMat, np.matmul(RotateMat,translateToZeroMat))
	newV = np.empty((0,2), float)
	for vertex in verticies:
		vertex = np.append(vertex , [1])
		temp = np.matmul(tfMat,vertex.T)
		keep = [True,True,False]
		temp = np.array(temp[keep])
		temp = np.array([temp])
		newV = np.vstack((newV, temp))
	return newV


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

def Animate(vertsicies, nextvert, edges, surfaces, colors):
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

def Animate2D(verticies, nextvert):
	anivert = np.copy(verticies)
	for n in range(60):
		for i in range(int(verticies.size/2)):
			dx = nextvert[i][0] - verticies[i][0]
			dy = nextvert[i][1] - verticies[i][1]
			temp = translate2d(np.array([anivert[i]]),dx/60,dy/60)
			anivert[i] = temp[0]
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		rotateScreen()
		#ShadowCube(verticies,edges,surfaces)
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
				dx = float(arg[1])
				dy = float(arg[2])
				nextvert = np.copy(verticies)
				for n in range(60):
					nextvert = translate2d(nextvert,dx/60,dy/60)
					glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
					#ShadowCube(verticies,edges,surfaces)
					Shape(nextvert)
					Sumbu2D()
					pygame.display.flip()
					pygame.time.wait(round(3000/60))
				verticies = translate2d(verticies,dx,dy)
			elif arg[0] == 'dilate':
				k = float(arg[1])
				nextvert = verticies
				for n in range(60):
					nextvert = dilate2d(nextvert,k**(1./60))
					glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
					#ShadowCube(verticies,edges,surfaces)
					Shape(nextvert)
					Sumbu2D()
					pygame.display.flip()
					pygame.time.wait(round(3000/60))
				verticies = dilate2d(verticies,k)
			elif arg[0] == 'rotate':
				degree = float(arg[1])
				x = float(arg[2])
				y = float(arg[3])
				nextvert = verticies
				for n in range(60):
					nextvert = rotate2d(nextvert,(degree/60), x, y)
					glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
					rotateScreen()
					#ShadowCube(verticies,edges,surfaces)
					Shape(nextvert)
					Sumbu2D()
					pygame.display.flip()
					pygame.time.wait(round(3000/60))
				verticies = rotate2d(verticies, degree, x, y)
			elif arg[0] == 'shear' :
				param = (arg[1])
				k = float(arg[2])
				nextvert = verticies
				for n in range(60):
					nextvert = shear2d(nextvert,param,(k/60))
					glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
					rotateScreen()
					#ShadowCube(verticies,edges,surfaces)
					Shape(nextvert)
					Sumbu2D()
					pygame.display.flip()
					pygame.time.wait(round(3000/60))
				verticies = shear2d(verticies,param,k)
			elif arg[0] == 'stretch' :
				param = (arg[1])
				k = float(arg[2])
				nextvert = verticies
				for n in range(60):
					nextvert = stretch2d(nextvert,param,(k**(1./60)))
					glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
					rotateScreen()
					#ShadowCube(verticies,edges,surfaces)
					Shape(nextvert)
					Sumbu2D()
					pygame.display.flip()
					pygame.time.wait(round(3000/60))
				verticies = stretch2d(verticies,param,k)
			elif arg[0] == 'custom' :
				a = float(arg[1])
				b = float(arg[2])
				c = float(arg[3])
				d = float(arg[4])
				Animate2D(verticies, custom2d(verticies,a,b,c,d))
				verticies = custom2d(verticies,a,b,c,d)
			elif arg[0] == 'reset':
				Animate2D(verticies, initvert)
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
			elif arg[0] == 'rotate':
				degreeX = float(arg[1])
				degreeY = float(arg[2])
				degreeZ = float(arg[3])
				x = float(arg[4])
				y = float(arg[5])
				z = float(arg[6])
				verticies = rotate(verticies, degreeX, degreeY, degreeZ, x, y, z)
			elif arg[0] == 'shear' :
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
					Sumbu()
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
			elif arg[0] == 'reset':
				Animate(verticies,initvert,edges,surfaces,colors)
				verticies = np.copy(initvert)
			commandexist = False
			
		
		
		Cube(verticies,edges,surfaces,colors)
		Sumbu3D()

		pygame.display.flip()
		
		pygame.time.wait(1)

main()


