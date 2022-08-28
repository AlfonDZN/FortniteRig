import bpy

from math import pi
from bpy.types import Operator

vertices = [(-1.8,0,0), (-1.78079,-0.19509,0), (-1.72388,-0.382683,0), (-1.63147,-0.55557,0), (-1.50711,-0.707107,0), (-1.35557,-0.83147,0), (-1.18268,-0.92388,0), (-0.995091,-0.980785,0), (-0.800001,-1,0), (-0.60491,-0.980785,0), (-0.417317,-0.92388,0), (-0.24443,-0.83147,0), (0.24443,-0.83147,0), (0.417317,-0.92388,0), (0.60491,-0.980785,0), (0.800001,-1,0), (0.995091,-0.980785,0), (1.18268,-0.92388,0), (1.35557,-0.83147,0), (1.50711,-0.707107,0), (1.63147,-0.55557,0), (1.72388,-0.382684,0), (1.78079,-0.19509,0), (1.8,0,0), (1.78079,0.19509,0), (1.72388,0.382684,0), (1.63147,0.55557,0), (1.50711,0.707107,0), (1.35557,0.83147,0), (1.18268,0.92388,0), (0.995091,0.980785,0), (0.800001,1,0), (0.60491,0.980785,0), (0.417317,0.92388,0), (0.24443,0.83147,0), (-0.24443,0.83147,0), (-0.417317,0.92388,0), (-0.60491,0.980785,0), (-0.800001,1,0), (-0.995091,0.980785,0), (-1.18268,0.92388,0), (-1.35557,0.83147,0), (-1.50711,0.707107,0), (-1.63147,0.55557,0), (-1.72388,0.382683,0), (-1.78079,0.19509,0)]

edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (11,12), (12,13), (13,14), (14,15), (15,16), (16,17), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23), (23,24), (24,25), (25,26), (26,27), (27,28), (28,29), (29,30), (30,31), (31,32), (32,33), (33,34), (34,35), (35,36), (36,37), (37,38), (38,39), (39,40), (40,41), (41,42), (42,43), (43,44), (44,45), (45,0)]

faces = []

nameList = [
    ("Circle", "eye"),
    ("R_eye.001", "ctrl_eyes"),
    ("R_eye.002", "ctrl_eye_r"),
    ("L_eye.001", "ctrl_eye_l")
]

boneList = ["R_eye", "L_eye"]

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

def renameObjects():
    for name, newName in nameList:
        #Get the object with name
        object = bpy.context.scene.objects.get(name)
        #Continue if no object of that name
        if object is None:
            continue
        #Rename
        object.name = newName

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


class eyeRig(Operator):
    bl_idname = "object.eye_rig"
    bl_label = "Fortnite Rig"
    bl_description = "Add an eye rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

        #Variable for bones
        editBone = bpy.data.objects[armature].data.edit_bones
        poseBone = bpy.data.objects[armature].pose.bones

        #Go into object mode to select the armature
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Make only the first layer visible
        for i in range(32):
            bpy.context.object.data.layers[0] = True
            bpy.context.object.data.layers[i] = False

        newMesh = bpy.data.meshes.new('newMesh')
        newMesh.from_pydata(vertices, edges, faces)
        newMesh.update()
        
        #Make object from the mesh
        newObject = bpy.data.objects.new('eyes', newMesh)
        viewLayer = bpy.context.view_layer
        viewLayer.active_layer_collection.collection.objects.link(newObject)

        #Add ctrl shapes for the individual eyes
        bpy.ops.mesh.primitive_circle_add()

        #Position the ctrl objects
        obj = bpy.context.scene.objects[armature]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        renameObjects()

        #Go into edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        #Create ctrl_eyes
        newEditBone('R_eye', 'head')

        #Create ctrl_eye
        for bone in boneList:
            newEditBone(bone, 'R_eye.001')

        #Go into object mode to rename objects and bones
        bpy.ops.object.mode_set(mode = 'OBJECT')
        renameBones()

        #Change location of the ctrl eye bones
        bpy.ops.object.mode_set(mode = 'EDIT')

        editBone['ctrl_eyes'].head[0] = obj.location[0]
        editBone['ctrl_eyes'].tail[0] = obj.location[0]

        for dummy, bone in nameList[1:]:
            editBone[bone].head[1] = -0.25
            editBone[bone].tail[1] = -0.27

        editBone['R_eye_lid_upper_mid'].parent = editBone['head']
        editBone['L_eye_lid_upper_mid'].parent = editBone['head']
        editBone['R_eye_lid_lower_mid'].parent = editBone['head']
        editBone['L_eye_lid_lower_mid'].parent = editBone['head']

        #Recalculate bone roll
        for dummy, bone in nameList[1:]:
            recalculateBoneRoll(bone, 'POS_Z')

        for bone in boneList:
            trackTo = bpy.data.objects[armature].pose.bones[bone].constraints.new('TRACK_TO')
            trackTo.target = bpy.data.objects[armature]
            if 'R' in bone:
                trackTo.subtarget = bpy.data.objects[armature].pose.bones['ctrl_eye_r'].name
            elif 'L' in bone:
                trackTo.subtarget = bpy.data.objects[armature].pose.bones['ctrl_eye_l'].name
            trackTo.up_axis = 'UP_Z'
            trackTo.track_axis = 'TRACK_Y'

        #Go back into pose mode to assign widgets
        bpy.ops.object.mode_set(mode = 'POSE')

        poseBone['ctrl_eyes'].custom_shape = bpy.data.objects['eyes']
        poseBone['ctrl_eyes'].custom_shape_rotation_euler[0] = pi/2
        poseBone['ctrl_eyes'].custom_shape_rotation_euler[1] = pi/2
        poseBone['ctrl_eyes'].custom_shape_scale_xyz = (1.75, 1.75, 1.75)

        poseBone['ctrl_eye_r'].custom_shape = bpy.data.objects['eye']
        poseBone['ctrl_eye_r'].custom_shape_rotation_euler[0] = pi/2

        poseBone['ctrl_eye_l'].custom_shape = bpy.data.objects['eye']
        poseBone['ctrl_eye_l'].custom_shape_rotation_euler[0] = pi/2

        bpy.ops.pose.select_all(action='DESELECT')

        #Go back into object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}