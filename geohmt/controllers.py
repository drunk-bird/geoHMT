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
        #search
        self.searchBar = ui_searchBar(position="topleft")
        self.searchBar.on_submit(self.searchBar_submited)
        self.searchBar.result_observe(self.search_result_change,names="value")
        self.add_control(self.searchBar)

        #draw tool
        self.draw_control = ipyleaflet.DrawControl(
            marker={"shapeOptions": {"color": "#3388ff"}},
            rectangle={"shapeOptions": {"color": "#3388ff"}},
            # circle={"shapeOptions": {"color": "#3388ff"}},
            circlemarker={},
            position="topleft",
            edit=True,
            remove=True,
        )

        self.draw_control.on_draw(self.handle_draw)


        self.add_control(LayersControl(position="topright"))
        self.add_control(FullScreenControl())
        self.add_control(self.draw_control)
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



    #Handles draw events
    def handle_draw(self,target, action, geo_json):
        print(target,action,geo_json)
        #action:created、
        try:
            self.roi_start = True
            # geom = geojson_to_ee(geo_json, False)
            # self.user_roi = geom
            # feature = ee.Feature(geom)
            self.draw_last_json = geo_json
            # self.draw_last_feature = feature
            # if action == "deleted" and len(self.draw_features) > 0:
                # self.draw_features.remove(feature)
                # self.draw_count -= 1
        #     else:
        #         self.draw_features.append(feature)
        #         self.draw_count += 1
        #     collection = ee.FeatureCollection(self.draw_features)
        #     self.user_rois = collection
        #     ee_draw_layer = ee_tile_layer(
        #         collection, {"color": "blue"}, "Drawn Features", False, 0.5
        #     )
        #     draw_layer_index = self.find_layer_index("Drawn Features")

        #     if draw_layer_index == -1:
        #         self.add_layer(ee_draw_layer)
        #         self.draw_layer = ee_draw_layer
        #     else:
        #         self.substitute_layer(self.draw_layer, ee_draw_layer)
        #         self.draw_layer = ee_draw_layer
        #     self.roi_end = True
        #     self.roi_start = False
        except Exception as e:
        #     self.draw_count = 0
        #     self.draw_features = []
        #     self.draw_last_feature = None
        #     self.draw_layer = None
        #     self.user_roi = None
        #     self.roi_start = False
        #     self.roi_end = False
        #     print("There was an error creating Earth Engine Feature.")
            raise Exception(e)











        # if "google_map" not in kwargs:
        #     layer = TileLayer(
        #     url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        #     attribution="Google",
        #     name="Google Maps",
        #     )
        #     self.add_layer(layer)



        