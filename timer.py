import threading,time
 
class timer(object):
    def __init__(self,sleep,callback):
        self.sleep=sleep
        self.callback=callback
        self.t=threading.Timer(self.sleep, self.callback)
        self.t.start()