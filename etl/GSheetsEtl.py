import arcpy
import requests
import csv
from etl.SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    """
    GSheetsEtl performs an Extract, Transform, and Load, or ETL, defined from the SpatialETL.py file, to
    process using an URL to a Google spreadsheet.
    The spreadsheet must contain an address and zip code column.

    Parameters:
    config_dict (dictionary): A dictionary containing a remote_url key to the Google
    spreadsheet and web geocoding service.
    """
    # A dictionary of configuration keys and values.
    config_dict = None

    def __init__(self, config_dict):
        """
        A configuration dictionary can be incredibly useful in programming. It allows use of a
        short-cut of sorts, rather than requiring the input of complex and often long paths.
        :param config_dict:
        """
        super().__init__(config_dict)

    def extract(self):
        """
        Extracting data from a Google spreadsheet to transform it and save it to a local file.
        :return:
        """
        print("Extracting addresses from Google form spreadsheet...")

        r = requests.get(self.config_dict.get('remote_url'))
        r.encoding = "utf-8"
        data = r.text
        with open(f"{self.config_dict.get('proj_dir')}Boulder_addresses.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        """
        Transforming the extracted data by performing some task(s) in order to clean up, standardize, verify, sort,
        or otherwise change to improve data quality or function.
        :return:
        """
        print("Add City, State")

        transformed_file = open(f"{self.config_dict.get('proj_dir')}new_addresses.csv", "w")
        transformed_file.write("X,Y,Type\n")
        with open(f"{self.config_dict.get('proj_dir')}Boulder_addresses.csv", "r") as partial_file:
            csv_dict = csv.DictReader(partial_file, delimiter=',')
            for row in csv_dict:
                address = row["Street Address"] + " Boulder CO"
                print(address)
                geocode_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + address\
                              + "&benchmark=2020&format=json"
                print(geocode_url)
                r = requests.get(geocode_url)

                resp_dict = r.json()
                x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                transformed_file.write(f"{x},{y},Residential\n")
        transformed_file.close()

    def load(self):
        """
        Loading provides the destination for the transformed data and stores it as defined by the program.
        :return:
        """

        # Description: Creates a point feature class from input table
        # Set environment settings
        arcpy.env.workspace = f"{self.config_dict.get('proj_dir')}WestNileOutbreak.gdb"
        arcpy.env.overwriteOutput = True

        # Set the local variables
        in_table = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdbnew_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"

        # Make the XY event layer...
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

        # Print the total rows
        print(arcpy.GetCount_management(out_feature_class))

    def process(self):
        """
        The process definition uses the self parameter in order to point to each individual tool. GSheetsEtl.py is
        referring to SpatialEtl.py, which is described by importing the SpatialEtl.py file by this file.
        :return:
        """
        self.extract()
        self.transform()
        self.load()
