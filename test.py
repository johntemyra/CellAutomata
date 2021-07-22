import sys
sys.path.append(r"D:\\Eget\\Programmering\\Python\\diverse\\MyLib")
import PyGrid
import time
from datetime import datetime, timedelta

class CellAutomata:
    def __init__(self):
        self.last_interaction = datetime.now()
        self._filled_cells = []
        self.rows = 100
        self.cols = 100

        self.myGrid = PyGrid.PGGrid(self.rows,self.cols,800,600)
        self.myGrid.tile_padding=0

        self.pause_step = False

    def remove_cell(self, pos):
        self.myGrid.remove_tile(pos[0],pos[1])
        self._filled_cells.remove(pos)

    def add_cell(self, pos):
        self.myGrid.set_tile(pos[0],pos[1])
        self._filled_cells.append(pos)

    def update(self, new_cells):
        for c in new_cells:
            pos, op_add = c
            if op_add:
                self.add_cell(pos)
            else:
                self.remove_cell(pos)

    def step(self):
        # new cell = exactly 3 neighbours
        # cell dies = fewer than 2 neighbours or more than 3 neighbours

        new_cells = []
        for row in range(0,self.rows):
            for col in range(0,self.cols):
                neighbour_count = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        if row + i < 0 or row + i >= self.rows:
                            continue
                        if col + j < 0 or col + j >= self.cols:
                            continue
                        if i == 0 and j == 0:
                            continue
                        if (row + i, col + j) in self._filled_cells:
                            neighbour_count += 1
                current_state = (row,col) in self._filled_cells
                if not current_state and neighbour_count == 3:
                    new_cells.append(((row,col),True))
                if current_state:
                    if neighbour_count < 2 or neighbour_count > 3:
                        new_cells.append(((row,col),False))
        self.update(new_cells)

    def handleInteraction(self):
        clicked_tile = self.myGrid.get_clicked_tile()
        now = datetime.now()
        cooldown_time = self.last_interaction + timedelta(milliseconds=500)
        # pause step
        if self.myGrid.key_pressed == 112: 
            if now > cooldown_time:
                self.last_interaction = datetime.now()
                if self.pause_step == True:
                    self.pause_step = False
                    print("unpausing")
                else:
                    print("pausing")
                    self.pause_step = True


        if clicked_tile:
            filled = self.myGrid.is_filled(clicked_tile[0],clicked_tile[1])
            if filled:
                if now > cooldown_time:
                    self.remove_cell(clicked_tile)
                    self.last_interaction = datetime.now()
            else:
                if now > cooldown_time:
                    self.add_cell(clicked_tile)
                    self.last_interaction = datetime.now()
                    

    def run(self):
        running = True
        count = 0
        while running:
            running = self.myGrid.update_drawing()
            self.handleInteraction()
            if count == 1:
                if not self.pause_step:
                    self.step()
                count = 0
            #time.sleep(0.001)
            count += 1

if __name__ == "__main__":
    program = CellAutomata()
    program.run()
    
