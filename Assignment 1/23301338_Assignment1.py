#Task1

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

WIDTH, HEIGHT = 500, 500
rainAngle = 0.0
BrightSky =0.0
rain_arr = []

for i in range(100):
    x1 = random.uniform(-250,250)
    y1= random.uniform(-250,250)
    rain_arr.append([x1,y1])
    
def drew_bg():
    
    glBegin(GL_TRIANGLES)
    glColor3f(BrightSky, BrightSky, BrightSky)
    
    glVertex2f(-250, 250)
    glVertex2f(-250, 50)
    glVertex2f(250, 50)
    
    glVertex2f(-250, 250)
    glVertex2f(250, 50)
    glVertex2f(250, 250)
    glEnd()
    
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.35, 0.194)
    
    glVertex2f(-250, 50)
    glVertex2f(-250, -250)
    glVertex2f(250, -250)
    
    glVertex2f(250, -250)
    glVertex2f(250, 50)
    glVertex2f(-250, 50)
    glEnd()
    
    
def treeDraw():
    
    glBegin(GL_TRIANGLES)
    x0_rgt =100
    y_peak = 50
    w = 25
    
    for i in range(6):
        x1 = x0_rgt + i* w
        x2  = x1 + w
        glColor3f(0.138, 0.309, 0.117)
        glVertex2f(x1, 0)
        glVertex2f(x2, 0)
        glColor3f(0.455, 0.718, 0.18)
        glVertex2f((x1+ x2) /2, y_peak)
        
    glEnd()
    
    glBegin(GL_TRIANGLES)
    x0_left = -100
    wleft = -25
    
    for i in range(6):
        x1 = x0_left +i * wleft
        x2 = x1 + wleft
        glColor3f(0.138, 0.309, 0.117)
        glVertex2f(x1, 0)
        glVertex2f(x2, 0)
        
        glColor3f(0.455, 0.718, 0.18)
        glVertex2f((x1 + x2) / 2, y_peak)
        
    glEnd()
    
def draw_house():
    glBegin(GL_TRIANGLES)
    glColor3f(0.992, 0.933, 0.957)
    glVertex2f(-100, 75)
    glVertex2f(100, -50)
    glVertex2f(-100, -50)
    glVertex2f(100, -50)
    glVertex2f(-100, 75)
    glVertex2f(100, 75)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.84, 0.75, 0.68)
    glVertex2f(-25,25)
    glVertex2f(25, -50)
    glVertex2f(25, 25)
    glVertex2f(25, -50)
    glVertex2f(-25, 25)
    glVertex2f(-25, -50)
    glEnd()
    
    
    glColor3f(0.671, 0.225, 0.345)
    glBegin(GL_TRIANGLES)
    glVertex2f(-145, 75)
    glVertex2f(145, 75)
    glVertex2f(0, 150)
    glEnd()
    
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.31, 0.29, 0.31)
    glVertex2f(10,-8)
    glVertex2f(14, -4)
    glVertex2f(14, -8)
    glVertex2f(14, -4)
    glVertex2f(10, -4)
    glVertex2f(10, -8)
    glEnd()
    
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.56, 0.69, 0.82)
    glVertex2f(50, 25)
    glVertex2f(75, 0)
    glVertex2f(50, 0)
    glVertex2f(75, 25)
    glVertex2f(50, 25)
    glVertex2f(75, 0)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.56, 0.69, 0.82)
    glVertex2f(-50, 25)
    glVertex2f(-75, 0)
    glVertex2f(-50, 0)
    
    glVertex2f(-75, 25)
    glVertex2f(-50, 25)
    glVertex2f(-75, 0)
    glEnd()
    
    
    glLineWidth(1.5)
    glColor3f(0.31, 0.29, 0.31)
    glBegin(GL_LINES)
    
    glVertex2f(62.5, 0)
    glVertex2f(62.5, 25)
    glVertex2f(50, 12.5)
    glVertex2f(75, 12.5)
    
    glVertex2f(-62.5, 0)
    glVertex2f(-62.5, 25)
    glVertex2f(-50, 12.5)
    glVertex2f(-75, 12.5)
    glEnd()
    
    
