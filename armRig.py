import bpy
from mathutils import *

from bpy.types import Operator

targetList = ["hand_r", "hand_l", "lowerarm_r", "lowerarm_l", "upperarm_r", "upperarm_l"]

#("BoneNameYouWantRenamed", "BoneNameToRenameBoneTo")
nameList = [
    ("hand_r.002", "mch_hand_r"),
    ("hand_l.002", "mch_hand_l"),

    ("lowerarm_r.001", "mch_lowerarm_r"),
    ("lowerarm_l.001", "mch_lowerarm_l"),
    ("upperarm_r.001", "mch_upperarm_r"),
    ("upperarm_l.001", "mch_upperarm_l"),

    ("hand_r.003", "ctrl_fk_hand_r"),
    ("hand_l.003", "ctrl_fk_hand_l"),
    ("lowerarm_r.002", "ctrl_fk_lowerarm_r"),
    ("lowerarm_l.002", "ctrl_fk_lowerarm_l"),
    ("upperarm_r.002", "ctrl_fk_upperarm_r"),
    ("upperarm_l.002", "ctrl_fk_upperarm_l"),

    ("hand_r.001", "ctrl_ik_hand_r"),
    ("hand_l.001", "ctrl_ik_hand_l")
]

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

class advancedArmRig(Operator):
    bl_idname = "object.arm_rig"
    bl_label = "Fortnite Rig"
    bl_description = "Add an IK rig for the arms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

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

        #Duplicate the hand bones for the IK rig
        for bone in targetList[:2]:
                newEditBone(bone, 'root')

        #Duplicate the other arm bones for the IK and FK rig
        for i in range(2):
            newEditBone("upperarm_r", "clavicle_r")
            newEditBone("upperarm_l", "clavicle_l")

        newEditBone("lowerarm_r", "upperarm_r.001")
        newEditBone("lowerarm_l", "upperarm_l.001")
        newEditBone("lowerarm_r", "upperarm_r.002")
        newEditBone("lowerarm_l", "upperarm_l.002")

        newEditBone("hand_r", "lowerarm_r.001")
        newEditBone("hand_l", "lowerarm_l.001")

        #Duplicate the hand bones for the FK rig
        newEditBone("hand_r", "lowerarm_r.002")
        newEditBone("hand_l", "lowerarm_l.002") 

        #Add pole target bones
        poleArm_r = bpy.data.objects[armature].data.edit_bones["lowerarm_r"].head
        bpy.ops.armature.bone_primitive_add(name = "ctrl_ik_pole_arm_r")
        bpy.data.objects[armature].data.edit_bones["ctrl_ik_pole_arm_r"].head = poleArm_r + Vector((0.0, 0.35, 0.0))
        bpy.data.objects[armature].data.edit_bones["ctrl_ik_pole_arm_r"].tail = poleArm_r + Vector((0.0, 0.45, 0.0))
            
        poleArm_l = bpy.data.objects[armature].data.edit_bones["lowerarm_l"].head
        bpy.ops.armature.bone_primitive_add(name = "ctrl_ik_pole_arm_l")
        bpy.data.objects[armature].data.edit_bones["ctrl_ik_pole_arm_l"].head = poleArm_l + Vector((0.0, 0.35, 0.0))
        bpy.data.objects[armature].data.edit_bones["ctrl_ik_pole_arm_l"].tail = poleArm_l + Vector((0.0, 0.45, 0.0))          

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Rename the duplicated hand bones
        renameBones()

        #Add IK Contraints in pose mode
        bpy.ops.object.mode_set(mode = 'POSE')

        for dummy, bone in nameList[:2]:
            armIK = bpy.data.objects[armature].pose.bones[bone].constraints.new('IK')

            #Set IK parameters
            armIK.target = bpy.data.objects[armature]
            armIK.pole_target = bpy.data.objects[armature]
            if bone == "mch_hand_r":
                armIK.subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_hand_r"].name
                armIK.pole_subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_pole_arm_r"].name
                armIK.pole_angle = calculatePoleAngle("clavicle_r", "ctrl_ik_hand_r", "ctrl_ik_pole_arm_r")
            if bone == "mch_hand_l":
                armIK.subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_hand_l"].name
                armIK.pole_subtarget = bpy.data.objects[armature].pose.bones["ctrl_ik_pole_arm_l"].name
                armIK.pole_angle = calculatePoleAngle("clavicle_l", "ctrl_ik_hand_l", "ctrl_ik_pole_arm_l")
            armIK.chain_count = 3
            armIK.use_rotation = True

        #Add copy transform contraints for the ik switch
        for bone in targetList:
            armCopyTransforms = bpy.data.objects[armature].pose.bones[bone].constraints.new('COPY_TRANSFORMS')
            armCopyTransforms.name = "ikCopyTransforms"

            #Set copy transform parameters
            armCopyTransforms.target = bpy.data.objects[armature]
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
                var.targets[0].data_path = 'my_tool.fSwitchArmsRight'
            elif "_l" in bone:
                driverInfluence = constraint.driver_add('influence')
                driverInfluence.driver.type = 'AVERAGE'
                var = driverInfluence.driver.variables.new()
                var.name = 'var'
                var.type = 'SINGLE_PROP'
                var.targets[0].id_type = 'SCENE'
                var.targets[0].id = bpy.context.scene
                var.targets[0].data_path = 'my_tool.fSwitchArmsLeft'

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Change bone layers in pose mode
        bpy.ops.object.mode_set(mode = 'POSE')

        #Loop through all the bones
        for bone in bpy.context.active_object.pose.bones[:]:
            if "ctrl_ik_hand" in bone.name or "ctrl_ik_pole_arm" in bone.name:
                bpy.context.object.data.bones[bone.name].layers[8] = True
                bpy.context.object.data.bones[bone.name].layers[0] = False
            if "ctrl_fk_hand" in bone.name or "ctrl_fk_lowerarm" in bone.name or "ctrl_fk_upperarm" in bone.name:
                bpy.context.object.data.bones[bone.name].layers[24] = True
                bpy.context.object.data.bones[bone.name].layers[0] = False
            if "mch_upperarm" in bone.name or "mch_lowerarm" in bone.name:
                bpy.context.object.data.bones[bone.name].layers[2] = True
                bpy.context.object.data.bones[bone.name].layers[0] = False

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}