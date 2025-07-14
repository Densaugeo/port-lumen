# sudo dnf install python3-devel zlib-devel
# python -m pip install numpy==1.26.4
# python -m pip install amulet-core==1.9.30

import re, sys, typing, dataclasses, logging, contextlib, json, pathlib
import builtins
logging.disable() # amulet is noisy, even at import
import amulet, numpy

world_path = pathlib.Path('/home/den-antares/projects/Port Lumen download for '
    'testing/port-lumen.den-antares.com:33580/port-lumen')
x_min = -680
x_max = -326
y_min = 39
y_max = 319
z_min = 90
z_max = 435

bubble_code = None
bubble_blocks = [] # type: typing.List[Coordinate]
bubble_columns = []

box_of_16 = amulet.SelectionBox([0, 0, 0], [16, 16, 16])

####################
# Helper Functions #
####################

def style(styles: typing.List[str | int], string: object = '',
width: int | None = None, reapply_after_reset: bool = False) -> str:
    string = str(string)
    
    if width is not None:
        assert width > 0
        
        if len(string) <= width: string = f'{string:{width}}'
        else: string = string[:max(width - 3, 0)] + min(width, 3)*'.'
    
    ansi_codes = ''
    
    if not isinstance(styles, list):
        styles = [styles]
    
    for style in styles:
        match style:
            case int():
                ansi_codes += f'\033[{style}m'
            case str() if re.fullmatch('#[0-9a-fA-F]{3}', style):
                r, g, b = (int(style[i], 16)*0xff//0xf for i in [1, 2, 3])
                ansi_codes += f'\033[38;2;{r};{g};{b}m'
            case str() if re.fullmatch('#[0-9a-fA-F]{6}', style):
                r, g, b = (int(style[i:i+2], 16) for i in [1, 3, 5])
                ansi_codes += f'\033[38;2;{r};{g};{b}m'
            case _:
                raise ValueError(f'Unknown style: {style}')
    
    reset = '\033[0m' if styles and string else ''
    
    if reapply_after_reset:
        string = string.replace('\033[0m', '\033[0m' + ansi_codes)
    
    return ansi_codes + string + reset

RESET = 0
BOLD = 1
GRAY = '#ccc'
MAGENTA = '#f0f'
VIOLET = '#c6f'
BLUE = '#4ad'
AQUA = '#1aba97'
GREEN = '#4d4'
ORANGE = '#ecb64a'
RED = '#f00'

def fail(message: str):
    print(f'{style([BOLD, RED], 'Error:')} {message}')
    sys.exit(1)

class status:
    _print_count = 0
    
    def _print(self, message: str, **kwargs):
        if self._print_count > 0:
            message = '├ ' + message.replace('\n', '\n│ ')
        
        status.builtin_print(style([GRAY], message,
            reapply_after_reset=True), **kwargs)
        
        self._print_count += 1 + message.count('\n')
    
    def _print_reset(self):
        status.builtin_print(f'\033[{self._print_count}F', end='')
        self._print_count = 0
    
    def __init__(self, message: str):
        assert '\n' not in message, 'Newlines in status headings not supported'
        
        self.message = message
    
    def __enter__(self):
        self._print(self.message + '...')
        builtins.print = self._print
    
    # .__exit__() takes a couple more exception args that I don't care about
    def __exit__(self, exc_type: type, *args):
        builtins.print = status.builtin_print
        
        message = self.message + '...'
        message += style([RED], 'ERR') if exc_type else style([GREEN], 'OK')
        # If pipes were printed, change last one to an end pipe
        if self._print_count > 1:
            message += f'\033[{self._print_count - 1}E└'
        
        self._print_reset()
        self._print(message)

status.builtin_print = builtins.print

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
class BubbleColumn:
    position: Coordinate
    height: int = 1

#############
# Main Code #
#############

bound_1 = Coordinate(x_min, y_min, z_min)
bound_2 = Coordinate(x_max, y_max, z_max)

print('Loading data:')

with status(f'Loading world {style([BOLD, ORANGE], world_path.name)}'):
    world = amulet.load_level(world_path)

with status('Loading chunks'):
    chunk_boxes = list(world.get_chunk_boxes('minecraft:overworld',
        amulet.SelectionBox(bound_1.as_tuple(), bound_2.as_tuple())))
    print(f'Loaded {style([VIOLET], len(chunk_boxes))} chunks')

with status('Validating chunks'):
    for chunk_box in chunk_boxes:
        assert type(chunk_box) == tuple
        assert len(chunk_box) == 2
        assert type(chunk_box[0]) == amulet.api.chunk.Chunk
        assert type(chunk_box[1]) == amulet.SelectionBox

with status('Validating block palette'):
    # .block_palette must be converted to a list, or LSP code completion breaks
    # inside this loop
    for i, block in enumerate(list(world.block_palette)):
        base_name = block.base_name
        name = amulet.Block.parse_blockstate_string(block.blockstate)[1]
        assert base_name == name
        if base_name != 'bubble_column': continue
        # drag = True indicates a sinking bubble column, which we don't care
        # about
        if block.base_block.properties['drag'].py_str != 'false': continue
        
        assert block.base_block.base_name == 'bubble_column'
        assert len(block.extra_blocks) == 1
        assert block.extra_blocks[0].base_name == 'water'
        assert block.extra_blocks[0].properties['falling'].py_str == 'false'
        assert block.extra_blocks[0].properties['flowing'].py_str == 'false'
        assert block.extra_blocks[0].properties['level'].py_str == '0'
        assert bubble_code is None
        bubble_code = i

    print('Blocks in palette: ' + style([VIOLET], len(world.block_palette)))
    print('Bubble column block index: ' + style([VIOLET], bubble_code))
print()



if bubble_code is None:
    sys.exit('No bubble columns found, nothing to do')

print('Preparing bubble columns:')

with status('Searching for bubble column blocks'):
    for chunk, selection_box in chunk_boxes:
        for key in chunk.blocks.sections:
            section = chunk.blocks.get_section(key)
            
            assert len(section) == 16
            assert len(section[0]) == 16
            assert len(section[0][0]) == 16
            
            section_origin = Coordinate(16*chunk.cx, 16*key, 16*chunk.cz)
            
            export_area_localized = amulet.SelectionBox(
                (bound_1 - section_origin).as_tuple(),
                (bound_2 - section_origin).as_tuple(),
            )
            
            intersection = export_area_localized.intersection(box_of_16)
            
            if intersection.volume == 0: continue
            
            if intersection.volume < 4096:
                section = section[
                    intersection.min_x:intersection.max_x,
                    intersection.min_y:intersection.max_y,
                    intersection.min_z:intersection.max_z,
                ]
            
            intersection_offset = Coordinate(intersection.min_x, 
                intersection.min_y, intersection.min_z)
            
            bubble_search = numpy.where(section == bubble_code)
            
            for x, y, z in zip(*bubble_search, strict=True):
                bubble_blocks.append(section_origin + intersection_offset +
                    Coordinate(x, y, z))
    
    print(f'Found {style([BLUE], len(bubble_blocks))} bubble column blocks')

with status(f'Consolidating bubble column blocks'):
    bubble_blocks.sort(key=lambda b: (b.x, b.z, b.y))
    
    for block in bubble_blocks:
        if len(bubble_columns) == 0:
            bubble_columns.append(BubbleColumn(block))
            continue
        
        if bubble_columns[-1].position.x != block.x \
        or bubble_columns[-1].position.z != block.z \
        or bubble_columns[-1].position.y + bubble_columns[-1].height != block.y:
            bubble_columns.append(BubbleColumn(block))
        else:
            bubble_columns[-1].height += 1
    
    print(f'Consolidated into {style([BLUE], len(bubble_columns))} bubble '
        'columns')
print()



print('Generating .gltf:')

gltf = {
    'asset': {
        'generator': 'Port Lumen VRC Exporter',
        'minVersion': '2.0',
        'version': '2.0',
    },
    'scene': 0,
    'scenes': [{
        'name': world_path.name,
        'nodes': [],
    }],
    'nodes': [],
}

with status('Attaching bubble columns'):
    for column in bubble_columns:
        gltf['scenes'][0]['nodes'].append(len(gltf['nodes']))
        gltf['nodes'].append({
            'name': '_bubble_column',
            'translation': [
                column.position.x + 0.5,
                column.position.y + column.height/2,
                column.position.z + 0.5
            ],
            'scale': [1, column.height, 1],
        })

with status(f'Saving as {style([BOLD, ORANGE], world_path.name + '.gltf')}'):
    with open(world_path.name + '.gltf', 'w') as f:
        json.dump(gltf, f)
