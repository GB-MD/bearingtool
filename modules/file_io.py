
import yaml
import pandas as pd


def load_data(file_name: str) -> tuple[pd.DataFrame]:
    loc_df = pd.read_excel(file_name, sheet_name=0)
    route_df = pd.read_excel(file_name, sheet_name=1)

    return loc_df, route_df

def write_data(df: pd.DataFrame) -> None:
    df.to_excel("results.xlsx", index=False)

def configLoader() -> dict:
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config
    


#Importing from LVNL if ever necessary
# import json

# url = 'https://services-eu1.arcgis.com/OtUwzhpKSdeXgRIB/arcgis/rest/services/Waypoints_data/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson'
# data = requests.get(url).json()

# with open("NL_WPTS.geojson", "w") as f:
#     json.dump(data,f)

# d = {}
# for entry in data['features']:
#     d[entry['properties']['Designator']] = tuple(entry['geometry']['coordinates'])