from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=8)
scene.set_floor(-1, (1, 1, 1))
scene.set_background_color((0, 0, 0))
scene.set_directional_light((1, 1, -1), 0.2, (0.1, 0.1, 0.1))


@ti.kernel
def initialize_voxels():
    draw_back()  # 背景板
    draw_capacitance((42, 42), 7, 9, 24, vec3((255.0/255, 255.0/255, 255.0/255)), vec3((221.0/255, 157.0/255, 4.0/255)))
    draw_capacitance((-48, -48), 3, 5, 12, vec3((255.0 / 255, 255.0 / 255, 255.0 / 255)),
                     vec3((0.0 / 255, 102.0 / 255, 255.0 / 255)))
    draw_capacitance((-48, -36), 3, 5, 12, vec3((255.0 / 255, 255.0 / 255, 255.0 / 255)),
                     vec3((0.0 / 255, 102.0 / 255, 255.0 / 255)))
    draw_cubic((-48, 0, 32), vec3(24, 12, 16), vec3(127./255, 106./255, 92./255), vec3(0.1, 0.1, 0.1))
    draw_cubic((-8, 0, 19), vec3(30, 3, 30), vec3(65./255, 54./255, 52./255), vec3(0, 0, 0))
    draw_cubic((-12, 0, 15), vec3(38, 2, 38), vec3(180./255, 0./255, 0./255), vec3(0, 0, 0))

    draw_cubic((12, 0, -54), vec3(36, 2, 36), vec3(0, 0, 0), vec3(0, 0, 0))
    draw_cubic((22, 0, -44), vec3(16, 2, 16), vec3(242./255, 228./255, 208./255), vec3(0, 0, 0))
    draw_cubic((24, 0, -42), vec3(12, 4, 12), vec3(127./255, 106./255, 92./255), vec3(0, 0, 0))

    for i in range(10):
        draw_resistance_1((-50, -20 + i * 4), vec3(232. / 255, 228. / 255, 208. / 255), vec3(232. / 255, 139. / 255, 0))
        draw_resistance_2((-30 + i * 3, -50), vec3(232. / 255, 228. / 255, 208. / 255),
                          vec3(155. / 255, 239. / 255, 60. / 255))
    for i in range(6):
        draw_resistance_1((40, -12 + (i * 8)), vec3(232. / 255, 228. / 255, 208. / 255),
                          vec3(150. / 255, 39. / 255, 197. / 255))
    draw_logo(vec3(3, 3, 30), 12)
    draw_logo(vec3(27, 4, -39), 6)

    draw_ic(vec3(-30, 0, -36), vec3(28, 4, 12), vec3(32./255, 32./255, 32./255), vec3(255, 255, 255), 8)
    draw_ic(vec3(16, 0, -10), vec3(12, 4, 16), vec3(32. / 255, 32. / 255, 32. / 255), vec3(255, 255, 255), 4)


@ti.func
def draw_back():
    for i, j in ti.ndrange((-64, 64), (-64, 64)):
        if (ti.abs(i)-60)**2 + (ti.abs(j)-60)**2 > 9:
            scene.set_voxel(vec3(i, 0, j), 1, vec3((255.0 / 255, 0, 0)))


@ti.func
def draw_cubic(pos, size, color, color_noise):
    for II in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(II, 1, color + color_noise * ti.random())


@ti.func
def draw_capacitance(pos, radius1, radius2, height, color1, color2):
    for x, y, z in ti.ndrange((pos[0] - radius1, pos[0] + radius1), (pos[1] - radius1, pos[1] + radius1), height):
        if (x-pos[0]) ** 2 + (y-pos[1]) ** 2 < radius1 ** 2:
            scene.set_voxel(vec3(x, z, y), 1, color1)
    for i, j, k in ti.ndrange((pos[0] - radius2, pos[0] + radius2), (pos[1] - radius2, pos[1] + radius2), height + 1):
        if radius1 ** 2 < (i - pos[0]) ** 2 + (j - pos[1]) ** 2 < radius2 ** 2:
            scene.set_voxel(vec3(i, k, j), 1, color2)


@ti.func
def draw_resistance_1(pos, color1, color2):
    scene.set_voxel(vec3(pos[0], 1, pos[1]), 1, color1)
    scene.set_voxel(vec3(pos[0]+4, 1, pos[1]), 1, color1)
    draw_cubic(vec3(pos[0]+1, 1, pos[1]), vec3(3, 1, 1), color2, vec3(0.1, 0.1, 0.1))


@ti.func
def draw_resistance_2(pos, color1, color2):
    scene.set_voxel(vec3(pos[0], 1, pos[1]), 1, color1)
    scene.set_voxel(vec3(pos[0], 1, pos[1] + 4), 1, color1)
    draw_cubic(vec3(pos[0], 1, pos[1] + 1), vec3(1, 1, 3), color2, vec3(0.1, 0.1, 0.1))


@ti.func
def draw_logo(pos, bit):
    for i in range(bit):
        scene.set_voxel(ivec3(pos[0] + i, pos[1], pos[2] + i), 1, vec3(255, 255, 255))
        scene.set_voxel(ivec3(pos[0] + i, pos[1], pos[2]), 1, vec3(255, 255, 255))
        scene.set_voxel(ivec3(pos[0] + i, pos[1], pos[2] + i / 2), 1, vec3(255, 255, 255))


@ti.func
def draw_ic(pos, size, color1, color2, bit):
    draw_cubic(pos, size, color1, vec3(0.1, 0.1, 0.1))
    for i in range(bit):
        scene.set_voxel(ivec3(pos[0] + size[0] / bit * i, 2, pos[2] - 1), 2, color2)
        scene.set_voxel(ivec3(pos[0] + size[0] / bit * i, 2, pos[2] + size[2]), 2, color2)


initialize_voxels()
scene.finish()
