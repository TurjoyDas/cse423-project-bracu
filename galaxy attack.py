from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

tempi = 0
sx = 500
sy = random.randint(50, 450)
score = 0
invisiblescore = -1
bossL_or_R = random.randint(0, 1)
game_state = 'Playing'
shooterlist = [[250, 70, 9]]
bosslist = [250, 400, 40]
bulletx, bullety = -1, -1
laserx, lasery = -1, -1
heartx, hearty = random.randint(50, 450), 470
invisiblex, invisibley = random.randint(50, 250), 470
bossbulletx, bossbullety = -1, -1
myhealthboss = 9
heartflag = True
invisibleflag = False
bullet1flag = False
bullet2flag = False
bullet3flag = False
bossflag = False
laserflag = False
bosshealth = 50

starlist = []
enemybulletflag = [False, False, False, False, False]
bossbulletflag = [False, False, False, False, False]
bossbulletlist = [[bosslist[0] - 90, bosslist[1]], [bosslist[0] - 50, bosslist[1]], [bosslist[0], bosslist[1]],
                 [bosslist[0] + 50, bosslist[1]], [bosslist[0] + 90, bosslist[1]]]

for i in range(300):
   starlist.append([random.randint(0, 500), random.randint(0, 500)])
enemylist = []
enemyarea = []
l = [-1, -1, -1, -1,-1]
for i in range(5):
   enemyarea.append(l)
a = 0
b = a + 80
for i in range(5):
   randomx = random.randint(a, b)
   randomy = random.randint(300, 420)
   randomshape = random.choice(['Box', 'Cir', 'Trig'])
   a += 100
   b = a + 80
   enemylist.append([randomx, randomy, 3, randomshape, randomx, randomy])

enemylistafterboss = [-100, -100, 3, 'Cir', -100, -100]


def draw_points(x, y, ps=1):
   glPointSize(ps)
   glBegin(GL_POINTS)
   glVertex2f(x, y)
   glEnd()


def midpoint_circle(cx, cy, r, half=False, heart=False):
   d = 1 - r
   x = 0
   y = r
   if half == True and heart == False:
       draw_points(x + cx, y + cy)
       draw_points(-x + cx, y + cy)

   if heart == True and half == False:
       draw_points(x + cx, y + cy)
       draw_points(y + cx, x + cy)
       draw_points(-x + cx, y + cy)
       draw_points(-y + cx, x + cy)

   if heart == False and half == False:
       draw_points(x + cx, y + cy)
       draw_points(-x + cx, y + cy)
       draw_points(-y + cx, x + cy)
       draw_points(-y + cx, -x + cy)
       draw_points(-x + cx, -y + cy)
       draw_points(x + cx, -y + cy)
       draw_points(y + cx, -x + cy)
       draw_points(y + cx, x + cy)

   while x < y:
       if d < 0:
           d = d + 2 * x + 3  # e
           x += 1
       else:
           d = d + 2 * x - 2 * y + 5  # se
           x += 1
           y -= 1

       if half == True and heart == False:
           draw_points(x + cx, y + cy)
           draw_points(-x + cx, y + cy)

       if heart == True and half == False:
           draw_points(x + cx, y + cy)
           draw_points(y + cx, x + cy)
           draw_points(-x + cx, y + cy)
           draw_points(-y + cx, x + cy)

       if heart == False and half == False:
           draw_points(x + cx, y + cy)
           draw_points(-x + cx, y + cy)
           draw_points(-y + cx, x + cy)
           draw_points(-y + cx, -x + cy)
           draw_points(-x + cx, -y + cy)
           draw_points(x + cx, -y + cy)
           draw_points(y + cx, -x + cy)
           draw_points(y + cx, x + cy)


def midpoint(x1, y1, x2, y2):
   zone = myzone(x1, y1, x2, y2)
   x1, y1 = n_to_zero(x1, y1, zone)
   x2, y2 = n_to_zero(x2, y2, zone)
   dx = x2 - x1
   dy = y2 - y1
   dinit = 2 * dy - dx
   dne = 2 * dy - 2 * dx
   de = 2 * dy
   for i in range(int(x1), int(x2)):
       a, b = zero_to_n(x1, y1, zone)
       if dinit >= 0:
           dinit = dinit + dne
           draw_points(a, b)
           x1 += 1
           y1 += 1
       else:
           dinit = dinit + de
           draw_points(a, b)
           x1 += 1


