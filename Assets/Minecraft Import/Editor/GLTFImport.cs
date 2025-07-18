/* 
 * Command to run this script:

& "C:\Program Files\Unity\Hub\Editor\2022.3.22f1\Editor\Unity.exe" `
-projectPath "C:\Users\Den Antares\AppData\Local\VRChatCreatorCompanion\VRChatProjects\port-lumen" `
-executeMethod GLTFImport.Run

 * This script spams a lot of "ArgumentNullException: Value cannot be null" in
 * Unity. I don't know why, but it seems to work anyway.
 */
using System.Collections.Generic;
using UdonSharp;
using UnityEditor;
using UnityEngine;
using VRC;

public class GLTFImport : MonoBehaviour {
  public static void Run() {
    bool success;
    
    string work_dir           = "Assets/Minecraft Import";
    string path_obj           = work_dir + "/port-lumen.gltf";
    string path_prefab        = work_dir + "/port-lumen-gltf.prefab";
    string path_bubble_column = work_dir +
      "/static-prefabs/Bubble Column.prefab";
    
    System.IO.File.Delete(path_prefab);
    System.IO.File.Delete(path_prefab + ".meta");
    
    var obj = AssetDatabase.LoadAssetAtPath<GameObject>(path_obj);
    var instance = (GameObject) PrefabUtility.InstantiatePrefab(obj);
    Debug.Log(instance);
    PrefabUtility.SaveAsPrefabAsset(instance, path_prefab, out success);
    // Regular destroy can't be called in edit mode
    GameObject.DestroyImmediate(instance);
    System.Diagnostics.Trace.Assert(success);
    
    var prefab = PrefabUtility.LoadPrefabContents(path_prefab);
    var prefab_bubble_column = PrefabUtility.LoadPrefabContents(
      path_bubble_column);
    
    for(int i = 0; i < prefab.transform.childCount; ++i) {
      var child = prefab.transform.GetChild(i).gameObject;

      if(child.name.StartsWith("bubble-column-")) {
        Instantiate(prefab_bubble_column, child.transform);
      }
    }
    
    PrefabUtility.SaveAsPrefabAsset(prefab, path_prefab, out success);
    PrefabUtility.UnloadPrefabContents(prefab);
    System.Diagnostics.Trace.Assert(success);
  }
}
