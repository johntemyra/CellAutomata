import sys
sys.path.append(r"D:\\Eget\\Programmering\\Python\\diverse\\MyLib")
import PyGrid
import time
from datetime import datetime, timedelta

class CellAutomata:
    def __init__(self):
        self.last_interaction = datetime.now()
        self._filled_cells = []
        self.rows = 50
        self.cols = 50

        caption = "Game Of Life: 'p' - pause, 'q' - quit, create cells with mouse"        
        self.myGrid = PyGrid.PGGrid(self.rows,self.cols,800,600,window_caption=caption)
        self.myGrid.tile_padding=0
        self.myGrid.nogrid = False

        self.simulation_speed = 100
        self.myGrid.draw_border = False
        self.pause_step = True
        self.last_clicked = None

    def remove_cell(self, pos):
        if pos in self._filled_cells:
            self.myGrid.remove_tile(pos[0],pos[1])
            self._filled_cells.remove(pos)

    def add_cell(self, pos):
        if pos not in self._filled_cells:
            self.myGrid.set_tile(pos[0],pos[1])
            self._filled_cells.append(pos)

    def update(self, new_cells):
        for c in new_cells:
            pos, op_add = c
            if op_add:
                self.add_cell(pos)
            else:
                self.remove_cell(pos)

    def count_neighbours(self, pos, recurse):
        neighbour_count = 0
        row,col = pos
        newborns = []
        for i in range(-1,2):
            for j in range(-1,2):
                if row + i < 0 or row + i >= self.rows:
                    continue
                if col + j < 0 or col + j >= self.cols:
                    continue
                if i == 0 and j == 0:
                    continue

                row_i = row + i
                col_j = col + j
                if recurse:
                    surrounding_count, _ = self.count_neighbours((row_i,col_j), recurse=False)
                    if surrounding_count == 3 and (row_i,col_j) not in self._filled_cells:
                        if (row_i,col_j) not in newborns:
                            newborns.append((row_i,col_j))
                if (row_i, col_j) in self._filled_cells:
                    neighbour_count += 1
        return neighbour_count, newborns

    def step(self):
        # new cell = exactly 3 neighbours
        # cell dies = fewer than 2 neighbours or more than 3 neighbours

        new_cells = []
        for c in self._filled_cells:
            neighbour_count,newborn_cells = self.count_neighbours(c,recurse=True)
            if neighbour_count < 2 or neighbour_count > 3:
                new_cells.append((c, False))
            for newbie in newborn_cells:
                new_cells.append((newbie, True))
        self.update(new_cells)

    def handleInteraction(self):
        now = datetime.now()
        cooldown_time = self.last_interaction + timedelta(milliseconds=200)
        # pause step
        if self.myGrid.key_pressed == 112: 
            if now > cooldown_time:
                self.last_interaction = datetime.now()
                if self.pause_step == True:
                    self.pause_step = False
                    self.myGrid.draw_border = True
                else:
                    self.myGrid.draw_border = False
                    self.pause_step = True

        #minus
        if self.myGrid.key_pressed == 1073741911:
            if now > cooldown_time:
                self.last_interaction = datetime.now()
                if self.simulation_speed - 10 > 1:
                    self.simulation_speed -= 10
        #plus
        if self.myGrid.key_pressed == 1073741910:
            if now > cooldown_time:
                self.last_interaction = datetime.now()
                if self.simulation_speed + 10 < 500:
                    self.simulation_speed += 10

        #c
        if self.myGrid.key_pressed == 99:
            if now > cooldown_time:
                self._filled_cells = []
                self.myGrid.clear_tiles()

        if self.myGrid.mouse_pressed:
            clicked_tile = self.myGrid.get_clicked_tile()
            if clicked_tile:
                filled = self.myGrid.is_filled(clicked_tile[0],clicked_tile[1])
                if clicked_tile != self.last_clicked:
                    self.last_clicked = clicked_tile
                    if filled:
                        self.remove_cell(clicked_tile)
                    else:
                        self.add_cell(clicked_tile)
        else:
            self.last_clicked = None

    def run(self):
        running = True
        count = 0
        while running:
            running = self.myGrid.update_drawing()
            self.handleInteraction()
            if count > self.simulation_speed:
                if not self.pause_step:
                    self.step()
                count = 0
            #time.sleep(0.1)
            count += 1

if __name__ == "__main__":
    program = CellAutomata()
    program.run()
    