def myzone(x1, y1, x2, y2):
   dx = x2 - x1
   dy = y2 - y1
   if abs(dx) >= abs(dy):
       if dx >= 0 and dy >= 0:
           return 0
       elif dx <= 0 and dy >= 0:
           return 3
       elif dx <= 0 and dy <= 0:
           return 4
       elif dx >= 0 and dy <= 0:
           return 7
   else:
       if dx >= 0 and dy >= 0:
           return 1
       elif dx <= 0 and dy >= 0:
           return 2
       elif dx <= 0 and dy <= 0:
           return 5
       elif dx >= 0 and dy <= 0:
           return 6


def zero_to_n(x, y, zone):
   if zone == 0:
       return x, y
   if zone == 1:
       return y, x
   if zone == 2:
       return -y, x
   if zone == 3:
       return -x, y
   if zone == 4:
       return -x, -y
   if zone == 5:
       return -y, -x
   if zone == 6:
       return y, -x
   if zone == 7:
       return x, -y


def n_to_zero(x, y, zone):
   if zone == 0:
       return x, y
   elif zone == 1:
       return y, x
   elif zone == 2:
       return y, -x
   elif zone == 3:
       return -x, y
   elif zone == 4:
       return -x, -y
   elif zone == 5:
       return -y, -x
   elif zone == 6:
       return -y, x
   elif zone == 7:
       return x, -y


def specialKeyListener(key, x, y):
   global shooter, game_state, laserpointlist, laserflag
   if key == GLUT_KEY_LEFT and game_state == 'Playing':
       laserflag = False
       for i in shooterlist:
           i[0] -= 10
           if i[0] < 20:
               i[0] = 20
   elif key == GLUT_KEY_RIGHT and game_state == 'Playing':
       laserflag = False
       for i in shooterlist:
           i[0] += 10
           if i[0] > 480:
               i[0] = 480
   elif key == GLUT_KEY_UP and game_state == 'Playing':
       laserflag = False
       for i in shooterlist:
           i[1] += 5
           if i[1] > 200:
               i[1] = 200
   elif key == GLUT_KEY_DOWN and game_state == 'Playing':
       laserflag = False
       for i in shooterlist:
           i[1] -= 5
           if i[1] - 54 < 0:
               i[1] = 54

   glutPostRedisplay()


def mouseListener(button, state, x, y):
   pass


def keyboardListener(key, x, y):
   global bullet1flag, bulletx, bullety, shooterlist, laserflag, laserx, lasery, laserpointlist, enemybulletflag, bossflag, bossbulletflag, bosslist
   global bossbulletlist
   if key == b' ' and game_state == 'Playing' and bullet1flag == False:
       bulletx, bullety = shooterlist[0][0], shooterlist[0][1] + 1
       bullet1flag = True

   elif key == b'l' and game_state == 'Playing' and laserflag == False:
       laserx, lasery = shooterlist[0][0], shooterlist[0][1] + 1
       laserflag = True
       bullet1flag = True
   elif key == b'l' and game_state == 'Playing' and laserflag == True:
       laserflag = False
       bullet1flag = False
   if bossflag == False:
       if key == b'1' and game_state == 'Playing' and enemybulletflag[0] == False:
           enemybulletflag[0] = True
       elif key == b'2' and game_state == 'Playing' and enemybulletflag[1] == False:
           enemybulletflag[1] = True

       elif key == b'3' and game_state == 'Playing' and enemybulletflag[2] == False:
           enemybulletflag[2] = True

       elif key == b'4' and game_state == 'Playing' and enemybulletflag[3] == False:
           enemybulletflag[3] = True

       elif key == b'5' and game_state == 'Playing' and enemybulletflag[4] == False:
           enemybulletflag[4] = True

   else:
       if key == b'a' and game_state == 'Playing':
           if bosslist[0] >= 105:
               bosslist[0] = bosslist[0] - 5
               for i in range(5):
                   bossbulletlist[i][0] -= 5

       if key == b'd' and game_state == 'Playing':
           if bosslist[0] <= 395:
               bosslist[0] = bosslist[0] + 5
               for i in range(5):
                   bossbulletlist[i][0] += 5

       if key == b'1' and game_state == 'Playing' and bossbulletflag[0] == False:

           bossbulletflag[0] = True

       elif key == b'2' and game_state == 'Playing' and bossbulletflag[1] == False:
           bossbulletflag[1] = True

       elif key == b'3' and game_state == 'Playing' and bossbulletflag[2] == False:
           bossbulletflag[2] = True

       elif key == b'4' and game_state == 'Playing' and bossbulletflag[3] == False:
           bossbulletflag[3] = True

       elif key == b'5' and game_state == 'Playing' and bossbulletflag[4] == False:
           bossbulletflag[4] = True


