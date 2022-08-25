import bpy

from bpy.types import Operator
from mathutils import Matrix
from math import radians

nameList = [
    ("mch_foot_r.001", "mch_heel_rot_r"),
    ("mch_foot_l.001", "mch_heel_rot_l"),
    ("mch_foot_r.002", "mch_ball_rot_r"),
    ("mch_foot_l.002", "mch_ball_rot_l"),
    ("ctrl_pivot_toe_r.001", "ctrl_ik_foot_r"),
    ("ctrl_pivot_toe_l.001", "ctrl_ik_foot_l")
]

suffix = ["_r", "_l"]

driverList = ["mch_roll_out_r", "mch_roll_out_l", "mch_roll_in_r", "mch_roll_in_l", "mch_ball_rot_r", "mch_ball_rot_l", "mch_heel_rot_r", "mch_heel_rot_l"]

layerList = [
    ("ctrl_pivot_toe", 10),
    ("ctrl_ik_foot", 10),
    ("ctrl_heel", 10),
    ("ctrl_ik_pole_leg", 10),
    ("ctrl_ball", 10),
    ("mch_roll_out", 4),
    ("mch_roll_in", 4),
    ("mch_ball_rot", 4),
    ("mch_heel_rot", 4)
]

recalculateBoneRollList = [
    ("ctrl_heel", "GLOBAL_POS_X"),
    ("ctrl_pivot_toe", "GLOBAL_POS_X"),
    ("mch_roll_out", "GLOBAL_POS_X"),
    ("mch_roll_in", "GLOBAL_POS_X"),
    ("mch_heel_rot", "GLOBAL_NEG_X"),
    ("mch_heel_rot", "GLOBAL_NEG_X"),
    ("mch_ball_rot", "GLOBAL_POS_X"),
    ("mch_ball_rot", "GLOBAL_POS_X")
]

def selectBone(boneName):
    for bone in bpy.context.active_object.data.edit_bones[:]:
        if bone.name == boneName:
            bone.select = True
            bone.select_head = True
            bone.select_tail = True

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

def boneLocation(boneName, newLocation):
    armature = bpy.context.scene.my_tool.sArmature
    editBone = bpy.data.objects[armature].data.edit_bones

    editBone[boneName].head[0] = editBone[newLocation].head[0]
    editBone[boneName].head[1] = editBone[newLocation].head[1]
    editBone[boneName].head[2] = editBone[boneName].tail[2]

def switchDirection(boneName, degrees):
    obj = bpy.context.edit_object
    arm = obj.data

    bone = arm.edit_bones.get(boneName)

    if bone:
        #Local axis of the bone
        x, y, z = bone.matrix.to_3x3().col
        #Rotation matrix around local x axis through the center
        R = (Matrix.Translation(bone.center) @
             Matrix.Rotation(radians(degrees), 4, x) @
             Matrix.Translation(-bone.center)
        )
        bone.transform(R)

def recalculateBoneRoll(boneName, axis):
    bpy.ops.armature.select_all(action = 'DESELECT')
    selectBone(boneName)
    bpy.ops.armature.calculate_roll(type = axis)

