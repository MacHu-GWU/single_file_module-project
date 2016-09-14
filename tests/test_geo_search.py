#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sfm.geo_search import GeoSearchEngine


def test_geo_search():
    point_data = [
        (1, 38.42522236, -93.29622264),
        (2, 40.22483194, -92.37676291),
        (3, 39.71873925, -91.76397842),
    ]
    
    search_engine = GeoSearchEngine()
    search_engine.train(point_data,
        key_id=lambda x: x[0],
        key_lat=lambda x: x[1],
        key_lng=lambda x: x[2],
    )

    def test_find_n_nearest():
        n_nearest = search_engine.find_n_nearest(39.0, -92.0, n=1)
        assert len(n_nearest) == 1
        
        n_nearest = search_engine.find_n_nearest(39.0, -92.0, radius=60.0)
        for dist, point in n_nearest:
            assert dist <= 60.0
        
        n_nearest = search_engine.find_n_nearest(39.0, -92.0)
        assert len(n_nearest) == len(point_data)
        last_dist = -1.0
        for dist, point in n_nearest:
            assert last_dist <= dist
            last_dist = dist

    test_find_n_nearest()
    

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])