
'''
Layered silhouette, made objects in same format
'''

import math
import cv2
import pygame
import numpy as np
from scipy import ndimage

from arrFuns import arrBlitSurf, arrBlit
import star
from Timer import Timer


IMAGEPATH = 'lass.png'
SIZE = (512,512)


class World():

    def __init__( self ):

        self.t = Timer()

        pygame.init()
        self.size = SIZE
        self.screen = pygame.display.set_mode( self.size )

        self.mpos = 50,50

        self.arr = loadImage( IMAGEPATH )
        self.arr = self.arr * -1 + 255

        sx,sy = self.size

        self.mAArr = np.fromfunction( lambda x,y: np.arctan2(y-sy,x-sx), (2*sx,2*sy) )
        self.mDArr = np.fromfunction( lambda x,y: np.hypot(  y-sy,x-sx), (2*sx,2*sy) )

        self.stars = star.World( self.size )
        self.silhouette = Silhouette( self, self.arr )
        self.moon = Moon( self )


    def draw( self ):

        self.t.end('irr')

        sarr = np.zeros( self.size+(3,) )
        sarr[:,:,0] = 10
        sarr[:,:,1] = 0
        sarr[:,:,2] = 10


        arrOverlayWhite( sarr, self.stars.drawnArr )
        self.t.end('stars')
        arrOverlayWhite( sarr, self.moon.draw( sarr.shape ) )
        self.t.end('moon')
        arrOverlayBlack( sarr, self.silhouette.foreground )
        self.t.end('fore')
        arrOverlayWhite( sarr, self.silhouette.draw( sarr.shape ) )
        self.t.end('silhouette')

        arrBlitSurf( self.screen, sarr )
        self.t.end('blit')
        pygame.display.update()

#----------------------------------------------------------------------------
class Silhouette():


    def __init__( self, world, arr ):

        self.world = world

        self.foreground = arr.copy()
        
        sobelx = ndimage.sobel( arr, axis=0, mode='constant')[:,:,0]
        sobely = ndimage.sobel( arr, axis=1, mode='constant')[:,:,0]

        self.sobela = np.arctan2(sobely,sobelx)
        self.sobelm = np.hypot(sobelx,sobely)
        

    def draw( self, shape ):

        arr = np.zeros( shape )

        mx,my = self.world.mpos
        sx,sy = self.world.size

        a =    self.world.mAArr[ sx-mx:2*sx-mx , sy-my:2*sy-my ]
        mdis = self.world.mDArr[ sx-mx:2*sx-mx , sy-my:2*sy-my ]
        
        rela = np.abs(a-self.sobela)
        rela[rela>math.pi] = 2*math.pi - rela[rela>math.pi]
        intensity = ( math.pi - rela*2 ) / math.pi * 255
        intensity *= self.sobelm/3421.2
        disMult = .5-mdis /  1024
        disMult[disMult<0] = 0
        intensity *= disMult

        arr[:,:,0] = intensity
        arr[:,:,1] = intensity
        arr[:,:,2] = intensity

        arr[ arr<0 ] = 0
        arr[ arr>255 ] = 255

        return arr

#-------------------------------------------------------------------------------
class Moon():

    def __init__( self, world ):

        self.world = world
        self.r = 512

        #arr = np.zeros( (2*r+1,2*r+1,3) )
        r = self.r
        arr = np.fromfunction( lambda x,y,z: 20/np.hypot(x-r-.5,y-r-.5) , (2*r+1,2*r+1,3) )


        arr *= 255
        arr -= 10
        arr[arr< 0 ] = 0
        arr[arr>200] = 255

        self.arr = arr
        
        #cv2.circle( arr, (r,r), r, (255,255,255), -1 )
        

    def draw( self, shape ):

        pos = self.world.mpos

        arr = np.zeros( shape )

        r = self.r
        arrBlit( arr, self.arr, pos[0], pos[1], middle = True, overlay = True )
        #arr[ pos[0]-r:pos[0]+r+1 , pos[1]-r:pos[1]+r+1 ] = self.arr
        #cv2.circle( arr, (pos[1],pos[0]) , 11, (255,255,255), -1 )
        return arr

#----------------------------------------------------------------------------

def loadImage( path ):
    return np.swapaxes( cv2.imread( path )[:,:,::-1] , 0, 1 )





def arrOverlayWhite( dest, source ):

    dest[:,:,:3] *= 1 - source[:,:,:3]/255
    dest[:,:,:3] += 1 * source[:,:,:3]


def arrOverlayBlack( dest, source):

    dest[:,:,:3] *= 1 - source[:,:,:3]/255
    #dest[:,:,:3] += 1 * source[:,:,:3]


def arrOverlay( dest, source):

    dest[:,:,0] *= 1 - source[:,:,3]/255
    dest[:,:,1] *= 1 - source[:,:,3]/255
    dest[:,:,2] *= 1 - source[:,:,3]/255

    dest[:,:,0] += source[:,:,0] * source[:,:,3]
    dest[:,:,1] += source[:,:,1] * source[:,:,3]
    dest[:,:,2] += source[:,:,2] * source[:,:,3]
    


def test():

    world = World()
    world.draw()
    
    clock = pygame.time.Clock()
    world.t = Timer()

    while True:
        
        clock.tick(30)
        world.t.end('tick')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                world.t.print()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
        if pygame.mouse.get_pressed()[0]:
            
            world.mpos = pygame.mouse.get_pos()
            world.draw()


if __name__ == '__main__':
    test()
