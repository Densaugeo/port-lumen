# Must enable RCON support in server's server.properties file:
# enable-rcon=true
# rcon.port=25575
# rcon.password=yourpassword
# 
# For ServerMiner hosts, make sure the default scheduled task that runs save_all
# every 10 mins is disabled. The CEO replied to my support ticket (very
# helpfully responding to several questions) and told me the save_all task is
# mainly in case a mod breaks the usual automatic saving and isn't needed for
# up-to-date vanilla.
# 
# Requires a port-lumen.toml file from the following template:
# 
# [download]
# hostname = "your.minecraft.server"
# rcon_port = 25575
# rcon_pass = "password"
# ftp_port = 38680
# ftp_user = "username"
# ftp_pass = "password"
# ftp_path = "/path/to/world"
# 
# [export]
# dimension = "dimensions/minecraft/overworld"
# min = [-680, 39, 90]
# max = [-326, 319, 435]

import os, sys, shutil, pathlib, contextlib, tomllib, ftplib

import mcipc.rcon.je

# WTF Windows (needed for ANSI codes, for some reason)
os.system('')

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

##########
# Config #
##########

with open('port-lumen.toml', 'rb') as f:
    toml = tomllib.load(f)

HOSTNAME  = str(toml['download']['hostname' ])
RCON_PORT = int(toml['download']['rcon_port'])
RCON_PASS = str(toml['download']['rcon_pass'])
FTP_PORT  = int(toml['download']['ftp_port' ])
FTP_USER  = str(toml['download']['ftp_user' ])
FTP_PASS  = str(toml['download']['ftp_pass' ])
FTP_PATH = pathlib.Path(toml['download']['ftp_path'])
SAVE_PATH = pathlib.Path('downloads') / FTP_PATH.name
REGION_PATH = pathlib.Path(toml['export']['dimension']) / 'region'

X_MIN = int(toml['export']['min'][0])
X_MAX = int(toml['export']['max'][0])
Z_MIN = int(toml['export']['min'][2])
Z_MAX = int(toml['export']['max'][2])

########
# Code #
########

@contextlib.contextmanager
def pause_saving():
    print(f'{BOLD}{WHITE}Preparing Minecraft server for export:{RESET}{GRAY}')
    
    print(f'Connecting to {VIOLET}rcon://{HOSTNAME}:{RCON_PORT}{GRAY}...',
        end='')
    with mcipc.rcon.je.Client(HOSTNAME, RCON_PORT, passwd=RCON_PASS) as rcon:
        print(f'{GREEN}OK{GRAY}')
        
        # Disables automatic saving but NOT saving with /save_all or /stop
        print('Pausing automatic saving...', end='')
        rcon.save_off()
        print(f'{GREEN}OK{GRAY}')
        
        print('Flushing save queue...', end='')
        rcon.save_all()
        print(f'{GREEN}OK{GRAY}\n')
    
    yield
    
    print(f'{BOLD}{WHITE}Restoring Minecraft server operation:{RESET}{GRAY}')
    
    print(f'Connecting to {VIOLET}rcon://{HOSTNAME}:{RCON_PORT}{GRAY}...',
        end='')
    with mcipc.rcon.je.Client(HOSTNAME, RCON_PORT, passwd=RCON_PASS) as rcon:
        print(f'{GREEN}OK{GRAY}')
        
        print('Resuming automatic saving...', end='')
        rcon.save_on()
        print(f'{GREEN}OK{RESET}\n')

def download_with_progress(ftp: ftplib.FTP, src: pathlib.Path | str,
dest: pathlib.Path | str):
    try:
        size = ftp.size(str(src.as_posix()))
    except ftplib.error_perm as e:
        print(f'{BOLD}{RED}Error:{RESET} Cannot find file '
            f'{VIOLET}ftp://{ftp.host}:{ftp.port}{src.as_posix()}{RESET}')
        print(e)
        sys.exit(1)
    
    bytes_counts = [0, size]
    progress_template = f'\rDownloading {BOLD}{ORANGE}{src.name:<15}{RESET}' \
        f'{GRAY}' '{color}{0:>10,}' f'{GRAY} / ' '{color}{1:>10,}' f' B{GRAY}'
    
    with open(dest, 'wb') as f:
        def write_with_progress(buffer: bytes):
            bytes_counts[0] += len(buffer)
            print(progress_template.format(*bytes_counts, color=VIOLET), end='')
            f.write(buffer)
        
        ftp_server.retrbinary(f'RETR {src.as_posix()}', write_with_progress)
    
    print(progress_template.format(*bytes_counts, color=AQUA))

print()

with pause_saving():
    print(f'{BOLD}{WHITE}Downloading region data:{RESET}{GRAY}')
    
    print(f'Connecting to {VIOLET}ftp://{HOSTNAME}:{FTP_PORT}{GRAY}...', end='')
    ftp_server = ftplib.FTP()
    ftp_server.connect(HOSTNAME, FTP_PORT)
    ftp_server.login(FTP_USER, FTP_PASS)
    print(f'{GREEN}OK{GRAY}')
    
    print(f'Clearing {BOLD}{ORANGE}{SAVE_PATH}{RESET}{GRAY} folder...', end='')
    try:
        shutil.rmtree(SAVE_PATH)
    except FileNotFoundError:
        pass
    print(f'{GREEN}OK{GRAY}')
    
    (SAVE_PATH / REGION_PATH).mkdir(parents=True)
    download_with_progress(ftp_server, FTP_PATH / 'level.dat',
        SAVE_PATH / 'level.dat')
    for x in range(X_MIN//512, X_MAX//512 + 1):
        for z in range(Z_MIN//512, Z_MAX//512 + 1):
            filename = f'r.{x}.{z}.mca'
            download_with_progress(ftp_server, FTP_PATH / REGION_PATH /
                filename, SAVE_PATH / REGION_PATH / filename)
    print(RESET)
    
    # Be careful of timing! I don't want ServerMiner's scheduled save task
    # running during this
