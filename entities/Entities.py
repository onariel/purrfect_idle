from Cat_counter import CatCounter

class Entities:
    cps = 0
    cats: CatCounter

    def __init__(self, cats):
        cats : CatCounter = cats

    def update_cps(self):
        cps = self.cats
