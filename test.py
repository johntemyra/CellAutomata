import sys
sys.path.append(r"D:\\Eget\\Programmering\\Python\\diverse\\MyLib")
import PyGrid
import time



if __name__ == "__main__":
    myGrid = PyGrid.PGGrid(20,20,800,600)
    myGrid.tile_padding=0
    running = True
    while running:
        running = myGrid.tick_continue()
        print(myGrid._get_tile_from_mousepos())    
        time.sleep(1)
    # for i in range(0,2):
    #     running = myGrid.tick()
    #     myGrid.set_tile(i,0)
