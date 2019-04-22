# -*- coding: utf-8 -*-

"""
n nearest 2D sphere search implementation.
"""

import heapq
from math import radians, cos, sin, asin, sqrt
from sqlalchemy import create_engine, MetaData, Table, Column, Index
from sqlalchemy import String, Float, PickleType
from sqlalchemy import select, and_


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
        """
        Feed data into database.

        :type data: list
        :param data: list of point object, can have other metadata, for example:
            [{"id": 10001, "lat": xxx, "lng": xxx}, ...]

        :type key_id: callable
        :param key_id: callable function, take point object as input, return object
            id, for example: lambda x: x["id"]

        :type key_lat: callable
        :param key_lat: callable function, take point object as input, return object
            latitude, for example: lambda x: x["lat"]

        :type key_lng: callable
        :param key_lng: callable function, take point object as input, return object
            longitude, for example: lambda x: x["lng"]
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
