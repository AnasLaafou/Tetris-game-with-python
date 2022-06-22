"""
TETRIS GAME version 1.0
created by Anas Laafou
"""

import pygame
import random
import sys
import time
import tetris_data as tetris
from helper import vec

pygame.init()

colors = {color:pygame.Color(color.upper()) for color in ["black", "white", "red", "green", "blue", "yellow"]}
for color in colors:
    globals()[color] = colors[color]

def draw_square(screen, pos=(0, 0), size=20, color=red):
    rct = pygame.draw.rect(screen, color, [*pos, size, size])
    return rct

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tetris Game")
gscboard = tetris.boardMatrix()
bgnboard = tetris.boardMatrix(size=(5, 5))
## Game Screen:
border_width = 5
gscpos = (1/2) * (vec(*screen.get_size()) - 20 * vec(*gscboard.size))
gscwh = (21 * vec(*gscboard.size) + vec(2, 2) + vec(border_width, border_width))
gamescreen = (screen, red,
              [*gscpos, *(21 * vec(*gscboard.size) + vec(2, 2) + vec(border_width, border_width))], border_width)

gsccoef = int(border_width//2) + 2
gscposes = []
for j in range(gscboard.size[1]):
    lposes = []
    for i in range(gscboard.size[0]):
        pos = (vec(*gscpos) + vec(gsccoef, gsccoef) + 21*vec(i, j))
        lposes.append(pos)
    gscposes.append(lposes)

## Bloc Generator:
bgnpos = vec(*gscpos) + 21*vec(gscboard.size[0], 0) + vec(border_width + 22, 0)
bgnwh = 107 + border_width
blocgenerator = (screen, red, [*bgnpos, bgnwh, bgnwh], border_width)
bgncenter = vec(*bgnpos) + vec((border_width + 1)/2 + 43,
                            (border_width + 1)/2 + 43)

bgncoef = int(border_width//2) + 2
bgnposes = []
for j in range(bgnboard.size[1]):
    lposes = []
    for i in range(bgnboard.size[0]):
        pos = (vec(*bgnpos) + vec(bgncoef, bgncoef) + 21*vec(i, j))
        lposes.append(pos)
    bgnposes.append(lposes)

## Score and Level:
level = 1
score = 0

sclvpos = vec(*gscpos) - vec(21*5 + 2*border_width + 22 + 30, 0)
lvpos = vec(*sclvpos) + vec(border_width, 25)
scpos = vec(*lvpos) + vec(0, 40)
sclvrect = (screen, red, [*sclvpos, 21*5 + 2*border_width + 30, 21*5 + 2*border_width], border_width)
sclvfont = pygame.font.SysFont("Courier", 25, bold=True)

spawned = []
generated = []

def update_board(board):
    #screen.fill(black)
    #draw_screen()
    if board == bgnboard:
        mode = "bgn"
    else:
        mode = "gsc"
    for ind in board.occuped_inds():
        _pos = conv_ind2pos(ind, mode=mode)
        draw_square(screen, pos=_pos, color=blue)
    #pygame.display.flip()

def conv_ind2pos(ind, mode="gsc"):
    return eval(f"{mode}poses[ind[1]][ind[0]]")

def generate_bloc():
    global generated, over
    if generated != []:
        return
    _id = random.choice(list(tetris.blocs_ids0.keys()))
    bloc = bgnboard.insert_bloc(_id)
    if not bloc.successfully_constructed:
        over = True    
    update_board(bgnboard)
    generated.append(bloc)

def spawn_bloc():
    global spawned, generated, over
    if generated == []:
        return 
    bloc = generated[-1]
    b = gscboard.insert_bloc(bloc.id)
    if not b.successfully_constructed:
        over = True
    update_board(gscboard)
    spawned.append(b)
    generated.remove(bloc)
    bgnboard.clear()
    update_board(bgnboard)
    
def move_bloc(bloc):
    global spawned
    gscboard.move(bloc, (0, 1))
    if bloc in spawned:
        spawned.remove(bloc)

clock = pygame.time.Clock()

def draw_screen():
    global score
    pygame.draw.rect(*gamescreen)
    pygame.draw.rect(*blocgenerator)    
    pygame.draw.rect(*sclvrect)
    if score >= 100:
        score = 100
    lvtext = sclvfont.render(f"Level:{level}", False, white)
    sctext = sclvfont.render(f"Score:{score}", False, white)
    screen.blit(lvtext, lvpos)
    screen.blit(sctext, scpos)

tfscpos, pfscpos, ifscpos = (0, 0), (0, 0), (0, 0)

def draw_firstscreen(mode=None):
    global tfscpos, pfscpos, ifscpos
    tfscfont = pygame.font.SysFont("Courier", 95, bold=True)
    tfscpos = vec(*gscpos) - vec(50, 0)
    pfscpos = vec(*gscpos) + vec(70, 150)
    ifscpos = vec(*gscpos) - vec(50, -250)
    title = tfscfont.render("TETRIS", False, green)
    screen.blit(title, tfscpos)
    if mode is None:
        pfscfont = pygame.font.SysFont("Courier", 50, bold=True)
        pfscpos = vec(*gscpos) + vec(70, 150)
        playbutton = pfscfont.render("PLAY", False, white)
        screen.blit(playbutton, pfscpos)

        ifscfont = pygame.font.SysFont("Courier", 50, bold=True)
        ifscpos = vec(*gscpos) - vec(50, -250)
        instructions = pfscfont.render("INSTRUCTIONS", False, white)
        screen.blit(instructions, ifscpos)
    elif mode == "effect play":
        button_effect("PLAY", pfscpos)

        ifscfont = pygame.font.SysFont("Courier", 50, bold=True)
        ifscpos = vec(*gscpos) - vec(50, -250)
        instructions = ifscfont.render("INSTRUCTIONS", False, white)
        screen.blit(instructions, ifscpos)
    elif mode == "effect instructions":
        pfscfont = pygame.font.SysFont("Courier", 50, bold=True)
        pfscpos = vec(*gscpos) + vec(70, 150)
        playbutton = pfscfont.render("PLAY", False, white)
        screen.blit(playbutton, pfscpos)

        button_effect("INSTRUCTIONS", ifscpos)

def button_effect(text, pos):
    _pos = vec(*pos) - vec(10, 10)
    e_font = pygame.font.SysFont("Courier", 55, bold=True)
    button = e_font.render(text, False, yellow)
    screen.blit(button, _pos)

def draw_interscreen():
    global level
    pygame.draw.rect(*gamescreen)
    pygame.draw.rect(*blocgenerator)    
    pygame.draw.rect(*sclvrect)
    istfont = pygame.font.SysFont("Courier", 30, bold=True)
    istpos = vec(*gscpos) + vec(border_width + 50, border_width + 100)
    _istpos = vec(*istpos) + vec(27, 50)
    _text = "Ready"
    if level < 10:
        text = f"Level 0{level}"
    else:
        text = f"Level {level}"
    isttext = istfont.render(text, False, white)
    _isttext = istfont.render(_text, False, white)
    screen.blit(isttext, istpos)
    screen.blit(_isttext, _istpos)

istrsc_imgs = ["up_arrow", "right_arrow", "left_arrow", "k_return"]
for i in range(len(istrsc_imgs)):
    istrsc_imgs[i] = pygame.image.load(f"{istrsc_imgs[i]}.png")

def draw_instrscreen():
    insfont = pygame.font.SysFont("Courier", 25, bold=True)
    insposes = [(100, 100), (100, 200), (100, 300), (100, 400)]
    texts = ["to rotate bloc",
             "to move bloc 1 square right",
             "to move bloc 1 square left",
             "to project bloc down !!"]
    for i in range(len(insposes)):
        ins = insfont.render(texts[i], False, white)
        screen.blit(istrsc_imgs[i], vec(*insposes[i]) - vec(90, 30))
        screen.blit(ins, insposes[i])

    button_effect("Back", (200, 500))
        
moved_rl = False
interscreen = False
firstscreen = True
selected = "play"
instrscreen = False
Gscreen = False
over = False

i = 0
first_bloc = 0
while True:
    
    if over:
        gofont = pygame.font.SysFont("Courier", 47, bold=True)
        go = gofont.render("GAME OVER", False, white)
        screen.blit(go, vec(*gscpos) + vec(0, 190))
        pygame.display.flip()
        time.sleep(2)
        break
        
    screen.fill(black)
    
    if firstscreen:
        draw_firstscreen(mode=f"effect {selected}")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    button_effect("PLAY", pfscpos)
                    selected = "play"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    button_effect("INSTRUCTIONS", ifscpos)
                    selected = "instructions"
                if event.key == pygame.K_RETURN:
                    if selected == "play":
                        firstscreen = False
                        interscreen = True
                    if selected == "instructions":
                        firstscreen = False
                        instrscreen = True
                        
    elif interscreen:
        draw_interscreen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                interscreen = False
                Gscreen = True
                first_bloc = 0
                
    elif instrscreen:
        draw_instrscreen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                instrscreen = False
                firstscreen = True
                
    elif Gscreen:
        draw_screen()
        if i % (40-level) == 0:
            if spawned == []:
                if not first_bloc:
                	generate_bloc()
                	first_bloc = 1
            if not gscboard.isfrozen():
                if not moved_rl:
                    move_bloc(current_bloc)
                    generate_bloc()
            if gscboard.isfrozen() and spawned == []:
                score += gscboard.evolution()
                spawn_bloc()
                if spawned != []:
                    current_bloc = spawned[0]
            if gscboard.isfrozen() and spawned != []:
                over = True
        update_board(bgnboard)
        update_board(gscboard)
        moved_rl = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    gscboard.move(current_bloc, (1, 0))
                    moved_rl = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    gscboard.move(current_bloc, (-1, 0))
                    moved_rl = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    gscboard.rotate(current_bloc)
                    moved_rl = True
                if event.key == pygame.K_RETURN:
                    gscboard.projection(current_bloc)
        if score >= 100:
            interscreen = True
            level += 1
            gscboard.clear()
            spawned = []
            generated = []
            score = 0
    pygame.display.flip()
    clock.tick(60)
    i += 1

pygame.quit()
sys.exit(0)
