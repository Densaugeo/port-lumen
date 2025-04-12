/* 
 * Command to run this script:

& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod MinewaysReworker.Run

 * Docs recommend adding -batchmode and -quit for full auto. 
 * 
 * Note that it can take 30+ minutes on first run. You can follow progress by
 * watching materials created in
 * `Assets/Den's Stuff/Mineways Export/Extracted Materials` and .meta files
 * modified in `Assets/Den's Stuff/Mineways Export/tex`.
 */

using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public static class Globals {
  public static Dictionary<string, (bool collider, bool cutout)> block_types = 
  new Dictionary<string, (bool, bool)> {
    // Name                                coll   cut
    { "Acacia_Fence"                    , (true , false) },
    { "Acacia_Fence_Gate"               , (true , false) },
    { "Acacia_Leaves"                   , (true , true ) },
    { "Acacia_Log"                      , (true , false) },
    { "Acacia_Sapling"                  , (false, true ) },
    { "Acacia_Trapdoor"                 , (true , true ) },
    { "Allium"                          , (false, true ) },
    { "Andesite"                        , (true , false) },
    { "Anvil"                           , (true , false) },
    { "Azalea"                          , (true , true ) },
    { "Azalea_Leaves"                   , (true , true ) },
    { "Azure_Bluet"                     , (false, true ) },
    { "Bamboo"                          , (true , true ) },
    { "Barrel"                          , (true , false) },
    { "Bed"                             , (true , false) },
    // Name                                coll   cut
    { "Bee_Nest"                        , (true , false) },
    { "Beehive"                         , (true , false) },
    { "Beetroot_Seeds"                  , (false, true ) },
    { "Bell"                            , (true , false) },
    { "Birch_Leaves"                    , (true , true ) },
    { "Birch_Log"                       , (true , false) },
    { "Black_Stained_Glass"             , (true , false) },
    { "Blast_Furnace"                   , (true , false) },
    { "Block_of_Iron"                   , (true , false) },
    { "Block_of_Raw_Copper"             , (true , false) },
    { "Blue_Orchid"                     , (false, true ) },
    { "Blue_Stained_Glass"              , (true , false) },
    { "Blue_Stained_Glass_Pane"         , (true , false) },
    { "Bookshelf"                       , (true , false) },
    { "Brewing_Stand"                   , (true , false) },
    // Name                                coll   cut
    { "Bricks"                          , (true , false) },
    { "Bubble_Column"                   , (false, false) },
    { "Cactus"                          , (true , false) },
    { "Campfire"                        , (true , false) },
    { "Campfire__4"                     , (true , true ) },
    { "Carrot"                          , (false, true ) },
    { "Cartography_Table"               , (true , false) },
    { "Cauldron"                        , (true , false) },
    { "Cauldron__4"                     , (true , false) },
    { "Cave_Vines"                      , (false, true ) },
    { "Cave_Vines_lit"                  , (false, true ) },
    { "Cave_Vines_Plant"                , (false, true ) },
    { "Chain"                           , (true , true ) },
    { "Cherry_Leaves"                   , (true , true ) },
    { "Cherry_Log"                      , (true , false) },
    // Name                                coll   cut
    { "Chest"                           , (true , false) },
    { "Chiseled_Stone_Bricks"           , (true , false) },
    { "Clay"                            , (true , false) },
    { "Coal_Ore"                        , (true , false) },
    { "Cobbled_Deepslate"               , (true , false) },
    { "Cobblestone"                     , (true , false) },
    { "Cobblestone_Slab"                , (true , false) },
    { "Cobblestone_Stairs"              , (true , false) },
    { "Cobblestone_Wall"                , (true , false) },
    { "Composter"                       , (true , false) },
    { "Conduit"                         , (true , false) },
    { "Copper_Ore"                      , (true , false) },
    { "Cornflower"                      , (false, true ) },
    { "Crafting_Table"                  , (true , false) },
    { "Damaged_Anvil"                   , (true , false) },
    // Name                                coll   cut
    { "Dandelion"                       , (false, true ) },
    { "Dark_Oak_Door"                   , (false, false) }, // Add collider after I have a way to open
    { "Dark_Oak_Fence"                  , (true , false) },
    { "Dark_Oak_Fence_Gate"             , (true , false) },
    { "Dark_Oak_Leaves"                 , (true , true ) },
    { "Dark_Oak_Log"                    , (true , false) },
    { "Dark_Oak_Pressure_Plate"         , (false, false) },
    { "Dark_Oak_Sign"                   , (false, false) },
    { "Dark_Oak_Slab"                   , (true , false) },
    { "Dark_Oak_Stairs"                 , (true , false) },
    { "Dark_Oak_Trapdoor"               , (true , false) },
    { "Dark_Oak_Wall_Sign"              , (false, false) },
    { "Dark_Oak_Wood_Planks"            , (true , false) },
    { "Dead_Bush"                       , (false, true ) },
    { "Deepslate_Tiles"                 , (true , false) },
    // Name                                coll   cut
    { "Deepslate_Tile_Slab"             , (true , false) },
    { "Deepslate_Tile_Stairs"           , (true , false) },
    { "Diorite"                         , (true , false) },
    { "Diorite_Slab"                    , (true , false) },
    { "Diorite_Wall"                    , (true , false) },
    { "Dirt"                            , (true , false) },
    { "Dirt_Path"                       , (true , false) },
    { "Dispenser"                       , (true , false) },
    { "Double_Cobblestone_Slab"         , (true , false) },
    { "Double_Dark_Oak_Slab"            , (true , false) },
    { "Double_Oak_Slab"                 , (true , false) },
    { "Double_Spruce_Slab"              , (true , false) },
    { "Double_Stone_Brick_Slab"         , (true , false) },
    { "Dripstone_Block"                 , (true , false) },
    { "Emerald_Ore"                     , (true , false) },
    { "Enchanting_Table"                , (true , false) },
    // Name                                coll   cut
    { "Ender_Chest"                     , (true , false) },
    { "Farmland"                        , (true , false) },
    { "Fence"                           , (true , false) },
    { "Fletching_Table"                 , (true , false) },
    { "Flowering_Azalea"                , (true , true ) },
    { "Flowering_Azalea_Leaves"         , (true , true ) },
    { "Furnace"                         , (true , false) },
    { "Glass"                           , (true , true ) },
    { "Glass_Pane"                      , (true , true ) },
    { "Glow_Lichen"                     , (false, true ) },
    { "Glowstone"                       , (true , false) },
    { "Granite"                         , (true , false) },
    { "Grass_Block"                     , (true , false) },
    { "Gravel"                          , (true , false) },
    { "Gray_Carpet"                     , (true , false) },
    { "Gray_Wool"                       , (true , false) },
    // Name                                coll   cut
    { "Green_Stained_Glass_Pane"        , (true , false) },
    { "Grindstone"                      , (true , false) },
    { "Hopper"                          , (true , false) },
    { "Iron_Bars"                       , (true , true ) },
    { "Iron_Ore"                        , (true , false) },
    { "Ladder"                          , (true , true ) },
    { "Lantern"                         , (true , true ) },
    { "Lapis_Lazuli_Ore"                , (true , false) },
    { "Lectern"                         , (true , false) },
    { "Lever"                           , (false, false) },
    { "Light_Blue_Glazed_Terracotta"    , (true , false) },
    { "Light_Carpet"                    , (true , false) },
    { "Light_Stained_Glass"             , (true , false) },
    { "Lightning_Rod"                   , (true , false) },
    { "Lilac"                           , (false, true ) },
    // Name                                coll   cut
    { "Lily_of_the_Valley"              , (false, true ) },
    { "Lily_Pad"                        , (true , true ) },
    { "Lit_Candle"                      , (true , true ) },
    { "Lit_Candle__32"                  , (true , true ) },
    { "Lit_Candle__48"                  , (true , true ) },
    { "Magma_Block"                     , (true , false) },
    { "Melon"                           , (true , false) },
    { "Melon_Stem_age_7"                , (false, true ) },
    { "Moss_Block"                      , (true , false) },
    { "Moss_Carpet"                     , (true , false) },
    { "Mossy_Cobblestone"               , (true , false) },
    { "Mossy_Cobblestone_Wall"          , (true , false) },
    { "Mossy_Stone_Bricks"              , (true , false) },
    { "Mud"                             , (true , false) },
    { "Nether_Portal"                   , (false, false) },
    // Name                                coll   cut
    { "Note_Block"                      , (true , false) },
    { "Oak_Door"                        , (false, true ) }, // Add collider after I have a way to open
    { "Oak_Leaves"                      , (true , true ) },
    { "Oak_Log"                         , (true , false) },
    { "Oak_Planks"                      , (true , false) },
    { "Oak_Slab"                        , (true , false) },
    { "Oak_Stairs"                      , (true , false) },
    { "Oak_Trapdoor"                    , (true , true ) },
    { "Oak_Wall_Sign"                   , (false, false) },
    { "Observer"                        , (true , false) },
    { "Obsidian"                        , (true , false) },
    { "Orange_Tulip"                    , (false, true ) },
    { "Oxeye_Daisy"                     , (false, true ) },
    { "Oxidized_Copper_Bulb"            , (true , false) },
    { "Oxidized_Copper_Door"            , (false, true ) }, // Add collider after I have a way to open
    // Name                                coll   cut
    { "Oxidized_Copper_Grate"           , (true , true ) },
    { "Peony"                           , (false, true ) },
    { "Pink_Petals"                     , (false, true ) },
    { "Pink_Tulip"                      , (false, true ) },
    { "Piston"                          , (true , false) },
    { "Piston_Head"                     , (true , false) },
    { "Podzol"                          , (true , false) },
    { "Pointed_Dripstone"               , (true , true ) },
    { "Polished_Diorite"                , (true , false) },
    { "Poppy"                           , (false, true ) },
    { "Potted_Allium"                   , (true , false) },
    { "Potted_Azure_Bluet"              , (true , false) },
    { "Potted_Flowering_Azalea"         , (true , false) },
    { "Potted_Lily_of_the_Valley"       , (true , false) },
    { "Potted_Orange_Tulip"             , (true , false) },
    { "Potted_Oxeye_Daisy"              , (true , false) },
    { "Potted_Poppy"                    , (true , false) },
    { "Potted_Red_Tulip"                , (true , false) },
    { "Potted_White_Tulip"              , (true , false) },
    // Name                                coll   cut
    { "Powered_Rail"                    , (true , true ) },
    { "Prismarine"                      , (true , false) },
    { "Pumpkin"                         , (true , false) },
    { "Purple_Stained_Glass"            , (true , false) },
    { "Purple_Stained_Glass_Pane"       , (true , false) },
    { "Rail"                            , (true , true ) },
    { "Red_Carpet"                      , (true , false) },
    { "Red_Tulip"                       , (false, true ) },
    { "Redstone_Comparator"             , (true , false) },
    { "Redstone_Lamp_(active)"          , (true , false) },
    { "Redstone_Repeater_(inactive)"    , (true , false) },
    { "Redstone_Torch_(active)"         , (false, true ) },
    { "Redstone_Torch_(inactive)"       , (false, true ) },
    { "Redstone_Wire_power_0"           , (false, true ) },
    { "Redstone_Wire_power_13"          , (false, true ) },
    // Name                                coll   cut
    { "Redstone_Wire_power_14"          , (false, true ) },
    { "Redstone_Wire_power_15"          , (false, true ) },
    { "Rooted_Dirt"                     , (true , false) },
    { "Rose_Bush"                       , (false, true ) },
    { "Sand"                            , (true , false) },
    { "Sandstone"                       , (true , false) },
    { "Seagrass"                        , (false, true ) },
    { "Short_Grass"                     , (false, true ) },
    { "Smithing_Table"                  , (true , false) },
    { "Smooth_Basalt"                   , (true , false) },
    { "Smooth_Stone"                    , (true , false) },
    { "Soul_Fire"                       , (false, true ) },
    { "Soul_Lantern"                    , (true , true ) },
    { "Soul_Sand"                       , (true , false) },
    { "Soul_Soil"                       , (true , false) },
    // Name                                coll   cut
    { "Spawner"                         , (true , true ) },
    { "Spruce_Button"                   , (false, false) },
    { "Spruce_Door"                     , (false, false) }, // Add collider after I have a way to open
    { "Spruce_Fence"                    , (true , false) },
    { "Spruce_Fence_Gate"               , (true , false) },
    { "Spruce_Leaves"                   , (true , true ) },
    { "Spruce_Log"                      , (true , false) },
    { "Spruce_Pressure_Plate"           , (false, false) },
    { "Spruce_Slab"                     , (true , false) },
    { "Spruce_Stairs"                   , (true , false) },
    { "Spruce_Trapdoor"                 , (true , false) },
    { "Spruce_Wall_Sign"                , (false, false) },
    { "Spruce_Wood_Planks"              , (true , false) },
    { "Stationary_Lava"                 , (false, false) },
    { "Stationary_Water"                , (false, false) },
    // Name                                coll   cut
    { "Sticky_Piston"                   , (true , false) },
    { "Stone"                           , (true , false) },
    { "Stone_Brick_Slab"                , (true , false) },
    { "Stone_Brick_Stairs"              , (true , false) },
    { "Stone_Brick_Wall"                , (true , false) },
    { "Stone_Bricks"                    , (true , false) },
    { "Stone_Button"                    , (false, false) },
    { "Stone_Cutter"                    , (true , false) },
    { "Stone_Pressure_Plate"            , (false, false) },
    { "Stone_Slab"                      , (true , false) },
    { "Stone_Stairs"                    , (true , false) },
    { "Stripped_Dark_Oak_Log"           , (true , false) },
    { "Stripped_Oak_Log"                , (true , false) },
    { "Stripped_Spruce_Log"             , (true , false) },
    { "Sugar_Cane"                      , (false, true) },
    // Name                                coll   cut
    { "Sunflower"                       , (false, true) },
    { "Tall_Grass"                      , (false, true ) },
    { "Tall_Seagrass"                   , (false, true ) },
    { "Target"                          , (true , false) },
    { "Torch"                           , (false, true ) },
    { "Vines"                           , (false, true ) },
    { "Wall_Banner"                     , (false, false) },
    { "Waxed_Copper_Trapdoor"           , (true , true ) },
    { "Weathered_Copper_Bulb"           , (true , false) },
    { "Weathered_Copper_Grate"          , (true , true ) },
    { "Wheat"                           , (false, true ) },
    { "White_Stained_Glass"             , (true , false) },
    { "White_Carpet"                    , (true , false) },
    { "White_Tulip"                     , (false, true ) },
    { "White_Wool"                      , (true , false) },
  };
}

