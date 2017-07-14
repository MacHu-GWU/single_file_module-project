#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import random
from sfm.geo_search import GeoSearchEngine


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
        (i + 1, lat + 5.0 * random.uniform(-1, 1),
         lng + 5.0 * random.uniform(-1, 1))
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

    n_nearest = search_engine.find_n_nearest(lat, lng, n=50, radius=20.0)
    dist_array = list()
    for dist, point in n_nearest:
        dist_array.append(dist)
        assert dist <= 50.0

    assert_is_all_ascending(dist_array)


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
