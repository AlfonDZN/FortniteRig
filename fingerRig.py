import bpy

from mathutils import Matrix
from math import pi

from bpy.types import Operator

suffix = ['_r', '_l']

nameList = [
    ('index_01', 'ctrl_fk_index_01'),
    ('middle_01', 'ctrl_fk_middle_01'),
    ('ring_01', 'ctrl_fk_ring_01'),
    ('pinky_01', 'ctrl_fk_pinky_01'),

    ('thumb_02', 'ctrl_fk_thumb_02'),
    ('index_02', 'ctrl_fk_index_02'),
    ('middle_02', 'ctrl_fk_middle_02'),
    ('ring_02', 'ctrl_fk_ring_02'),
    ('pinky_02', 'ctrl_fk_pinky_02'),

    ('thumb_03', 'ctrl_fk_thumb_03'),
    ('index_03', 'ctrl_fk_index_03'),
    ('middle_03', 'ctrl_fk_middle_03'),
    ('ring_03', 'ctrl_fk_ring_03'),
    ('pinky_03', 'ctrl_fk_pinky_03')
]

parentList = [
    ('ctrl_fk_thumb_02', 'thumb_01'),
    ('ctrl_fk_thumb_03', 'ctrl_fk_thumb_02'),
    ('ctrl_thumb_fingers', 'thumb_01'),

    ('ctrl_fk_index_01', 'index_metacarpal'),
    ('ctrl_fk_index_02', 'ctrl_fk_index_01'),
    ('ctrl_fk_index_03', 'ctrl_fk_index_02'),
    ('ctrl_index_fingers', 'index_metacarpal'),

    ('ctrl_fk_middle_01', 'middle_metacarpal'),
    ('ctrl_fk_middle_02', 'ctrl_fk_middle_01'),
    ('ctrl_fk_middle_03', 'ctrl_fk_middle_02'),
    ('ctrl_middle_fingers', 'middle_metacarpal'),

    ('ctrl_fk_ring_01', 'ring_metacarpal'),
    ('ctrl_fk_ring_02', 'ctrl_fk_ring_01'),
    ('ctrl_fk_ring_03', 'ctrl_fk_ring_02'),
    ('ctrl_ring_fingers', 'ring_metacarpal'),

    ('ctrl_fk_pinky_01', 'pinky_metacarpal'),
    ('ctrl_fk_pinky_02', 'ctrl_fk_pinky_01'),
    ('ctrl_fk_pinky_03', 'ctrl_fk_pinky_02'),
    ('ctrl_pinky_fingers', 'pinky_metacarpal')
]

layerList = [
    ('ctrl_thumb_fingers', 27),
    ('ctrl_fk_thumb_02', 27),
    ('ctrl_fk_thumb_03', 27),
    ('ctrl_index_fingers', 27),
    ('ctrl_fk_index_01', 27),
    ('ctrl_fk_index_02', 27),
    ('ctrl_fk_index_03', 27),
    ('ctrl_middle_fingers', 27),
    ('ctrl_fk_middle_01', 27),
    ('ctrl_fk_middle_02', 27),
    ('ctrl_fk_middle_03', 27),
    ('ctrl_ring_fingers', 27),
    ('ctrl_fk_ring_01', 27),
    ('ctrl_fk_ring_02', 27),
    ('ctrl_fk_ring_03', 27),
    ('ctrl_pinky_fingers', 27),
    ('ctrl_fk_pinky_01', 27),
    ('ctrl_fk_pinky_02', 27),
    ('ctrl_fk_pinky_03', 27)
]

def renameBones():
    for name, newName in nameList:
        for sym in suffix:
            #Get the pose bone with name
            poseBone = bpy.context.object.pose.bones.get(name + sym + '.001')
            #Continue if no bone of that name
            if poseBone is None:
                continue
            #Rename
            poseBone.name = newName + sym

def newEditBone(boneName):
    armature = bpy.context.scene.my_tool.sArmature
    arm = bpy.context.object.data
    
    for bone in arm.edit_bones[:]:
        if bone.name == boneName:
            copyBone = arm.edit_bones.new(bone.name)

            copyBone.head = bone.head
            copyBone.tail = bone.tail
            #copyBone.parent = bpy.data.objects[armature].data.edit_bones[parent]
            copyBone.matrix = bone.matrix

