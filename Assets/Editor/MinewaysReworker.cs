/* 
 * Command to run this script:

& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod MinewaysReworker.Run

 * Docs recommend adding -batchmode and -quit for full auto
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
    { "Bricks"                          , (true , false) },
    // Name                                coll   cut
    { "Bubble_Column"                   , (false, false) },
    { "Cactus"                          , (true , false) },
    { "Campfire"                        , (true , false) },
    { "Campfire__4"                     , (true , true ) },
    { "Carrot"                          , (false, true ) },
    { "Cauldron"                        , (true , false) },
    { "Cauldron__4"                     , (true , false) },
    { "Cave_Vines"                      , (false, true ) },
    { "Cave_Vines_lit"                  , (false, true ) },
    { "Cave_Vines_Plant"                , (false, true ) },
    { "Chain"                           , (true , true ) },
    { "Cherry_Leaves"                   , (true , true ) },
    { "Cherry_Log"                      , (true , false) },
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
    { "Dandelion"                       , (false, true ) },
    { "Dark_Oak_Door"                   , (false, false) }, // Add collider after I have a way to open
    { "Dark_Oak_Fence"                  , (true , false) },
    { "Dark_Oak_Fence_Gate"             , (true , false) },
    // Name                                coll   cut
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
    { "Double_Spruce_Slab"              , (true , false) },
    { "Double_Stone_Brick_Slab"         , (true , false) },
    { "Dripstone_Block"                 , (true , false) },
    { "Emerald_Ore"                     , (true , false) },
    { "Enchanting_Table"                , (true , false) },
    { "Ender_Chest"                     , (true , false) },
    { "Farmland"                        , (true , false) },
    { "Fence"                           , (true , false) },
    { "Fletching_Table"                 , (true , false) },
    { "Flowering_Azalea"                , (true , true ) },
    // Name                                coll   cut
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
    { "Green_Stained_Glass_Pane"        , (true , false) },
    { "Grindstone"                      , (true , false) },
    { "Hopper"                          , (true , false) },
    { "Iron_Bars"                       , (true , true ) },
    { "Iron_Ore"                        , (true , false) },
    { "Ladder"                          , (true , true ) },
    { "Lantern"                         , (true , false) },
    { "Lapis_Lazuli_Ore"                , (true , false) },
    { "Lectern"                         , (true , false) },
    { "Lever"                           , (false, false) },
    { "Light_Blue_Glazed_Terracotta"    , (true , false) },
    { "Light_Carpet"                    , (true , false) },
    { "Light_Stained_Glass"             , (true , false) },
    { "Lightning_Rod"                   , (true , false) },
    { "Lilac"                           , (false, true ) },
    { "Lily_of_the_Valley"              , (false, true ) },
    { "Lily_Pad"                        , (true , true ) },
    { "Magma_Block"                     , (true , false) },
    { "Moss_Block"                      , (true , false) },
    { "Moss_Carpet"                     , (true , false) },
    { "Mossy_Cobblestone"               , (true , false) },
    // Name                                coll   cut
    { "Mossy_Cobblestone_Wall"          , (true , false) },
    { "Mossy_Stone_Bricks"              , (true , false) },
    { "Mud"                             , (true , false) },
    { "Nether_Portal"                   , (false, false) },
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
    { "Orange_Tulip"                    , (false, true) },
    { "Oxeye_Daisy"                     , (false, true) },
    { "Oxidized_Copper_Bulb"            , (true , false) },
    { "Oxidized_Copper_Door"            , (false, true ) }, // Add collider after I have a way to open
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
    { "Potted_Flowering_Azalea"         , (true , false) },
    { "Potted_Orange_Tulip"             , (true , false) },
    // Name                                coll   cut
    { "Potted_Poppy"                    , (true , false) },
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
    { "Soul_Lantern"                    , (true , false) },
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
    { "Sunflower"                       , (false, true) },
    // Name                                coll   cut
    { "Tall_Grass"                      , (false, true ) },
    { "Tall_Seagrass"                   , (false, true ) },
    { "Target"                          , (true , false) },
    { "Torch"                           , (false, true ) },
    { "Vines"                           , (false, true) },
    { "Waxed_Copper_Trapdoor"           , (true , true ) },
    { "Weathered_Copper_Bulb"           , (true , false) },
    { "Weathered_Copper_Grate"          , (true , true ) },
    { "Wheat"                           , (false, true ) },
    { "White_Stained_Glass"             , (true , false) },
    { "White_Tulip"                     , (false, true ) },
  };
}

public class MinewaysReworker : MonoBehaviour {
  public static void Run() {
    bool success;
    string path_stem = "Assets/Den's Stuff/Mineways Export/port-lumen";
    
    System.IO.File.Delete(path_stem + ".prefab");
    System.IO.File.Delete(path_stem + ".prefab.meta");
    
    var obj = AssetDatabase.LoadAssetAtPath<GameObject>(path_stem + ".obj");
    var instance = (GameObject) PrefabUtility.InstantiatePrefab(obj);
    PrefabUtility.SaveAsPrefabAsset(instance, path_stem + ".prefab",
      out success);
    // Regular destroy can't be called in edit mode
    GameObject.DestroyImmediate(instance);
    System.Diagnostics.Trace.Assert(success);
    
    var prefab = PrefabUtility.LoadPrefabContents(path_stem + ".prefab");
    for(int i = 0; i < prefab.transform.childCount; ++i) {
      var child = prefab.transform.GetChild(i).gameObject;
      
      try {
        var info = Globals.block_types[child.name];
        
        if(info.collider) {
          child.AddComponent<MeshCollider>();
        }
      } catch(KeyNotFoundException) {
        Debug.LogWarning("Unrecognized block type `" + child.name +
          "`. Please add it to Globals.block_types");
      }
    }
    PrefabUtility.SaveAsPrefabAsset(prefab, path_stem + ".prefab", out success);
    PrefabUtility.UnloadPrefabContents(prefab);
    System.Diagnostics.Trace.Assert(success);
    
    AssetDatabase.Refresh();
  }
}
