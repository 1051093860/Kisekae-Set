import re

class CNFConfigParser:
    def __init__(self, filename):
        self.filename = filename
        self.memory_size = None
        self.screen_size = (448, 320)  # 默认值
        self.palettes = []
        self.external_color = None
        self.cells = []
        self.sets = []
        self.comments = []     

    def parse(self):
        with open(self.filename, 'r',encoding='shift-jis') as file:
            for line in file:
                self.parse_line(line)

    def parse_line(self, line:str):
        if(line.startswith(' ') or line.startswith('\t')):
            self.parse_set_nextline(line)
            return
        
        line = line.strip()
        if line.startswith('='):
            self.parse_memory_size(line)
        elif line.startswith('('):
            self.parse_screen_size(line)
        elif line.startswith('%'):
            self.parse_palette(line)
        elif line.startswith('['):
            self.parse_external_color(line)
        elif line.startswith('#'):
            self.parse_cell(line)
        elif line.startswith('$'):
            self.parse_set(line)
        elif line.startswith(';'):
            self.comments.append(line[1:].strip())
        elif line == '':
            pass
        else:
            raise ValueError(f"Invalid line({len(line)}): \n{line}")

    def parse_memory_size(self, line):
        parts = line.split()
        if len(parts) == 2 and parts[1].endswith('K'):
            self.memory_size = parts[1]

    def parse_screen_size(self, line):
        parts = line[1:-1].split(',')
        if len(parts) == 2:
            self.screen_size = tuple(map(int, parts))

    def parse_palette(self, line):
        filename = line[1:].strip()
        self.palettes.append(filename)

    def parse_external_color(self, line):
        color_code = int(line[1:].strip())
        self.external_color = color_code

    def parse_cell(self, line:str):
        setids = line.split(':')
        parts = setids[0]
        setids = setids[1].split(';')[0].split()
        palid = parts.split('*')
        parts = palid[0]
        palid = int(palid[1].strip()) if len(palid) > 1 else 0

        mark = parts.split()
        filename = mark[1].strip()
        mark = mark[0].split('.')
        fixation = int(mark[1]) if len(mark) == 2 else 0
        mark = int(mark[0][1:])
        
        cell = {
            'mark':mark,
            'fixation':fixation,
            'palid':palid,
            'filename':filename,
            'setids':setids
        }

        self.cells.append(cell)

    def parse_set_nextline(self, line):
        line = line.strip()
        parts = re.split(r'\s+', line.strip())
        coordinates = [tuple(map(int, p.split(','))) if p != '*' else (0,0) for p in parts]
        self.sets[-1]['coordinates'].extend(coordinates)

    def parse_set(self, line):
        parts = re.split(r'\s+', line[1:].strip())
        palette_group = int(parts[0])
        coordinates = [tuple(map(int, p.split(','))) if p != '*' else (0,0) for p in parts[1:]]
        set = {
            'palette_group':palette_group,
            'coordinates':coordinates
        }
        self.sets.append(set)

    def display_info(self):
        print(f"Memory Size: {self.memory_size}")
        print(f"Screen Size: {self.screen_size}")
        print(f"Palettes: {self.palettes}")
        print(f"External Color: {self.external_color}")
        print("Cells:")
        for cell in self.cells:
            print(cell)
        print("Sets:")
        for set in self.sets:
            print(f"  Group {set['palette_group']}: {set['coordinates']}")
        print("Comments:")
        for comment in self.comments:
            print(f"  {comment}")

if __name__ == '__main__':
    config_parser = CNFConfigParser('water1.cnf')
    config_parser.parse()
    config_parser.display_info()