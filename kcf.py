import struct

default_palette = [
0x4b,0x69,0x53,0x53,0x10,0x0c,0x00,0x00,0x10,0x00,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x0F,0x00,0xF0,0x00,0xFF,0x00,0x00,0x0F,0x0F,0x0F,0xF0,0x0F,0xFF,0x0F,
0x77,0x07,0x0A,0x00,0xA0,0x00,0xAA,0x00,0x00,0x0A,0x0A,0x0A,0xA0,0x0A,0xAA,0x0A
]

class Palette:
    def __init__(self,path_or_data:str|bytes) -> None:
        if(isinstance(path_or_data, str)):
            with open(path_or_data, 'rb') as file:
                path_or_data = file.read()
        self.data = path_or_data
        self.GS = True if self.data[:4] == b'KiSS' else False
        if self.GS:
            self.palette_mask = struct.unpack('B', self.data[4:5])[0]
            self.bit_per_color =  struct.unpack('B', self.data[5:6])[0]
            self.colors_per_palette = struct.unpack('H', self.data[8:10])[0]
            self.palette_count = struct.unpack('H', self.data[10:12])[0]
            self.data = self.data[32:]
        else:
            self.palette_mask = 0
            self.bit_per_color = 12
            self.colors_per_palette = 16
            self.palette_count = 10

        self.pals = []
        self.parse_palette()

    def parse_palette(self):
        idx = 0
        if(self.bit_per_color == 12):
            for i in range(self.palette_count):
                pal = []
                for j in range(self.colors_per_palette):
                    color = (
                        (self.data[idx] >> 4) * 0x11,
                        (self.data[idx+1] & 0xf) * 0x11,
                        (self.data[idx] & 0xf) * 0x11,
                        0xff if j else 0
                    )
                    idx += 2
                    pal.append(color)
                self.pals.append(pal)
        elif(self.bit_per_color == 24):
            for i in range(self.palette_count):
                pal = []
                for j in range(self.colors_per_palette):
                    color = (
                        self.data[idx],
                        self.data[idx+1],
                        self.data[idx+2],
                        0xff if j else 0
                    )
                    idx += 3
                    pal.append(color)
                self.pals.append(pal)
        else:
            raise Exception("Unsupported bit per color")
        
    def display(self):
        print((self.pals[0][0]))

    def getpal(self, group:int):
        return self.pals[group]
    
if __name__ == '__main__':
    p = Palette('water1.kcf')
    p.display()
