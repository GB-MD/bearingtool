import requests
import time
import os
import pandas as pd
from pyproj import Geod
from pygeodesy import toDMS, parseDMS

def getDeclination(config: dict, lon: float, lat: float) -> float:
    model = config['model']
    assert model in ["WMM", "WMMHR", "IGRF"], "Specified model is not supported"

    time.sleep(1)

    year, month, day = config['year'], config['month'], config['day']
    url = os.getenv("NOAA_URL")
    payload = {
        'key': os.getenv("NOAA_API_KEY"), 'lat1': str(lat), 'lon1': str(lon),
        'startYear': str(year), 'startMonth': str(month), 'startDay': str(day),
        'model': model, 'resultFormat': 'json'
        }

    data = requests.get(url, params = payload).json()
    return data["result"][0]["declination"]

def aggMeasurements(config: dict, loc_df: pd.DataFrame, route_df: pd.DataFrame) -> pd.DataFrame:
    geom = []

    if config['arp']['used']:
        arp_loc = config['arp']['arp_loc']
        arp_loc = [parseDMS(i) if not is_float(i) else i for i in arp_loc]
        in_arp = checkRadiusARP(config, arp_loc, loc_df)

    for _, row in route_df.iterrows():
        start = row["From"]
        end = row["To"]

        loc1 = loc_df.loc[loc_df["Name"] == start, ["Latitude", "Longitude"]].values.tolist()[0]
        loc2 = loc_df.loc[loc_df["Name"] == end, ["Latitude", "Longitude"]].values.tolist()[0]

        loc1 = [parseDMS(i) if not is_float(i) else i for i in loc1]
        loc2 = [parseDMS(i) if not is_float(i) else i for i in loc2]

        entry = getDirections(config, loc1, loc2, arp = arp_loc) if end in in_arp else getDirections(config, loc1, loc2)

        geom.append([start, end] + entry)
        

    df = pd.DataFrame(geom, columns=["From", "To", "In ARP?", "Dist [km]", "Dist [nm]",
                                      "True Azi [dd]", "True Azi [DMS]", "Mag Decl [dd]",
                                        "Mag Azi [dd]", "Mag Azi [DMS]"])
    
    return df

#Checks which waypoints are within the ARP radius of 25nm
def checkRadiusARP(config: dict, arp_loc: list[float], loc_df: pd.DataFrame, ref = "WGS84") -> set[str]:
    g = Geod(ellps=ref)
    lat1, lon1 = arp_loc[0], arp_loc[1]

    s = set()
    for _, row in loc_df.iterrows():
        
        loc2 = [row["Latitude"], row["Longitude"]]
        loc2 = [parseDMS(i) if not is_float(i) else i for i in loc2]
        lat2, lon2 = loc2[0], loc2[1]

        _, _, dist = g.inv(lon1, lat1, lon2, lat2)

        if dist/(1852) < config['arp']['arp_radius']:
            s.add(row["Name"])

    return s

#All in decimal degrees
def getDirections(config: dict, loc1: list[float], loc2: list[float], 
                  ref = "WGS84", arp = []) -> tuple[float, str]:
    g = Geod(ellps=ref)

    lat1, lon1 = loc1[0], loc1[1]
    lat2, lon2 = loc2[0], loc2[1]

    azi12, _, dist = g.inv(lon1, lat1, lon2, lat2)

    #Bearings between [0, 360]
    if azi12 < 0:
        azi12 += 360

    decl12 = config['arp']['arp_decl'] if arp else getDeclination(config, lon2, lat2)

    if arp:
        return [True, dist/1000, dist/(1852), azi12, toDMS(azi12), decl12, azi12 + decl12, toDMS(azi12 + decl12)]
    
    else:
        return [False, dist/1000, dist/(1852), azi12, toDMS(azi12), decl12, azi12 + decl12, toDMS(azi12 + decl12)]

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
        
    except (ValueError, TypeError):
        return False
    