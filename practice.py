import logging
import arcpy
import yaml
from etl.GSheetsEtl import GSheetsEtl


def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)

    logging.basicConfig(filename=f"{config_dict.get('proj_dir')}wnv.log",
                        filemode='w',
                        level=logging.DEBUG)

    logging.debug('This is a debug statement!')
    logging.info('This will get logged to a file!')
    logging.warning('This is a Warning!')
    logging.error('This is an Error!')

    return config_dict


# Define the ETL.
def etl():
    logging.debug("Starting ETL Method...")
#    print("Start etl process...")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()
    logging.debug("Ending ETL Method!")


# Define the buffer function.
def buffer(layer, dist):
    logging.debug("Starting Buffer Method...")
    units = " feet"
    dist = dist + units
    output_layer = layer + "_buf"

    fc_list = arcpy.ListFeatureClasses()
    for fc in fc_list:
        if output_layer == fc:
            arcpy.Delete_management(fc)
#            print(f"Deleted {fc}")
    arcpy.Buffer_analysis(layer, output_layer, dist, "FULL", "ROUND", "ALL")
#    print("Buffer created " + output_layer)
    logging.debug("Ending Buffer Method!")
    return output_layer


# Define the intersect function.
def intersect(inter_list):
    logging.debug("Starting Intersect Method...")
#    print(inter_list)
    output_layer = input("Please name the intersect layer to be created: ")
    arcpy.Intersect_analysis(inter_list, output_layer)
#    print("Intersect created.")
    logging.debug("Ending Intersect Method!")
    return output_layer


# Define the main function.
def main():
    logging.debug("Starting Main Function...")
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
    aprx = arcpy.mp.ArcGISProject(r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.aprx")
    for map in aprx.listMaps():
        print("Map: " + map.name)
        for lyr in map.listLayers():
            print("- " + lyr.name)

    # Create container for layers.
    layer_list = ["Mosquito_Larval_Sites", "Wetlands_Regulatory", "OSMP_Properties", "Lakes_and_Reservoirs",
                  "avoid_points"]
#    print("These five map layers will be buffered to the extent you choose: ")
#    print(layer_list)

    # Define workspace.
    resultsgeodatabase = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb\\"
    arcpy.env.workspace = resultsgeodatabase

    featureclass = arcpy.ListFeatureClasses()
#    print(arcpy.ListFeatureClasses())
    logging.debug("Ending Main Method!")

    for layer in layer_list:
        print(layer)

        # Ask user for buffer distance input.
        dist = input("Please type in a buffer distance between 1000-5000 feet: ")
        bufferlayer = buffer(layer, dist)

    featureclass = arcpy.ListFeatureClasses()
#    print(arcpy.ListFeatureClasses())

    inter_list = ["Mosquito_Larval_Sites_buf", "Wetlands_Regulatory_buf", "OSMP_Properties_buf",
                  "Lakes_and_Reservoirs_buf"]
    output_intersectlayer = intersect(inter_list)

    target_features = "Boulder_addresses"
    join_features = output_intersectlayer
    out_feature_class = "spatial_join"

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
    print("Spatial join layer created.")

    target_features = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb\spatial_join"
    erase_features = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb\avoid_points_buf"
    out_feature_class = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb" \
                        r"\output_final_analysis "

    arcpy.Erase_analysis(target_features, erase_features, out_feature_class)
    print("Erase layer created.")
    print("Have a great day!")


if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()

main()
