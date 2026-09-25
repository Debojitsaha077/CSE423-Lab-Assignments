import math 
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

gridLen = 600
fY = 120

px, py = 0.0, 0.0
pAng = 0.0
gunAng = 0.0
lyfe = 5
sc = 0
miss = 0
gameOver = False

cheatM = False
cheatV = False
fPerson = False
cheatCool = 0

camAng = 180.0
camHei = 500.0
camRad = 600.0

enm = []
bullet = []

def badEnmy():
    while True:
        ex = random.uniform(-gridLen+ 50, gridLen-50)
        ey = random.uniform(-gridLen+ 50, gridLen-50)
        
        if math.hypot(ex - px, ey - py)> 300:
            return {'x': ex, 'y': ey, 's': 1.0, 'sd': 1}
        
        
def resetGm():
    global px,py, pAng,gunAng,lyfe, sc, miss, gameOver
    global cheatM, cheatV, fPerson, cheatCool
    global camAng, camHei, enm, bullet
    
    px,py =0.0, 0.0
    pAng = 0.0
    gunAng = 0.0
    lyfe = 5
    sc = 0
    miss = 0
    gameOver = False
    cheatM = False
    cheatV = False
    fPerson = False
    cheatCool = 0
    camAng = 180.0
    camHei = 500.0
    bullet = []
    enm = []
    for _ in range(5):
        enm.append(badEnmy())
        

def drawTxt(x, y, text, colour=(1, 1, 1), font= GLUT_BITMAP_HELVETICA_18):
    glColor3f(*colour)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x,y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
        

def keyboardlistener(key, x, y):
    global px, py, pAng, gunAng, cheatM,cheatV, gameOver
    
    if key == b'r' or key == b'R':
        resetGm()
        return
    
    if gameOver:
        return
    
    if key == b'w' or key == b'W' :
        px += math.cos(math.radians(pAng)) *8
        py += math.sin(math.radians(pAng)) *8
        
    elif key == b's' or key == b'S':
        px -= math.cos(math.radians(pAng)) *8
        py -= math.sin(math.radians(pAng)) *8
        
    elif key == b'a' or key == b'A':
            pAng = (pAng +10) % 360
            if not cheatM : gunAng = pAng
            
            
    elif key == b'd' or key == b'D':
            pAng = (pAng -10)% 360
            if not cheatM : gunAng = pAng
            
    elif key == b'c' or key == b'C':
            cheatM = not cheatM
            if not cheatM:
                gunAng = pAng
                
    elif key == b'v' or key == b'V':
            cheatV = not cheatV
        
    if px > gridLen -20 : px = gridLen -20
    if px < -gridLen +20 : px = -gridLen +20
    if py > gridLen -20 : py = gridLen -20
    if py < -gridLen +20 : py = -gridLen +20
    
    
            
def specialkeylist(key, x, y):
    global camAng, camHei
    if key == GLUT_KEY_UP:
        camHei += 15
    elif key == GLUT_KEY_DOWN:
        camHei -= 15
        
    elif key == GLUT_KEY_LEFT:
        camAng = (camAng + 3) % 360
    elif key == GLUT_KEY_RIGHT:
        camAng = (camAng - 3) % 360
        
def mouselist(button, st, x, y):
    global fPerson, bullet
    if button == GLUT_LEFT_BUTTON and st == GLUT_DOWN:
        if not gameOver:
            bullet.append({'x': px, 'y': py, 'a': gunAng})
            
    if button == GLUT_RIGHT_BUTTON and st == GLUT_DOWN:
         fPerson = not fPerson
         

def setCam():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fY, 1.25, 0.1, 1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if fPerson:
        viewAng = gunAng if (cheatM and cheatV) else pAng
        camX = px + math.cos(math.radians(viewAng)) * 15
        camY = py + math.sin(math.radians(viewAng)) * 15
        camZ = 65 
        
        lookX = camX + math.cos(math.radians(viewAng)) * 100
        lookY = camY + math.sin(math.radians(viewAng)) * 100
        
        gluLookAt(camX, camY, camZ, lookX, lookY, camZ, 0, 0, 1)       
        
    else:
        cx = camRad * math.cos(math.radians(camAng))
        cy = camRad * math.sin(math.radians(camAng))
        cz = camHei
        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)
        
def idle():
    global gameOver, lyfe, sc, miss, px, py, gunAng
    global enm, bullet, cheatCool
    
    if not gameOver:
        for b in bullet[:]:
            b['x'] += math.cos(math.radians(b['a'])) * 5
            b['y'] += math.sin(math.radians(b['a'])) * 5
            
            if abs(b['x']) > gridLen or abs(b['y']) > gridLen:
                bullet.remove(b)
                miss += 1
                if miss >= 10:
                    gameOver = True
                    
                continue
            
            for e in enm:
                if math.hypot(b['x'] - e['x'], b['y'] - e['y']) < (22 * e['s']):
                    sc += 10
                    if b in bullet: bullet.remove(b)
                    enm.remove(e)
                    enm.append(badEnmy())
                    break
                
        for e in enm:
            dist = math.hypot(px - e['x'], py - e['y'])
            if dist > 0:
                e['x'] += (px - e['x']) / dist * 0.1 
                e['y'] += (py - e['y']) / dist * 0.1 
                
            e['s'] += e['sd'] * 0.001
            if e['s'] > 1.4: e['sd'] = -1
            elif e['s'] < 0.6: e['sd'] = 1
            
            if dist < 30:
                lyfe -= 1
                enm.remove(e)
                enm.append(badEnmy())
                if lyfe <= 0:
                    gameOver = True
                    
        if cheatM:
            gunAng = (gunAng + 2.0)% 360
            cheatCool -= 1
            
            if cheatCool <= 0:
                for e in enm:
                    angleE = math.degrees(math.atan2(e['y'] - py, e['x'] - px))
                    diff = (angleE - gunAng) % 360
                    if diff > 180: diff -= 360
                    
                    
                    if abs(diff) < 10:
                        bullet.append({'x': px, 'y': py, 'a': angleE})
                        cheatCool = 20
                        break
                        
    glutPostRedisplay() 
    
    
