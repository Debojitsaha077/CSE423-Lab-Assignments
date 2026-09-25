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
    
    glPointSize(10.0)
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
    