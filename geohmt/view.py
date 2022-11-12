import ipywidgets as widgets
from ipyfilechooser import FileChooser
import ipyleaflet
from ipyleaflet import WidgetControl
import ipyevents
import ee
from IPython.display import display



class ui_searchBar(WidgetControl):

    def __init__(self, **kwargs):

        self.setupUi()
        self.connect()
        if "widget" not in kwargs:
            kwargs["widget"] = self.search_widget

        super().__init__(**kwargs)



    def setupUi(self):

        self.search_button = widgets.ToggleButton(
            value=False,
            tooltip="Search location/data",
            icon="search",
            layout=widgets.Layout(
                width="28px", height="28px", padding="0px 0px 0px 4px"
            ),
        )

        self.search_type = widgets.Dropdown(
            options=[('adress', 1), ('data', 2)],
            value= 1,
            description='',
            disabled=False,
            layout=widgets.Layout(min_width="50px", max_width="50px"),
            )
        # self.search_type.style.description_width = "110px"

        self.search_box = widgets.Text(
            placeholder="Search by place name or address",
            tooltip="Search location",
            layout=widgets.Layout(width="300px"),
        )

        self.search_output = widgets.Output(
            layout={
                "max_width": "340px",
                "max_height": "350px",
                "overflow": "scroll",
            }
        )

        self.search_results = widgets.RadioButtons()

        self.assets_dropdown = widgets.Dropdown(
            options=[],
            layout=widgets.Layout(min_width="279px", max_width="279px"),
        )

        import_btn = widgets.Button(
            description="import",
            button_style="primary",
            tooltip="Click to import the selected asset",
            layout=widgets.Layout(min_width="57px", max_width="57px"),
        )

        self.search_bar = widgets.HBox([self.search_type,self.search_box])
        self.search_result_widget = widgets.VBox([self.search_bar])
        self.search_widget = widgets.HBox([self.search_button])

        self.typeValue = self.search_type.value

        # self.widget = search_widget


    def connect(self):
        search_event = ipyevents.Event(
        source=self.search_widget, watched_events=["mouseenter", "mouseleave"]
        )
        search_event.on_dom_event(self.handle_search_event)


        self.search_button.observe(self.search_btn_click, "value")


        self.search_type.observe(self.search_type_changed,names="value")

        # self.search_box.on_submit(self.on_submit)


        


    def on_submit(self,callback):
        self.search_box.on_submit(callback)

    def result_observe(self, callback, names="value"):
        self.search_results.observe(callback,names=names)





    def handle_search_event(self,event):

        if event["type"] == "mouseenter":
            self.search_widget.children = [self.search_button, self.search_result_widget]
            # search_type.value = "name/address"
        elif event["type"] == "mouseleave":
            if not self.search_button.value:
                self.search_widget.children = [self.search_button]
                # self.search_result_widget.children = [self.search_type, self.search_box]


    def search_btn_click(self,change):
        if change["new"]:
            self.search_widget.children = [self.search_button, self.search_result_widget]
            # self.search_type.value = "name/address"
        else:
            self.search_widget.children = [self.search_button]
            # self.search_result_widget.children = [self.search_bar, self.search_box]


    def search_type_changed(self,change):

        self.search_box.value = ""
        self.search_output.clear_output()

        if change["new"] == 1:

            self.search_box.placeholder = "Search by place name or address, e.g., beijing"
            # assets_dropdown.options = []
            self.search_result_widget.children = [
                self.search_bar,
                # self.search_output,
            ]
            
        elif change["new"] == 2:
            self.search_box.placeholder = (
                "Search GEE data catalog by keywords, e.g., elevation"
            )
            self.search_result_widget.children = [
                self.search_bar,
                # self.search_box,
                # self.assets_combo,
                # self.search_output,
            ]


    def submit_changed(self):
        self.search_result_widget.children = [
            self.search_bar,
            self.search_output,
        ]
        with self.search_output:
            self.search_output.clear_output(wait=True)
            print("Searching ...")

    def show_results(self):
        if self.search_results is not None:
            with self.search_output:
                self.search_output.clear_output(wait=True)
                display(self.search_results)
        else:
            with self.search_output:
                self.search_output.clear_output()
                print("No results could be found.")



