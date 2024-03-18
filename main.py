import display as dsp
import pygame
import math
dsp.init()

from display import OTD_MENU, OTD_UI, run, RES_FORM
from display import OTD_GAME as OTD

class MyAnim(dsp.Animation):
    def __init__(self, object, radius, count):
        self.chase = object
        self.time = 2
        self.step = 0
        self.stop = False
        self.done = False
        self.visible = True
        self.radius = radius
        self.count = count
        self.angle = 0
    
    def act(self):
        self.angle += 5
    
    def draw(self, surface: pygame.Surface):
        points = []
        for i in range(self.count):
            a = self.angle + 360*i/self.count
            x = self.chase.x + math.cos(a/180*math.pi) * self.radius
            y = self.chase.y - math.sin(a/180*math.pi) * self.radius
            points.append((x, y))
            pygame.draw.circle(surface, (200,0,150), (x,y), 2)
        
            
class sprite_obj(dsp.objects_parent):
    def __init__(self, surf: pygame.Surface, x: int, y: int):
        self.surf = surf
        self.x = x
        self.y = y
    
    def act(self):
        self.x = (self.x+1)%RES_FORM[0]
        self.y = (self.y+1)%RES_FORM[1]
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, (self.x, self.y))


def prepare():
    global sprite, x, y
    sprite = sprite_obj(pygame.image.load("sprite.png"), 0, 0)
    spriteAnim = MyAnim(sprite, 100, 7)
    OTD.visible = True
    OTD.add_anim(spriteAnim)

def act():
    global run, sprite, x, y
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            dsp.stop()
    
    sprite.act()
    
    OTD.add_obj(sprite)
    return
    


if __name__=="__main__":
    dsp.start(prepare, act)