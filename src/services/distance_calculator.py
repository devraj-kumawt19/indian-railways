import math
from typing import List, Dict


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def calculate_engine_distance(engine: Dict, coaches: List[Dict]) -> float:
    """
    Calculate linear distance in metres between engine and the last coach end.
    engine: {'lat': float, 'lon': float}
    coaches: list of {'length_m': float, 'offset': float, 'lat': float, 'lon': float}
    If coaches provide lat/lon, prefer those; otherwise compute based on engine and cumulative lengths along same bearing.
    """
    if not coaches:
        raise ValueError('Coaches list empty')

    eng_lat = float(engine.get('lat'))
    eng_lon = float(engine.get('lon'))

    # if last coach has coordinates, compute distance directly
    last = coaches[-1]
    if 'lat' in last and 'lon' in last:
        return _haversine(eng_lat, eng_lon, float(last['lat']), float(last['lon']))

    # otherwise approximate by cumulative length along straight line for simple use-case
    total_length = 0.0
    for c in coaches:
        total_length += float(c.get('length_m', 0.0))

    # return total_length as straight-line approximation (meters)
    return total_length
