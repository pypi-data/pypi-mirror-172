import json
import os


class Scenes:
    def __init__(self):
        self.scene_path = "./scenes"
        self.create_path()

    def create_path(self):
        if not os.path.exists(self.scene_path):
            # if the demo_folder2 directory is
            # not present then create it.
            os.makedirs(self.scene_path)

    def check_scene_exist(self, id):
        file_path = os.path.join(self.scene_path, f"{id}.json")
        return (lambda x: True if os.path.exists(x) else False)(file_path)

    def create_scene(self, id, name):
        # Data to be written
        dictionary = {
            "id": id,
            "name": id.upper(),
            "scene_image": name,
            "levels": [
                {
                    "tileSize": 256,
                    "size": 256,
                    "fallbackOnly": True
                },
                {
                    "tileSize": 512,
                    "size": 512
                },
                {
                    "tileSize": 512,
                    "size": 1024
                },
                {
                    "tileSize": 512,
                    "size": 2048
                },
                {
                    "tileSize": 512,
                    "size": 4096
                }
            ],
            "faceSize": 4096,
            "initialViewParameters": {
                "pitch": 0,
                "yaw": 0,
                "fov": 1.5707963267948966
            }
        }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Writing to sample.json
        with open(os.path.join(self.scene_path, f"{id}.json"), "w") as outfile:
            outfile.write(json_object)
        outfile.close()

    def save_scene(self, id, data):
        if self.check_scene_exist(id):
            with open(os.path.join(self.scene_path, f"{id}.json"), "r") as outfile:
                scene_data = json.loads(outfile.read())
                if 'hotspot' in scene_data:
                    del scene_data['hotspot']
                scene_data['hotspot'] = data
            with open(os.path.join(self.scene_path, f"{id}.json"), "w") as outfile:
                json_object = json.dumps(scene_data, indent=4)
                print(json_object)
                outfile.write(json_object)
            outfile.close()
            return json.loads(json_object)
        else:
            return None

    def get_scene(self, id):
        if self.check_scene_exist(id):
            with open(os.path.join(self.scene_path, f"{id}.json"), "r") as outfile:
                return json.loads(outfile.read())
        else:
            return {
                "id": id,
                "name": id.upper(),
                "scene_image": "default",
                "levels": [
                    {
                        "tileSize": 256,
                        "size": 256,
                        "fallbackOnly": True
                    },
                    {
                        "tileSize": 512,
                        "size": 512
                    },
                    {
                        "tileSize": 512,
                        "size": 1024
                    },
                    {
                        "tileSize": 512,
                        "size": 2048
                    },
                    {
                        "tileSize": 512,
                        "size": 4096
                    }
                ],
                "faceSize": 4096,
                "initialViewParameters": {
                    "pitch": 0,
                    "yaw": 0,
                    "fov": 1.5707963267948966
                }
            }