def drawPlay():
    glPushMatrix()
    glTranslatef(px, py, 0)
    
    if gameOver:
        glRotatef(-90, 1, 0, 0) 
        glTranslatef(0, 0, -30) 
        
    glPushMatrix()
    glRotatef(pAng, 0, 0, 1)
    
    glColor3f(0.3, 0.5, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 35)
    glScalef(1.0, 0.6, 1.4)
    glutSolidCube(30)
    glPopMatrix()
    
    glColor3f(0.0, 0.0, 0.8)
    glPushMatrix()
    glTranslatef(0, -10, 20)
    glRotatef(180, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 6, 3, 20, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 10, 20)
    glRotatef(180, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 3, 20, 10, 10)
    glPopMatrix()
    
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 65)
    gluSphere(gluNewQuadric(), 12, 16, 16)
    glPopMatrix()
    
    glPopMatrix()
    glPushMatrix()
    
    glRotatef(gunAng, 0, 0, 1)
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(10, 0, 45)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 6, 3, 40, 10, 10) # 0 radius at top makes it pointed
    glPopMatrix()

    glColor3f(1.0, 0.8, 0.6)

    glPushMatrix()
    glTranslatef(0, 14, 45)
    gluSphere(gluNewQuadric(), 6, 10, 10)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 3, 25, 10, 10) 
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -14, 45)
    gluSphere(gluNewQuadric(), 6, 10, 10)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 3, 25, 10, 10) 
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()
    
def showScr():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setCam()
    
    glBegin(GL_QUADS)
    wall = [
        ((-gridLen, -gridLen, 0), (gridLen, -gridLen, 0), (gridLen, -gridLen, 100), (-gridLen, -gridLen, 100), (0, 0, 1)),
        ((-gridLen, gridLen, 0), (gridLen, gridLen, 0), (gridLen, gridLen, 100), (-gridLen, gridLen, 100), (0, 1, 1)),
        ((-gridLen, -gridLen, 0), (-gridLen, gridLen, 0), (-gridLen, gridLen, 100), (-gridLen, -gridLen, 100), (0, 0, 0.5)),
        ((gridLen, -gridLen, 0), (gridLen, gridLen, 0), (gridLen, gridLen, 100), (gridLen, -gridLen, 100), (0, 1, 0)),
    ]
    
    for w in wall:
        glColor3f(*w[4])
        for i in range(4):
            glVertex3f(*w[i])
            
    for i in range(-gridLen, gridLen, 75):
        for j in range(-gridLen, gridLen, 75):
            if((i // 75)+(j // 75)) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
                
            else:
                glColor3f(0.7, 0.5, 0.95)
                
            glVertex3f(i, j, 0)
            glVertex3f(i + 75, j, 0)
            glVertex3f(i + 75, j + 75, 0)
            glVertex3f(i, j + 75, 0)
            
    glEnd()
    
    drawPlay()
    for e in enm:
        glPushMatrix()
        glTranslatef(e['x'], e['y'], 20)
        glScalef(e['s'], e['s'], e['s'])
        
        glColor3f(1.0, 0.0, 0.0)
        gluSphere(gluNewQuadric(), 15, 16, 16)
        
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, 0, 16)
        gluSphere(gluNewQuadric(), 8, 10, 10)
        glPopMatrix()
        
    for b in bullet:
        glPushMatrix()
        glTranslatef(b['x'], b['y'], 45)
        glRotatef(b['a'], 0, 0, 1)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidCube(8)
        glPopMatrix()
        
    drawTxt(10, 770, f"Player life remaining: {lyfe}")
    drawTxt(10, 740, f"Game Score: {sc}")
    drawTxt(10, 710, f"Player bullet missed: {miss}")
    
    if gameOver:
        drawTxt(350, 450, "Game Over!", colour=(1.0, 0.0, 0.0), font= GLUT_BITMAP_TIMES_ROMAN_24)
        drawTxt(320, 420, "Press 'R' to Restart the arena", colour=(1.0, 0.0, 0.0), font= GLUT_BITMAP_HELVETICA_18)
        
    glutSwapBuffers()
    
    
def main():
    resetGm()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Bullet Frenzy - PyOpenGL")
    
    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(showScr)
    glutKeyboardFunc(keyboardlistener)
    glutSpecialFunc(specialkeylist)
    glutMouseFunc(mouselist)
    glutIdleFunc(idle)

    glutMainLoop()
    
if __name__ == "__main__":
    main()
                
            
                   
                   
        
        
        
    
    