class finishFeetRig(Operator):
    bl_idname = "object.feet_rig"
    bl_label = "Fortnite Rig"
    bl_description = "Add an IK rig for the fingers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

        #Variable for edit bones
        editBone = bpy.data.objects[armature].data.edit_bones

        #Go into object mode to select the armature
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Set the armature as active
        obj = bpy.context.scene.objects[armature]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        #Make only the first layer visible
        for i in range(32):
            bpy.context.object.data.layers[0] = True
            bpy.context.object.data.layers[i] = False

        #Go into edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        #Disable x-mirror
        bpy.context.object.data.use_mirror_x = False

        for i in range(2):
            newEditBone("mch_foot_r", "root")
            newEditBone("mch_foot_l", "root")
        newEditBone("ctrl_pivot_toe_r", "root")
        newEditBone("ctrl_pivot_toe_l", "root")

        #Rename bones
        bpy.ops.object.mode_set(mode = 'OBJECT')
        renameBones()
        bpy.ops.object.mode_set(mode = 'EDIT')

        boneLocation("mch_heel_rot_r", "ctrl_heel_r")
        boneLocation("mch_heel_rot_l", "ctrl_heel_l")
        boneLocation("mch_ball_rot_r", "ctrl_heel_r")
        boneLocation("mch_ball_rot_l", "ctrl_heel_l")

        for i in suffix:
            editBone["ctrl_ik_foot" + i].head[0] = (editBone["ctrl_pivot_toe" + i].head[0] + editBone["ctrl_heel" + i].head[0]) / 2
            editBone["ctrl_ik_foot" + i].head[1] = (editBone["ctrl_pivot_toe" + i].head[1] + editBone["ctrl_heel" + i].head[1]) / 2

            editBone["ctrl_ik_foot" + i].tail[0] = (editBone["ctrl_pivot_toe" + i].head[0] + editBone["ctrl_heel" + i].head[0]) / 2
            editBone["ctrl_ik_foot" + i].tail[1] = (editBone["ctrl_pivot_toe" + i].head[1] + editBone["ctrl_heel" + i].head[1]) / 2

        #Recalculate bone rolls
        for dummy, bone in nameList:
            recalculateBoneRoll(bone, "GLOBAL_POS_X")

        #Switch bone directions
        switchDirection("mch_ball_rot_r", 180)
        switchDirection("mch_ball_rot_l", 180)

        #Parenting
        for i in suffix:
            editBone["ctrl_pivot_toe" + i].parent = editBone["ctrl_ik_foot" + i]
            editBone["ctrl_heel" + i].parent = editBone["ctrl_ik_foot" + i]
            editBone["mch_roll_in" + i].parent = editBone["ctrl_pivot_toe" + i]
            editBone["mch_roll_out" + i].parent = editBone["mch_roll_in" + i]
            editBone["mch_heel_rot" + i].parent = editBone["mch_roll_out" + i]
            editBone["mch_ball_rot" + i].parent = editBone["mch_heel_rot" + i]
            editBone["ctrl_ball" + i].parent = editBone["mch_heel_rot" + i]
            editBone["ctrl_ik_leg" + i].parent = editBone["mch_ball_rot" + i]

        #Recalculate bone rolls
        for bone, axis in recalculateBoneRollList:
            for suf in suffix:
                recalculateBoneRoll(bone + suf, axis)

        #Go into pose mode
        bpy.ops.object.mode_set(mode = 'POSE')

        #Adding drivers to the roll bones
        for bone in driverList[:4]:
            rotation = bpy.data.objects[armature].pose.bones[bone].driver_add('rotation_quaternion', 1)
            rotation.driver.type = 'SCRIPTED'

            if "out_r" in bone or "in_l" in bone:
                rotation.driver.expression = '-var'
            else:
                rotation.driver.expression = 'var'
            
            var = rotation.driver.variables.new()
            var.type = 'TRANSFORMS'
            var.targets[0].id = bpy.data.objects[armature]
            var.targets[0].transform_type = 'ROT_X'
            var.targets[0].transform_space = 'LOCAL_SPACE'

            if "out_r" in bone or "in_r" in bone:
                var.targets[0].bone_target = "ctrl_heel_r"
            elif "out_l" in bone or "in_l" in bone:
                var.targets[0].bone_target = "ctrl_heel_l"
                
        #Adding drivers to the rotation bones
        for bone in driverList[4:]:
            rotation = bpy.data.objects[armature].pose.bones[bone].driver_add('rotation_quaternion', 3)
            rotation.driver.type = 'SCRIPTED'

            if "ball" in bone:
                rotation.driver.expression = 'var'
            elif "heel" in bone:
                rotation.driver.expression = '-var'

            var = rotation.driver.variables.new()
            var.type = 'TRANSFORMS'
            var.targets[0].id = bpy.data.objects[armature]
            var.targets[0].transform_type = 'ROT_Z'
            var.targets[0].transform_space = 'LOCAL_SPACE'

            if "rot_r" in bone:
                var.targets[0].bone_target = "ctrl_heel_r"
            elif "rot_l" in bone:
                var.targets[0].bone_target = "ctrl_heel_l"

        #Fix missing handles on F-Curve
        try:
            for i in range(50):
                driver = bpy.data.objects[armature].animation_data.drivers[i]

                if driver.data_path.split('"')[1] in driverList:
                    mod = driver.modifiers[0]
                    driver.modifiers.remove(mod)

                    driver.keyframe_points.add(2)

                    co = [(0.0, 0.0), (1.0, 1.0)]
                    handles = [[(-1.0, 0.0), (1/3, 1/3)],[(2/3, 2/3), (4/3, 4/3)]]
                    for i in range(len(co)):
                        driver.keyframe_points[i].co = co[i]
                        driver.keyframe_points[i].handle_left_type = 'FREE'
                        driver.keyframe_points[i].handle_right_type = 'FREE'
                        driver.keyframe_points[i].handle_left = handles[i][0]
                        driver.keyframe_points[i].handle_right = handles[i][1]
        except:
            pass

        #Change bone layers
        for bone, layer in layerList:
            for suf in suffix:
                bpy.context.object.data.bones[bone + suf].layers[layer] = True
                bpy.context.object.data.bones[bone + suf].layers[0] = False

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}