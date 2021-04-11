class Element:
    def reset(self):
        raise NotImplementedError

    def step(self, t, dt):
        raise NotImplementedError

class ActiveElement(Element):
    def step(self, action, t, dt):
        raise NotImplementedError