public class MinewaysReworker : MonoBehaviour {
  public static void Run() {
    bool success;
    
    string work_dir    = "Assets/Minecraft Import";
    string path_obj    = work_dir + "/port-lumen.obj";
    string path_prefab = work_dir + "/port-lumen.prefab";
    string path_tex    = work_dir + "/tex";
    string path_mats   = work_dir + "/Extracted Materials";
    
    System.IO.File.Delete(path_prefab);
    System.IO.File.Delete(path_prefab + ".meta");
    System.IO.Directory.CreateDirectory(work_dir + "/Extracted Materials");
    
    var obj = AssetDatabase.LoadAssetAtPath<GameObject>(path_obj);
    var instance = (GameObject) PrefabUtility.InstantiatePrefab(obj);
    PrefabUtility.SaveAsPrefabAsset(instance, path_prefab, out success);
    // Regular destroy can't be called in edit mode
    GameObject.DestroyImmediate(instance);
    System.Diagnostics.Trace.Assert(success);
    
    var prefab = PrefabUtility.LoadPrefabContents(path_prefab);
    for(int i = 0; i < prefab.transform.childCount; ++i) {
      var child = prefab.transform.GetChild(i).gameObject;
      
      if(!Globals.block_types.ContainsKey(child.name)) {
        Debug.LogWarning("Unrecognized block type `" + child.name +
          "`. Please add it to Globals.block_types");
        continue;
      }
      var info = Globals.block_types[child.name];
      
      if(info.collider) {
        child.AddComponent<MeshCollider>();
      }
      
      foreach(var mat in child.GetComponent<Renderer>().sharedMaterials) {
        string path_mat = path_mats + "/" + mat.name + ".mat";
        
        // This takes a long time to run, so check if it's really needed first
        if(!System.IO.File.Exists(path_mat)) {
          string result = AssetDatabase.ExtractAsset(mat, path_mat);
          System.Diagnostics.Trace.Assert(string.IsNullOrEmpty(result));
          
          // This causes existing materials to be replaced with the new ones. I
          // don't know why
          string path_other = AssetDatabase.GetAssetPath(mat);
          AssetDatabase.WriteImportSettingsIfDirty(path_other);
          AssetDatabase.ImportAsset(path_other, ImportAssetOptions.ForceUpdate);
        }
        
        var new_mat = AssetDatabase.LoadAssetAtPath<Material>(path_mat);
        
        if(info.cutout) {
          new_mat.shader = Shader.Find("Particles/Standard Surface");
          new_mat.SetFloat("_Cull", (float) UnityEngine.Rendering.CullMode.Off);
          
          // Equivalent to setting render mode to cutout. Based on instructions
          // at https://docs.unity3d.com/Manual/StandardShaderMaterialParameterRenderingMode.html
          // Note that I used StandardShaderGUI.cs (not
          // StandardParticlesShaderGUI.cs, as you might expect when using
          // the particle shader - I tried that one but it didn't work).
          // The renderQueue setting in StandardShaderGUI.cs is more
          // complex, but I borrowed 3000 from a random forum post and it
          // worked.
          new_mat.SetFloat("_Mode", 1);
          new_mat.SetOverrideTag("RenderType", "TransparentCutout");
          new_mat.SetFloat("_SrcBlend",
            (float) UnityEngine.Rendering.BlendMode.One);
          new_mat.SetFloat("_DstBlend",
            (float) UnityEngine.Rendering.BlendMode.Zero);
          new_mat.SetFloat("_ZWrite", 1.0f);
          new_mat.EnableKeyword("_ALPHATEST_ON");
          new_mat.DisableKeyword("_ALPHABLEND_ON");
          new_mat.DisableKeyword("_ALPHAPREMULTIPLY_ON");
          new_mat.renderQueue = 3000;
        } else {
          new_mat.SetFloat("_SpecularHighlights", 0.0f);
        }
      }
    }
    PrefabUtility.SaveAsPrefabAsset(prefab, path_prefab, out success);
    PrefabUtility.UnloadPrefabContents(prefab);
    System.Diagnostics.Trace.Assert(success);
    
    foreach(var file in new System.IO.DirectoryInfo(path_tex).GetFiles("*.png")
    ) {
      var png = AssetImporter.GetAtPath(path_tex + "/" + file.Name)
        as TextureImporter;
      
      // This takes a long time to run, so check if it's really needed first
      if(png.textureCompression != TextureImporterCompression.Uncompressed
      || png.filterMode != FilterMode.Point) {
        png.textureCompression = TextureImporterCompression.Uncompressed;
        png.filterMode = FilterMode.Point;
        png.SaveAndReimport();
      }
    }
    
    AssetDatabase.Refresh();
  }
}
