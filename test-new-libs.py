# Python libraries to evaluate:
# - mcapy from https://github.com/wensheng/mcapy
# - anvil-parser-2 from https://github.com/0xTiger/anvil-parser2
# 
# Rust libraries of interest:
# - mca from https://github.com/VilleOlof/mca
# - mca-parser from https://github.com/funnyboy-roks/mca-parser
# 
# Issues to report on mca (if selected):
# - .get_section() and .stream_blocks() need a doc string update for section
#   ranges
# - .get_palette() needs an update

import re, sys, typing, dataclasses, logging, contextlib, json, pathlib
import builtins, tomllib

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

##############
# Key Inputs #
##############

OLD_OVERWORLD = pathlib.Path('/projects/Port Lumen download for testing') \
    / 'port-lumen.den-antares.com:33580' / 'port-lumen' / 'region'

NEW_OVERWORLD = pathlib.Path('/projects/Port Lumen download for testing 2') \
    / 'port-lumen.den-antares.com:33580' / 'port-lumen' \
    / 'dimensions' / 'minecraft' / 'overworld' / 'region'

x_min = -680
x_max = -326
y_min = 39
y_max = 319
z_min = 90
z_max = 435

print()

print(
f'{BOLD}{WHITE}Boundaries{RESET}  Block  Chunk  Region\n'
f'x_min: {VIOLET}{x_min:9} {BLUE}{x_min//16:6} {AQUA}{x_min//512:6}{RESET}\n'
f'x_max: {VIOLET}{x_max:9} {BLUE}{x_max//16:6} {AQUA}{x_max//512:6}{RESET}\n'
f'y_min: {VIOLET}{y_min:9} {BLUE}{y_min//16:6} {AQUA}{y_min//512:6}{RESET}\n'
f'y_max: {VIOLET}{y_max:9} {BLUE}{y_max//16:6} {AQUA}{y_max//512:6}{RESET}\n'
f'z_min: {VIOLET}{z_min:9} {BLUE}{z_min//16:6} {AQUA}{z_min//512:6}{RESET}\n'
f'z_max: {VIOLET}{z_max:9} {BLUE}{z_max//16:6} {AQUA}{z_max//512:6}{RESET}\n'
)

region_indices = []
for x in range(x_min//512, x_max//512 + 1):
    for z in range(z_min//512, z_max//512 + 1):
        region_indices.append((x, z))
print(f'Regions indices to load: {region_indices}')
print()

################
# Testing Area #
################

print(f'{BOLD}{WHITE}==== Testing {CYAN}mca{WHITE} library ===={RESET}\n')

import mca

regions = []
for region_index in region_indices:
    regions.append(mca.Region.from_file(
        str(NEW_OVERWORLD / f'r.{region_index[0]}.{region_index[1]}.mca')))

print(f'{BOLD}{WHITE}What\'s a {VIOLET}Region{WHITE} look like?{RESET}')
print(regions[1])
print(dir(regions[1]))
print()

print(f'{BOLD}{WHITE}What\'s a {BLUE}Chunk{WHITE} look like?{RESET}')
chunk = regions[1].get_chunk(3, 17)
print(chunk)
print(dir(chunk))
#print(chunk.tile_entities)
#print(chunk.tile_entities[0].pretty_tree())
print()

print(f'{BOLD}{WHITE}What\'s a {AQUA}Block{WHITE} look like?{RESET}')
block = regions[1].get_chunk(3, 17).get_block(0, 0, 0)
print(block)
print(dir(block))
#print(block.id)
#print(block.name())
#print(block.namespace)
#print(block.properties)
print()

#print(f'{BOLD}{WHITE}What\'s an {MAGENTA}entity{WHITE} look like?{RESET}')
#entity = regions[1].get_chunk(3, 17).tile_entities[0]
#print(entity)
#print(dir(entity))
#print(entity.pretty_tree())
#print(entity.id)
#print(entity.items())
#print(entity.keys())
#print(entity.name)
#print(entity.namestr())
#print(entity.tags)
#print(entity.value)
#print(entity.values())
#print(entity.valuestr())
#print(entity.tags[0])
#print(entity.tags[1])
#print(entity.tags[2])
#print(entity.tags[3])
#print(entity.tags[4])
#print(entity.tags[5])
#print()

bubble_column_blocks = []
chiseled_bookshelves = []

chunk = regions[1].get_chunk(3, 17)
for i in range(-4, 20):
    section = chunk.get_section(i)
    
    search = False
    
    for block_tag in section['block_states']['palette']:
        if block_tag['Name'].value == 'minecraft:chiseled_bookshelf':
            print(f'Found a chisel shelf in section {i}')
            search = True
        if block_tag['Name'].value == 'minecraft:bubble_column':
            print(f'Found a bubble column in section {i}')
            search = True
    
    if search:
        for x in range(16):
            for y in range(16):
                for z in range(16):
                    block = chunk.get_block(x, 16*i + y, z)
                    if block.name() == 'minecraft:chiseled_bookshelf':
                        chiseled_bookshelves.append(Coordinate(x, y, z))
                    if block.name() == 'minecraft:bubble_column':
                        bubble_column_blocks.append(Coordinate(x, y, z))
print(bubble_column_blocks)
print(chiseled_bookshelves)
#print(section)
#print(dir(section))
#print(section.pretty_tree())
#print()
#palette = section['block_states']['palette']
#print(palette.pretty_tree())
#print(dir(palette))
#for x in palette:
#    #print(mca.Block.from_palette(x))
#    print(x['Name'])
print()

# Column with chiseled bookshelf
#chunk = regions[1].get_chunk(3, 17)
#for x in range(3, 4):
#    for y in range(63, 70):
#        block = chunk.get_block(x, y, 11)
#        print(block)
#        print(block.properties)
#for entity in chunk.tile_entities:
#    if entity.get('id').value == 'minecraft:chiseled_bookshelf':
#        print(entity.pretty_tree())
#        for item in entity.get('Items'):
#            print(item)
#            book_content = \
#                item.get('components').get('minecraft:written_book_content')
#            print(book_content.get('title').get('raw').value)
#            for page in book_content.get('pages'):
#                print(page.get('raw').value)

# Bubble column near spawn
#chunk = regions[1].get_chunk(2, 17)
#for y in range(63, 70):
#    block = chunk.get_block(11, y, 4)
#    print(block)
#    print(block.properties)

# Column with a sign
#chunk = regions[1].get_chunk(2, 15)
#for x in range(15, 16):
#    for y in range(63, 70):
#        block = chunk.get_block(x, y, 13)
#        print(block)
#        print(block.properties)
#for entity in chunk.tile_entities:
#    if entity.get('x').value == -465 and entity.get('y').value == 67 \
#    and entity.get('z').value == 253:
#        print(entity)
#        print(entity.get('id').value)
#        print(entity.get('front_text').get('messages'))


'''import anvil

region = anvil.Region.from_file(str(world_path / 'dimensions' / 'minecraft'
    / 'overworld' / 'region' / 'r.0.0.mca'))

# You can also provide the region file name instead of the object
chunk = anvil.Chunk.from_region(region, 0, 0)

# If `section` is not provided, will get it from the y coords
# and assume it's global
block = chunk.get_block(0, 0, 0)

print("==== anvil ====")
print(region)
print(dir(region))
print(chunk)
print(dir(chunk))
print(block)
print(dir(block))
print(block.id)
print(block.name())
print(block.namespace)
print(block.properties)
print()
'''

