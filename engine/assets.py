import os.path

import pygame

ROOT_DIR = os.getcwd()

class AssetPipeline:
    __base_url: str = os.path.join(ROOT_DIR, "assets")
    asset_dict: dict[str, any] = dict()

    @staticmethod
    def get_instance():
        if not hasattr(AssetPipeline, "__instance"):
            AssetPipeline.__instance = AssetPipeline()

        return AssetPipeline.__instance

    def get_image(self, key: str) -> pygame.Surface:
        if key in self.asset_dict:
            return self.asset_dict[key]
        
        path = self.__build_path(key)
        

        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found")

        image = pygame.image.load(path)
        self.asset_dict[key] = image

        return image
    
    def __build_path(self, key: str):
        return os.path.join(self.__base_url, key)
        