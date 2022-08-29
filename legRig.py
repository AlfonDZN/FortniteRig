import bpy

from math import pi
from mathutils import *

from bpy.types import Operator

suffix = ['_r', '_l']

targetList = ["thigh_r", "thigh_l", "calf_r", "calf_l", "foot_r", "foot_l", "ball_r", "ball_l"]

parentList = [
    ("thigh_r", "pelvis"),
    ("thigh_l", "pelvis"),
    ("thigh_r", "pelvis"),
    ("thigh_l", "pelvis"),
    ("calf_r", "thigh_r.001"),
    ("calf_l", "thigh_l.001"),
    ("calf_r", "thigh_r.002"),
    ("calf_l", "thigh_l.002"),
    ("foot_r", "calf_r.001"),
    ("foot_l", "calf_l.001"),
    ("foot_r", "calf_r.002"),
    ("foot_l", "calf_l.002"),
    ("ball_r", "foot_r.001"),
    ("ball_l", "foot_l.001"),
    ("ball_r", "foot_r.002"),
    ("ball_l", "foot_l.002")
]

#("BoneNameYouWantRenamed", "BoneNameToRenameBoneTo")
nameList = [
    ("foot_r.001", "mch_foot_r"),
    ("foot_l.001", "mch_foot_l"),
    ("thigh_r.001", "mch_thigh_r"),
    ("thigh_l.001", "mch_thigh_l"),
    ("foot_r.002", "ctrl_fk_foot_r"),
    ("foot_l.002", "ctrl_fk_foot_l"),
    ("calf_r.002", "ctrl_fk_calf_r"),
    ("calf_l.002", "ctrl_fk_calf_l"),
    ("thigh_r.002", "ctrl_fk_thigh_r"),
    ("thigh_l.002", "ctrl_fk_thigh_l"),
    ("ball_r.001", "ctrl_ball_r"),
    ("ball_l.001", "ctrl_ball_l"),
    ("ball_r.002", "ctrl_fk_ball_r"),
    ("ball_l.002", "ctrl_fk_ball_l"),
    ("foot_r.003", "ctrl_ik_leg_r"),
    ("foot_l.003", "ctrl_ik_leg_l"),
    ("calf_r.001", "mch_calf_r"),
    ("calf_l.001", "mch_calf_l")
]

poleList = ["ctrl_ik_pole_leg_r", "ctrl_ik_pole_leg_l"]

newLocationList = [
    ("thigh_r", "calf_r"),
    ("thigh_l", "calf_l"),
    ("calf_r", "foot_r"),
    ("calf_l", "foot_l"),
    ("foot_r", "ball_r"),
    ("foot_l", "ball_l")
]

def selectBone(boneName):
    for bone in bpy.context.active_object.data.edit_bones[:]:
        if bone.name == boneName:
            bone.select = True
            bone.select_head = True
            bone.select_tail = True

def scaleBone(boneName, scale):
    length = bpy.context.object.data.edit_bones[boneName].length
    bpy.context.object.data.edit_bones[boneName].length = length * scale

def locationTail(oldLocationName, newLocationName):
    head = bpy.context.object.data.edit_bones[newLocationName].head
    bpy.context.object.data.edit_bones[oldLocationName].tail = head

def renameBones():
    for name, newName in nameList:
        #Get the pose bone with name
        poseBone = bpy.context.object.pose.bones.get(name)
        #Continue if no bone of that name
        if poseBone is None:
            continue
        #Rename
        poseBone.name = newName

def newEditBone(boneName, parent):
    armature = bpy.context.scene.my_tool.sArmature
    arm = bpy.context.object.data
    
    for bone in arm.edit_bones[:]:
        if bone.name == boneName:
            copyBone = arm.edit_bones.new(bone.name)

            copyBone.head = bone.head
            copyBone.tail = bone.tail
            copyBone.matrix = bone.matrix
            copyBone.parent = bpy.data.objects[armature].data.edit_bones[parent]

def recalculateBoneRoll(boneName, axis):
    bpy.ops.armature.select_all(action = 'DESELECT')
    selectBone(boneName)
    bpy.ops.armature.calculate_roll(type = axis)

def calculatePoleAngle(baseBone, ikBone, poleBone):
    armature = bpy.context.scene.my_tool.sArmature

    def signed_angle(vector_u, vector_v, normal):
        #Normal specifies orientation
        angle = vector_u.angle(vector_v)
        if vector_u.cross(vector_v).angle(normal) < 1:
            angle = -angle
        return angle

    def get_pole_angle(base_bone, ik_bone, pole_location):
        pole_normal = (ik_bone.tail - base_bone.head).cross(pole_location - base_bone.head)
        projected_pole_axis = pole_normal.cross(base_bone.tail - base_bone.head)
        return signed_angle(base_bone.x_axis, projected_pole_axis, base_bone.tail - base_bone.head)

    base_bone = bpy.data.objects[armature].pose.bones[baseBone]
    ik_bone   = bpy.data.objects[armature].pose.bones[ikBone]
    pole_bone = bpy.data.objects[armature].pose.bones[poleBone]

    pole_angle_in_radians = get_pole_angle(
        base_bone,
        ik_bone,
        pole_bone.matrix.translation)

    return pole_angle_in_radians