def shooter(x, y, life, invisible=None):
   if invisible != None:
       glColor3f(0.5, 0.5, 0.5)
   else:
       if 1 <= life <= 3:
           glColor3f(1, 0, 0)
       elif 4 <= life <= 6:
           glColor3f(1, 1, 0)
       elif 7 <= life <= 9:
           glColor3f(0, 1, 0)
   midpoint(x - 20, y - 40, x, y)
   midpoint(x + 20, y - 40, x, y)
   midpoint(x - 20, y - 40, x + 20, y - 40)
   midpoint_circle(x - 10, y - 47, 7)
   midpoint_circle(x + 10, y - 47, 7)
   midpoint(x - 10, y - 20, x - 20, y - 20)
   midpoint(x - 15, y - 30, x - 20, y - 20)
   midpoint(x + 10, y - 20, x + 20, y - 20)
   midpoint(x + 15, y - 30, x + 20, y - 20)


def bullet(bx, by, a, b, c):
   global shooter
   glColor3f(a, b, c)
   midpoint_circle(bx, by, 3)
   # draw_points(bx,by,5)


def enemy(x, y, life, shape):
   if 0.1 <= life <= 1:
       glColor3f(1, 0, 0)
   elif 1.1 <= life <= 2:
       glColor3f(1, 1, 0)
   elif 2.1 <= life <= 3:
       glColor3f(0, 0.6, 1)

   if shape == 'Box':
       midpoint(x + 15, y, x - 15, y)
       midpoint(x - 15, y, x - 15, y + 30)
       midpoint(x + 15, y, x + 15, y + 30)
       midpoint(x - 15, y + 30, x + 15, y + 30)
       midpoint(x - 15, y + 30, x + 15, y)
       midpoint(x - 15, y, x + 15, y + 30)
       midpoint_circle(x - 8, y + 36, 6)
       midpoint_circle(x + 8, y + 36, 6)
   elif shape == "Cir":
       midpoint_circle(x, y + 14, 15)
       midpoint_circle(x, y + 14, 7)
       midpoint_circle(x - 8, y + 34, 6)
       midpoint_circle(x + 8, y + 34, 6)
   else:
       midpoint(x - 15, y + 30, x + 15, y + 30)
       midpoint(x - 15, y + 30, x, y)
       midpoint(x + 15, y + 30, x, y)
       midpoint(x - 8, y + 15, x + 8, y + 15)
       midpoint_circle(x - 8, y + 36, 6)
       midpoint_circle(x + 8, y + 36, 6)


def boss(x, y, life):
   if life <= 0:
       glColor3f(0, 0, 0)
       return 'Game Over'
   if 1 <= life <= 10:
       glColor3f(1, 0, 0)
   if 11 <= life <= 20:
       glColor3f(1, 0.35, 0.35)
   if 21 <= life <= 30:
       glColor3f(0.95, 0.95, 0.5)
   if 31 <= life <= 40:
       glColor3f(0.8, 0.5, 1)

   # outer body
   midpoint(x - 100, y, x + 100, y)
   midpoint(x - 80, y + 40, x + 80, y + 40)
   midpoint(x - 100, y, x - 80, y + 40)
   midpoint(x + 100, y, x + 80, y + 40)

   # face

   midpoint(x - 20, y + 5, x + 20, y + 5)
   midpoint_circle(x - 60, y + 25, 8)
   midpoint_circle(x + 60, y + 25, 8)
   midpoint_circle(x - 60, y + 25, 2)
   midpoint_circle(x + 60, y + 25, 2)
   midpoint_circle(x, y - 50, 70, True)

   # sparks
   midpoint(x, y - 10, x - 10, y)
   midpoint(x, y - 10, x + 10, y)

   midpoint(x - 50, y - 10, x - 50 - 10, y)

   midpoint(x - 50, y - 10, x - 50 + 10, y)
   midpoint(x - 90, y - 10, x - 90 - 10, y)
   midpoint(x - 90, y - 10, x - 90 + 10, y)

   midpoint(x + 50, y - 10, x + 50 - 10, y)
   midpoint(x + 50, y - 10, x + 50 + 10, y)
   midpoint(x + 90, y - 10, x + 90 - 10, y)
   midpoint(x + 90, y - 10, x + 90 + 10, y)


