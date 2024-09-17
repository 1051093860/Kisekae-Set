from typing import Tuple
from cel import Cell
from cnf import CNFConfigParser
from kcf import Palette

class KiSSEngine:
    def __init__(self,root) -> None:
        cnf_file_name = [i for i in os.listdir(root) if i.endswith('.cnf')][0]
        # print(cnf_file_name)
    
        self.cnf = CNFConfigParser(os.path.join(root, cnf_file_name))
        self.cnf.parse()

        self.palettes:list[Palette] = []
        self.cells:dict[int,Cell] = {}
        self.sets:list[Tuple[int,int]] = []

        self.load_palettes()
        self.load_cells()
        self.load_sets()
    
    def load_palettes(self):
        for i in self.cnf.palettes:
            self.palettes.append(Palette(i))
            # print(f'load {i}')

    def load_cells(self):
        for i in self.cnf.cells:
            mark = i['mark']
            self.cells[mark] = (Cell(i['filename']))
            # print(f'load {i["filename"]}')

    def load_sets(self):
        for i in self.cnf.sets:
            self.sets.append((i['palette_group'],i['coordinates']))

    def get_drawing(self,set_idx:int):
        imgs = []
        for mark,cell in self.cells.items():
            cur_set = self.sets[set_idx]
            pal_grp = cur_set[0]
            pos = cur_set[1][mark]
            img = cell.use_palette(self.palettes[pal_grp].getpal(0))
            imgs.append((img, pos))
        return imgs

import pygame
pygame.init()
class KiSS:
    def __init__(self,kissengine:KiSSEngine) -> None:
        self.screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)
        pygame.display.set_caption("KiSekae")
        self.clock = pygame.time.Clock()
        self.kiss = kissengine

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update_input()
            self.update_logics()
            self.update_graphics()
   
    def update_input(self):
        pass

    def update_logics(self):
        pass

    def draw_img(self,img,x,y):
        image_surface = pygame.Surface((img.shape[1], img.shape[0]), pygame.SRCALPHA)
        pygame.surfarray.pixels3d(image_surface)[:, :, :] = img[:, :, :3].transpose(1,0,2)  # RGB 部分
        pygame.surfarray.pixels_alpha(image_surface)[:, :] = img[:, :, 3].transpose(1,0)  # Alpha 通道
        self.screen.blit(image_surface, (x, y))

    def update_graphics(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        pal = self.kiss.palettes[0].getpal(0)

        for img,pos in self.kiss.get_drawing(0):
            self.draw_img(img, *pos)
            
        # Update display
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == '__main__':
    import os
    Root = os.path.abspath('.')
    kissengine = KiSSEngine(Root)
    KiSS(kissengine).main()