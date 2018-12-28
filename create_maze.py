#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

import matplotlib.pyplot as plt

SIZE = 8
MAZE_SIZE = 11 * SIZE + 1

walllist = np.ones((SIZE * 2 + 1, SIZE * 2 + 1), dtype=np.int32)

movelist = ["up", "right", "up", "right", "up", "left", "up", "right"]
# movelist = ["right"]

RED = (255, 0, 0)
BLUE = (0, 0, 255)

maze = np.zeros((MAZE_SIZE, MAZE_SIZE, 3), dtype=np.uint8)

for y in range(1, SIZE * 2 + 1, 2):
    walllist[y, 0] = 3
    walllist[y, -1] = 3

for x in range(1, SIZE * 2 + 1, 2):
    walllist[0, x] = 3
    walllist[-1, x] = 3

walllist[-2, 2] = 3
walllist[-4, 2] = 3

for y in range(0, SIZE * 2 + 1, 2):
    for x in range(0, SIZE * 2 + 1, 2):
        walllist[y, x] = -1
        cv2.rectangle(maze, (x * 11 // 2, y * 11 // 2), (x * 11 // 2, y * 11 // 2), RED)

for y in range(1, SIZE * 2, 2):
    for x in range(1, SIZE * 2, 2):
        walllist[y, x] = 2

clusterlist = np.zeros((SIZE * 2 + 1, SIZE * 2 + 1), dtype=np.int32) - 1

c = 1
for y in range(SIZE * 2 + 1):
    for x in range(SIZE * 2 + 1):
        if walllist[y, x] == 2:
            clusterlist[y, x] = c
            c += 1

clusterlist[-2, 1] = 0

sy = -2
sx = 1
for move in movelist:
    print(move)
    if move == "up":
        walllist[sy - 1, sx] = 0
        clusterlist[sy - 2, sx] = 0
        sy -= 2
    elif move == "down":
        walllist[sy + 1, sx] = 0
        clusterlist[sy + 2, sx] = 0
        sy += 2
    elif move == "right":
        walllist[sy, sx + 1] = 0
        clusterlist[sy, sx + 2] = 0
        sx += 2
    elif move == "left":
        walllist[sy, sx - 1] = 0
        clusterlist[sy, sx - 2] = 0
        sx -= 2

print(sy,sx)

for s in ((0,1),(0,-1),(1,0),(-1,0)):
    ssx = sx-s[0]
    ssy = sy-s[1]
    if walllist[ssy,ssx] != 0:
        walllist[ssy,ssx] = 3

    # print(walllist[:,1]==1)
# walllist[walllist[:,1]==1,1] = 0
# clusterlist[clusterlist[:,1]>0,1] = 0


print(walllist)
print("-" * 20)
print(clusterlist)
print("*" * 20)

while (np.count_nonzero(clusterlist > 0)):
    existswall = np.where(walllist == 1)
    size = len(existswall[0])
    a = np.random.randint(0, size)
    ey = existswall[0][a]
    ex = existswall[1][a]
    if walllist[ey - 1, ex] == -1:
        f1x = ex - 1
        f2x = ex + 1
        f1y = ey
        f2y = ey
    else:
        f1x = ex
        f2x = ex
        f1y = ey - 1
        f2y = ey + 1

    c1 = clusterlist[f1y, f1x]
    c2 = clusterlist[f2y, f2x]
    if c1 == c2:
        continue
    walllist[ey, ex] = 0
    if c1 < c2:
        clusterlist[clusterlist == c2] = c1
    else:
        clusterlist[clusterlist == c1] = c2

amaze = maze.copy()

for y in range(0, SIZE * 2 + 1, 2):
    for x in range(0, SIZE * 2 + 1):
        if walllist[y, x] == 1 or walllist[y, x] == 3:
            cv2.rectangle(amaze, ((x - 1) * 11 // 2 + 1, y * 11 // 2), ((x - 1) * 11 // 2 + 10, y * 11 // 2),
                          RED)

for y in range(0, SIZE * 2 + 1):
    for x in range(0, SIZE * 2 + 1, 2):
        if walllist[y, x] == 1 or walllist[y, x] == 3:
            cv2.rectangle(amaze, (x * 11 // 2, (y - 1) * 11 // 2 + 1), (x * 11 // 2, (y - 1) * 11 // 2 + 10),
                          RED)

plt.imshow(amaze)
plt.show()
