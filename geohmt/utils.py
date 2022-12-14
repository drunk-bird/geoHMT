


def random_string(string_length=3,seed = False):
    """Generates a random string of fixed length.

    Args:
        string_length (int, optional): Fixed length. Defaults to 3.
        seed (bool, optional): Weather uses seed. Defaults to False.

    Returns:
        _type_: A random string
    """    
    
    import random
    import string

    if seed:
        random.seed(1)

    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


# EE Authentication and Initialization #

def ee_initialize(token_name="EARTHENGINE_TOKEN"):
    """Authenticates Earth Engine and initialize an Earth Engine session

    Args:
        token_name (str, optional): The token name of the github environment. Defaults to "EARTHENGINE_TOKEN".
    """    
    import ee
    import os

    if ee.data._credentials is None:
        try:
            ee_token = os.environ.get(token_name)
            if ee_token is not None:
                credential_file_path = os.path.expanduser(
                    "~/.config/earthengine/credentials"
                    )
                if not os.path.exists(credential_file_path):
                    os.makedirs(
                        os.path.dirname(credential_file_path), exist_ok=True)
                    if ee_token.startswith("{") and ee_token.endswith("}"
                    ):  # deals with token generated by new auth method (earthengine-api>=0.1.304).
                        token_dict = json.loads(ee_token)
                        with open(credential_file_path, "w") as f:
                            f.write(json.dumps(token_dict))

            ee.Initialize()
        except Exception:
            ee.Authenticate()
            ee.Initialize()




def geocode(location, max_rows=10, reverse=False):
    """Search location by address and lat/lon coordinates.

    Args:
        location (str): Place name or address
        max_rows (int, optional): Maximum number of records to return. Defaults to 10.
        reverse (bool, optional): Search place based on coordinates. Defaults to False.

    Returns:
        list: Returns a list of locations.
    """
    import geocoder

    if not isinstance(location, str):
        print("The location must be a string.")
        return None

    if not reverse:

        locations = []
        addresses = set()
        g = geocoder.arcgis(location, maxRows=max_rows)

        for result in g:
            address = result.address
            if address not in addresses:
                addresses.add(address)
                locations.append(result)

        if len(locations) > 0:
            return locations
        else:
            return None

    else:
        try:
            if "," in location:
                latlon = [float(x) for x in location.split(",")]
            elif " " in location:
                latlon = [float(x) for x in location.split(" ")]
            else:
                print(
                    "The lat-lon coordinates should be numbers only and separated by comma or space, such as 40.2, -100.3"
                )
                return
            g = geocoder.arcgis(latlon, method="reverse")
            locations = []
            addresses = set()

            for result in g:
                address = result.address
                if address not in addresses:
                    addresses.add(address)
                    locations.append(result)

            if len(locations) > 0:
                return locations
            else:
                return None

        except Exception as e:
            print(e)
            return None



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
    from ipyleaflet import TileLayer

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