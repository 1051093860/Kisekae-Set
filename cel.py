import struct
import numpy as np

class Cell:
    def __init__(self,path_or_data:str|bytes) -> None:
        if(isinstance(path_or_data, str)):
            with open(path_or_data, 'rb') as file:
                path_or_data = file.read()
        self.data = path_or_data
        self.GS = True if self.data[:4] == b'KiSS' else False
        if self.GS:
            self.cell_file_mark = struct.unpack('B', self.data[4:5])[0]
            self.bit_per_pixel =  struct.unpack('B', self.data[5:6])[0]
            self.x_size = struct.unpack('H', self.data[6:8])[0]
            self.y_size = struct.unpack('H', self.data[8:10])[0]
            self.x_offset = struct.unpack('B', self.data[10:12])[0]
            self.y_offset = struct.unpack('B', self.data[14:16])[0]
            self.data = self.data[32:]
        else:
            self.x_size, self.y_size = struct.unpack('HH', self.data[:4])
            self.bit_per_pixel = 4
            self.data = self.data[4:]
            if(self.x_size*self.y_size < len(self.data) * 2):
                self.x_size+=1
            assert self.x_size*self.y_size == len(self.data) * 2

        self.parse_data()
    
    def parse_data(self):
        data = np.frombuffer(self.data, dtype=np.uint8)
        if self.bit_per_pixel == 4:
            high = data >> 4
            low = data & 0x0F
            data = np.ravel((high, low),'F')
        elif self.bit_per_pixel == 8:
            pass
        else:
            raise Exception("Unsupported bit per pixel")
        self.img_indices = data.reshape((self.y_size, self.x_size))
    
    def use_palette(self, palette:np.ndarray):
        if not isinstance(palette, np.ndarray):
            palette = np.array(palette)
        img = np.zeros((self.y_size, self.x_size, 4), dtype=np.uint8)
        img[:] = palette[self.img_indices]
        return img

if __name__ == '__main__':
    from kcf import Palette
    import cv2
    p = Palette('water1.kcf')
    c = Cell('k_chea1.cel')
    img = c.use_palette(p.getpal(0))
    print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    cv2.imwrite('test.png', img)