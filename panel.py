import bpy

from bpy.types import Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, FloatProperty

class MySettings(PropertyGroup):
    sArmature : StringProperty(
            name = "Name",
            description = "Enter the name of the armature"
        )

    bArms : BoolProperty(
            name = "Arms",
            description = "Add a rig for the arms",
            default = False
        )

    bLegs : BoolProperty(
        name = "Legs",
        description = "Add a rig for the legs",
        default = False
    )

    bFeet : BoolProperty(
        name = "Feet",
        description = "Add a rig for the feet",
        default = False
    )

    bEyes : BoolProperty(
        name = "Eyes",
        description = "Add a rig for the eyes",
        default = False
    )

    bFingers : BoolProperty(
        name = "Fingers",
        description = "Add a rig for the fingers",
        default = False
    )

    fSwitchArmsRight : FloatProperty(
        name = "Arm right",
        description = "An ik/fk switch for the right arm",
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchArmsLeft : FloatProperty(
        name = "Arm Left",
        description = "An ik/fk switch for the left arm",
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchLegsLeft : FloatProperty(
        name = "Leg left",
        description = "An ik/fk switch for the left leg",
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchLegsRight : FloatProperty(
        name = "Leg right",
        description = "An ik/fk switch for the right leg",
        default = 0,
        min = 0,
        max = 1
    )

    bVisibleBaseRig : BoolProperty(
        name = "Base rig",
        description = "Make the base rig (in)visible",
        default = True
    )

    bVisibleIKArms : BoolProperty(
        name = "IK arms",
        description = "Make the IK arm bones (in)visible",
        default = True
    )

    bVisibleFKArms : BoolProperty(
        name = "FK arms",
        description = "Make the FK arm bones (in)visible",
        default = True
    )

    bVisibleIKLegs : BoolProperty(
        name = "IK Legs",
        description = "Make the IK leg bones (in)visible",
        default = True
    )

    bVisibleFKLegs : BoolProperty(
        name = "FK Legs",
        description = "Make the FK leg bones (in)visible",
        default = True
    )

    bPinned : BoolProperty(
        name = "Pin",
        description = "Pin the panel",
        default = False
    )

class Rig_PT_Panel(Panel):
    bl_label = "Advanced Fortnite Rig"
    bl_idname = "RIG_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig"

    def draw(self, context):
        layout = self.layout
        mytool = context.scene.my_tool

        row = layout.row()
        row.prop(mytool, "sArmature")

        row = layout.row()
        row.operator('object.rig', text="Add advanced rig", icon = "CON_KINEMATIC")

        row = layout.row()
        row.label(text = "Select which rigs to add")

        row = layout.row()
        row.prop(mytool, "bArms")

        row = layout.row()
        row.prop(mytool, "bLegs")

        row = layout.row()
        row.prop(mytool, "bFeet")
        row.enabled = mytool.bLegs

        """row = layout.row()
        row.prop(mytool, "bEyes")
        row.enabled = False

        row = layout.row()
        row.prop(mytool, "bFingers")
        row.enabled = False"""

class Rig_PT_Subpanel_hide(Panel):
    bl_parent_id = "RIG_PT_Panel"
    bl_label = "Bone layers"
    bl_idname = "RIG_PT_Subpanel_hide"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
            
        if bpy.context.object.data.layers[0]:
            layout.operator('object.base_rig_hide', text = "Base rig", icon = "HIDE_OFF")
        else:
            layout.operator('object.base_rig_hide', text = "Base rig", icon = "HIDE_ON")

        if bpy.context.scene.my_tool.bArms:
            row = layout.row()
            if bpy.context.object.data.layers[8]:
                row.operator('object.ik_arm_hide', text = "IK arm", icon = "HIDE_OFF")
            else:
                row.operator('object.ik_arm_hide', text = "IK arm", icon = "HIDE_ON")

            if bpy.context.object.data.layers[24]:
                row.operator('object.fk_arm_hide', text = "FK arm", icon = "HIDE_OFF")
            else:
                row.operator('object.fk_arm_hide', text = "FK arm", icon = "HIDE_ON")

        if bpy.context.scene.my_tool.bLegs:
            row = layout.row()
            if bpy.context.object.data.layers[9]:
                row.operator('object.ik_leg_hide', text = "IK leg", icon = "HIDE_OFF")
            else:
                row.operator('object.ik_leg_hide', text = "IK leg", icon = "HIDE_ON")

            if bpy.context.object.data.layers[25]:
                row.operator('object.fk_leg_hide', text = "FK leg", icon = "HIDE_OFF")
            else:
                row.operator('object.fk_leg_hide', text = "FK leg", icon = "HIDE_ON")

        if bpy.context.scene.my_tool.bFeet:
            row = layout.row()
            if bpy.context.object.data.layers[10]:
                row.operator('object.foot_hide', text = "Foot", icon = "HIDE_OFF")
            else:
                row.operator('object.foot_hide', text = "Foot", icon = "HIDE_ON")

class Rig_PT_Subpanel_switches(Panel):
    bl_parent_id = "RIG_PT_Panel"
    bl_label = "Switches"
    bl_idname = "RIG_PT_Subpanel_switches"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        mytool = context.scene.my_tool

        if bpy.context.scene.my_tool.bArms:
                row = layout.row()
                row.prop(mytool, "fSwitchArmsLeft", icon = 'VIEW_PAN')
                row.prop(mytool, "fSwitchArmsRight", icon = 'VIEW_PAN')

        if bpy.context.scene.my_tool.bLegs:
                row = layout.row()
                row.prop(mytool, "fSwitchLegsLeft")
                row.prop(mytool, "fSwitchLegsRight")

class Rig_PT_Subpanel_finish(Panel):
    bl_parent_id = "RIG_PT_Panel"
    bl_label = "Finish"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        mytool = context.scene.my_tool

        layout.operator('object.feet_rig', text = "Finish foot rig")