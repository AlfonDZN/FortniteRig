import bpy

from bpy.utils import register_class, unregister_class

from . panel import Rig_PT_Panel, Rig_PT_Subpanel_finish, MySettings
from . advancedFortniteRig import rig
from . widgets.widgets import useWidgets
from . armRig import advancedArmRig
from . legRig import advancedLegRig
from . addFeetBones import addFeetBones
from . finishFeetRig import finishFeetRig
from . eyeRig import eyeRig
from . fingerRig import advancedFingerRig

bl_info = {
    "name" : "Fortnite Rig",
    "author" : "Alfon",
    "description" : "",
    "blender" : (3, 2, 2),
    "version" : (1, 2, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Rig"
}

classes = (Rig_PT_Panel, Rig_PT_Subpanel_finish, useWidgets, rig, advancedArmRig, advancedLegRig, addFeetBones, finishFeetRig,
           eyeRig, advancedFingerRig, MySettings)

def register():
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type = MySettings)

def unregister():
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()