class advancedLegRig(Operator):
    bl_idname = "object.leg_rig"
    bl_label = "Fortnite leg rig"
    bl_description = "Add an IK rig for the legs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

        #Variable for the bones
        editBone = bpy.data.objects[armature].data.edit_bones
        poseBone = bpy.data.objects[armature].pose.bones

        #Go into object mode to select the armature
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Set the armature as active
        obj = bpy.context.scene.objects[armature]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        for i in range(32):
            bpy.context.object.data.layers[0] = True
            bpy.context.object.data.layers[i] = False

        #Go into edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        #Switch directions of the ball bones
        scaleBone("ball_r", -1)
        scaleBone("ball_l", -1)

        #Change head and tail location of the leg bones
        for oldLocation, newLocation in newLocationList:
            locationTail(oldLocation, newLocation)

        #Recalculate bone roll
        recalculateBoneRoll("foot_r", "GLOBAL_POS_X")
        recalculateBoneRoll("foot_l", "GLOBAL_POS_X")
        recalculateBoneRoll("ball_r", "GLOBAL_POS_X")
        recalculateBoneRoll("ball_l", "GLOBAL_POS_X")

        #Duplicate the leg bones for the IK and FK rig
        for bone, parent in parentList:
            newEditBone(bone, parent)

        #Add ctrl ik leg bone
        newEditBone("foot_r", "root")
        newEditBone("foot_l", "root")

        #Change the position of the tail
        editBone["foot_r.003"].tail[0] = editBone["foot_r"].head[0]
        editBone["foot_r.003"].tail[1] = 0.13
        editBone["foot_r.003"].tail[2] = editBone["foot_r"].head[2]

        editBone["foot_l.003"].tail[0] = editBone["foot_l"].head[0]
        editBone["foot_l.003"].tail[1] = 0.13
        editBone["foot_l.003"].tail[2] = editBone["foot_l"].head[2]

        #Add pole target bones
        poleLeg_r = editBone["calf_r"].head
        bpy.ops.armature.bone_primitive_add(name = "ctrl_ik_pole_leg_r")
        editBone["ctrl_ik_pole_leg_r"].head = poleLeg_r + Vector((0.0, -0.35, 0.0))
        editBone["ctrl_ik_pole_leg_r"].tail = poleLeg_r + Vector((0.0, -0.45, 0.0))

        poleLeg_l = editBone["calf_l"].head
        bpy.ops.armature.bone_primitive_add(name = "ctrl_ik_pole_leg_l")
        editBone["ctrl_ik_pole_leg_l"].head = poleLeg_l + Vector((0.0, -0.35, 0.0))
        editBone["ctrl_ik_pole_leg_l"].tail = poleLeg_l + Vector((0.0, -0.45, 0.0))          

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Rename the duplicated hand bones
        renameBones()

        #Go into edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        #Change parent of pole and ctrl ik leg bones
        editBone["ctrl_ik_pole_leg_r"].parent = editBone["root"]
        editBone["ctrl_ik_pole_leg_l"].parent = editBone["root"]
        editBone["mch_foot_r"].parent = editBone["ctrl_ik_leg_r"]
        editBone["mch_foot_l"].parent = editBone["ctrl_ik_leg_l"]

        #Add IK Contraints in pose mode
        bpy.ops.object.mode_set(mode = 'POSE')

        for dummy, bone in nameList[16:]:
            legIK = bpy.data.objects[armature].pose.bones[bone].constraints.new('IK')
            #Set IK parameters
            legIK.target = bpy.data.objects[armature]
            legIK.pole_target = bpy.data.objects[armature]
            legIK.chain_count = 2
            if bone == "mch_calf_r":
                legIK.subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_leg_r"].name
                legIK.pole_subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_pole_leg_r"].name
                legIK.pole_angle = calculatePoleAngle("mch_thigh_r", "ctrl_ik_leg_r", "ctrl_ik_pole_leg_r")
            elif bone == "mch_calf_l":
                legIK.subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_leg_l"].name
                legIK.pole_subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_pole_leg_l"].name
                legIK.pole_angle = calculatePoleAngle("mch_thigh_l", "ctrl_ik_leg_l", "ctrl_ik_pole_leg_l")

        #Add copy transform contraints for the ik switch
        for bone in targetList:
            armCopyTransforms = bpy.data.objects[armature].pose.bones[bone].constraints.new('COPY_TRANSFORMS')
            armCopyTransforms.name = "ikCopyTransforms"

            #Set copy transform parameters
            armCopyTransforms.target = bpy.data.objects[armature]
            if "ball" in bone:
                armCopyTransforms.subtarget = "ctrl_" + bone
            else:
                armCopyTransforms.subtarget = "mch_" + bone

        #Add copy transform constraints for the fk switch
        for bone in targetList:
            armCopyTransforms = bpy.data.objects[armature].pose.bones[bone].constraints.new('COPY_TRANSFORMS')
            armCopyTransforms.name = "fkCopyTransforms"

            #Set copy transform parameters
            armCopyTransforms.target = bpy.data.objects[armature]
            armCopyTransforms.subtarget = "ctrl_fk_" + bone

        #Add drivers for the ik/fk switch
        for bone in targetList:
            constraint = bpy.data.objects[armature].pose.bones[bone].constraints["fkCopyTransforms"]
            if "_r" in bone:
                driverInfluence = constraint.driver_add('influence')
                driverInfluence.driver.type = 'AVERAGE'
                var = driverInfluence.driver.variables.new()
                var.name = 'var'
                var.type = 'SINGLE_PROP'
                var.targets[0].id_type = 'SCENE'
                var.targets[0].id = bpy.context.scene
                var.targets[0].data_path = 'my_tool.fSwitchLegsRight'
            elif "_l" in bone:
                driverInfluence = constraint.driver_add('influence')
                driverInfluence.driver.type = 'AVERAGE'
                var = driverInfluence.driver.variables.new()
                var.name = 'var'
                var.type = 'SINGLE_PROP'
                var.targets[0].id_type = 'SCENE'
                var.targets[0].id = bpy.context.scene
                var.targets[0].data_path = 'my_tool.fSwitchLegsLeft'

        #Go into edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        recalculateBoneRoll("ctrl_ik_leg_r", "GLOBAL_POS_X")
        recalculateBoneRoll("ctrl_ik_leg_l", "GLOBAL_POS_X")

        #Change bone layers in pose mode
        bpy.ops.object.mode_set(mode = 'POSE')

        for dummy, bone in nameList:
            if "ik" in bone or "ctrl_ball" in bone:
                bpy.context.object.data.bones[bone].layers[9] = True
                bpy.context.object.data.bones[bone].layers[0] = False
            elif "fk" in bone:
                bpy.context.object.data.bones[bone].layers[25] = True
                bpy.context.object.data.bones[bone].layers[0] = False
            elif "mch" in bone:
                bpy.context.object.data.bones[bone].layers[3] = True
                bpy.context.object.data.bones[bone].layers[0] = False

        for bone in poleList:
            bpy.context.object.data.bones[bone].layers[9] = True
            bpy.context.object.data.bones[bone].layers[0] = False

        #Add widgets
        if bpy.context.scene.my_tool.bWidgets:
            for suf in suffix:
                poseBone['ctrl_ik_pole_leg' + suf].custom_shape = bpy.data.objects['poleTarget']
                poseBone['ctrl_ik_pole_leg' + suf].custom_shape_scale_xyz = (0.5, 0.5, 0.5)

                poseBone['ctrl_ik_leg' + suf].custom_shape = bpy.data.objects['ik_leg']
                poseBone['ctrl_ik_leg' + suf].custom_shape_scale_xyz = (1, 1.25, 1)
                poseBone['ctrl_ik_leg' + suf].custom_shape_translation = (0.02, -0.01, 0.01)
                poseBone['ctrl_ik_leg' + suf].custom_shape_rotation_euler[1] = -pi/2

                poseBone['ctrl_ball' + suf].custom_shape = bpy.data.objects['ctrl_toe']
                poseBone['ctrl_ball' + suf].custom_shape_scale_xyz = (1.5, 1.5, 1.5)
                poseBone['ctrl_ball' + suf].custom_shape_translation = (-0.03, 0, 0.006)
                poseBone['ctrl_ball' + suf].custom_shape_rotation_euler = (0, pi/2, -pi/2)

                poseBone['ctrl_fk_thigh' + suf].custom_shape = bpy.data.objects['fk']
                poseBone['ctrl_fk_thigh' + suf].custom_shape_scale_xyz = (0.25, 0.25, 0.25)
                poseBone['ctrl_fk_thigh' + suf].custom_shape_rotation_euler[0] = pi/2

                poseBone['ctrl_fk_calf' + suf].custom_shape = bpy.data.objects['fk']
                poseBone['ctrl_fk_calf' + suf].custom_shape_scale_xyz = (0.25, 0.25, 0.25)
                poseBone['ctrl_fk_calf' + suf].custom_shape_rotation_euler[0] = pi/2
                
                poseBone['ctrl_fk_foot' + suf].custom_shape = bpy.data.objects['fk']
                poseBone['ctrl_fk_foot' + suf].custom_shape_scale_xyz = (0.5, 0.5, 0.5)
                poseBone['ctrl_fk_foot' + suf].custom_shape_rotation_euler[0] = pi/2

                poseBone['ctrl_fk_ball' + suf].custom_shape = bpy.data.objects['ctrl_toe']
                poseBone['ctrl_fk_ball' + suf].custom_shape_scale_xyz = (1.5, 1.5, 1.5)
                poseBone['ctrl_fk_ball' + suf].custom_shape_translation = (-0.03, 0, 0.006)
                poseBone['ctrl_fk_ball' + suf].custom_shape_rotation_euler = (0, pi/2, -pi/2)

        return {'FINISHED'}