"""Main module."""

import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl,TileLayer

class Map(ipyleaflet.Map):
    
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
