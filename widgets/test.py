import os
import json

def readWidgets():
        wgts = {}

        jsonFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'meshData.json')
        if os.path.exists(jsonFile):
            f = open(jsonFile)
            wgts = json.load(f)
        print(wgts[0])

readWidgets()