import json
import os


class Hotspot:
    def __init__(self):
        self.scene_path = "./scenes"

    def check_scene_exist(self, scene):
        file_path = os.path.join(self.scene_path, f"{scene}.json")
        return (lambda x: True if os.path.exists(x) else False)(file_path)

    def create_hotspot(self, scene, hotspot):
        if self.check_scene_exist(scene):
            with open(os.path.join(self.scene_path, f"{scene}.json"), "r") as outfile:
                scene_data = json.loads(outfile.read())
                if 'hotspot' in scene_data:
                    res = list(filter(lambda i: i['elementId'] != hotspot['elementId'], scene_data['hotspot']))
                    scene_data['hotspot'] = res
                else:
                    scene_data['hotspot'] = []
                scene_data['hotspot'].append(hotspot)
            outfile.close()
            with open(os.path.join(self.scene_path, f"{id}.json"), "w") as outfile:
                json_object = json.dumps(scene_data, indent=4)
                outfile.write(json_object)
            outfile.close()
            return json.loads(json_object)
        else:
            return None

    def get_hotspot(self, scene, hotspot):
        if self.check_scene_exist(scene):
            with open(os.path.join(self.scene_path, f"{scene}.json"), "r") as outfile:
                scene_data = json.loads(outfile.read())
                res = list(filter(lambda i: i['elementId'] == hotspot, scene_data['hotspot']))
            outfile.close()
            return res[0]
        else:
            return []

    def get_all_hotspot(self, scene):
        if self.check_scene_exist(scene):
            with open(os.path.join(self.scene_path, f"{scene}.json"), "r") as outfile:
                scene_data = json.loads(outfile.read())
            outfile.close()
            return scene_data['hotspot']
        else:
            return []
