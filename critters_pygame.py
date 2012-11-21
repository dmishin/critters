import pygame
from pygame.locals import *
import numpy 
from critters import *
from random import randint, shuffle

from numpy.fft import fft2

class Field:
    def __init__(self, cells, generation = 0):
        if isinstance(cells, tuple):
            cells = numpy.zeros(cells,dtype=numpy.uint8)
        self.cells = cells
        self.generation = generation

    def next(self, func=critters_func):
        gen = self.generation
        (eval_even, eval_odd)[gen % 2](self.cells, func)
        self.generation = gen+1

    def noise_box( self, x0, y0, x1, y1, percentage=50 ):
        fld = self.cells
        num_random_points = int((x1-x0)*(y1-y0)*percentage)
        for _ in xrange( num_random_points ):
            x = randint( x0, x1 )
            y = randint( y0, y1 )
            fld[x,y] = 1

    def variadic_noise( self, x0, y0, x1, y1 ):
        pass
    def clear(self):
        self.cells *= 0;

def func_fron_index( i ):
    return make_rfinv_func( *[ (i >> bit) & 1 for bit in xrange(6)] )


if __name__=="__main__":
    pygame.init()
    pygame.font.init()
    
    func_index = 0
    func = func_fron_index( func_index )
    print "Using function #%d: %s"%(func_index, func)

    frame_steps = 16
    fourier_mode = True

    screen = pygame.display.set_mode((512, 512))

    S = 100
    fld = Field( (512, 512) )
    def new_random_fld():
        fld.clear()
        fld.noise_box( 256-S, 256-S, 256+S, 256+S, 0.9 )


    new_random_fld()

    surf = pygame.surfarray.make_surface( fld.cells )
    generation = 0

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT,):
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    new_random_fld()
                elif event.key in (K_n, K_p):
                    func_index += 1 if event.key == K_n else -1
                    func = func_fron_index( func_index )
                    print "Using function #%d: %s"%(func_index, func)
                    new_random_fld()
                elif event.key == K_f:
                    fourier_mode = not fourier_mode
                

        for i in xrange(frame_steps):
            fld.next(func)

        if fourier_mode:
            fc = (numpy.log(numpy.abs(fft2( fld.cells ))) + 128).astype( numpy.uint8)
            pygame.surfarray.blit_array(surf,  fc )
        else:
            pygame.surfarray.blit_array(surf,  fld.cells*255 )
            
        screen.blit(surf, (0,0))
        

        pygame.display.update()
        #pygame.time.delay(100)
    

#Functions:
# Function: [0, 1, 1, 0, 0, 0] - stringy patterns. Interesing
# Function: [0, 1, 0, 0, 0, 1] - blob gas. mid interest
# Function: [0, 0, 0, 0, 1, 1] - diag gas. mid interest
# Function: [1, 0, 0, 1, 0, 1] - critters?
# Function: [1, 0, 0, 1, 1, 0] - again critters?

# Function: [1, 0, 1, 0, 1, 1] - pulsating box. Strange.
# Function: [1, 1, 0, 1, 0, 1] - limited noise
# Function: [0, 1, 1, 1, 0, 0] - growing rectangular patterns
# Function: [0, 1, 1, 1, 0, 0] - non-growing noise
# Function: [1, 1, 0, 1, 1, 1] - Gas, omnidirectional
# Function: [0, 1, 0, 0, 0, 0] - slit stringies. Mostly circular blob
# Function: [0, 1, 0, 1, 0, 0] - new throne-like patterns


# Function: [0, 0, 1, 0, 1, 0] - Gas and borders, nice!
