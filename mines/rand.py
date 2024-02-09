import random

class sigma:
    def predict(self, safeSpots):
        count = 0
        grid = [0]*25
        while count < safeSpots:
            a = random.randint(0, 24)
            if grid[a] == 1:
                continue
            grid[a] = 1
            count += 1
        return grid
