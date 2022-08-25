import bpy

from bpy.types import Operator

class baseRigVisible(Operator):
    bl_label = "Visible ik arm rig"
    bl_idname = "object.base_rig_hide"
    bl_description = "Make the base rig (in)visible"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.object.data.layers[0] = not bpy.context.object.data.layers[0] 

        return {'FINISHED'}

class ikArmVisible(Operator):
    bl_label = "Visible ik arm rig"
    bl_idname = "object.ik_arm_hide"
    bl_description = "Make the ik arm rig (in)visible"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.my_tool.bArms:
            bpy.context.object.data.layers[8] = not bpy.context.object.data.layers[8] 

        return {'FINISHED'}

class fkArmVisible(Operator):
    bl_label = "Visible fk arm rig"
    bl_idname = "object.fk_arm_hide"
    bl_description = "Make the fk arm rig (in)visible"
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.scene.my_tool.bArms:
            bpy.context.object.data.layers[24] = not bpy.context.object.data.layers[24]

        return {'FINISHED'}

class ikLegVisible(Operator):
    bl_label = "Visible ik leg rig"
    bl_idname = "object.ik_leg_hide"
    bl_description = "Make the ik leg rig (in)visible"
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.scene.my_tool.bLegs:
            bpy.context.object.data.layers[9] = not bpy.context.object.data.layers[9]

        return {'FINISHED'}

class fkLegVisible(Operator):
    bl_label = "Visible fk leg rig"
    bl_idname = "object.fk_leg_hide"
    bl_description = "Make the fk leg rig (in)visible"
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.scene.my_tool.bLegs:
            bpy.context.object.data.layers[25] = not bpy.context.object.data.layers[25]

        return {'FINISHED'}

class feetVisible(Operator):
    bl_label = "Visible foot rig"
    bl_idname = "object.foot_hide"
    bl_description = "Make the foot rig (in)visible"
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.scene.my_tool.bFeet:
            bpy.context.object.data.layers[10] = not bpy.context.object.data.layers[10]

        return {'FINISHED'}