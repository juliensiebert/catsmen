from abc import ABCMeta, abstractmethod



class EventLoop(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.loop = True

    def stop(self):
        self.loop = False

    @abstractmethod
    def run(self):
        pass
