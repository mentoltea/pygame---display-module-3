from typing import Any, NewType
from types import FunctionType
import pygame
import math
import read_settings
from threading import Thread

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

def init():
    global wn, clock, window, fullscreen, WIN_X, WIN_Y, FPS, TICK, RES_FORM, run
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
    run = True



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

        for layer in OTD.layers:
            window.blit( layer[0], (layer[1], layer[2]) )

        for txt in OTD.textures:
            txt[0].set_alpha(txt[4])
            if txt[3]==0 and txt[5]==0 and txt[6]==0:
                window.blit(txt[0] , (txt[1],txt[2]) )
                continue
            temp_texture, new_topleft = get_trans(txt[0], txt[5], txt[6], txt[3], (txt[1], txt[2]))
            temp_texture.set_colorkey( temp_texture.get_at((0,0)) )
            window.blit( temp_texture, new_topleft )

        for obj in OTD.objects:
            obj.draw(window)
            
        for anim in OTD.animations:
            anim.draw(window)
            
            
            
            
        OTD.clear()
                
        
        wn.blit(get_trans_old(window, WIN_X, WIN_Y, 0), (0,0))
        pygame.display.update()


class objects_parent:
    def draw(self, surface: pygame.Surface):
        pass

class Animation(objects_parent):
    time: float
    step: int
    stop: bool
    done: bool
    visible: bool
    def act(self):
        pass

class objects_to_draw_class:
    def __init__(self):
        self.textures: list[tuple[pygame.Surface, int, int, float, int, int, int]] = list()
        self.objects: list[objects_parent] = list()
        self.layers: list[tuple[pygame.Surface, int, int]] = list()
        self.animations: list[Animation] = list()
        self.transfer = dict()
        
        
    def __call__(self, *args, **kwargs):
        if "overload" in kwargs:
            overload = kwargs["overload"]
        kwargs.pop("overload")
        if overload == "obj":
            self.add_obj(*args, **kwargs)
        elif overload == "txt":
            self.add_txt(*args, **kwargs)
        elif overload == "lyr":
            self.add_lyr(*args, **kwargs)
        elif overload == "anim":
            self.add_anim(*args, **kwargs)


    def add_obj(self, obj: objects_parent):
        self.objects.append(obj)
    
    
    def add_txt(self, texture: pygame.Surface, x:int, y:int, rotation=0, trans=255, x_size=None, y_size=None):
        if x_size == None:
            x_size = texture.get_width()
        if y_size == None:
            y_size = texture.get_height()
        self.textures.append((texture, x, y, rotation, trans, x_size, y_size))

    def add_lyr(self, layer: pygame.Surface, x:int, y:int):
        self.layers.append((layer, x, y))
        
    def add_anim(self, anim: Animation) -> Any:
        self.animations.append(anim)
    
    def update_anims(self):
        for anim in self.animations:
            if anim.done:
                self.animations.remove(anim)
                return
            if not anim.stop:
                anim.act()
        
    def remove(self, key):
        del self.list[key]

    def clear(self):
        self.textures.clear()
        self.objects.clear()
        self.layers.clear()
        self.transfer.clear()
        for anim in self.animations:
            if anim.done:
                self.animations.remove(anim)

OTD = objects_to_draw_class()

def stop():
    global run
    run = False

def start(prepare: FunctionType, act: FunctionType):
    global run, TICK, TICK_COUNTER
    
    draw_thread = Thread(target = window_update, args=(), daemon=True)
    draw_thread.start()
    prepare()
    try:
        while run:
            clock.tick(TICK)
            TICK_COUNTER = (TICK_COUNTER+1)%TICK
            OTD.update_anims()
            act()

            
    except Exception as e:
        run = False
        draw_thread.join()
        print("extremal window closing")    
        raise e

    draw_thread.join()

    read_settings.save(settings)
    pygame.quit()
