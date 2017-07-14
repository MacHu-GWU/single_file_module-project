#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heapq
from math import radians, cos, sin, asin, sqrt
from sqlalchemy import create_engine, MetaData, Table, Column, Index
from sqlalchemy import String, Float, PickleType
from sqlalchemy import select, and_, func


AVG_EARTH_RADIUS = 6371  # in km


def great_circle(point1, point2, miles=True):
    """ Calculate the great-circle distance bewteen two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: great_circle((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = list(map(radians, [lat1, lng1, lat2, lng2]))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng / 2) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers


class GeoSearchEngine(object):
    def __init__(self, name="point", database=":memory:"):
        self.engine = create_engine("sqlite:///%s" % database)
        self.metadata = MetaData()
        self.t_point = Table(name, self.metadata,
                             Column("id", String),
                             Column("lat", Float),
                             Column("lng", Float),
                             Column("data", PickleType),
                             )

    def train(self, data, key_id, key_lat, key_lng, clear_old=True):
        """Feed data into database.
        """
        engine, t_point = self.engine, self.t_point
        if clear_old:
            try:
                t_point.drop(engine)
            except:
                pass
        t_point.create(engine)

        table_data = list()
        for record in data:
            id = key_id(record)
            lat = key_lat(record)
            lng = key_lng(record)
            row = {"id": id, "lat": lat, "lng": lng, "data": record}
            table_data.append(row)

        ins = t_point.insert()
        engine.execute(ins, table_data)

        index = Index('idx_lat_lng', t_point.c.lat, t_point.c.lng)
        index.create(engine)

    def find_n_nearest(self, lat, lng, n=5, radius=None):
        """Find n nearest point within certain distance from a point.

        :param lat: latitude of center point.
        :param lng: longitude of center point. 
        :param n: max number of record to return.
        :param radius: only search point within ``radius`` distance.

        **中文文档**
        """
        engine, t_point = self.engine, self.t_point
        if radius:
            # Use a simple box filter to minimize candidates
            # Define latitude longitude boundary
            dist_btwn_lat_deg = 69.172
            dist_btwn_lon_deg = cos(lat) * 69.172
            lat_degr_rad = abs(radius * 1.05 / dist_btwn_lat_deg)
            lon_degr_rad = abs(radius * 1.05 / dist_btwn_lon_deg)

            lat_lower = lat - lat_degr_rad
            lat_upper = lat + lat_degr_rad
            lng_lower = lng - lon_degr_rad
            lng_upper = lng + lon_degr_rad

            filters = [
                t_point.c.lat >= lat_lower,
                t_point.c.lat <= lat_upper,
                t_point.c.lat >= lng_lower,
                t_point.c.lat >= lng_upper,
            ]
        else:
            radius = 999999.9
            filters = []

        s = select([t_point]).where(and_(*filters))

        heap = list()
        for row in engine.execute(s):
            dist = great_circle((lat, lng), (row.lat, row.lng))
            if dist <= radius:
                heap.append((dist, row.data))

        # Use heap sort to find top-K nearest
        n_nearest = heapq.nsmallest(n, heap, key=lambda x: x[0])
        return n_nearest


#--- Unittest ---
if __name__ == "__main__":
    import random

    def assert_is_all_ascending(array):
        """Assert that this is a strictly asceding array.
        """
        for i, j in zip(array[1:], array[:-1]):
            if (i is not None) and (j is not None):
                assert i >= j

    def assert_is_all_descending(array):
        """Assert that this is a strictly desceding array.
        """
        for i, j in zip(array[1:], array[:-1]):
            if (i is not None) and (j is not None):
                assert i <= j

    def test_geo_search():
        lat, lng = 39.096793, -94.579978
        point_data = [
            (i + 1, lat + 2.0 * random.uniform(-1, 1),
             lng + 2.0 * random.uniform(-1, 1))
            for i in range(1000)
        ]

        search_engine = GeoSearchEngine()
        search_engine.train(point_data,
                            key_id=lambda x: x[0],
                            key_lat=lambda x: x[1],
                            key_lng=lambda x: x[2],
                            )

        n_nearest = search_engine.find_n_nearest(lat, lng, n=1)
        assert len(n_nearest) == 1

        n_nearest = search_engine.find_n_nearest(lat, lng, n=5, radius=50.0)
        dist_array = list()
        for dist, point in n_nearest:
            dist_array.append(dist)
            assert dist <= 50.0

        assert_is_all_ascending(dist_array)

    test_geo_search()
