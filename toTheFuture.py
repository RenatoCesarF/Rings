def advance(pos, rot, amt):
    pos[0] += math.cos(rot) * amt
    pos[1] += math.sin(rot) * amt
    return pos

def render_mana(loc, size=[2, 3], color1=(255, 255, 255), color2=(12, 230, 242)):
    global game_time
    points = []
    for i in range(8):
        points.append(advance([10,10], game_time / 30 + i / 8 * math.pi * 2, (math.sin((game_time * math.sqrt(i)) / 20) * size[0] + size[1])))
    pygame.draw.polygon(display, color1, points)
    pygame.draw.polygon(display, color2, points, 1)
