import math
import matplotlib.pyplot as plt
import time
import sys
import pygame
from pygame.locals import *


def f1(x1, x2, t):
    return x2


def f2(x1, x2, t):
    return -q1 * math.sin(x1) + q2 * math.sin(w * t - x1)


'''initial conditions and inputs'''

file = open('input.txt', 'r').readlines()
for f in file:
    exec(f)

t = 0
q1 = g / b
q2 = R * w ** 2 / b
theta0 = theta.copy()

y = []
x = []

while t <= T:
    y.append(theta[0])
    x.append(t)

    x1, x2 = theta[0], theta[1]

    k11 = dt * f1(x1, x2, t)
    k21 = dt * f2(x1, x2, t)
    k12 = dt * f1(x1 + 0.5 * k11, x2 + 0.5 * k21, t + 0.5 * dt)
    k22 = dt * f2(x1 + 0.5 * k11, x2 + 0.5 * k21, t + 0.5 * dt)
    k13 = dt * f1(x1 + 0.5 * k12, x2 + 0.5 * k22, t + 0.5 * dt)
    k23 = dt * f2(x1 + 0.5 * k12, x2 + 0.5 * k22, t + 0.5 * dt)
    k14 = dt * f1(x1 + k13, x2 + k23, t + dt)
    k24 = dt * f2(x1 + k13, x2 + k23, t + dt)
    theta[0] += (k11 + 2 * k12 + 2 * k13 + k14) / 6
    theta[1] += (k21 + 2 * k22 + 2 * k23 + k24) / 6
    t += dt

plt.plot(x, y, color='black')
plt.title("angle of the rod (relative to the vertical axis)")
plt.xlabel('Time (s)')
plt.ylabel("theta (radian)")
plt.show()

print("visualizing the simulation")

pygame.init()

font = pygame.font.Font('cour.ttf', 20)

D = pygame.display.set_mode((X, Y))
pygame.display.set_caption("a point mass attached to a circulating wheel by a massless rod")

scale = (Y / 2 - 15) / (R + b)

i0 = i = 0
runningtime = 3

txtR = font.render("R : " + str(R) + " (m)", True, (0, 0, 255))
txtg = font.render("g : " + str(g) + " (m/s^2)", True, (0, 0, 255))
txtb = font.render("b : " + str(b) + " (m)", True, (0, 0, 255))
txtw = font.render("w : " + str(w) + " (s^-1)", True, (0, 0, 255))
txtinitial = font.render("initial conditions :  [" + str(theta0[0]) + " (rad) , " + str(theta0[1]) + "  (rad/s)]", True,
                         (0, 0, 255))
txtslow = font.render("slow motion factor : " + str(slow_motion_factor) + "X", True, (0, 0, 255))
rtime0 = time.time()

while True:

    pygame.time.wait(runningtime)
    pyevents = pygame.event.get()
    for event in pyevents:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    i = int(((time.time() - rtime0) / slow_motion_factor / dt)) % len(x)

    if i != i0:
        i0 = i
        txttime = font.render("Time : " + str(round(x[i], 3)) + " (s)", True, (0, 255, 0))

        D.fill((0, 0, 0))

        D.blit(txttime, (0, 0))

        D.blit(txtslow, (0, 20))
        D.blit(txtinitial, (0, 40))
        D.blit(txtg, (0, 60))
        D.blit(txtw, (0, 80))
        D.blit(txtb, (0, 100))
        D.blit(txtR, (0, 120))

        pygame.draw.circle(D, (255, 0, 0), (X // 2, Y // 2), R * scale, 1)
        pygame.draw.line(D, (255, 255, 255),
                         (int(X / 2 + R * scale * math.sin(w * x[i])), int(Y / 2 + R * scale * math.cos(w * x[i]))), (
                             int(X / 2 + R * scale * math.sin(w * x[i]) + b * scale * math.sin(y[i])),
                             int(Y / 2 + R * scale * math.cos(w * x[i]) + b * scale * math.cos(y[i]))), 1)
        pygame.draw.circle(D, (0, 0, 255), (int(X / 2 + R * scale * math.sin(w * x[i]) + b * scale * math.sin(y[i])),
                                            int(Y / 2 + R * scale * math.cos(w * x[i]) + b * scale * math.cos(y[i]))),
                           5)

        pygame.display.update()

    else:
        continue