def drawLaser():
   global laserx, lasery
   glColor3f(0.7, 0, 0)
   midpoint(laserx, lasery, laserx, lasery + 500)


def drawstar(list1):
   glColor3f(1, 1, 1)
   for i in list1:
       draw_points(i[0], i[1])


def checkcolission():
   global bulletx, bullety, enemylist, enemyarea, bullet1flag, laserx, lasery, tempi
   if bullet1flag == True:
       for i in range(len(enemyarea)):
           if enemyarea[i][0] <= bulletx <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
               return i
           elif enemyarea[i][0] <= bulletx - 15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
               return i
           elif enemyarea[i][0] <= bulletx + 15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
               return i
           elif enemyarea[i][0] <= bulletx - 15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety + 30 <= enemyarea[i][
               3]:
               return i
           elif enemyarea[i][0] <= bulletx + 15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety + 30 <= enemyarea[i][
               3]:
               return i
           elif enemyarea[i][0] <= bulletx <= enemyarea[i][1] and enemyarea[i][2] <= bullety + 30 <= enemyarea[i][3]:
               return i
   elif laserflag == True:
       for i in range(len(enemyarea)):
           if enemyarea[i][0] < laserx < enemyarea[i][1]:
               return str(i)

   return None


def checkclash():
   global enemyarea, shooterlist
   for i in range(len(enemyarea)):
       if enemyarea[i][0] <= shooterlist[0][0] <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1] <= \
               enemyarea[i][3]:
           return i
       if enemyarea[i][0] <= shooterlist[0][0] - 20 <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1] - 40 <= \
               enemyarea[i][3]:
           return i
       if enemyarea[i][0] <= shooterlist[0][0] + 20 <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1] - 40 <= \
               enemyarea[i][3]:
           return i

   return None


def drawheart(x, y):
   glColor3f(0.9, 0, 0)
   midpoint_circle(x - 5, y + 17, 5, False, True)
   midpoint_circle(x + 5, y + 17, 5, False, True)
   midpoint(x, y, x - 10, y + 17)
   midpoint(x, y, x + 10, y + 17)
   glColor3f(0.9, 0.15, 0.96)
   midpoint_circle(x - 2.5, y + 12, 2.5, False, True)
   midpoint_circle(x + 2.5, y + 12, 2.5, False, True)

   midpoint(x, y, x - 10, y + 17)
   midpoint(x, y, x + 10, y + 17)


def drawinvisible(x, y):
   glColor3f(1, 1, 1)
   midpoint(x, y, x - 7.5, y + 20)
   midpoint(x, y, x + 7.5, y + 20)
   midpoint(x - 10, y + 7, x + 10, y + 7)
   midpoint(x - 7.5, y + 20, x + 10, y + 7)
   midpoint(x - 10, y + 7, x + 7.5, y + 20)


