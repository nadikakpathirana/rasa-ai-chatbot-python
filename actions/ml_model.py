import time

import osmnx as ox


def get_slots_using_location(place_name):
    # place_name = "Ottawa, Ontario, Canada"

    tags = {
        'leisure': ['swimming_pool', 'swimming_area', 'track'],  # swimming_places, walking_paths
        'sport': ['swimming', 'running'],  # swimming_places, walking_paths
        'highway': 'footway',  # walking_paths
        'footway': 'sidewalk',  # walking_paths
        # 'route': ['foot', 'running'] # walking_paths
        # 'route': True
    }

    places = ox.geometries_from_address(place_name, tags=tags, dist=10000)
    places.head()
    print(places.head())

    # collect swim info
    swimming_places_found = False
    try:
        length = len(places[(places['leisure'] == 'swimming_pool')])
        if length > 0:
            swimming_places_found = True
    except:
        pass

    try:
        if not swimming_places_found:
            length = len(places[(places['leisure'] == 'swimming_area')])
            if length > 0:
                swimming_places_found = True
    except:
        pass

    try:
        if not swimming_places_found:
            length = len(places[(places['sport'] == 'swimming')])
            if length > 0:
                swimming_places_found = True
    except:
        pass

    # collect walking info
    walking_paths_found = False
    try:
        length = len(places[(places['leisure'] == 'track')])
        if length > 0:
            walking_paths_found = True
    except:
        pass

    try:
        if not walking_paths_found:
            length = len(places[(places['highway'] == 'footway')])
            if length > 0:
                walking_paths_found = True
    except:
        pass

    try:
        if not walking_paths_found:
            length = len(places[(places['route'] == 'foot')])
            if length > 0:
                walking_paths_found = True
    except:
        pass

    try:
        if not walking_paths_found:
            length = len(places[(places['route'] == 'running')])
            if length > 0:
                walking_paths_found = True
    except:
        pass

    try:
        if not walking_paths_found:
            length = len(places[(places['leisure'] == 'running')])
            if length > 0:
                walking_paths_found = True
    except:
        pass

    try:
        if not walking_paths_found:
            length = len(places[(places['sport'] == 'running')])
            if length > 0:
                walking_paths_found = True
    except:
        pass

    return swimming_places_found, walking_paths_found


# if "__main__" == __name__:
#     print("started")
#     start_time = time.time()
#     fill_slots_using_location("Victoria, British Columbia")
#     end_time = time.time()
#     print(str(end_time - start_time) + "seconds")

