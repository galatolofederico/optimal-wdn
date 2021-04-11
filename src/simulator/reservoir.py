from src.simulator.element import Element

class Reservoir(Element):
    def __init__(self, system=None, max_volume=None, min_volume=0, initial_volume=0):
        assert system is not None, "Each reservoir must be in a System, use the keyword argument 'system' to specify it"
        assert type(system).__name__ == "System", "'system' must be a System"
        
        assert max_volume is not None, "You have to specify a reservoir maximum volume"

        self.system = system
        self.max_volume = max_volume
        self.min_volume = min_volume
        self.initial_volume = initial_volume

        self.system.add_reservoir(self)

        self.reset()

    def increase(self, volume):
        self.current_volume = self.current_volume + volume
        overflow = 0
        
        if self.current_volume > self.max_volume:
            #print("WARNING: Reservoir is overflowing")
            overflow = self.current_volume - self.max_volume
            self.overflow_volume += overflow
        
        self.current_volume = min(self.current_volume, self.max_volume)
        return overflow

    def decrease(self, volume):
        self.current_volume = self.current_volume - volume
        underflow = 0

        if self.current_volume < self.min_volume:
            #print("CRITICAL: Reservoir is underflowing")
            underflow = self.min_volume - self.current_volume
            self.underflow_volume += underflow
        
        self.current_volume = max(self.current_volume, self.min_volume)
        return underflow

    def step(self, t, dt):
        return {
            "current_volume": self.current_volume,
            "overflow_volume": self.overflow_volume,
            "underflow_volume": self.underflow_volume,
        }

    def reset(self):
        self.current_volume = self.initial_volume
        self.overflow_volume = 0
        self.underflow_volume = 0