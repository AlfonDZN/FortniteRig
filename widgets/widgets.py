import bpy
import os
import json

from math import pi

from bpy.types import Operator

widgetList = ['ik_hand', 'poleTarget', 'fk', 'ik_leg', 'ctrl_toe', 'foot_pivot', 'fingers', 'eyes', 'eye', 'root', 'pelvis']

class useWidgets(Operator):
    bl_idname = "object.widgets"
    bl_label = "Fortnite Rig"
    bl_description = "Add wigets to the bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Variable of the armature to add the rig to
        armature = bpy.context.scene.my_tool.sArmature

        #Variable for the bones
        editBone = bpy.data.objects[armature].data.edit_bones
        poseBone = bpy.data.objects[armature].pose.bones

        #Go into object mode to select the armature
        bpy.ops.object.mode_set(mode = 'OBJECT')

        #Read the json file
        wgts = {}

        jsonFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'meshData.json')
        if os.path.exists(jsonFile):
            f = open(jsonFile)
            wgts = json.load(f)

        #Check if widget does not already exists
        exists = False
        for wgt in widgetList:
            existingWidget = bpy.context.scene.objects.get(wgt)
            if existingWidget:
                exists = True

        if bpy.context.scene.my_tool.bWidgets:
            for wgt in widgetList:
                if not exists:
                    newMesh = bpy.data.meshes.new('widget')
                    newMesh.from_pydata(wgts[wgt]['vertices'], wgts[wgt]['edges'],wgts[wgt]['faces'])
                    newMesh.update()

                    #Make object from the mesh
                    newObject = bpy.data.objects.new(wgt, newMesh)
                    viewLayer = bpy.context.view_layer
                    viewLayer.active_layer_collection.collection.objects.link(newObject)

        #Check if 'widgets' collection already exists
        for col in bpy.data.collections:
            if col.name == 'widgets':
                collectionFound = True
            else:
                collectionFound = False

        #Create new collection for the widgets
        if not collectionFound:
            collection = bpy.context.blend_data.collections.new(name = 'widgets')
            bpy.context.collection.children.link(collection)
        #Put the widgets in a collection
        for widget in widgetList:
            if not exists:
                bpy.context.collection.objects.unlink(bpy.data.objects[widget])
                bpy.data.collections['widgets'].objects.link(bpy.data.objects[widget])

        #Exclude widget collection
        bpy.context.layer_collection.children['widgets'].exclude = True

        #Check if the pelvis and/or root already have a custom bone shape
        if not poseBone['root'].custom_shape or not poseBone['pelvis'].custom_shape:
            #Add widget for pevis and the root
            poseBone['root'].custom_shape = bpy.data.objects['root']
            poseBone['root'].custom_shape_scale_xyz = (1.5, 1.5, 1.5)
            poseBone['root'].custom_shape_rotation_euler = (pi/2, 0, 0)

            poseBone['pelvis'].custom_shape = bpy.data.objects['pelvis']
            poseBone['pelvis'].custom_shape_scale_xyz = (2, 2, 2)

            bpy.ops.object.mode_set(mode = 'EDIT')
            if round(abs(editBone['pelvis'].head[0]), 1) == round(abs(editBone['pelvis'].tail[0]), 1):
                poseBone['pelvis'].custom_shape_rotation_euler = (pi/2, 0, 0)
            elif round(abs(editBone['pelvis'].head[1]), 1) == round(abs(editBone['pelvis'].tail[1]), 1):
                poseBone['pelvis'].custom_shape_rotation_euler = (0, pi/2, 0)

            bpy.ops.object.mode_set(mode = 'OBJECT')

        return {'FINISHED'}