import time

class Timer():

    def __init__( self ):

        self.times = {}
        self.startTime = time.time()

    def end( self, name ):

        if name not in self.times.keys():
            self.times[name] = 0

        endTime = time.time()
        self.times[name] += endTime-self.startTime

        self.startTime = endTime

    def print( self ):

        for key in self.times:
            print( '{:<12}{:<5}'.format(key,self.times[key]) )
