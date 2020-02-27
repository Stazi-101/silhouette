import numpy as np
import pygame

def arrIndexes( ssize, dsize, x, y, middle = False ):

    pass

def arrBlit( dest, source, x, y, middle = False, overlay = False ):

    ssize = source.shape
    dsize = dest.shape

    if middle:
        x -= ssize[0]//2 
        y -= ssize[1]//2 

    sleft = 0
    stop  = 0
    srig = ssize[0]
    sbot = ssize[1]

    dleft = x
    dtop  = y
    drig = x + srig
    dbot = y + sbot

    if dleft < 0:
        sleft -= dleft
        dleft = 0

    if dtop < 0:
        stop -= dtop
        dtop = 0

    if drig > dsize[0]:
        srig -= drig - dsize[0]
        drig = dsize[0]

    if dbot > dsize[1]:
        sbot -= dbot - dsize[1]
        dbot = dsize[1]

    if overlay:
        arrOverlayWhite( dest[ dleft:drig , dtop:dbot, : ] , source[ sleft:srig , stop:sbot , : ] )
    else:
        dest[ dleft:drig , dtop:dbot ] = source[ sleft:srig , stop:sbot ]


def arrOverlay( dest, source):

    dest[:,:,0] *= 1 - source[:,:,3]/255
    dest[:,:,1] *= 1 - source[:,:,3]/255
    dest[:,:,2] *= 1 - source[:,:,3]/255

    dest[:,:,0] += source[:,:,0] * source[:,:,3]
    dest[:,:,1] += source[:,:,1] * source[:,:,3]
    dest[:,:,2] += source[:,:,2] * source[:,:,3]


def arrOverlayWhite( dest, source ):

    dest[:,:,:3] *= 1 - source[:,:,:3]/255
    dest[:,:,:3] += 1 * source[:,:,:3]


def arrBlitSurf( surf, arr ):

    if len(arr.shape) == 2:
        narr = np.array( (arr,arr,arr) )

    surfarray = pygame.surfarray.pixels3d(surf)

    ax,ay = arr.shape[:2]
    surfarray[:ax,:ay] = arr
    del surfarray
