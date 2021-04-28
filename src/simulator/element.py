class Element:
    def __init__(self, name):
        self.name = name
    
    def reset(self):
        raise NotImplementedError

    def step(self, t, dt):
        raise NotImplementedError

class ActiveElement(Element):
    def step(self, action, t, dt):
        raise NotImplementedError