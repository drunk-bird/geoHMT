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






#shpfile transform geojson
def shp_to_geojson(shp,savefile=None):
    """Converts a shapefile to GeoJSON.

    Args:
        shp (str): The file path to the input shapefile.
        savefile (str, optional): the file path to the output GeoJSoN. Defaults to None.

    Raises:
        FileNotFoundError: If the input shapefile does not exist.

    Returns:
        dict: the dictionary of the GeoJSON.
    """

    import json
    import shapefile

    shp = os.path.abspath(shp)

    if not os.path.exists(shp):
        raise FileNotFoundError("Shapefile file could not be found.")

    shp_obj = shapefile.Reader(shp)
    geojson = shp_obj.__geo_interface__

    if savefile is None:
        return geojson

    else:
        savefile = os.path.abspath(savefile)
        out_dir = os.path.dirname(savefile)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(savefile,"w") as f:
            f.write(json.dumps(geojson))




def ee_tile_layer(
    ee_object, vis_params={}, name="ee layer untitled", shown=True, opacity=1.0
    ):
    """Converts Earth Engine layer to ipleaflet Tilelayer.

    Args:
        ee_object (Collection|Feature|Image|MapId): The Earth Engine object.
        vis_params (dict, optional): The visualization parameters. Defaults to {}.
        name (str, optional): The name of the layer. Defaults to "Layer untitled".
        shown (bool, optional): A flag indicating whether the layer should be on by default. Defaults to True.
        opacity (float, optional): The layer's opacity represented as a number between 0 and 1. Defaults to 1.0.

    Raises:
        AttributeError: _description_

    Returns:
        _type_: _description_
    """    

    import ee

    image = None

    if vis_params is None:
        vis_params = {}

    if (
        not isinstance(ee_object, ee.Image)
        and not isinstance(ee_object, ee.ImageCollection)
        and not isinstance(ee_object, ee.FeatureCollection)
        and not isinstance(ee_object, ee.Feature)
        and not isinstance(ee_object, ee.Geometry)
    ):
        err_str = "\n\nThe image argument in 'addLayer' function must be an instace of one of ee.Image, ee.Geometry, ee.Feature or ee.FeatureCollection."
        raise AttributeError(err_str)

    if (
        isinstance(ee_object, ee.geometry.Geometry)
        or isinstance(ee_object, ee.feature.Feature)
        or isinstance(ee_object, ee.featurecollection.FeatureCollection)
    ):
        features = ee.FeatureCollection(ee_object)

        width = 2

        if "width" in vis_params:
            width = vis_params["width"]

        color = "000000"

        if "color" in vis_params:
            color = vis_params["color"]

        image_fill = features.style(**{"fillColor": color}).updateMask(
            ee.Image.constant(0.5)
        )
        image_outline = features.style(
            **{"color": color, "fillColor": "00000000", "width": width}
        )

        image = image_fill.blend(image_outline)
    elif isinstance(ee_object, ee.image.Image):
        image = ee_object
    elif isinstance(ee_object, ee.imagecollection.ImageCollection):
        image = ee_object.mosaic()

    map_id_dict = ee.Image(image).getMapId(vis_params)
    tile_layer = TileLayer(
        url=map_id_dict["tile_fetcher"].url_format,
        attribution="Google Earth Engine",
        name=name,
        opacity=opacity,
        visible=shown,
    )
    
    return tile_layer