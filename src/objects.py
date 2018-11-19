from OpenGL.GL import *
from OpenGL.GLU import *

def Cube(verticies,edges,surfaces,colors):
# Menyiapkan semua yang diperlukan untuk menampilkan sebuah kubus yang berwarna
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
# Menyiapkan semua yang diperlukan untuk menampilkan sebuah shape yang terbentuk dari
# titik-titik verticies dengan diwarnai tengahnya
	glBegin(GL_POLYGON)
	glColor3fv([255,0,0])
	for i in range(int(verticies.size/2)):
		glVertex2fv(verticies[i])
	glEnd()

	glBegin(GL_LINES)
	glColor3fv([255,255,255])
	for i in range(int(verticies.size/2)):
		if i == 0:
			glVertex2fv(verticies[int(verticies.size/2)-1])
			glVertex2fv(verticies[i])
		else:
			glVertex2fv(verticies[i-1])
			glVertex2fv(verticies[i])
	glEnd()


def ShadowCube(verticies,edges,surfaces):
# Menyiapkan semua yang diperlukan untuk menampilkan sebuah kerangka dari kubus (hanya garis)
    glBegin(GL_LINES)
    glColor3fv([255,255,255])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def ShadowShape(verticies):
# Menyiapkan semua yang diperlukan untuk menampilkan kerangka dari shape (hanya garis antar titik)
    glBegin(GL_LINES)
    glColor3fv([255,255,255])
    for i in range(int(verticies.size/2)):
        if i == 0:
            glVertex2fv(verticies[int(verticies.size/2)-1])
            glVertex2fv(verticies[i])
        else:
            glVertex2fv(verticies[i-1])
            glVertex2fv(verticies[i])
    glEnd()

def Sumbu3D(): 
# Menyiapkan semua yang diperlukan untuk menampilkan sumbu dalam bidang 3D
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
# Menyiapkan semua yang diperlukan untuk menampilkan sumbu dalam bidang 2D 
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
