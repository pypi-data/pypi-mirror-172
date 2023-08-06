from html import escape

import numpy as np
from AnyQt.QtCore import QSize, Qt, QObject

from Orange.data import Domain, Table, ContinuousVariable
from Orange.widgets import settings, gui
from Orange.widgets.settings import DomainContextHandler
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.utils.plot import OWPlotGUI
from Orange.widgets.visualize.utils.plotutils import PlotWidget
from Orange.widgets.visualize.utils.widget import OWDataProjectionWidget
from Orange.widgets.widget import OWWidget
from orangecontrib.geo.utils import find_lat_lon
from orangecontrib.geo.widgets.plotutils import MapMixin, MAX_LONGITUDE, \
    MAX_LATITUDE, deg2norm, MapViewBox, TILE_PROVIDERS, DEFAULT_TILE_PROVIDER
from orangewidget.utils.signals import Input
from orangewidget.utils.widgetpreview import WidgetPreview
from orangewidget.widget import Msg


class GpxGraph(QObject, gui.OWComponent):
    freeze = settings.Setting(False)
    tile_provider_key = settings.Setting(DEFAULT_TILE_PROVIDER)

    def __init__(self, scatter_widget, parent):
        super().__init__(parent)
        self.view_box = MapViewBox(self)
        self.plot_widget = PlotWidget(
            viewBox=self.view_box, parent=parent, background=None,
        )
        gui.OWComponent.__init__(self, scatter_widget)
        MapMixin.__init__(self)

    def update_coordinates(self):
        """
        Trigger the update of coordinates while keeping other features intact.

        The method gets the coordinates by calling `self.get_coordinates`,
        which in turn calls the widget's `get_coordinate_data`. The number of
        coordinate pairs returned by the latter must match the current number
        of points. If this is not the case, the widget should trigger
        the complete update by calling `reset_graph` instead of this method.
        """
        x, y = self.get_coordinates()
        if x is None or len(x) == 0:
            return

        self._reset_view(x, y)
        if self.scatterplot_item is None:
            if self.sample_indices is None:
                indices = np.arange(self.n_valid)
            else:
                indices = self.sample_indices
            kwargs = dict(x=x, y=y, data=indices)
            self.scatterplot_item = CurvePlotItem(**kwargs)
            self.scatterplot_item.sigClicked.connect(self.select_by_click)
            self.scatterplot_item_sel = CurvePlotItem(**kwargs)
            self.plot_widget.addItem(self.scatterplot_item_sel)
            self.plot_widget.addItem(self.scatterplot_item)
        else:
            self.scatterplot_item.setCoordinates(x, y)
            self.scatterplot_item_sel.setCoordinates(x, y)

        if not self.freeze:
            self.update_view_range()
        print(self.scatterplot_item)

    def update_sizes(self):
        pass

    def update_colors(self):
        pass

    def update_selection_colors(self):
        pass

    def update_shapes(self):
        pass

    def _reset_view(self, x_data, y_data):
        """
        This functionality is moved to update_view_range which is called after
        update_coordinates because this is not called if there is no data and
        it also interferes with map freeze.
        """
        pass

    def update_view_range(self, match_data=True):
        """
        Update what part of tha map is shown.
        :param match_data: if True update so that all data is shown else just
        update current view
        """
        if match_data:
            # if we have no data then show the whole map
            min_x, max_x, min_y, max_y = 0, 1, 0, 1
            if self.scatterplot_item is not None:
                x_data, y_data = self.scatterplot_item.getData()
                if len(x_data):
                    min_x, max_x = np.min(x_data), np.max(x_data)
                    min_y, max_y = np.min(y_data), np.max(y_data)
        else:
            [min_x, max_x], [min_y, max_y] = self.view_box.viewRange()

        self._update_view_range(min_x, max_x, min_y, max_y, not match_data)

    def reset_button_clicked(self):
        """Reset map so that all data is displayed"""
        self.update_view_range()


class GpxMapGraph(MapMixin, GpxGraph):
    def __init__(self, scatter_widget, parent):
        GpxGraph.__init__(self, scatter_widget, parent)
        MapMixin.__init__(self)

    def update_tile_provider(self):
        super()._update_tile_provider(TILE_PROVIDERS[self.tile_provider_key])

    def clear(self):
        super().clear()
        if self.freeze:
            # readd map items that are cleared
            self.plot_widget.addItem(self.b_map_item)
            self.plot_widget.addItem(self.map_item)
        else:
            self.clear_map()


