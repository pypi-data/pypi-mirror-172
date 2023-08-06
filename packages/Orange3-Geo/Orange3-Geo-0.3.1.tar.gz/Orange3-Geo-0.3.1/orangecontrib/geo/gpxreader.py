import gpxpy

import numpy as np

from Orange.data import FileFormat, ContinuousVariable, Table, Domain, \
    TimeVariable
from Orange.widgets.data.owfile import OWFile
from orangewidget.utils.widgetpreview import WidgetPreview


class GpxReader(FileFormat):
    """Reader for basket (sparse) files"""
    EXTENSIONS = ('.gpx', )
    DESCRIPTION = 'GPS Exchange Format'

    def read(self):
        attrs = (ContinuousVariable("track", number_of_decimals=0),
                 ContinuousVariable("segment", number_of_decimals=0),
                 ContinuousVariable("latitude", number_of_decimals=7),
                 ContinuousVariable("longitude", number_of_decimals=7),
                 ContinuousVariable("elevation", number_of_decimals=1),
                 TimeVariable("time", have_time=True, have_date=True))

        gpx_file = open(self.filename)
        gpx = gpxpy.parse(gpx_file)
        x = np.empty(
            (sum(len(seg.points)
                 for track in gpx.tracks
                 for seg in track.segments),
             len(attrs)), dtype=float)
        idx = 0
        for trkid, track in enumerate(gpx.tracks):
            for segid, segment in enumerate(track.segments):
                for ptid, point in enumerate(segment.points, start=idx):
                    x[ptid] = (trkid, segid,
                               point.latitude, point.longitude, point.elevation,
                               point.time.timestamp())
                idx += len(segment.points)

        if np.all(x[:, 1] == 0):
            x = np.hstack((x[:, :1], x[:, 2:]))
            attrs = attrs[:1] + attrs[2:]
        if np.all(x[:, 0] == 0):
            x = x[:, 1:]
            attrs = attrs[1:]
        return Table.from_numpy(Domain(attrs), x)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWFile).run()
