# Fedora:
# python3.13 -m pip install mcipc==2.4.2
# sudo dnf install wget1
# 
# Ubuntu:
# python3.13 -m pip install mcipc==2.4.2 --break-system-packages
# sudo ln -s /usr/bin/wget /usr/bin/wget1
# 
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
# Must create a serverminer-download.toml file from the following template:
# hostname = "your.minecraft.server"
# rcon_port = 25575
# rcon_pass = "password"
# ftp_port = 38680
# ftp_user = "username"
# ftp_pass = "password"
# world_path = "/path/to/world"
# save_path = "mc-download"

import shutil, pathlib, contextlib, tomllib, subprocess
import mcipc.rcon.je

with open('serverminer-download.toml', 'rb') as f:
    toml = tomllib.load(f)

HOSTNAME = str(toml['hostname'])
RCON_PORT = int(toml['rcon_port'])
RCON_PASS = str(toml['rcon_pass'])
FTP_PORT = int(toml['ftp_port'])
FTP_USER = str(toml['ftp_user'])
FTP_PASS = str(toml['ftp_pass'])
WORLD_PATH = pathlib.Path(toml['world_path'])
SAVE_PATH = pathlib.Path(toml['save_path'])

@contextlib.contextmanager
def pause_saving():
    print(f'Connecting to rcon://{HOSTNAME}:{RCON_PORT}...', end='')
    with mcipc.rcon.je.Client(HOSTNAME, RCON_PORT, passwd=RCON_PASS) as rcon:
        print('OK')
        
        # Disables automatic saving but NOT saving with /save_all or /stop
        print('\tPausing automatic saving...', end='')
        rcon.save_off()
        print('OK')
        
        # Flushes save cue
        print('\tFlushing save queue...', end='')
        rcon.save_all()
        print('OK\n')
    
    yield
    
    print(f'Connecting to rcon://{HOSTNAME}:{RCON_PORT}...', end='')
    with mcipc.rcon.je.Client(HOSTNAME, RCON_PORT, passwd=RCON_PASS) as rcon:
        print('OK')
        
        print('\tResuming automatic saving...', end='')
        rcon.save_on()
        print('OK\n')

with pause_saving():
    print(f'Clearing `{SAVE_PATH}` folder...', end='')
    try:
        shutil.rmtree(SAVE_PATH)
    except FileNotFoundError:
        pass
    print('OK\n')
    
    print(f'Downloading world at {WORLD_PATH} to `{SAVE_PATH}`...')
    wget_result = subprocess.run([
        'wget1', '-m', f'ftp://{HOSTNAME}:{FTP_PORT}{WORLD_PATH}',
        '--ftp-user', FTP_USER, '--ftp-pass', FTP_PASS,
        '--no-verbose', '--directory-prefix', SAVE_PATH,
    ], check=True)
    print('Download complete\n')
    
    # Be careful of timing! I don't want ServerMiner's scheduled save task
    # running during this

print(f'World downloaded to `{SAVE_PATH}/{HOSTNAME}:{FTP_PORT}{WORLD_PATH}`')
