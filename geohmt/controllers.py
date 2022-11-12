import os
import ipywidgets as widgets
from ipyleaflet import WidgetControl
from ipyfilechooser import filechooser
from  IPython.display import display
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl,TileLayer
from .view import ui_searchBar
from .utils import geocode
import ee




class viewerController(ipyleaflet.Map):

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

        # initail the control
        self.initControlBar()
        
        #
        self.search_locations = None
        self.search_loc_marker = None




    def initControlBar(self):

        self.clear_controls()

        self.searchBar = ui_searchBar(position="topleft")
        self.searchBar.on_submit(self.searchBar_submited)
        self.searchBar.result_observe(self.search_result_change,names="value")
        self.add_control(self.searchBar)


        self.add_control(LayersControl(position="topright"))
        self.add_control(FullScreenControl())
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))



    def searchBar_submited(self,text):
        
        if text.value != "":
            self.searchBar.submit_changed()
            if self.searchBar.typeValue == 1:
                g = geocode(text.value)
            elif self.searchBar.typeValue == 2:
                self.searchBar.show_results()
                # self.default_style = {"cursor": "wait"}
                # ee_assets = search_ee_data(text.value, source="all")
                # self.search_datasets = ee_assets
                # asset_titles = [x["title"] for x in ee_assets]
                # assets_dropdown.options = asset_titles
                # search_output.clear_output()
                # if len(ee_assets) > 0:
                #     html_widget.value = ee_data_html(ee_assets[0])
                # with search_output:
                #     display(html_widget)
                # self.default_style = {"cursor": "default"}
                return

            self.search_locations = g
            if g is not None and len(g) > 0:
                top_loc = g[0]
                coordinate = (top_loc.lat, top_loc.lng)
                self.search_loc_geom = ee.Geometry.Point(top_loc.lng, top_loc.lat)
                if self.search_loc_marker is None:
                    marker = ipyleaflet.Marker(
                        location=coordinate,
                        draggable=False,
                        name="Search location",
                    )
                    self.search_loc_marker = marker
                    self.add_layer(marker)
                    self.center = coordinate
                else:
                    marker = self.search_loc_marker
                    marker.location = coordinate
                    self.center = coordinate
                self.searchBar.search_results.options = [x.address for x in g]
            
            self.searchBar.show_results()

            # else:
            #     with search_output:
            #         search_output.clear_output()
            #         print("No results could be found.")


    def search_result_change(self,change):

        # print(self.searchBar.search_results.value,self.searchBar.search_results.index)
        result_index = self.searchBar.search_results.index
        locations = self.search_locations
        location = locations[result_index]
        coordinate = (location.lat, location.lng)
        self.search_loc_geom = ee.Geometry.Point(location.lng, location.lat)
        marker = self.search_loc_marker
        marker.location = coordinate
        self.center = coordinate















        # if "google_map" not in kwargs:
        #     layer = TileLayer(
        #     url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        #     attribution="Google",
        #     name="Google Maps",
        #     )
        #     self.add_layer(layer)



        