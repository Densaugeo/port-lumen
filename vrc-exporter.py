# Requires a port-lumen.toml file from the template in serverminer-download.py


# Python libraries to evaluate:
# - mcapy from https://github.com/wensheng/mcapy
# - anvil-parser-2 from https://github.com/0xTiger/anvil-parser2
# 
# Issues to report on anvil-parser2
# - .get_section() and .stream_blocks() need a doc string update for section
#   ranges
# - .get_block() needs a doc string / type hint update to show passing an int
#   to section is not allowed
# - .get_palette() needs an update

import sys, time, re, typing, dataclasses, logging, json, enum
import pathlib, contextlib, tomllib

import anvil, nbt

###################
# Terminal Colors #
###################

RESET     = '\x1b[0m'
BOLD      = '\x1b[1m'
FAINT     = '\x1b[2m'
ITALIC    = '\x1b[3m'
UNDERLINE = '\x1b[4m'
BLINK     = '\x1b[5m'
INVERT    = '\x1b[7m'
STRIKE    = '\x1b[9m'
WHITE     = '\x1b[38;2;255;255;255m' #fff
GRAY      = '\x1b[38;2;204;204;204m' #ccc
MAGENTA   = '\x1b[38;2;255;0;255m'   #f0f
VIOLET    = '\x1b[38;2;204;102;255m' #c6f
BLUE      = '\x1b[38;2;68;170;221m'  #4ad
CYAN      = '\x1b[38;2;68;221;221m'  #4dd
AQUA      = '\x1b[38;2;26;186;151m'  #1aba97
GREEN     = '\x1b[38;2;68;221;68m'   #4d4
ORANGE    = '\x1b[38;2;236;182;74m'  #ecb64a
RED       = '\x1b[38;2;255;0;0m'     #f00
WARNING_ORANGE = '\x1b[38;2;246;116;0m' # from KWrite's makefile highlighting

##########################
# Custom Data Structures #
##########################

@dataclasses.dataclass
class Coordinate:
    x: int
    y: int
    z: int
    
    def __add__(self, other: typing.Self) -> typing.Self:
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: typing.Self) -> typing.Self:
        return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def as_tuple(self) -> (int, int, int):
        return (self.x, self.y, self.z)

@dataclasses.dataclass
class ExportArea:
    min: Coordinate
    max: Coordinate
    
    def get_section_overlap(self, cx: int, sy: int, cz: int) \
    -> (range, range, range):
        section_coordinate = Coordinate(16*cx, 16*sy, 16*cz)
        min_local = self.min - section_coordinate
        max_local = self.max - section_coordinate
        
        return (
            range(max(0, min_local.x), min(16, max_local.x + 1)),
            range(max(0, min_local.y), min(16, max_local.y + 1)),
            range(max(0, min_local.z), min(16, max_local.z + 1)),
        )
    
    def contains(self, coord: Coordinate) -> bool:
        return (
            self.min.x <= coord.x <= self.max.x and
            self.min.y <= coord.y <= self.max.y and
            self.min.z <= coord.z <= self.max.z
        )

