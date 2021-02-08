

class Component:

    def __init__(self, mmu):
        self._mmu = mmu
        self._register()
    
    def _register(self):
        self._mmu.register_component(self)
    
    def read(self, address):
        input('not implemented')
    
    def write(self, address, value):
        input('not implemented')

    def is_in_range(self, address):
        input('not implemented')
        return False