"""Main module for the geoHMT."""

import os
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl,TileLayer
from .utils import random_string,ee_initialize
from .controllers import viewerController



class geohmt():
    """this Map class inherits the ipyleaflet Map class.

    Args:
        ipyleaflet (class): An ipyleaflet map.
    """    
    
    def __init__(self,**kwargs):

        # Authenticates Earth Engine and initializes an Earth Engine session
        if "ee_initialize" not in kwargs.keys():
            kwargs["ee_initialize"] = True
        if kwargs["ee_initialize"]:
            ee_initialize()

        self.map = viewerController()
        


        # if "center" not in kwargs:
        #     kwargs["center"] = [35,105]
        
        # if "zoom" not in kwargs:
        #     kwargs["zoom"] = 4
        
        # if "scroll_wheel_zoom" not in kwargs:
        #     kwargs["scroll_wheel_zoom"] = True

        # #inherit the class of ipyleaflet.Map
        # super().__init__(**kwargs)

        # # set the widget size
        # if "height" not in kwargs:
        #     self.layout.height = "600px"
        # else:
        #     self.layout.height = kwargs["height"]

        # self.clear_controls()

        # # set the variable
        # self.draw_count = 0
        # self.draw_objects = []
        # self.draw_last_object = None
        



        # # add the control
        # self.add_control(FullScreenControl())
        # self.add_control(LayersControl(position="topright"))
        # self.add_control(DrawControl(position="topleft"))
        # self.add_control(MeasureControl())
        # self.add_control(ScaleControl(position="bottomleft"))



        # if "google_map" not in kwargs:
        #     layer = TileLayer(
        #     url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        #     attribution="Google",
        #     name="Google Maps",
        #     )
        #     self.add_layer(layer)

    def show(self):
        return self.map




    # load geojson
    # def add_geojson(self,geojson,style=None,layer_name="Untitled"):
    #     """adds a GeoJson file to the map.

    #     Args:
    #         geojson (str): The file path to the input GeoJSON
    #         style (dict, optional): The style for the Geojson layer. Defaults to None.
    #         layer_name (str, optional): the layer name for the GeoJSON. Defaults to "Untitled".

    #     Raises:
    #         FileNotFoundError: If the provided file dose not exist.
    #         TypeError: If the input geojson is not a str or dict.
    #     """        

    #     import json

    #     if isinstance(geojson,str):
    #         if not os.path.exists(geojson):
    #             raise FileNotFoundError("GeoJSON file could not be found.")
            
    #         with open(geojson) as f:
    #             data = json.load(f)
        
    #     elif isinstance(geojson,dict):
    #         data = geojson

    #     else:
    #         raise TypeError("the input file must be a type of str or dict.")

    #     if style is None:
    #         style = {
    #             "stroke" : True,
    #             "color" : "#000000",
    #             "weight" : 2,
    #             "opacity" : 1,
    #             "fill" : True,
    #             "fillColor" : "#000000",
    #             "fillOpacity" : 0.4,
    #         }
        
    #     geo_json = ipyleaflet.GeoJSON(data=data,style=style,name=layer_name)
    #     self.add_layer(geo_json)


    # # load shapefile
    # def add_shapefile(self,shp,style=None,layer_name="Untitled"):
    #     """Adds a shapefile layer to the map.

    #     Args:
    #         shp (str): The file path to the input shapefile.
    #         style (dict, optional): The style dictionary. Defaults to None.
    #         layer_name (str, optional): The layer name for the shapefile layer. Defaults to "Untitled".
    #     """        
    #     geojson = shp_to_geojson(shp)
    #     self.add_geojson(geojson,style=style,layer_name=layer_name)


    # def add_ee_layer(
    #     self, ee_object, vis_params={}, layer_name="ee layer untitled", shown=True, opacity=1.0
    #     ):
    #     """Adds a Earth Engine object to the map.

    #     Args:
    #         ee_object (Collection|Feature|Image|MapId): The Earth Engine object.
    #         vis_params (dict, optional): The visualization parameters. Defaults to {}.
    #         name (_type_, optional): The name of the layer. Defaults to None.
    #         shown (bool, optional): A flag indicating whether the layer should be on by default. Defaults to True.
    #         opacity (float, optional): The layer's opacity represented as a number between 0 and 1. Defaults to 1.0.
    #     """        
    #     ee_layer = ee_tile_layer(ee_object, vis_params, layer_name, shown, opacity)
    #     self.add_layer(ee_layer)

    # addLayer = add_ee_layer






