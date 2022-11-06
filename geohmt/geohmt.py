"""Main module for the geoHMT."""

import os
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl,TileLayer
from .utils import random_string


class Map(ipyleaflet.Map):
    """this Map class inherits the ipyleaflet Map class.

    Args:
        ipyleaflet (class): An ipyleaflet map.
    """    
    
    def __init__(self,**kwargs):
        
        if "center" not in kwargs:
            kwargs["center"] = [35,105]
        
        if "zoom" not in kwargs:
            kwargs["zoom"] = 4
        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        #inherit the class of ipyleaflet.Map
        super().__init__(**kwargs)

        # set the widget size
        if "height" not in kwargs:
            self.layout.height = "600px"
        else:
            self.layout.height = kwargs["height"]

        # add the control
        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        if "google_map" not in kwargs:
            layer = TileLayer(
            url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attribution="Google",
            name="Google Maps",
            )
            self.add_layer(layer)

    # load geojson
    def add_geojson(self,geojson,style=None,layer_name="Untitled"):
        """adds a GeoJson file to the map.

        Args:
            geojson (str): The file path to the input GeoJSON
            style (dict, optional): The style for the Geojson layer. Defaults to None.
            layer_name (str, optional): the layer name for the GeoJSON. Defaults to "Untitled".

        Raises:
            FileNotFoundError: If the provided file dose not exist.
            TypeError: If the input geojson is not a str or dict.
        """        

        import json

        if isinstance(geojson,str):
            if not os.path.exists(geojson):
                raise FileNotFoundError("GeoJSON file could not be found.")
            
            with open(geojson) as f:
                data = json.load(f)
        
        elif isinstance(geojson,dict):
            data = geojson

        else:
            raise TypeError("the input file must be a type of str or dict.")

        if style is None:
            style = {
                "stroke" : True,
                "color" : "#000000",
                "weight" : 2,
                "opacity" : 1,
                "fill" : True,
                "fillColor" : "#000000",
                "fillOpacity" : 0.4,
            }
        
        geo_json = ipyleaflet.GeoJSON(data=data,style=style,name=layer_name)
        self.add_layer(geo_json)


    # load shapefile
    def add_shapefile(self,shp,style=None,layer_name="Untitled"):
        """Adds a shapefile layer to the map.

        Args:
            shp (str): The file path to the input shapefile.
            style (dict, optional): The style dictionary. Defaults to None.
            layer_name (str, optional): The layer name for the shapefile layer. Defaults to "Untitled".
        """        
        geojson = shp_to_geojson(shp)
        self.add_geojson(geojson,style=style,layer_name=layer_name)


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