class advancedFingerRig(Operator):
    bl_idname = 'object.finger_rig'
    bl_label = 'Fortnite Rig'
    bl_description = 'Add an IK rig for the fingers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

        #Variable for the bones
        poseBone = bpy.data.objects[armature].pose.bones
        editBone = bpy.data.objects[armature].data.edit_bones

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

        #Duplicate bones
        for bone in nameList:
            for suf in suffix:
                newEditBone(bone[0] + suf)

        #Duplicate ctrl finger bones
        for bone in nameList[:5]:
            for suf in suffix:
                newEditBone(bone[0] + suf)

        #Rename bones
        bpy.ops.object.mode_set(mode = 'OBJECT')

        renameBones()

        #Rename manually
        for suf in suffix:
            poseBone['thumb_02' + suf + '.002'].name = 'ctrl_thumb_fingers' + suf
            poseBone['index_01' + suf + '.002'].name = 'ctrl_index_fingers' + suf
            poseBone['middle_01' + suf + '.002'].name = 'ctrl_middle_fingers' + suf
            poseBone['ring_01' + suf + '.002'].name = 'ctrl_ring_fingers' + suf
            poseBone['pinky_01' + suf + '.002'].name = 'ctrl_pinky_fingers' + suf

        bpy.ops.object.mode_set(mode = 'EDIT')

        #Parenting
        for parent, child in parentList:
            for suf in suffix:
                editBone[parent + suf].parent = editBone[child + suf]

                #Lock the location and rotation of the ctrl finger bones
                if 'fingers' in parent:
                    poseBone[parent + suf].lock_location[0] = True
                    poseBone[parent + suf].lock_location[2] = True
                    poseBone[parent + suf].lock_rotation_w = True
                    poseBone[parent + suf].lock_rotation[0] = True
                    poseBone[parent + suf].lock_rotation[1] = True
                    poseBone[parent + suf].lock_rotation[2] = True


        bpy.ops.object.mode_set(mode = 'POSE')

        #Add copy transforms constraint
        for bone in nameList:
            for suf in suffix:
                fingerCopyTransforms = poseBone[bone[0] + suf].constraints.new('COPY_TRANSFORMS')
                fingerCopyTransforms.name = "fingerCopyTransforms"

                #Set copy transform parameters
                fingerCopyTransforms.target = bpy.data.objects[armature]
                fingerCopyTransforms.subtarget =  'ctrl_fk_' + bone[0] + suf

        #Change bone layers
        for bone, layer in layerList:
            for suf in suffix:
                bpy.context.object.data.bones[bone + suf].layers[layer] = True
                bpy.context.object.data.bones[bone + suf].layers[0] = False

        #Add copy rotation constraints
        for bone in nameList[5:]:
            for suf in suffix:
                #Add bone constraint
                fingerCopyRotation = poseBone[bone[1] + suf].constraints.new('COPY_ROTATION')
                fingerCopyRotation.name = "fingerCopyRotation"

                #Set copy transform parameters
                fingerCopyRotation.target = bpy.data.objects[armature]
                if not 'thumb' in bone[1]:
                    fingerCopyRotation.subtarget = bone[1][:-1] + '1' + suf
                elif 'thumb' in bone[1]:
                    fingerCopyRotation.subtarget = bone[1][:-1] + '2' + suf
                fingerCopyRotation.target_space = 'LOCAL'
                fingerCopyRotation.owner_space = 'LOCAL'
                fingerCopyRotation.mix_mode = 'AFTER'

        #Add drivers
        for bone in nameList[:5]:
            for suf in suffix:
                #Add driver
                driverRotation = poseBone[bone[1] + suf].driver_add('rotation_quaternion', 3)
                driverRotation.driver.type = 'SCRIPTED'
                driverRotation.driver.expression = '-var * 10'

                var = driverRotation.driver.variables.new()
                var.type = 'TRANSFORMS'
                var.targets[0].id = bpy.data.objects[armature]
                var.targets[0].bone_target = 'ctrl_' + bone[0][:-2] + 'fingers' + suf
                var.targets[0].transform_type = 'LOC_Y'
                var.targets[0].transform_space = 'LOCAL_SPACE'

        #Add widgets
        if bpy.context.scene.my_tool.bWidgets:
            for suf in suffix:
                poseBone['ctrl_thumb_fingers' + suf].custom_shape = bpy.data.objects['fingers']
                poseBone['ctrl_thumb_fingers' + suf].custom_shape_translation[1] = 0.05
                poseBone['ctrl_thumb_fingers' + suf].custom_shape_rotation_euler[1] = pi / 2

                poseBone['ctrl_index_fingers' + suf].custom_shape = bpy.data.objects['fingers']
                poseBone['ctrl_index_fingers' + suf].custom_shape_translation[1] = 0.075
                poseBone['ctrl_index_fingers' + suf].custom_shape_rotation_euler[1] = pi / 2

                poseBone['ctrl_middle_fingers' + suf].custom_shape = bpy.data.objects['fingers']
                poseBone['ctrl_middle_fingers' + suf].custom_shape_translation[1] = 0.075
                poseBone['ctrl_middle_fingers' + suf].custom_shape_rotation_euler[1] = pi / 2

                poseBone['ctrl_ring_fingers' + suf].custom_shape = bpy.data.objects['fingers']
                poseBone['ctrl_ring_fingers' + suf].custom_shape_translation[1] = 0.075
                poseBone['ctrl_ring_fingers' + suf].custom_shape_rotation_euler[1] = pi / 2

                poseBone['ctrl_pinky_fingers' + suf].custom_shape = bpy.data.objects['fingers']
                poseBone['ctrl_pinky_fingers' + suf].custom_shape_translation[1] = 0.075
                poseBone['ctrl_pinky_fingers' + suf].custom_shape_rotation_euler[1] = pi / 2

            for bone in layerList:
                for suf in suffix:
                    if not 'finger' in bone[0] and not 'metacarpal' in bone[0] and not 'thumb_01' in bone[0]:
                        poseBone[bone[0] + suf].custom_shape = bpy.data.objects['eye']
                        if not '03' in bone[0]:
                            poseBone[bone[0] + suf].custom_shape_scale_xyz = (0.5, 0.5, 0.5)
                        elif '03' in bone[0]:
                            poseBone[bone[0] + suf].custom_shape_scale_xyz = (0.25, 0.25, 0.25)
                        poseBone[bone[0] + suf].custom_shape_rotation_euler = (pi/2, pi/2, 0)

        bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}