def rainDraw():
    global rainAngle, rain_arr
    
    glLineWidth(2)
    glColor3f(0.136, 0.787, 1.0)
    
    glBegin(GL_LINES)
    for i in rain_arr:
        x,y = i
        glVertex2f(x, y)
        glVertex2f(x+ rainAngle* 2, y-10)
    glEnd()
    
    for i in rain_arr:
        i[0] += rainAngle
        i[1] -= 2
        
        if i[0] > 250:
            i[0] = -250
        elif i[0] < -250:
            i[0] = 250
            
        if i[1] < -260:
            i[0] = random.uniform(-250, 250)
            i[1] = 250
        
def windControl (key, x, y):
    global rainAngle
    if key == GLUT_KEY_RIGHT:
        rainAngle += 0.25
    elif key == GLUT_KEY_LEFT:
        rainAngle -= 0.25
        
    glutPostRedisplay()
    
def dayNight(key,x,y):
    global BrightSky
    if key == b'n':
        BrightSky = max(0.0, BrightSky- 0.1)
        
    elif key == b'd':
        BrightSky = min(1.0, BrightSky+0.1)
    glutPostRedisplay() 


def animate():
    glutPostRedisplay()
    
def set_projection():
    glViewport(0,0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    set_projection()
    glLoadIdentity()
    
    drew_bg()
    treeDraw()
    draw_house()
    rainDraw()
    
    glutSwapBuffers()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Task-1: Building a House in Rainfall")
    glutInitWindowPosition(100, 100)
    
    glutDisplayFunc(display)
    glutKeyboardFunc(dayNight)
    glutSpecialFunc(windControl)
    glutIdleFunc(animate)
    
    glutMainLoop()
    
if __name__ == "__main__":
    main()
        
  #----------------------------------------------------------------------------------------------      



#task 2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

Screen = 500
partList = []

vel = 0.05
isPaused = False
isBlinking = False

isDark = False
lastToggle = 0.0

def mapCoordinate(mouse_x, mouse_y):
    gl_x = mouse_x - (Screen /2)
    gl_y = (Screen /2) - mouse_y
    return gl_x, gl_y

def  createParticles(x, y):
    return {
        'posX' : x,
        'posY' : y,
        'dirX' : random.choice([-1.0, 1.0]),
        'dirY' : random.choice([-1.0, 1.0]),
        'color': (random.random(), random.random(), random.random() )
    }
    
    
def setupView():
    
    glViewport(0,0, Screen, Screen)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glOrtho(-250.0, 250.0, -250.0, 250.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupView()
    
    glPointSize(5.0)
    glBegin(GL_POINTS)
    
    for i in partList:
        if isBlinking and isDark:
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(*i['color'])
            
        glVertex2f(i['posX'],i['posY'])
        
    glEnd()
    glutSwapBuffers()
    
def animate():
    global isDark, lastToggle
    
    currTime = time.time()
    
    if isBlinking:
        if currTime - lastToggle >= 0.5:
            isDark = not isDark
            lastToggle = currTime
            
    else:
        isDark = False

    if not isPaused:
        for i  in partList:
            i['posX'] += i['dirX'] * vel
            i['posY'] += i['dirY'] * vel
            
            if i['posX'] >= 250.0 or i['posX'] <= -250.0:
                i['dirX'] *= -1.0
                
            if i['posY'] >= 250.0 or i['posY'] <= -250.0:
                i['dirY'] *= -1.0
    glutPostRedisplay()
            
                    
def handleMouse( button, state, x, y):
    global isBlinking, isPaused
    
    if isPaused:
        return
    
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            
            gl_x, gl_y = mapCoordinate(x,y)
            partList.append(createParticles(gl_x, gl_y))
        
        elif button == GLUT_LEFT_BUTTON:
            
            isBlinking = not isBlinking    
    
    glutPostRedisplay()
    
def handleKeyboard(key, x, y):
    global isPaused
    
    if key == b' ':
        isPaused = not isPaused
        
    glutPostRedisplay()
    
def handleKeys(key, x, y):
    
    global vel, isPaused
    
    if isPaused:
        return
    
    if key == GLUT_KEY_UP:
        vel += 0.05
        
    elif key == GLUT_KEY_DOWN:
        vel = max(0.0, vel- 0.05)
        
    glutPostRedisplay()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(Screen, Screen)
    glutCreateWindow(b"Task 2: Building the Amazing Box")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(handleMouse)
    glutKeyboardFunc(handleKeyboard)
    glutSpecialFunc(handleKeys)
    
    glutMainLoop()
    
if __name__ == '__main__' :
    main()
          