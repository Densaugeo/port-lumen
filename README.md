# Port Lumen

VRChat upload of a Minecraft port city

## Key Locations

`Assets/Den's Stuff/Mineways Export`
- Is what the name suggests.

`Assets/Den's Stuff/Extracted Materials`
- Mineways export materials must be "extracted" before editing them. I think this is because extracting creates a separate copy from the original.

`Assets/Editor/MinewaysReworker.cs`
- Can be run with Unity startup to fix Mineways export issues.

## Mineways Export

Settings to import model from Mineways
- File > Open World > Den + Zy
- File > Export for Rendering (Ctrl+R)
- `Assets/Den's Stuff/Mineways Export/port-lumen.obj`
- Depth = 39
- Height = max (319)
- X = -680..-326
- Z = 133..405
- Select "Export all textures to three large, mosaic images"
- Uncheck "Center model around the origin"
- Ok

Texture blur can be fixed by changing these settings on every import texture image:
- Filter mode = Point (no filter)
- Compression = None

Getting grass/plants to appear correctly requires these steps:
- Select .fbx import > materials tab > extract materials
- Edit material/shader rendering mode = cutout
- Haven't figured out how to make double-sided
- .obj file can be replaced and material changes will be preserved
  * Not sure what happens if the new .obj file adds new materials

Adding colliders was surprisingly easy
- Add a MeshCollider component. That's it. Convex colliders are optional
- Colliders are lost when .obj file is replaced
- Now handled by MinewaysReworker