def afterbossanimate():  # after boss appears this will be the animate function
   global bosslist, bullet1flag, bulletx, bullety, bossL_or_R, bossbulletlist, shooterlist
   if bullet1flag == True:
       if bosslist[0] - 100 <= bulletx <= bosslist[0] + 100 and bosslist[1] <= bullety <= bosslist[1] + 40:
           bullet1flag = False
           bosslist[2] -= 2
   elif laserflag == True:
       if bosslist[0] - 100 <= laserx <= bosslist[0] + 100:
           bosslist[2] -= 1
           print(bosslist[2])

   for i in range(len(bossbulletflag)):
       if bossbulletflag[i] == True:
           bossbulletlist[i][1] = bossbulletlist[i][1] - 10

   for i in range(5):
       if bossbulletflag[i] == True:
           if bossbulletlist[i][1] < 0:
               bossbulletlist[i][1] = bosslist[1]
               bossbulletflag[i] = False

           if shooterlist[0][0] - 20 <= bossbulletlist[i][0] <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= \
                   bossbulletlist[i][1] <= shooterlist[0][1]:
               bossbulletflag[i] = False
               bossbulletlist[i][1] = bosslist[1]

               shooterlist[0][2] = shooterlist[0][2] - 1


def animate():
   global shooterlist, starlist, bulletx, bullety, bullet1flag, enemybulletflag, enemylist, enemybulletlist, enemyarea, score, laserflag
   global hearty, heartx, heartflag, invisiblex, invisibley, invisibleflag, invisiblescore, bossflag, bossbulletlist
   global tempi, sx, sy
   if score == 10:
       score = 0
       bossflag = True
       shooterlist[0][2] = 9

   if bossflag == False:
       a = random.randint(1, 2)
       if a == 1:
           for i in range(len(enemylist)):
               for j in range(50):
                   disr = enemylist[i][0] + 0.02
                   if disr + 15 >= 500:
                       pass
                   else:
                       enemylist[i][0] += 0.02
       elif a == 2:
           for i in range(len(enemylist)):
               for j in range(50):
                   disl = enemylist[i][0] - 0.02
                   if disl - 15 <= 0:
                       pass
                   else:
                       enemylist[i][0] -= 0.02

       for i in range(len(enemylist)):
           enemylist[i][1] -= 0.25
           enemylist[i][5] -= 0.25
           enemylist[i][4] = enemylist[i][0]
           if enemylist[i][1] + 40 < 0:
               randomx = random.randint(i * 100, (i * 100) + 80)
               randomy = random.randint(300, 420)
               randomshape = random.choice(['Box', 'Cir', 'Trig'])
               enemylist[i] = [randomx, randomy, 3, randomshape, randomx, randomy]

       for i in range(len(enemybulletflag)):
           if enemybulletflag[i] == True:
               enemylist[i][5] -= 40
               if shooterlist[0][0] - 20 <= enemylist[i][4] <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= \
                       enemylist[i][5] <= shooterlist[0][1]:
                   if invisibleflag == False:
                       shooterlist[0][2] -= 1
                       print(shooterlist[0][2])
                   else:
                       pass

           if enemylist[i][5] < 0:
               enemylist[i][5] = enemylist[i][1]
               enemybulletflag[i] = False

       for i in range(len(enemyarea)):
           enemyarea[i] = [enemylist[i][0] - 15, enemylist[i][0] + 15, enemylist[i][1], enemylist[i][1] + 30]

       idx = checkcolission()

       if idx != None:
           if type(idx) == str:
               idx = int(idx)
               enemylist[idx][2] -= 0.1
           else:
               enemylist[idx][2] -= 1
               bullet1flag = False
           if enemylist[idx][2] <= 0:
               laserflag = False
               randomx = random.randint(idx * 100, (idx * 100) + 80)
               randomy = random.randint(300, 420)
               randomshape = random.choice(['Box', 'Cir', 'Trig'])
               enemylist[idx] = [randomx, randomy, 3, randomshape, randomx, randomy]  # scored
               bulletx, bullety = -1, -1
               score += 1
               print("SCORE: ", score)

       clash = checkclash()
       if clash != None:
           shooterlist[0][2] -= 3
           randomx = random.randint(clash * 100, (clash * 100) + 80)
           randomy = random.randint(300, 420)
           randomshape = random.choice(['Box', 'Cir', 'Trig'])
           enemylist[clash] = [randomx, randomy, 3, randomshape, randomx, randomy]  # scored
   else:
       afterbossanimate()

   # -------------------------------------------------------------------------------------------------------------------------------------------------
   for i in starlist:
       i[1] -= 2
       if i[1] == 0:
           starlist.append([random.randint(0, 500), 500])
       elif i[1] == -1:
           starlist.append([random.randint(0, 500), 500])

   if bullet1flag == True:
       bullety += 40
   if bullety > 500:
       bullet1flag = False

   sx = (sx - 3) % 500
   sy = (sy - 3) % 500

   hearty = hearty - 1

   if hearty + 20 < 0:
       heartflag = True  # ignore
       hearty = 470
       heartx = random.randint(50, 450)

   if shooterlist[0][2] <= 6:
       if shooterlist[0][0] - 20 <= heartx <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= hearty <= \
               shooterlist[0][1]:
           shooterlist[0][2] += 3
           heartflag = True
           hearty = 470
           heartx = random.randint(50, 450)

   if bossflag == False:
       invisibley = (invisibley - 1) % 500
       invisiblex = (invisiblex + 3) % 500
   if bossflag == True:
       invisibley = 1000000
       invisibley = 1000000

   if invisibleflag == False:

       if shooterlist[0][0] - 20 <= invisiblex <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= invisibley <= \
               shooterlist[0][1]:
           invisibleflag = True
           invisiblescore = score
           invisiblex, invisibley = random.randint(50, 250), 470

   if invisiblescore != score:
       invisibleflag = False
       invisiblescore = -1

   glutPostRedisplay()


