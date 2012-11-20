from random import randint
from PIL import Image
from critters import evaluate_steps, eval_even, eval_odd
import numpy
import time


def noise_box( fld, x0, y0, x1, y1, percentage=50 ):
    num_random_points = int((x1-x0)*(y1-y0)*percentage)
    for _ in xrange( num_random_points ):
        x = randint( x0, x1 )
        y = randint( y0, y1 )
        fld[x,y] = 1


def initial_pattern_2squares(N, R, percentage):
    fld = numpy.zeros((N,N), dtype = numpy.uint8 )
    c = N / 2

    noise_box( fld, c-R, c-R, c, c, percentage )
    noise_box( fld, c, c, c+R, c+R, percentage )

    return fld

def initial_pattern_square(N, R, percentage):
    if isinstance(R, tuple):
        rx, ry = R
    else:
        rx, ry = R,R
    fld = numpy.zeros((N,N), dtype = numpy.uint8 )
    c = N / 2
    noise_box( fld, c-rx, c-ry, c+rx, c+ry, percentage )
    return fld

def plot_population( fld, steps2 ):
    import matplotlib.pyplot as pp
    pop = []
    for i in xrange(steps2):
        pop.append( numpy.sum(fld))
        eval_even(fld)
        eval_odd (fld)
    pop.append( numpy.sum(fld))
    
    pp.plot( pop )
    pp.show()

def show_field( arr ):
    image = Image.fromarray(arr, mode="P")
    image.putpalette( [0,0,0,255,255,255] )
    image.show()


if __name__=="__main__":
    N = 256
    S = 10**7
    print "Testing critters algorithm on %dx%d field, %d steps"%(N, N, S)

    
    if True:
    
        fld = initial_pattern_square(N, (90,10), 1.0)
        t_start = time.time()
        evaluate_steps( fld, S )
        t_end = time.time()
        dt = t_end - t_start
        print "Finished in %g seconds, %g steps/s"%(dt, S/dt)
        show_field( fld )

    if False:
        plot_population( initial_pattern_square(N, 60, 0.7), S )

