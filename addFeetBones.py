import bpy

from bpy.types import Operator

nameList = [
    ("ctrl_ik_leg_r.001", "ctrl_pivot_toe_r"),
    ("ctrl_ik_leg_l.001", "ctrl_pivot_toe_l"),
    ("ctrl_ik_leg_r.002", "ctrl_heel_r"),
    ("ctrl_ik_leg_l.002", "ctrl_heel_l"),
    ("ctrl_ik_leg_r.003", "mch_roll_out_r"),
    ("ctrl_ik_leg_l.003", "mch_roll_out_l"),
    ("ctrl_ik_leg_r.004", "mch_roll_in_r"),
    ("ctrl_ik_leg_l.004", "mch_roll_in_l")
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

def boneLocation(boneName, headX, headY, headZ, tailX, tailY, tailZ):
    armature = bpy.context.scene.my_tool.sArmature
    editBone = bpy.data.objects[armature].data.edit_bones

    editBone[boneName].head[0] = headX
    editBone[boneName].head[1] = headY
    editBone[boneName].head[2] = headZ

    editBone[boneName].tail[0] = tailX
    editBone[boneName].tail[1] = tailY
    editBone[boneName].tail[2] = tailZ

def recalculateBoneRoll(boneName, axis):
    bpy.ops.armature.select_all(action = 'DESELECT')
    selectBone(boneName)
    bpy.ops.armature.calculate_roll(type = axis)

class addFeetBones(Operator):
    bl_idname = "object.feet_bones"
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

        #Add the guiding bones
        for i in range(4):
            newEditBone("ctrl_ik_leg_r", "root")
            newEditBone("ctrl_ik_leg_l", "root")

        #Go back into object mode to rename bones
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Rename bones
        renameBones()

        #Go back into edit mode to change the position of the guiding bones
        bpy.ops.object.mode_set(mode = 'EDIT')

        #Change the position of the guiding bones
        boneLocation("ctrl_pivot_toe_r", -0.175, -0.175, 0, -0.175, -0.175, 0.08)
        boneLocation("ctrl_heel_r", -0.15, 0.1, 0, -0.15, 0.1, 0.08)
        boneLocation("mch_roll_out_r", -0.225, -0.08, 0, -0.1, -0.08, 0)
        boneLocation("mch_roll_in_r", -0.1, -0.08, 0, -0.225, -0.08, 0)

        boneLocation("ctrl_pivot_toe_l", 0.175, -0.175, 0, 0.175, -0.175, 0.08)
        boneLocation("ctrl_heel_l", 0.15, 0.1, 0, 0.15, 0.1, 0.08)
        boneLocation("mch_roll_out_l", 0.225, -0.08, 0, 0.1, -0.08, 0)
        boneLocation("mch_roll_in_l", 0.1, -0.08, 0, 0.225, -0.08, 0)

        #Recalculate bone rolls
        for dummy, bone in nameList:
            recalculateBoneRoll(bone, "GLOBAL_POS_X")

        #Deselect all selected bones
        bpy.ops.armature.select_all(action='DESELECT')
        #Enable x-mirror
        bpy.context.object.data.use_mirror_x = True
        #Enable local mode
        bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'        

        return {'FINISHED'}