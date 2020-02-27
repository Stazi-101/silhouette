import pygame; print('p')
import random
import numpy as np; print('n')



class World():


    def __init__(self,size):

        self.size = size

        self.res = 3

        self.pos = [1,1]

        self.allStars = [0]*100

        pygame.init()
        self.screen = pygame.display.set_mode( self.size )
        self.surface = pygame.Surface( self.size )

        self.genArr()
        self.drawArr()


    def genArr(self):

        sx,sy = self.size
        rarr = np.random.rand(sx,sy)
        threshholds = [ 36/i**2 for i in range(1,20) ]

        threshholds = [ t/36/50 for t in threshholds ]

        

        
        self.arr = np.zeros( (sx,sy) )
        for i in threshholds:
            self.arr[ rarr<i ] += 1

        '''
        for i in range(3,20):
            pass
            print( (self.arr==i).sum() , end=', ')
        print()
        '''
        #print( self.arr[:20,:20] )
        


        return

    
    def drawArr(self):
        
        sx,sy = self.size
        sarr = np.zeros( (sx,sy) )
        sarr[self.arr<=4] = 255/4*self.arr[self.arr<=4]
        self.arr[self.arr>4] += 2

        for x in range( 0,sx,self.res ):
            for y in range( 0,sy,self.res ):
                size = self.arr[x,y]
                if size:
                    r = self.getStar(size).shape[0]//2
                    arrOverlay2D( sarr[ x-r:x+r+1 , y-r:y+r+1 ] , self.getStar(size) )
                    #self.screen.blit( self.getStar(r), (x-r,y-r) )

        sarr3D = np.zeros( (sx,sy,3) )
        sarr3D[:,:,0] = sarr
        sarr3D[:,:,1] = sarr
        sarr3D[:,:,2] = sarr

        self.drawnArr = sarr3D

        #arrBlitSurf( self.surface, sarr3D )

        


    def getStar(self,n):

        n = int(n)

        n = len(self.allStars)-1 if n>=len(self.allStars) else n
        #print(self.allStars[n]) #HEREEEEEEEEEEEEEEE****************************************************

        if type( self.allStars[n] ) == int:
            self.allStars[n] = starArr( n )
        
        #self.allStars[n] = self.allStars[n] if not self.allStars[n]==0 else starArr( n )
        #print(self.allStars[n])
        
        return self.allStars[n]

            
        
def main():

    world = World( (512,512) )
    world.genArr()
    world.drawArr()
    arrBlitSurf( world.surface, world.drawnArr )
    world.screen.blit( world.surface, (0,0) )
    pygame.display.update()
    
    loop(world)
               

def loop(world):

    clock = pygame.time.Clock()
    
    while True:
        
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                world.genArr()
                world.drawArr()
                arrBlitSurf( world.surface, world.drawnArr )
                world.screen.blit( world.surface, (0,0) )

                pygame.display.update()

        

def starArr( r ):

    arr = np.ones( (2*r+1,2*r+1) )

    for x in range(-r,r+1):
        for y in range(-r,r+1):
            if x or y:
                val = ( x**2 + y**2 )**-.5 * r/100
                val *= abs( r/(x+.5) * r/(y+.5) * .2 )**.5
                arr[x+r,y+r]  =  val
            
    arr -= arr[0,0]

    arr *= 255
    arr[arr>255] = 255
    arr[ arr<0 ] = 0

    return arr


def arrOverlay2D( dest, source ):

    if len(dest.shape)==2:

        try:
            dest *= 1-source/255
            dest += source
        except ValueError:
            pass
        return


    try:

        dest[:,:,0] *= 1 - source[:,:]/255
        dest[:,:,1] *= 1 - source[:,:]/255
        dest[:,:,2] *= 1 - source[:,:]/255  
    
        dest[:,:,0] += source[:,:]
        dest[:,:,1] += source[:,:]
        dest[:,:,2] += source[:,:]

    except ValueError:
        return


def arrBlitSurf( surf, arr ):

    if len(arr.shape) == 2:
        narr = np.array( (arr,arr,arr) )

    surfarray = pygame.surfarray.pixels3d(surf)

    ax,ay = arr.shape[:2]
    surfarray[:ax,:ay] = arr
    del surfarray


def sizeDistrib( maxLength ):
    
    x = random.random()
    y = random.random()
    dis = (max((x,y)))
    n = int(1/dis)
    return n if n<maxLength else maxLength

    

if __name__=='__main__':
    main()
    pygame.quit()
