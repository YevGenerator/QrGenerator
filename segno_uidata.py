
from typing import Any

class PdfSegnoData(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self["light"] = (255,255,255)
        self["dark"] = (0,0,0)
        self["scale"] = 10
        self["border"] = 1
    
    @property
    def fore_color(self)-> tuple:
        return self["dark"]

    @property
    def back_color(self)-> tuple:
        return self["light"]

    @property
    def scale(self)-> int:
        return self["scale"]

    @fore_color.setter
    def fore_color(self, value: tuple):
        self["dark"]=value

    @back_color.setter
    def back_color(self, value: tuple):
        self["light"]=value

    
    @property
    def border_width(self)-> int:
        return self["border"]
    

    @border_width.setter
    def border_width(self, value: int):
        self["border"]=value
        

    @scale.setter
    def scale(self, value: int):
        self["scale"]=value
        

class MicroSegnoData(PdfSegnoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self["finder_dark"]=(0,0,0)
        self["finder_light"]=(255,255,255)
        self["quiet_zone"]=(255,255,255)
    
    @property
    def finder_back_color(self)-> tuple:
        return self["finder_light"]
    
    @property
    def finder_fore_color(self)-> tuple:
        return self["finder_dark"]


    @finder_back_color.setter
    def finder_back_color(self, value: tuple):
        self["finder_light"]=value
        
    @finder_fore_color.setter
    def finder_fore_color(self, value: tuple):
        self["finder_dark"]=value
        
    @property
    def border_color(self)-> tuple:
        return self["quiet_zone"]
    
    @border_color.setter
    def border_color(self, value: tuple):
        self["quiet_zone"]=value
        
        
class AllSegnoData(MicroSegnoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self["alignment_dark"]=(0,0,0)
        self["alignment_light"]=(255,255,255)
    
    @MicroSegnoData.finder_back_color.setter
    def finder_back_color(self, value: tuple):
        MicroSegnoData.finder_back_color.fset(self, value)
        self["alignment_light"]=value
        
    @MicroSegnoData.finder_fore_color.setter
    def finder_fore_color(self, value: tuple):
        MicroSegnoData.finder_fore_color.fset(self, value)
        self["alignment_dark"]=value
        

    
