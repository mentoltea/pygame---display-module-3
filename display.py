import pygame
import math
import read_settings
from threading import Thread

#READ SETTINGS
settings = read_settings.read()

fullscreen = int(settings["fullscreen"])
if not fullscreen:
    WIN_X = int(settings["real_x_size"])
    WIN_Y = int(settings["real_y_size"])
FPS = int(settings["fps"])
TICK = int(settings["tick"])
RES_FORM = (int(settings["virtual_x_size"]), int(settings["virtual_y_size"]))

FPS_COUNTER=0
TICK_COUNTER=0

#FORM WINDOW
pygame.init()
pygame.mixer.init()

if fullscreen:
    flags = pygame.FULLSCREEN
    wn = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], flags, vsync=1)
    RES_CURRENT = pygame.display.get_desktop_sizes()[0]
    (WIN_X, WIN_Y) = RES_CURRENT
else:
    wn = pygame.display.set_mode((WIN_X,WIN_Y), vsync=1)
    RES_CURRENT = (WIN_X, WIN_Y)

if 0 in RES_FORM:
    RES_FORM = RES_CURRENT

pygame.display.set_caption("display by s7k")

clock = pygame.time.Clock()
window = pygame.Surface((RES_FORM[0], RES_FORM[1]))

#IMAGE TRANSFORMATION FUNCTIONS
def get_trans(Surf, size_x, size_y, angle, topleft):
    def r(image, angle, topleft):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

        return rotated_image, new_rect.topleft
    def trans(Surf, w, h):
        return pygame.transform.scale(Surf, (w,h))
    return r(trans(Surf, size_x, size_y), angle, topleft)

def get_trans_old(Surf, width, height, angle):
    return pygame.transform.rotate(pygame.transform.scale(Surf, (int(round(width)), int(round(height)))), int(round(angle)))


#WINDOW DRAW FUNCTION
def window_update():
    while 1:
        global run, clock, FPS, FPS_COUNTER, wn, window, RES_FORM, WIN_X, WIN_Y, OTD
        if not run:
            break
        clock.tick(FPS)
        FPS_COUNTER = (FPS_COUNTER+1)%FPS
        wn.fill((0,0,0))
        window.fill((255,255,255))


        for key in OTD.list:
            obj = OTD.list[key]
            obj[0].set_alpha(obj[4])
            if obj[3]==0 and obj[5]==0 and obj[6]==0:
                window.blit(obj[0] , (obj[1],obj[2]) )
                continue
            temp_texture, new_topleft = get_trans(obj[0], obj[5], obj[6], obj[3], (obj[1], obj[2]))
            temp_texture.set_colorkey( temp_texture.get_at((0,0)) )
            window.blit( temp_texture, new_topleft )

        OTD.clear()
                
        
        wn.blit(get_trans_old(window, WIN_X, WIN_Y, 0), (0,0))
        pygame.display.update()

class objects_to_draw_class:
    def __init__(self):
        self.list = dict()
        self.transfer = dict()

    def __call__(self, key, texture, x, y, rotation=0, trans=255, x_size=None, y_size=None):
        if key not in self.list:
            if x_size == None:
                x_size = texture.get_width()
            if y_size == None:
                y_size = texture.get_height()
            self.list[key] = (texture, x, y, rotation, trans, x_size, y_size)

    def remove(self, key):
        del self.list[key]

    def clear(self):
        self.list.clear()

OTD = objects_to_draw_class()


def act():
    global run
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
    
    
    return

run = True
draw_thread = Thread(target = window_update, args=(), daemon=True)
draw_thread.start()

x, y = 0, 0
sprite = pygame.image.load('sprite.png')


try:
    while run:
        clock.tick(TICK)
        TICK_COUNTER = (TICK_COUNTER+1)%TICK
        act()
        x = (x+1)%RES_FORM[0]
        y = (y+1)%RES_FORM[1]

        OTD('test', sprite, x,y, rotation = 0.5)
        
except Exception as e:
    run = False
    
    draw_thread.join()
    print("extremal window closing")    
    raise e

draw_thread.join()

read_settings.save(settings)
pygame.quit()
