import pygame as pg
from math import *
import numpy as np
import itertools

WIDTH = 0
HEIGHT = 0
BLACK = (0,0,0)
WHITE = (225,225,225)

clock = pg.time.Clock()

g_break_amp = 0

# cube_count = 10

def setup(screen, etc):
    global HEIGHT, WIDTH, g_k2
    WIDTH = etc.xres
    HEIGHT = etc.yres
    g_k2 = etc.knob2
    etc.bg_color(BLACK)
    # etc.bg_color(etc.color_picker_bg(WHITE))

scale = 50

circle_pos = [1280/2, 720/2]

cube_positions = [
    (0,0),
    (100,100),
    (-100,-100),
    (100,-100),
    (-100,100),
    (200,0),
    (-200,0),
    (0,200),
    (0,-200),
    (200,200),
    (-200,-200),
    (200,-200),
    (-200,200),
    (300,-100),
    (300,100),
    (-300,100),
    (-300,-100)
]

# arr1 = [0,-100-200,-300,-400]
# arr2 = [0,100,200,300]
# cube_positions = list(itertools.product(arr1, arr2))

angle = 0

points = []
for point in itertools.product((-1,1), repeat=3):
    points.append(np.array(point))
idx = [1,5,7,3,0,4,6,2]
points = [points[i] for i in idx]

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0]
])

projected_points = [
    [n,n] for n in range(len(points))
]

def connect_points(i,j,points,cube_surface,bamp,cube_color,thickness):
    pg.draw.line(
        cube_surface,
        cube_color,
        (points[i][0]*bamp,points[i][1]), 
        (points[j][0],points[j][1]*bamp),
        thickness
    )

def draw(screen, etc):
    global angle, scale, g_k2, g_break_amp, cube_count
    clock.tick(60)
    cube_surface = pg.Surface((scale*2+circle_pos[0],scale*2+ circle_pos[1]))
    cube_surface.set_colorkey(BLACK)
    cube_color = etc.color_picker(etc.knob4)
    thickness = int(abs(etc.audio_in[0]*0.0003058)+1)
    cube_count = int(etc.knob5*100/6.25)+1
    
    # increase rotation speed with knob 2
    k2 = int(etc.knob2*30 + 1)
    angle_amp = k2
    if k2 > g_k2:
        angle_amp += 1
        
    g_k2 = k2
        
    angle += (0.01 * angle_amp)
    
    scale = int(abs(etc.knob1 * 50 - (cube_count * 2) + 50))
    
    # rotation matrices
    rotation_z = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    
    # create cube coordinates
    i=0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        # pg.draw.circle(screen, BLACK, (x, y), 1)
        i += 1

    # position knob
    break_amp = etc.knob3 * .5 +.5
    bamp = break_amp
    if break_amp > g_break_amp:
        bamp -= .01
    g_break_amp = break_amp
    
    # draw the lines 
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points,cube_surface,bamp,cube_color,thickness)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points,cube_surface,bamp,cube_color,thickness)
        connect_points(p, (p+4), projected_points,cube_surface,bamp,cube_color,thickness)
    
    # blit
    for i in range(cube_count):
        # surf = pg.transform.rotate(cube_surface, i*5)
        surf = cube_surface
        screen.blit(surf,(cube_positions[i]))
    
        
    # ***************** print value for debugging *****************************
    # print_val = str(int(etc.knob5*100/5)+1)
    # print_surface = pg.Surface((400,400))
    # font = pg.font.Font('freesansbold.ttf', 32)
    # text = font.render(print_val, True, (0,0,0), (225,225,225))
    # textbox = text.get_rect()
    # textbox.center = (200,200)
    # screen.blit(text,textbox)
