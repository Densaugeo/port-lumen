# Port Lumen

VRChat upload of a Minecraft port city

## Mineways Export

Download (in WSL):
```bash
cd ???
???
```

Settings to import model from Mineways:
- File > Open World > Find Your World... > `C:\Users\Den Antares\Downloads\serverminer-download\port-lumen.den-antares.com33580\port-lumen\level.dat`
- File > Export for Rendering (Ctrl+R)
- `Assets/Minecraft Import/port-lumen.obj`
- Depth = 39
- Height = max (319)
- X = -680..-326
- Z = 90..435
- Uncheck "Center model around the origin"
- Ok

## Import

First time:
- Place .obj, .mtl, and `tex` folder in `Assets/Minecraft Import`
- Lanuch Unity with the following command:
```
& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod MinewaysReworker.Run

# Docs recommend adding -batchmode and -quit for full auto (to be investigated
# later)
```

Note that it can take 30+ minutes on first run. You can follow progress by watching materials created in `Assets/Den's Stuff/Mineways Export/Extracted Materials` and .meta files modified in `Assets/Den's Stuff/Mineways Export/tex`.

Updates:
- Replace .obj and .mtl files in `Assets/Minecraft Import`
  * Do not delete associated .meta files. If you do, you will have to delete `Extracted Materials` and wait for the script to repopulate it
  * Deleting .prefab and .prefab.meta is not required, the script will do that itself
  * This can be done by manually placing the exported files, or by directly exporting to this location
- Copy the `tex` folder into `Assets/Minecraft Import` and skip existing files (this is to add any new textures)
- Launch Unity using same command as for first time import

Reworker script performs the following fixes:
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
