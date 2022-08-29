import bpy
import os
import json

from bpy.types import Operator

widgetList = ['ik_hand', 'poleTarget', 'fk', 'ik_leg', 'ctrl_toe', 'foot_pivot']

class useWidgets(Operator):
    bl_idname = "object.widgets"
    bl_label = "Fortnite Rig"
    bl_description = "Add wigets to the bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
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

        return {'FINISHED'}