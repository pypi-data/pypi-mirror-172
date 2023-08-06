import cv2
import numpy as np
from harvesters.core import Harvester
from typing import Optional, Union
import sys
import os
import glob
from enum import Enum
import copy

class Colorspace(Enum):
    RGB = 1
    BGR = 2
    HSV = 3
    GRAYSCALE = 4

class USSCamera:
    def __init__(self, connection_arg, cti_file: Optional[str] = None):
        self.harvesters_obj = None
        self.image_acquirer_obj = None

        #Operating System Check - Not Sure if needed
        if(sys.platform not in ["win32", "linux"]):
            raise OSError("Incorrect Operating System; must be on a Windows NT, Linux, or BSD platform.")

        #Attempt to Auto-Find CTI File
        if cti_file is None:
            #Designed to work only with the MatrixVision CTI file - to be tested with others
            try:
                cti_file = glob.glob(f"{os.environ['GENICAM_GENTL64_PATH']}/*.cti")[0]

            except OSError as e:
                raise OSError(f"MatrixVision CTI file not found, download it from http://static.matrix-vision.com/mvIMPACT_Acquire/2.41.0/")


        #Create Harvesters Object
        self.harvesters_obj = Harvester()
        self.harvesters_obj.add_file(cti_file)
        self.harvesters_obj.update()

        #Check if Camera List is Empty
        if(len(self.harvesters_obj.device_info_list) == 0):
            raise ValueError("No Cameras Found on Network")

        #Attempt to create the image acquirer 
        try:
            self.image_acquirer_obj = self.harvesters_obj.create(connection_arg)
        
        except ValueError as e:
            raise e

    #TO REVIEW: SHOULD COLORSPACE CONVERSIONS HAPPEN INSIDE OF THIS FUNCTION OR A DIFFERENT FUNCTION?
    def get_image(self, setting: Optional[Colorspace] = None) -> np.ndarray:
        self.image_acquirer_obj.start()
        rtn_frame = None
        with self.image_acquirer_obj.fetch() as buffer:
            component = buffer.payload.components[0]
            frame = component.data.reshape(component.height, component.width,int(component.num_components_per_pixel))
            rtn_frame = copy.deepcopy(frame)
        self.image_acquirer_obj.stop()

        if(setting is not None):
            raise NotImplementedError

        return rtn_frame

    def get_camera_attribute(self, attribute: Optional[str] = None) -> Union[list,tuple]:
        if(attribute is None):
            attribute_list = []
            for index,item in enumerate(dir(self.image_acquirer_obj.remote_device.node_map)):
                try:
                    attribute_dir = dir(eval(f'self.image_acquirer_obj.remote_device.node_map.{item}'))
                    if 'value' in attribute_dir:
                        attribute_list.append((item, eval(f'self.image_acquirer_obj.remote_device.node_map.{item}.value')))
                        
                except Exception as e:
                    pass
        
            return attribute_list

        else:
            try:
                if type(attribute) is str:
                    return (attribute, eval(f'self.image_acquirer_obj.remote_device.node_map.{attribute}.value'))
                else:
                    raise TypeError(f"Expected argument 'attribute' to be of type <class 'str'> but got type {type(attribute)}")

            except AttributeError:
                raise AttributeError(f'No such camera attribute with name {attribute}')
        
    def set_camera_attribute(self,setting: str,value):
        try:
            exec(f'self.image_acquirer_obj.remote_device.node_map.{setting}.value = {value}')

        except Exception as e:
            raise e