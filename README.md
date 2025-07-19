# Port Lumen

VRChat upload of a Minecraft port city

## Mineways Export

Download (in WSL):
```bash
cd VRChatProjects/port-lumen

# Note: Config file `serverminer-download.toml` must be prepared according to
# instructions in serverminer-download.py
python3 serverminer-download.py
python3 vrc-exporter.py
```

Export model from Mineways using these settings:
- File > Open World > Find Your World... > `C:\Users\Den Antares\Downloads\serverminer-download\port-lumen.den-antares.com:33580\port-lumen\level.dat`
- File > Export for Rendering (Ctrl+R)
- `Assets/Minecraft Import/port-lumen.obj`
- Depth = 39
- Height = max (319)
- X = -680..-326
- Z = 90..435
- Uncheck "Center model around the origin"
- Ok

## Import

Launch Unity with the following command:

```powershell
& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod MinewaysReworker.Run

# Docs recommend adding -batchmode and -quit for full auto (to be investigated
# later)
```

Note that it can take 30+ minutes on first run. You can follow progress by watching materials created in `Assets/Den's Stuff/Mineways Export/Extracted Materials` and .meta files modified in `Assets/Den's Stuff/Mineways Export/tex`.

Close Unity and relaunch with the following command:

```powershell
& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod GLTFImport.Run
```

Notes regarding updates:
- The Mineways config above replaces the .obj and .mtl files in `Assets/Minecraft Import`
- Do not delete associated .meta files. If you do, you will have to delete `Extracted Materials` and wait for the script to repopulate it

Reworker script performs the following fixes:
- Deletes and replaces the .prefab and .prefab.meta from the Mineways export
- Fixes texture blur by changing these settings on every imported texture image:
  * Filter mode = Point (no filter)
  * Compression = None
- Extracts all materials to `Extracted Materials` folder next to imported file
- Updates all sprite-like materials to:
  * Use shader `Particles/Standard Surface`
  * Disable backface culling
  * Cutout rendering mode
- Updates all non-sprite-like materials to:
  * Remove specular highlights
- Updates all emissive materials to:
  * Enable emission (no lighting yet)
  * Use correspond emissive texture from `tex-emissive`
- Attaches mesh colliders to all meshes that need them

VRC Import script does the following:
- Deletes and replaces the .prefab and .prefab.meta from the .gltf export
- Places bubble column elevators as specified in the .gltf export