@dataclasses.dataclass
class RegionBank:
    path: pathlib.Path
    _regions: dict[(int, int), anvil.Region] = dataclasses.field(
        default_factory=dict)
    
    def load_region(self, x: int, z: int):
        self._regions[(x, z)] = anvil.Region.from_file(
            str(self.path / f'r.{x}.{z}.mca'))
    
    def get_region(self, x: int, z: int) -> anvil.Region:
        return self._regions[(x, z)]
    
    def get_chunk(self, x: int, z: int) -> anvil.Chunk:
        return self._regions[(x//32, z//32)].get_chunk(x % 32, z % 32)
    
    def get_block(self, x: int, y: int, z: int) -> anvil.Block:
        return self.get_chunk(x//16, z//16).get_block(x % 16, y, z % 16)

@dataclasses.dataclass
class BubbleColumn:
    position: Coordinate
    height: int = 1

@dataclasses.dataclass
class WrittenBook:
    title: str
    text: str
    
    @classmethod
    def from_nbt(cls, item: nbt.nbt.TAG_Compound) -> typing.Self:
        assert item['id'].value == 'minecraft:written_book'
        
        content = item['components']['minecraft:written_book_content']
        title = content['title']['raw'].value
        text = ''.join([page['raw'].value for page in content['pages']])
        
        return cls(title, text)

class Facing(enum.Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    
    @classmethod
    def from_nbt(cls, tag: nbt.nbt.TAG_String) -> typing.Self:
        v = tag.value
        
        if   v == 'north': return cls.North
        elif v == 'east' : return cls.East
        elif v == 'south': return cls.South
        elif v == 'west' : return cls.West

@dataclasses.dataclass
class ChiselShelf:
    coord: Coordinate
    facing: Facing
    books: list[WrittenBook] = dataclasses.field(default_factory=list)
    
    @classmethod
    def from_nbt(cls, entity: nbt.nbt.TAG_Compound) -> typing.Self:
        coord = Coordinate(entity['x'].value, entity['y'].value,
            entity['z'].value)
        
        block = rb.get_block(coord.x, coord.y, coord.z)
        facing = Facing.from_nbt(block.properties['facing'])
        
        result = cls(coord, facing)
        
        for item in entity['Items']:
            if item['id'].value == 'minecraft:written_book':
                result.books.append(WrittenBook.from_nbt(item))
        
        return result

##########
# Config #
##########

with open('port-lumen.toml', 'rb') as f:
    toml = tomllib.load(f)

FTP_PATH = pathlib.Path(toml['download']['ftp_path'])
SAVE_PATH = pathlib.Path('downloads') / FTP_PATH.name
REGION_PATH = SAVE_PATH / pathlib.Path(toml['export']['dimension']) / 'region'
EXPORT_PATH = pathlib.Path('Assets') / 'Minecraft Import' \
    / f'{FTP_PATH.name}.gltf'

X_MIN = int(toml['export']['min'][0])
X_MAX = int(toml['export']['max'][0])
Y_MIN = int(toml['export']['min'][1])
Y_MAX = int(toml['export']['max'][1])
Z_MIN = int(toml['export']['min'][2])
Z_MAX = int(toml['export']['max'][2])

export_area = ExportArea(
    Coordinate(*toml['export']['min']),
    Coordinate(*toml['export']['max']),
)

##############
# Key Inputs #
##############

OLD_OVERWORLD = pathlib.Path('/projects/Port Lumen download for testing') \
    / 'port-lumen.den-antares.com:33580' / 'port-lumen' / 'region'

NEW_OVERWORLD = pathlib.Path('/projects/Port Lumen download for testing 2') \
    / 'port-lumen.den-antares.com:33580' / 'port-lumen' \
    / 'dimensions' / 'minecraft' / 'overworld' / 'region'

#REGION_PATH = OLD_OVERWORLD

print()

print(
f'{BOLD}{WHITE}Boundary    Block  Section  Region{RESET}\n'
f'X_min: {VIOLET}{X_MIN:9} {BLUE}{X_MIN//16:7} {AQUA}{X_MIN//512:7}{RESET}\n'
f'X_max: {VIOLET}{X_MAX:9} {BLUE}{X_MAX//16:7} {AQUA}{X_MAX//512:7}{RESET}\n'
f'Y_min: {VIOLET}{Y_MIN:9} {BLUE}{Y_MIN//16:7} {GRAY}      - {RESET}\n'
f'Y_max: {VIOLET}{Y_MAX:9} {BLUE}{Y_MAX//16:7} {GRAY}      - {RESET}\n'
f'Z_min: {VIOLET}{Z_MIN:9} {BLUE}{Z_MIN//16:7} {AQUA}{Z_MIN//512:7}{RESET}\n'
f'Z_max: {VIOLET}{Z_MAX:9} {BLUE}{Z_MAX//16:7} {AQUA}{Z_MAX//512:7}{RESET}\n'
)

##########################
# Bock and Entity Search #
##########################

chisel_shelves = []
bubble_coords = []

print(f'{BOLD}{WHITE}Loading region files:{RESET}{GRAY}')
print(f'Expecting region files in {BOLD}{ORANGE}{REGION_PATH}{RESET}{GRAY}')
rb = RegionBank(REGION_PATH)

for x in range(X_MIN//512, X_MAX//512 + 1):
    for z in range(Z_MIN//512, Z_MAX//512 + 1):
        print(f'Loading region {AQUA}({x}, {z}){GRAY} from '
            f'{BOLD}{ORANGE}r.{x}.{z}.mca{RESET}{GRAY} - ', end='')
        
        rb.load_region(x, z)
        
        print(f'{GREEN}OK{GRAY}')
print(RESET)

chunk_count = (X_MAX//16 + 1 - X_MIN//16)*(Z_MAX//16 + 1 - Z_MIN//16)
section_count = chunk_count*(Y_MAX//16 + 1 - Y_MIN//16)
print(f'{BOLD}{WHITE}Scanning {VIOLET}{section_count}{WHITE} sections across '
    f'{VIOLET}{chunk_count}{WHITE} chunks:{RESET}{GRAY}')

print(f'Searching for blocks - ', end='')
sections_searched = 0
start_time = time.monotonic()
for cx in range(X_MIN//16, X_MAX//16 + 1):
    for cz in range(Z_MIN//16, Z_MAX//16 + 1):
        chunk = rb.get_chunk(cx, cz)
        
        for sy in range(Y_MIN//16, Y_MAX//16 + 1):
            section = chunk.get_section(sy)
            
            search = False
            
            for block_tag in section['block_states']['palette']:
                if block_tag['Name'].value == 'minecraft:bubble_column':
                    search = True
            
            if search:
                sections_searched += 1
                
                x_range, y_range, z_range = export_area.get_section_overlap(
                    cx, sy, cz)
                
                for x in x_range:
                    for y in y_range:
                        for z in z_range:
                            block = chunk.get_block(x, y, z, section)
                            
                            if block.name() == 'minecraft:bubble_column' \
                            and block.properties['drag'].value == 'false':
                                bubble_coords.append(Coordinate(
                                    16*cx + x, 16*sy + y, 16*cz + z))
print(f'{GREEN}OK{GRAY}')
print(f'├ Completed in '
    f'{BOLD}{AQUA}{time.monotonic() - start_time:.3} s{RESET}{GRAY}')
print(f'├ {VIOLET}{sections_searched}{GRAY} sections required in-depth search')
print(f'└ Found {VIOLET}{len(bubble_coords)}{GRAY} rising bubble column blocks')

print(f'Searching for block entities - ', end='')
for cx in range(X_MIN//16, X_MAX//16 + 1):
    for cz in range(Z_MIN//16, Z_MAX//16 + 1):
        chunk = rb.get_chunk(cx, cz)
        
        for entity in chunk.tile_entities:
            if entity['id'].value != 'minecraft:chiseled_bookshelf':
                continue
            
            if not export_area.contains(Coordinate(entity['x'].value, 
            entity['y'].value, entity['z'].value)):
                continue
            
            chisel_shelves.append(ChiselShelf.from_nbt(entity))
print(f'{GREEN}OK{GRAY}')
print(f'└ Found {VIOLET}{len(chisel_shelves)}{GRAY} chiseled bookshelves')
print(RESET)

####################
# Feature Analysis #
####################

bubble_columns = []

print(f'{BOLD}{WHITE}Analyzing features:{RESET}{GRAY}')

print(f'Consolidating {BLUE}{len(bubble_coords)}{GRAY} bubble column blocks')
bubble_coords.sort(key=lambda b: (b.x, b.z, b.y))
for i in range(len(bubble_coords)):
    if i and bubble_coords[i] == bubble_coords[i - 1] + Coordinate(0, 1, 0):
        bubble_columns[-1].height += 1
    else:
        bubble_columns.append(BubbleColumn(bubble_coords[i]))
print(f'└ Consolidated into {BLUE}{len(bubble_columns)}{GRAY} bubble columns')

print(f'Examining {BLUE}{len(chisel_shelves)}{GRAY} chiseled bookshelves')
for chisel_shelf in chisel_shelves:
    protv = False
    
    for book in chisel_shelf.books:
        print(f'├ Found book {BOLD}{CYAN}{book.title}{RESET}{GRAY} at '
            f'{BLUE}{chisel_shelf.coord.as_tuple()}{GRAY}')
        
        if book.title == 'ProTV':
            if not protv:
                protv = True
            else:
                print(f'└ {WARNING_ORANGE}Warning:{GRAY} Found multiple '
                    f'{CYAN}ProTV{GRAY} books, using first')
    
    if protv:
        print(f'│ └ {WARNING_ORANGE}Warning:{GRAY} ProTV placement not yet '
            f'implemented')
print(f'└ Found {CYAN}{sum(len(c.books) for c in chisel_shelves)}{GRAY} books')
print(RESET)

###################
# GLTF Generation #
###################

print(f'{BOLD}{WHITE}Generating .gltf:{RESET}{GRAY}')

gltf = {
    'asset': {
        'generator': 'Port Lumen VRC Exporter',
        'minVersion': '2.0',
        'version': '2.0',
    },
    'scene': 0,
    'scenes': [{
        'name': FTP_PATH.name,
        'nodes': [],
    }],
    'nodes': [],
}

print(f'Attaching bubble columns')
for i, column in enumerate(bubble_columns):
    # Height is reduced by 1/8 block to account for water surface at top of
    # being 1/8 block below block boundary
    height = column.height - 0.125
    
    gltf['scenes'][0]['nodes'].append(len(gltf['nodes']))
    gltf['nodes'].append({
        'name': f'bubble-column-{i}',
        'translation': [
            column.position.x + 0.5,
            column.position.y + height/2,
            column.position.z + 0.5
        ],
        'scale': [1, height, 1],
    })

print(f'Saving as {BOLD}{ORANGE}{EXPORT_PATH}{RESET}{GRAY} - ',
    end='')
with open(EXPORT_PATH, 'w') as f:
    json.dump(gltf, f)
print(f'{GREEN}OK{GRAY}')
print(RESET)
