import pygame, os, sys, time

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH//4, (HEIGHT-200)//4))
score_surf = pygame.Surface((WIDTH//4, (200)//4))

pygame.display.set_caption("Family Fued")

pygame.mouse.set_visible(False)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

rounds = [
    {
        1: {
            'question':"Dont look here",
            'points':1
        },
        2: {
            'question':"somthing more goes here",
            'points':4
        },
        3: {
            'question':"what happend",
            'points':15
        },
        4: {
            'question':"what happend",
            'points':15
        },
        5: {
            'question':"what happend",
            'points':15
        },
        6: {
            'question':"what happend",
            'points':15
        },
        7: {
            'question':"what happend",
            'points':15
        },
        8: {
            'question':"what happend",
            'points':15
        },
    },
     {
        1: {
            'question':"What is the name of the chicken?",
            'points':1
        },
        2: {
            'question':"somthing more goes here",
            'points':4
        },
        3: {
            'question':"what happend",
            'points':15
        },
        4: {
            'question':"what happend",
            'points':15
        },
        5: {
            'question':"what happend",
            'points':15
        },
        6: {
            'question':"what happend",
            'points':15
        },
        7: {
            'question':"what happend",
            'points':15
        },
        8: {
            'question':"what happend",
            'points':15
        },
    },
]

font = pygame.font.Font(resource_path('m04.ttf'), 8)
font_crang = pygame.font.Font(resource_path('Lady Radical.ttf'), 16)
xfont = pygame.font.Font(resource_path('Lady Radical.ttf'), 8)
megafont = pygame.font.Font(resource_path('m04.ttf'), 80)
hand_imgs = [pygame.image.load(resource_path('handclosed.png')), pygame.image.load(resource_path('handpointer.png'))]

wrong_sound = pygame.mixer.Sound(resource_path('wrong-sound.wav'))
wrong_sound.set_volume(0.5)

cursor_img_rect = hand_imgs[0].get_rect()

Rnd = 0
mv = 0
boxes = []
placeholders = []
spacing = 5
num = 0
click = False
mv = 0
nxtrnd = False
check = ['closed' for x in range(8)]

# __________________________________Team stuff__________________________________
vel = [0, 0]
score = [0, 0]
current_team = 0

wrong_answers = [0, 0]

clock = time.time()
width, height = (surface.get_width()//2) - (spacing * 1.5), (((surface.get_height())//4)) - (spacing * 1.5)

for x in range(2):
    for y in range(4):
        boxes.append([pygame.Rect(x*(width+spacing) + 5 + mv, y*(height+spacing) + 5 + mv, width, height), [0, 0]])
        placeholders.append(pygame.Rect(x*(width+spacing) + 5 + mv, y*(height+spacing) + 5 + mv, width, height))

lines1 = [[[0, 0], [0, surface.get_height()], 5]]
lines2 = [[[0, 0], [surface.get_width(), 0], 5]]
lines3 = [[[surface.get_width(), 0], [surface.get_width(), surface.get_height()], 5]]
lines4 = [[[0, surface.get_height()], [surface.get_width(), surface.get_height()], 5]]

def scroll_lines1():
    global lines1
    new_lines = []

    for i in lines1:
        if i[2] < 0:
            lines1.remove(i)
        i[0][0] += 0.1
        i[1][0] += 0.1
        i[2] -= 0.04

        if i[2] == 3.0399999999999983:
            new_lines.append([[0, 0], [0, surface.get_height()], 5])

        if i[2] > 0:
            new_lines.append(i)
        elif i[2] <= 0:
            if i in new_lines:
                new_lines.remove(i)

    lines1 = new_lines

    for i in lines1:
        if i[2] > 0:
            pygame.draw.line(surface, ((0, 18, 41)), i[0], i[1], int(i[2]))

def scroll_lines2():
    global lines2
    new_lines = []

    for i in lines2:
        if i[2] < 0:
            lines2.remove(i)
        i[0][1] += 0.1
        i[1][1] += 0.1
        i[2] -= 0.04

        if i[2] == 3.0399999999999983:
            new_lines.append([[0, 0], [surface.get_width(), 0], 5])

        if i[2] > 0:
            new_lines.append(i)
        elif i[2] <= 0:
            if i in new_lines:
                new_lines.remove(i)

    lines2 = new_lines

    for i in lines2:
        if i[2] > 0:
            pygame.draw.line(surface, ((0, 18, 41)), i[0], i[1], int(i[2]))

def scroll_lines3():
    global lines3
    new_lines = []

    for i in lines3:
        if i[2] < 0:
            lines3.remove(i)
        i[0][0] -= 0.1
        i[1][0] -= 0.1
        i[2] -= 0.04

        if i[2] == 3.0399999999999983:
            new_lines.append([[surface.get_width(), 0], [surface.get_width(), surface.get_height()], 5])

        if i[2] > 0:
            new_lines.append(i)
        elif i[2] <= 0:
            if i in new_lines:
                new_lines.remove(i)

    lines3 = new_lines

    for i in lines3:
        if i[2] > 0:
            pygame.draw.line(surface, ((0, 18, 41)), i[0], i[1], int(i[2]))

def scroll_lines4():
    global lines4
    new_lines = []

    for i in lines4:
        if i[2] < 0:
            lines4.remove(i)
        i[0][1] -= 0.1
        i[1][1] -= 0.1
        i[2] -= 0.04

        if i[2] == 3.0399999999999983:
            new_lines.append([[0, surface.get_height()], [surface.get_width(), surface.get_height()], 5])

        if i[2] > 0:
            new_lines.append(i)
        elif i[2] <= 0:
            if i in new_lines:
                new_lines.remove(i)

    lines4 = new_lines

    for i in lines4:
        if i[2] > 0:
            pygame.draw.line(surface, ((0, 18, 41)), i[0], i[1], int(i[2]))

def all_equal(iterator):
    return len(set(iterator)) <= 1

def blit():
    
    score_surf.fill((2, 48, 71))

    t1 = font.render('TEAM 1', False, ((255, 255, 255)))
    t2 = font.render('TEAM 2', False, ((255, 255, 255)))
    
    score_surf.blit(t1, (4,6))
    score_surf.blit(t2, (score_surf.get_width() - 4 - t2.get_width() - 1, 6))

    pygame.draw.rect(score_surf, ((255, 255, 255)), pygame.Rect(2, 3, score_surf.get_width() - 4, score_surf.get_height() - 6), 1)
    
    if current_team == 1:
        pygame.draw.rect(score_surf, ((251, 133, 0)), pygame.Rect(score_surf.get_width() - 4 - t2.get_width() - 4, 3, t2.get_width() + 6, score_surf.get_height() - 6), 1)
        pygame.draw.rect(score_surf, ((255, 255, 255)), pygame.Rect(2, 3, 52, score_surf.get_height() - 6), 1)
    else:
        pygame.draw.rect(score_surf, ((251, 133, 0)), pygame.Rect(2, 3, 52, score_surf.get_height() - 6), 1)
        pygame.draw.rect(score_surf, ((255, 255, 255)), pygame.Rect(score_surf.get_width() - 4 - t2.get_width() - 4, 3, t2.get_width() + 6, score_surf.get_height() - 6), 1)
    
    pygame.draw.line(score_surf, ((255, 255, 255)), (score_surf.get_width() - 4 - t2.get_width() - 4, 3 + 30), (score_surf.get_width() - 4 - t2.get_width() + t2.get_width(), 3 + 30))
    pygame.draw.line(score_surf, ((255, 255, 255)), (2, 3 + 30), (53, 3+30))

    for i in range(wrong_answers[0]):
        text = xfont.render('X', False, ((255, 255, 255)))
        score_surf.blit(text, (12 + (i*text.get_width()), 3 + 30))

    for i in range(wrong_answers[1]):
        text = xfont.render('X', False, ((255, 255, 255)))
        score_surf.blit(text, (score_surf.get_width() - 4 - t2.get_width() - 4 + (i*text.get_width()) + 12, 3 + 30))
 
    if not start_q:
        fftext1 = font_crang.render('F A M I L Y', False, ((255, 255, 255)))
        fftext2 = font_crang.render('F E U D', False, ((255, 255, 255)))

        score_surf.blit(fftext1, ((score_surf.get_width()/2) - (fftext1.get_width()/2), (score_surf.get_height()/2) - fftext1.get_height()))
        score_surf.blit(fftext2, ((score_surf.get_width()/2) - (fftext2.get_width()/2), (score_surf.get_height()/2)))

    score_surf.blit(font.render(str(score[0]), False, ((255, 255, 255))), (t1.get_width()/2, t1.get_height() + 15))
    score_surf.blit(font.render(str(score[1]), False, ((255, 255, 255))), (score_surf.get_width() - t2.get_width() + t2.get_width()/2 - 6, t2.get_height() + 15))

    display_x()

    screen.blit(pygame.transform.scale(surface, (1200, 600)), (0, 200))
    screen.blit(pygame.transform.scale(score_surf, (WIDTH, 200)), (0, 0))

    pygame.display.update()

c = 0
got_wrong = [False, False]
start_q = False

def display_x():
    global c, got_wrong, clock
    c += 1
    
    if c == 100:
        got_wrong = [False, False]

    if got_wrong[0]:
        if c % 20 in range(1, 13) and c <= 100:
            txt = megafont.render('X', False, ((235, 64, 52)), ((255, 255, 255)))
            surface.blit(txt, (surface.get_width()/2 - txt.get_width()/2, surface.get_height()/2 - txt.get_height()/2))
        wrong_sound.play()

    elif got_wrong[1]:
        if c % 20 in range(1, 13) and c <= 100:
            txt = megafont.render('X', False, ((235, 64, 52)), ((255, 255, 255)))
            surface.blit(txt, (surface.get_width()/2 - txt.get_width()/2, surface.get_height()/2 - txt.get_height()/2))
        wrong_sound.play()

    else:
        c = 0

def render_wrapped_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    return lines

danger_mode = [False, False]
def gameLoop():
    global Rnd, mv, click, nxtrnd, clock, current_team, wrong_answers, got_wrong, danger_mode, check, start_q

    running = True
    while running:
        surface.fill((2, 48, 71))

        pos = list(pygame.mouse.get_pos())
        ratio_x = (WIDTH / surface.get_width())
        ratio_y = (HEIGHT / surface.get_height())
        scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)

        scroll_lines1()
        scroll_lines2()
        scroll_lines3()
        scroll_lines4()

        for event in pygame.event.get():  
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if Rnd < len(rounds):
                        current_team = not current_team
                        danger_mode = [False, False]
                        got_wrong = [False, False]
                        check = ['closed' for x in range(8)]
                        wrong_answers = [0,0]
                        Rnd += 1
                        boxes.clear()
                        current_team = 0
                        clock = time.time()
                        nxtrnd = True
                        start_q = False
                        for x in range(2):
                            for y in range(4):
                                boxes.append([pygame.Rect(x*(width+spacing) + 5 + mv, y*(height+spacing) + 5 + mv, width, height), [0, 0]])

                if event.key == pygame.K_1:
                    current_team = 0
                    
                elif event.key == pygame.K_2:
                    current_team = 1

                if event.key == pygame.K_x:
                    wrong_answers[current_team] += 1
                    got_wrong[current_team] = True
                
                if event.key == pygame.K_q:
                    start_q = True

            if event.type == pygame.QUIT:
                running = False

        if wrong_answers[current_team] >= 3:
            if current_team == 0:
                current_team = 1
                danger_mode[0] = True

            elif current_team == 1:
                current_team = 0
                danger_mode[1] = True

        if danger_mode[0]:
            if ['open' for x in range(8)] == check:
                score[1] = score[0] + score[1]
                score[0] = 0
            else:
                if got_wrong[1]:
                    current_team = not current_team  
                    wrong_answers[0] = 0   
                    got_wrong[1] = False
                    danger_mode[0] = False

        if danger_mode[1]:
            if ['open' for x in range(8)] == check:
                score[0] = score[1] + score[0]
                score[1] = 0
            else:
                if got_wrong[0]:
                    current_team = not current_team  
                    wrong_answers[1] = 0   
                    got_wrong[0] = False
                    danger_mode[1] = False

        for key in rounds[Rnd]:
            placeholder = placeholders[key - 1]
            pygame.draw.rect(surface, ((255, 255, 255)), pygame.Rect(placeholder.x + 2, placeholder.y + 2, placeholder.width, placeholder.height), border_radius=3)
            pygame.draw.rect(surface, ((33, 158, 188)), pygame.Rect(placeholder.x + 2, placeholder.y + 2, placeholder.width, placeholder.height), 1, border_radius=3)

            text = rounds[Rnd][key]['question']

            lines = render_wrapped_text(text, font, placeholder.width - 10)
            
            y_offset = 0
            for line in lines:
                text_surface = font.render(line, True, ((0, 0, 0)))
                surface.blit(text_surface, (placeholder.x + (width/2) - (text_surface.get_width()/2), placeholder.y + (height/2) - (text_surface.get_height()/2) + y_offset))
                y_offset += text_surface.get_height()


        for i in boxes:
            if i[0].collidepoint(scaled_pos):
                mv = 2
                if click:
                    if i[0].x < surface.get_width() / 2:
                        i[1][0] = -5
                    else:
                        i[1][0] = 5
                    
                    score[current_team] += rounds[Rnd][boxes.index(i) + 1]['points']

                    check[boxes.index(i)] = 'open'
                    click = False

            else:
                mv = 0

            i[0].x += i[1][0]

            pygame.draw.rect(surface, ((0, 18, 41)), pygame.Rect(i[0].x + 2, i[0].y + 2, i[0].width, i[0].height), border_radius=3)
            pygame.draw.rect(surface, ((142, 202, 230)), pygame.Rect(i[0].x+mv, i[0].y + mv, i[0].width, i[0].height), border_radius=3)
            pygame.draw.rect(surface, ((33, 158, 188)), pygame.Rect(i[0].x + mv, i[0].y + mv, i[0].width, i[0].height), 2, border_radius=3)

            pygame.draw.circle(surface, ((33, 158, 188)), (i[0].x + (width/2) + mv, i[0].y + (height/2) + mv), (height/3), 2)
            
            image = font.render(str((boxes.index(i)) + 1), True, ((33, 158, 188)))

            surface.blit(image, (i[0].x + (width/2) + mv - (image.get_width()/2), i[0].y + (height/2) + mv - (image.get_height()/2)))

        cursor_img_rect.center = scaled_pos

        if not click:
            surface.blit(hand_imgs[1], cursor_img_rect)
        else:
            surface.blit(hand_imgs[0], cursor_img_rect)

        blit()
    

    pygame.quit()

# Go to gameLoop
gameLoop()
