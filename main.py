import display as dsp
#from display import OTD, RES_FORM
import pygame

dsp.init()


def prepare():
    global sprite, x, y
    sprite = pygame.image.load("sprite.png")
    x, y = 0, 0

def act():
    global run, sprite, x, y
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            dsp.stop()
    x = (x+1)%RES_FORM[0]
    y = (y+1)%RES_FORM[1]

    OTD.add_txt(sprite, x, y)
    
    return
    


if __name__=="__main__":
    OTD = dsp.OTD
    run = dsp.run
    RES_FORM = dsp.RES_FORM
    dsp.start(prepare, act)