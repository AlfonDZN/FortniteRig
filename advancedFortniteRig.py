import bpy

from bpy.types import Operator

class rig(Operator):
    bl_label = "Advanced Fortnite Rig"
    bl_idname = "object.rig"
    bl_description = "Add a rig for the selected parts of the armature"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        if bpy.context.scene.my_tool.bWidgets:
            bpy.ops.object.widgets() 
        if bpy.context.scene.my_tool.bArms:
            bpy.ops.object.arm_rig()
        if bpy.context.scene.my_tool.bLegs:
            bpy.ops.object.leg_rig()
        if bpy.context.scene.my_tool.bEyes:
            bpy.ops.object.eye_rig()            
        if bpy.context.scene.my_tool.bFeet:
            bpy.ops.object.feet_bones()  

        return {'FINISHED'}