class OWGpxViewer(OWWidget):
    name = 'Geo Map'
    description = 'Show data points on a world map.'
    icon = "icons/GeoMap.svg"
    priority = 100

    replaces = [
        "Orange.widgets.visualize.owmap.OWMap",
    ]

    contextHandler = DomainContextHandler()
    attr_lat = settings.ContextSetting(None)
    attr_lon = settings.ContextSetting(None)

    GRAPH_CLASS = GpxMapGraph
    graph = settings.SettingProvider(GpxMapGraph)

    class Error(OWDataProjectionWidget.Error):
        no_lat_lon_vars = Msg("Data has no latitude and longitude variables.")

    class Warning(OWDataProjectionWidget.Warning):
        missing_coords = Msg(
            "Plot cannot be displayed because '{}' or '{}' "
            "is missing for all data points")
        out_of_range = Msg("Points with out of range latitude or longitude are not displayed.")
        no_internet = Msg("Cannot fetch map from the internet. "
                          "Displaying only cached parts.")

    class Information(OWDataProjectionWidget.Information):
        missing_coords = Msg(
            "Points with missing '{}' or '{}' are not displayed")

    class Inputs:
        data = Input("Data", Table, default=True)

    def __init__(self):
        super().__init__()

        self._attr_lat, self._attr_lon = None, None

        box = gui.vBox(self.mainArea, True, margin=0)
        self.graph = self.GRAPH_CLASS(self, box)
        box.layout().addWidget(self.graph.plot_widget)

        self.gui = OWPlotGUI(self)

        self.lat_lon_model = DomainModel(DomainModel.MIXED,
                                         valid_types=ContinuousVariable)

        lat_lon_box = gui.vBox(self.controlArea, box="Layout", spacing=0)
        options = dict(
            labelWidth=75, orientation=Qt.Horizontal, sendSelectedValue=True,
            valueType=str, contentsLength=14
        )

        print(self.graph)
        gui.comboBox(lat_lon_box, self, 'graph.tile_provider_key', label='Map:',
                     items=list(TILE_PROVIDERS),
                     callback=self.update_tile_provider, **options)

        gui.comboBox(lat_lon_box, self, 'attr_lat', label='Latitude:',
                     callback=self.setup_plot,
                     model=self.lat_lon_model, **options,
                     searchable=True)

        gui.comboBox(lat_lon_box, self, 'attr_lon', label='Longitude:',
                     callback=self.setup_plot,
                     model=self.lat_lon_model, **options,
                     searchable=True)

        gui.checkBox(
            lat_lon_box, self,
            value="graph.freeze",
            label="Freeze map",
            tooltip="If checked, the map won't change position to fit new data.")

        self.graph.show_internet_error.connect(self._show_internet_error)

    def sizeHint(self):
        return QSize(950, 550)

    def _show_internet_error(self, show):
        if not self.Warning.no_internet.is_shown() and show:
            self.Warning.no_internet()
        elif self.Warning.no_internet.is_shown() and not show:
            self.Warning.no_internet.clear()

    def get_embedding(self):
        self.valid_data = None
        if self.data is None:
            return None

        lat_data = self.get_column(self.attr_lat, filter_valid=False)
        lon_data = self.get_column(self.attr_lon, filter_valid=False)
        if lat_data is None or lon_data is None:
            return None

        self.Warning.missing_coords.clear()
        self.Information.missing_coords.clear()
        self.valid_data = np.isfinite(lat_data) & np.isfinite(lon_data)
        if self.valid_data is not None and not np.all(self.valid_data):
            msg = self.Information if np.any(self.valid_data) else self.Warning
            msg.missing_coords(self.attr_lat.name, self.attr_lon.name)

        in_range = (-MAX_LONGITUDE <= lon_data) & (lon_data <= MAX_LONGITUDE) &\
                   (-MAX_LATITUDE <= lat_data) & (lat_data <= MAX_LATITUDE)
        in_range = ~np.bitwise_xor(in_range, self.valid_data)
        self.Warning.out_of_range.clear()
        if in_range.sum() != len(lon_data):
            self.Warning.out_of_range()
        if in_range.sum() == 0:
            return None
        self.valid_data &= in_range

        x, y = deg2norm(lon_data, lat_data)
        # invert y to increase from bottom to top
        y = 1 - y
        return np.vstack((x, y)).T

    def check_data(self):
        super().check_data()

        if self.data is not None and (len(self.data) == 0 or
                                      len(self.data.domain.variables) == 0):
            self.data = None

    def init_attr_values(self):
        lat, lon = None, None
        if self.data is not None:
            lat, lon = find_lat_lon(self.data, filter_hidden=True)
            if lat is None or lon is None:
                # we either find both or we don't have valid data
                self.Error.no_lat_lon_vars()
                self.data = None
                lat, lon = None, None

        self.lat_lon_model.set_domain(self.data.domain if self.data else None)
        self.attr_lat, self.attr_lon = lat, lon

    @property
    def effective_variables(self):
        return [self.attr_lat, self.attr_lon] \
            if self.attr_lat and self.attr_lon else []

    @property
    def effective_data(self):
        eff_var = self.effective_variables
        if eff_var and self.attr_lat.name == self.attr_lon.name:
            eff_var = [self.attr_lat]
        return self.data.transform(Domain(eff_var))

    def showEvent(self, ev):
        super().showEvent(ev)
        # reset the map on show event since before that we didn't know the
        # right resolution
        self.graph.update_view_range()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        # when resizing we need to constantly reset the map so that new
        # portions are drawn
        self.graph.update_view_range(match_data=False)

    def _point_tooltip(self, point_id, skip_attrs=()):
        point_data = self.data[point_id]
        vars = (self.attr_lat, self.attr_lon)
        text = "<br/>".join(
            escape('{} = {}'.format(var.name, point_data[var]))
            for var in vars if var)
        return text

    def update_tile_provider(self):
        self.graph.update_tile_provider()

    def setup_plot(self):
        pass

    @Inputs.data
    def set_data(self, data):
        self.data = data


if __name__ == "__main__":
    data = Table("/Users/janez/iCloud/STKP-opravljeno/35, 36a - Dom pod Peco - Logarska.gpx")
    WidgetPreview(OWGpxViewer).run(data)
