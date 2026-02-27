from modules.file_io import load_data, write_data, configLoader
from modules.utils import aggMeasurements
from dotenv import load_dotenv

def main() -> None:
    load_dotenv()
    config = configLoader()
    loc_df, route_df = load_data(config['file_name'])
    results = aggMeasurements(config, loc_df, route_df)
    write_data(results)
    
if __name__ == "__main__":
    main()