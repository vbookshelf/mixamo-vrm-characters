"""
Mixamo FBX -> VRM converter for Blender.

Requires the "VRM Add-on for Blender" to be installed and enabled:
https://vrm-addon-for-blender.info/en-us/

Usage:
1. Edit FBX_PATH / VRM_PATH below if your files live somewhere else.
2. Open Blender > Scripting tab > paste this whole script > Run.
3. Check the System Console (Window > Toggle System Console) for any
   "WARNING - couldn't find these required bones" messages.
4. Before trusting the output, open the VRM tab > Humanoid panel and
   confirm nothing is shown in red.
"""

import re
from pathlib import Path

import bpy

# ------------------------------------------------------------------
# EDIT THESE TWO PATHS IF NEEDED
# ------------------------------------------------------------------
FBX_PATH = str(Path.home() / "Desktop" / "character.fbx")
VRM_PATH = str(Path.home() / "Desktop" / "character.vrm")
# ------------------------------------------------------------------

# 1. Make sure the VRM add-on is actually enabled
if not hasattr(bpy.ops.export_scene, "vrm"):
    raise RuntimeError(
        "The VRM add-on isn't enabled. Go to Edit > Preferences > Add-ons, "
        "search 'VRM', and enable it (download from "
        "https://vrm-addon-for-blender.info/en-us/ if you don't have it)."
    )

if not Path(FBX_PATH).exists():
    raise RuntimeError(f"FBX not found at {FBX_PATH} — edit FBX_PATH at the top of the script.")

# 2. Clear the default scene so we start clean
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.meshes) + list(bpy.data.armatures):
    if block.users == 0:
        bpy.data.batch_remove([block])

# 3. Import the Mixamo FBX
bpy.ops.import_scene.fbx(
    filepath=FBX_PATH,
    use_anim=False,  # we only need the mesh + skeleton, not the animation clip
    automatic_bone_orientation=False,
)

# 4. Find the imported armature
armature = next((o for o in bpy.context.selected_objects if o.type == "ARMATURE"), None)
if armature is None:
    raise RuntimeError("No armature found after import — check FBX_PATH points to a rigged Mixamo FBX.")

# 5. Apply rotation/scale so the VRM add-on doesn't choke on FBX import transforms
bpy.ops.object.select_all(action="DESELECT")
for obj in bpy.data.objects:
    if obj.type in {"ARMATURE", "MESH"}:
        obj.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# 6. Map Mixamo bone names -> VRM 1.0 humanoid bone attributes
MIXAMO_TO_VRM = {
    "Hips": "hips",
    "Spine": "spine",
    "Spine1": "chest",
    "Spine2": "upper_chest",
    "Neck": "neck",
    "Head": "head",

    "LeftShoulder": "left_shoulder",
    "LeftArm": "left_upper_arm",
    "LeftForeArm": "left_lower_arm",
    "LeftHand": "left_hand",
    "RightShoulder": "right_shoulder",
    "RightArm": "right_upper_arm",
    "RightForeArm": "right_lower_arm",
    "RightHand": "right_hand",

    "LeftUpLeg": "left_upper_leg",
    "LeftLeg": "left_lower_leg",
    "LeftFoot": "left_foot",
    "LeftToeBase": "left_toes",
    "RightUpLeg": "right_upper_leg",
    "RightLeg": "right_lower_leg",
    "RightFoot": "right_foot",
    "RightToeBase": "right_toes",

    "LeftHandThumb1": "left_thumb_metacarpal",
    "LeftHandThumb2": "left_thumb_proximal",
    "LeftHandThumb3": "left_thumb_distal",
    "LeftHandIndex1": "left_index_proximal",
    "LeftHandIndex2": "left_index_intermediate",
    "LeftHandIndex3": "left_index_distal",
    "LeftHandMiddle1": "left_middle_proximal",
    "LeftHandMiddle2": "left_middle_intermediate",
    "LeftHandMiddle3": "left_middle_distal",
    "LeftHandRing1": "left_ring_proximal",
    "LeftHandRing2": "left_ring_intermediate",
    "LeftHandRing3": "left_ring_distal",
    "LeftHandPinky1": "left_little_proximal",
    "LeftHandPinky2": "left_little_intermediate",
    "LeftHandPinky3": "left_little_distal",

    "RightHandThumb1": "right_thumb_metacarpal",
    "RightHandThumb2": "right_thumb_proximal",
    "RightHandThumb3": "right_thumb_distal",
    "RightHandIndex1": "right_index_proximal",
    "RightHandIndex2": "right_index_intermediate",
    "RightHandIndex3": "right_index_distal",
    "RightHandMiddle1": "right_middle_proximal",
    "RightHandMiddle2": "right_middle_intermediate",
    "RightHandMiddle3": "right_middle_distal",
    "RightHandRing1": "right_ring_proximal",
    "RightHandRing2": "right_ring_intermediate",
    "RightHandRing3": "right_ring_distal",
    "RightHandPinky1": "right_little_proximal",
    "RightHandPinky2": "right_little_intermediate",
    "RightHandPinky3": "right_little_distal",
}

# Bones VRM actually requires — everything else is nice-to-have
REQUIRED_VRM_BONES = {
    "hips", "spine", "head",
    "left_upper_leg", "left_lower_leg", "left_foot",
    "right_upper_leg", "right_lower_leg", "right_foot",
    "left_upper_arm", "left_lower_arm", "left_hand",
    "right_upper_arm", "right_lower_arm", "right_hand",
}


def strip_mixamo_prefix(name: str) -> str:
    # handles "mixamorig:Hips", "mixamorig1:Hips", "mixamorig_Hips", etc.
    return re.sub(r"^mixamorig\d*[:_]", "", name)


bone_lookup = {strip_mixamo_prefix(b.name): b.name for b in armature.data.bones}

armature.data.vrm_addon_extension.spec_version = "1.0"
human_bones = armature.data.vrm_addon_extension.vrm1.humanoid.human_bones

assigned, missing = [], []
for mixamo_name, vrm_attr in MIXAMO_TO_VRM.items():
    blender_bone_name = bone_lookup.get(mixamo_name)
    if blender_bone_name is None:
        if vrm_attr in REQUIRED_VRM_BONES:
            missing.append(mixamo_name)
        continue
    getattr(human_bones, vrm_attr).node.bone_name = blender_bone_name
    assigned.append(vrm_attr)

print(f"[mixamo_to_vrm] Assigned {len(assigned)} humanoid bones automatically.")
if missing:
    print(f"[mixamo_to_vrm] WARNING - couldn't find these required bones: {missing}")
    print("[mixamo_to_vrm] Open the VRM tab > Humanoid panel in the 3D viewport sidebar")
    print("[mixamo_to_vrm] and assign the missing ones by hand before exporting.")

# 7. Minimal meta info (edit these if you care about the values)
try:
    meta = armature.data.vrm_addon_extension.vrm1.meta
    meta.vrm_name = "character"
    meta.version = "1.0"
    if len(meta.authors) == 0:
        meta.authors.add().value = "Unknown"
except Exception as e:
    print(f"[mixamo_to_vrm] Could not set meta info automatically ({e}); set it in the VRM tab.")

# 8. Export
bpy.ops.export_scene.vrm(filepath=VRM_PATH)
print(f"[mixamo_to_vrm] Exported to {VRM_PATH}")