def bossbullet(x, y, r):
   glColor3f(0.95, 0.95, 0.3)
   midpoint_circle(x, y, r)

   midpoint(x - 5, y + 3.5, x - 5, y - 3.5)
   midpoint(x - 5, y + 3.5, x - 12, y)
   midpoint(x - 5, y - 3.5, x - 12, y)

   midpoint(x + 5, y + 3.5, x + 5, y - 3.5)
   midpoint(x + 5, y + 3.5, x + 12, y)
   midpoint(x + 5, y - 3.5, x + 12, y)

   midpoint(x + 3.5, y - 5, x - 3.5, y - 5)
   midpoint(x + 3.5, y - 5, x, y - 12)
   midpoint(x - 3.5, y - 5, x, y - 12)

   midpoint(x + 3.5, y + 5, x - 3.5, y + 5)
   midpoint(x + 3.5, y + 5, x, y + 12)
   midpoint(x - 3.5, y + 5, x, y + 12)


def drawshootstar(sx, sy):
   glColor3f(0.5, 0.5, 0.5)
   draw_points(sx, sy, 15)
   glColor3f(1, 1, 1)
   draw_points(sx, sy, 8)


def showScreen():
   global game_state, shooterlist, bossflag, enemylist, starlist, bulletx, bullety, enemybulletflag, enemylist, laserx, lasery, laserpointlist, laserflag, enemybulletlist
   global heartx, hearty, heartflag, invisiblex, invisibley, invisibleflag, bosslist, bossbulletx, bossbullety, bossbulletflag, bossbulletlist
   global sx, sy
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   iterate()
   drawstar(starlist)

   for i in shooterlist:
       if i[2] == 0:
           game_state = 'Game Over'
       if invisibleflag == False:
           shooter(i[0], i[1], i[2])
       if invisibleflag == True:
           shooter(i[0], i[1], i[2], 'invisible')

   if bossflag == False:
       for i in enemylist:
           if i[2] == 0:
               enemylist.remove(i)

           enemy(i[0], i[1], i[2], i[3])

       for i in range(len(enemybulletflag)):
           if enemybulletflag[i] == True:
               bullet(enemylist[i][4], enemylist[i][5], 1, 0.5, 0)

   if bossflag == True:
       boss(bosslist[0], bosslist[1], bosslist[2])
       for i in range(len(bossbulletflag)):
           if bossbulletflag[i] == True:
               bossbullet(bossbulletlist[i][0], bossbulletlist[i][1], 5)

       if bosslist[2] <= 0:
           game_state = 'Game Over, Win'

   if bullet1flag == True:
       if laserflag == False:
           bullet(bulletx, bullety, 1, 0.5, 0)

   if laserflag == True:
       drawLaser()

   if heartflag == True:
       drawheart(heartx, hearty)
   drawshootstar(sx, sy)
   drawinvisible(invisiblex, invisibley)

   glutSwapBuffers()


def iterate():
   glViewport(0, 0, 500, 500)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Game")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
