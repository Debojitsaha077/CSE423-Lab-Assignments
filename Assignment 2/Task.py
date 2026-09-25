from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

winWidth = 400
winHei = 600
score= 0
gameOver = False
paused = False
cheat = False
lastTime = time.time()

catcherWid = 80
catcherHei = 20
catcherX = winWidth //2
catcherY = 20
catcherSpeed = 300

diamondS = 15
diamondX = random.randint(diamondS, winWidth- diamondS)
diamondY = winHei -60
diamondSpeedBase = 150
diamondSpeed = diamondSpeedBase
diamondColor = [random.random(), random.random(), random.random()]

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 -y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
        if dx >= 0 and dy < 0: return 7
        
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5
        if dx >= 0 and dy < 0: return 6
        
    
def toZone_0(zone, x, y):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y
    
def fromZone_0(zone, x, y):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y
    
def drawMidpointLine(x1, y1, x2, y2, color):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    zone = findZone(x1, y1, x2, y2)
    x1_0, y1_0 = toZone_0(zone, x1, y1)
    x2_0, y2_0 = toZone_0(zone, x2, y2)
    
    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = 2* dy - dx
    inc_E = 2* dy
    inc_NE = 2* (dy- dx)
    
    x = x1_0
    y = y1_0
    
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    
    while x <= x2_0:
        origX, origY = fromZone_0(zone, x, y)
        glVertex2f(origX, origY)
        if d> 0 :
            d += inc_NE
            y += 1
        else:
            d+= inc_E
            
        x += 1
        
    glEnd()
    
def draw_catcher():
    global catcherX, catcherY, catcherWid, catcherHei, gameOver
    color = [1.0, 0.0, 0.0] if gameOver else [1.0, 1.0, 1.0]
    w = catcherWid/2
    h = catcherHei
    
    drawMidpointLine(catcherX - w, catcherY +h, catcherX +w, catcherY + h, color )
    drawMidpointLine(catcherX - w +10, catcherY, catcherX +w -10, catcherY , color )
    drawMidpointLine(catcherX - w, catcherY +h, catcherX-w+10 , catcherY, color )
    drawMidpointLine(catcherX + w, catcherY +h, catcherX +w -10, catcherY, color )

def drawDiamond():
    global diamondX, diamondY, diamondS, diamondColor, gameOver
    if gameOver:
        return
    
    s = diamondS
    
    drawMidpointLine(diamondX, diamondY+ s, diamondX +s-5, diamondY, diamondColor )
    drawMidpointLine(diamondX, diamondY+ s, diamondX -s+5, diamondY, diamondColor )
    drawMidpointLine(diamondX + s -5, diamondY, diamondX, diamondY-s, diamondColor )
    drawMidpointLine(diamondX -s +5, diamondY, diamondX, diamondY -s, diamondColor )

def drawUni_buttons():
    drawMidpointLine(40, 560, 10, 560, [0.0, 1.0, 1.0])
    drawMidpointLine(10, 560, 25, 575, [0.0, 1.0, 1.0])
    drawMidpointLine(10, 560, 25, 545, [0.0, 1.0, 1.0])
    
    
    if paused:
        drawMidpointLine(190, 575, 190, 545, [1.0, 0.75, 0.0])
        drawMidpointLine(190, 575, 215, 560, [1.0, 0.75, 0.0])
        drawMidpointLine(190, 545, 215, 560, [1.0, 0.75, 0.0])
        
    else:
        drawMidpointLine(195, 575, 195, 545, [1.0, 0.75, 0.0])
        drawMidpointLine(205, 575, 205, 545, [1.0, 0.75, 0.0])
        
    
    drawMidpointLine(360, 575, 390, 545, [1.0, 0.0, 0.0])
    drawMidpointLine(360, 545, 390, 575, [1.0, 0.0, 0.0])
    

def resetDiamond():
    global diamondX, diamondY, diamondColor
    diamondX = random.randint(20, winWidth-20)
    diamondY = winHei - 60
    
    diamondColor = [random.uniform(0.5, 1.0),random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]
    
    
def restartGame():
    global score, gameOver,paused, diamondSpeed, catcherX
    score = 0 
    gameOver = False
    paused = False
    diamondSpeed = diamondSpeedBase
    catcherX = winWidth // 2
    print( "Starting Over")
    print( f"Score : {score}")
    resetDiamond()
    
def checkCollision():
    d_x = diamondX - (diamondS - 5)
    d_y = diamondY - diamondS
    d_w = (diamondS -5) * 2
    d_h = diamondS * 2
    
    
    c_x = catcherX - (catcherWid / 2)
    c_y = catcherY
    c_w = catcherWid
    c_h = catcherHei
    
    
    return (d_x < c_x + c_w and
            d_x + d_w > c_x and
            d_y < c_y + c_h and
            d_y + d_h > c_y)
 
    
def keyboardListener(key, x, y):
    global cheat
    if key == b'c':
        cheat = not cheat
        state = "Activated" if cheat else "Deactivated"
        print( f"Cheat Mode {state}!")
    glutPostRedisplay()
    

def specialListener(key, x, y):
    global catcherX
    if paused or gameOver or cheat:
        return
    
    step = 25
    if key == GLUT_KEY_LEFT:
        catcherX = max(catcherWid // 2, catcherX- step)
    
    elif key == GLUT_KEY_RIGHT:
        catcherX = min(winWidth -(catcherWid // 2), catcherX + step)
    glutPostRedisplay()
    
    
def mouselistener(button, state, x,y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        gl_y = winHei - y
        
        if 530 <= gl_y <= 590:
            if 0 <= x <= 60:
                restartGame()
                
            elif 170 <= x <= 230:
                if not gameOver:
                    paused = not paused
                    
            elif 340 <= x <= 400:
                print(f"Goodbye! Final Score: {score}")
                glutLeaveMainLoop()
                
    glutPostRedisplay()
    

def animate():
    global diamondY, catcherX, lastTime, score, gameOver, diamondSpeed
    
    currTime = time.time()
    dt = currTime - lastTime
    lastTime = currTime
    
    
    if paused or gameOver:
        glutPostRedisplay()
        return
    
    diamondY -= diamondSpeed * dt
    
    if cheat:
        if catcherX < diamondX:
            catcherX += catcherSpeed * dt
        elif catcherX > diamondX:
            catcherX -= catcherSpeed * dt
            
        
        catcherX = max(catcherWid // 2, min(winWidth- (catcherWid // 2), catcherX))
        
    if checkCollision():
        score +=1
        print(f"Score: {score}")
        diamondSpeed +=10
        resetDiamond()
        
    elif diamondY + diamondS < catcherY:
        gameOver = True
        print(f"Game Over! Final Score: {score}")
        
    glutPostRedisplay()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    drawUni_buttons()
    draw_catcher()
    drawDiamond()
    glutSwapBuffers()
    
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, winWidth, 0, winHei)
    

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHei)
    glutInitWindowPosition(100, 100)
    
    
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS )
    glutCreateWindow(b"Catch the Diamonds!")
    
    init()
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialListener)
    glutMouseFunc(mouselistener)
    
    print("Welcome to Catch the Diamonds!")
    print(f"Score: {score}")
    
    glutMainLoop()
    
        
        
            