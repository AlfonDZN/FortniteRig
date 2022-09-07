import bpy

from bpy.types import Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, FloatProperty

class MySettings(PropertyGroup):
    sArmature : StringProperty(
            name = 'Name',
            description = 'Enter the name of the armature'
        )

    bWidgets : BoolProperty(
        name = 'Widgets',
        description = 'Use widgets for the bones',
        default = True
    )

    bArms : BoolProperty(
            name = 'Arms',
            description = 'Add a rig for the arms',
            default = False
        )

    bLegs : BoolProperty(
        name = 'Legs',
        description = 'Add a rig for the legs',
        default = False
    )

    bFeet : BoolProperty(
        name = 'Feet',
        description = 'Add a rig for the feet',
        default = False
    )

    bEyes : BoolProperty(
        name = 'Eyes',
        description = 'Add a rig for the eyes',
        default = False
    )

    bFingers : BoolProperty(
        name = 'Fingers',
        description = 'Add a rig for the fingers',
        default = False
    )

    fSwitchArmsRight : FloatProperty(
        name = 'Arm right',
        description = 'An ik/fk switch for the right arm',
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchArmsLeft : FloatProperty(
        name = 'Arm Left',
        description = 'An ik/fk switch for the left arm',
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchLegsLeft : FloatProperty(
        name = 'Leg left',
        description = 'An ik/fk switch for the left leg',
        default = 0,
        min = 0,
        max = 1
    )

    fSwitchLegsRight : FloatProperty(
        name = 'Leg right',
        description = 'An ik/fk switch for the right leg',
        default = 0,
        min = 0,
        max = 1
    )

    bVisibleBaseRig : BoolProperty(
        name = 'Base rig',
        description = 'Make the base rig (in)visible',
        default = True
    )

    bVisibleIKArms : BoolProperty(
        name = 'IK arms',
        description = 'Make the IK arm bones (in)visible',
        default = False
    )

    bVisibleFKArms : BoolProperty(
        name = 'FK arms',
        description = 'Make the FK arm bones (in)visible',
        default = False
    )

    bVisibleFingers : BoolProperty(
        name = 'Fingers',
        description = 'Make the finger bones (in)visible',
        default = False
    )

    bVisibleIKLegs : BoolProperty(
        name = 'IK Legs',
        description = 'Make the IK leg bones (in)visible',
        default = False
    )

    bVisibleFKLegs : BoolProperty(
        name = 'FK Legs',
        description = 'Make the FK leg bones (in)visible',
        default = False
    )

    bVisibleFeet : BoolProperty(
        name = 'Feet',
        description = 'Make the feet bones (in)visible',
        default = False
    )

class Rig_PT_Panel(Panel):
    bl_label = 'Fortnite Rig'
    bl_idname = 'RIG_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig'

    def draw(self, context):
        layout = self.layout
        mytool = context.scene.my_tool

        ##################################
        ##             Rigs            ###
        ##################################
        box = layout.box()
        box.prop(mytool, 'sArmature')
 
        row = box.row()
        row.operator('object.rig', text='Add rig', icon = 'CON_KINEMATIC')
        row.prop(mytool, 'bWidgets', icon = 'BONE_DATA')

        sub = box.column(align = True)
        sub.label(text = 'Select which rigs to add')

        sub.prop(mytool, 'bEyes')

        sub.prop(mytool, 'bArms')

        sub.prop(mytool, 'bFingers')

        sub.prop(mytool, 'bLegs')
        
        sub.prop(mytool, 'bFeet')
        #row.enabled = mytool.bLegs




        ##################################
        ##            Layers           ###
        ##################################
        box = layout.box()
        row = box.row()
        row.label(text = 'Bone layers')

        row = box.row()
        if bpy.context.scene.my_tool.bVisibleBaseRig:
            row.prop(mytool, 'bVisibleBaseRig', text = 'Base rig', icon = 'HIDE_OFF')
            bpy.context.object.data.layers[0] = True
        
        if not bpy.context.scene.my_tool.bVisibleBaseRig:
            row.prop(mytool, 'bVisibleBaseRig', text = 'Base rig', icon = 'HIDE_ON')
            bpy.context.object.data.layers[0] = False

        if bpy.context.scene.my_tool.bArms:
            row = box.row()
            if bpy.context.scene.my_tool.bVisibleIKArms:
                row.prop(mytool, 'bVisibleIKArms', text = 'IK arm', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[8] = True
            if not bpy.context.scene.my_tool.bVisibleIKArms:
                row.prop(mytool, 'bVisibleIKArms', text = 'IK arm', icon = 'HIDE_ON')
                bpy.context.object.data.layers[8] = False

            if bpy.context.scene.my_tool.bVisibleFKArms:
                row.prop(mytool, 'bVisibleFKArms', text = 'FK arm', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[24] = True
            if not bpy.context.scene.my_tool.bVisibleFKArms:
                row.prop(mytool, 'bVisibleFKArms', text = 'FK arm', icon = 'HIDE_ON')
                bpy.context.object.data.layers[24] = False

        if bpy.context.scene.my_tool.bFingers:
            row = box.row()
            if bpy.context.scene.my_tool.bVisibleFingers:
                row.prop(mytool, 'bVisibleFingers', text = 'Fingers', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[27] = True
            if not bpy.context.scene.my_tool.bVisibleFingers:
                row.prop(mytool, 'bVisibleFingers', text = 'Fingers', icon = 'HIDE_ON')
                bpy.context.object.data.layers[27] = False

        if bpy.context.scene.my_tool.bLegs:
            row = box.row()
            if bpy.context.scene.my_tool.bVisibleIKLegs:
                row.prop(mytool, 'bVisibleIKLegs', text = 'IK legs', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[9] = True
            if not bpy.context.scene.my_tool.bVisibleIKLegs:
                row.prop(mytool, 'bVisibleIKLegs', text = 'Ik legs', icon = 'HIDE_ON')
                bpy.context.object.data.layers[9] = False

            if bpy.context.scene.my_tool.bVisibleFKLegs:
                row.prop(mytool, 'bVisibleFKLegs', text = 'FK legs', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[25] = True
            if not bpy.context.scene.my_tool.bVisibleFKLegs:
                row.prop(mytool, 'bVisibleFKLegs', text = 'Fk legs', icon = 'HIDE_ON')
                bpy.context.object.data.layers[25] = False

        if bpy.context.scene.my_tool.bFeet:
            row = box.row()
            if bpy.context.scene.my_tool.bVisibleFeet:
                row.prop(mytool, 'bVisibleFeet', text = 'Feet', icon = 'HIDE_OFF')
                bpy.context.object.data.layers[10] = True
            if not bpy.context.scene.my_tool.bVisibleFeet:
                row.prop(mytool, 'bVisibleFeet', text = 'Feet', icon = 'HIDE_ON')
                bpy.context.object.data.layers[10] = False


        ##################################
        ##           Switches          ###
        ##################################
        if bpy.context.scene.my_tool.bArms or bpy.context.scene.my_tool.bLegs:
            box = layout.box()
            row = box.row()
            row.label(text = 'Switches')

            if bpy.context.scene.my_tool.bArms:
                row = box.row()
                row.prop(mytool, 'fSwitchArmsLeft')
                row.prop(mytool, 'fSwitchArmsRight')

            if bpy.context.scene.my_tool.bLegs:
                row = box.row()
                row.prop(mytool, 'fSwitchLegsLeft')
                row.prop(mytool, 'fSwitchLegsRight')

class Rig_PT_Subpanel_finish(Panel):
    bl_parent_id = 'RIG_PT_Panel'
    bl_label = 'Finish'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        layout.operator('object.feet_rig', text = 'Finish foot rig')