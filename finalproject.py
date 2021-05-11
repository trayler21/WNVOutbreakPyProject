import logging
import arcpy
import yaml
from etl.GSheetsEtl import GSheetsEtl


# Define the setup, complete with logging messaging capabilities.
def setup():
    """
    The setup will contain all logging messages explained and defined, and use the config_dict.get method rather
    than a hard-coded path.
    """
    try:
        with open('config/wnvoutbreak.yaml') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)

        logging.basicConfig(filename=f"{config_dict.get('proj_dir')}wnv.log",
                            filemode='w', level=logging.DEBUG)

        logging.debug('This is a debug statement!')
        logging.info('This will get logged to a file!')
        logging.warning('This is a Warning!')
        logging.error('This is an Error!')
        return config_dict
    except Exception as e:
        print(f"Error in setup! {e}")


# Define the ETL.
def etl():
    """
    The ETL method involves extracting the data from where you want it from, transforming it in some way to
    complement or improve the data, and loading it into the desired location.
    :return:
    """
    try:
        logging.debug("Starting ETL Method...")
        etl_instance = GSheetsEtl(config_dict)
        etl_instance.process()
        logging.debug("Ending ETL Method!")
    except Exception as e:
        print(f"Error in etl! {e}")


# Define the buffer function.
def buffer(layer, dist):
    """
    The buffer method will produce buffer parameters for all original layers within the map. This method will also
    provide the ability to delete pre-existing layers in order to keep the project orderly and succinct.
    :param layer: all map layers
    :param dist: 1500 feet
    :return:
    """
    try:
        logging.debug("Starting Buffer Method...")
        units = " feet"
        dist = dist + units
        output_layer = layer + "_buf"
        fc_list = arcpy.ListFeatureClasses()
        for fc in fc_list:
            if output_layer == fc:
                arcpy.Delete_management(fc)
        arcpy.Buffer_analysis(layer, output_layer, dist, "FULL", "ROUND", "ALL")
        logging.debug("Ending Buffer Method!")
        return output_layer
    except Exception as e:
        print(f"Error in buffer! {e}")


# Define the intersect function.
def intersect(inter_list):
    """
    The intersect method will run an intersect tool in order to create a layer that reveals the areas of
    highest risk of West Nile Virus exposure.
    :param inter_list:
    :return: output_layer
    """
    try:
        logging.debug("Starting Intersect Method...")
        output_layer = input("Please name the intersect layer to be created: ")
        arcpy.Intersect_analysis(inter_list, output_layer)
        print("Intersect layer created.")
        logging.debug("Ending Intersect Method!")
        return output_layer
    except Exception as e:
        print(f"Error in intersect! {e}")


# Define the main function.
def main():
    """
    This main method creates a basic container for the layers to be used throughout the project,
    uses the config_dict.get tool to steer the code to the project directory, and defines the workspace.
    :return:
    """
    try:
        logging.debug("Starting West Nile Virus Simulation...")
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
        aprx = arcpy.mp.ArcGISProject(r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak"
                                      r"\WestNileOutbreak.aprx")
        for map in aprx.listMaps():
            print("Map: " + map.name)
            for lyr in map.listLayers():
                print("- " + lyr.name)
        logging.debug("Ending West Nile Virus Simulation!")
    except Exception as e:
        print(f"Error in main! {e}")

    # Create container for layers.
    layer_list = ["Mosquito_Larval_Sites", "Wetlands_Regulatory", "OSMP_Properties", "Lakes_and_Reservoirs",
                  "avoid_points"]

    # Define workspace.
    resultsgeodatabase = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb\\"
    arcpy.env.workspace = resultsgeodatabase

    for layer in layer_list:
        print(layer)

        # Ask user for buffer distance input.
        dist = input("Please type in a buffer distance between 1000-5000 feet: ")
        buffer_layer = buffer(layer, dist)

    feature_class = arcpy.ListFeatureClasses()

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
                        r"\output_final_analysis"

    arcpy.Erase_analysis(target_features, erase_features, out_feature_class)
    print("Erase layer created.")


# Define and set the spatial reference.
def set_spatial_reference(aprx):
    """
    The spatial reference method will allow the program to set the project and it's map to the
    spatial reference of choice, in this case, the NAD 1983 State Plane Colorado North projected coordinate system.
    :param aprx: ArcPRO project object
    :return: projection as defined
    """
    try:
        logging.debug("Starting set_spatial_reference Method...")
        map_doc = aprx.listMaps()[0]
        # https://www.spatialreference.org/ref/esri/102653/
        state_plane_noco = arcpy.SpatialReference(102653)
        map_doc.spatialReference = state_plane_noco
        logging.debug("Ending set-spatial_reference Method!")
    except Exception as e:
        print(f"Error in set_spatial_reference! {e}")


# Define the export map call.
def export_map(aprx):
    """
    The export map method allows the program to export the map, including requesting user input in
    order to add a subtitle to the map title.
    :return: export
    """
    try:
        lyt = aprx.listLayouts()[0]
        subtitle = input("Please provide a subtitle for the West Nile Virus Outbreak map: ")
        for el in lyt.listElements():
            print(el.name)
            if "Title" in el.name:
                el.text = el.text + subtitle
    except Exception as e:
        print(f"Error in export_map! {e}")


#  Set up target addresses layer.
def target_addresses(aprx):
    """
    This targets the addresses within the Boulder residential addresses layer that are due to receive
    spraying services for mosquito virus mitigation.
    :return:
    """
    try:
        target_features = "Boulder_addresses"
        join_features = "spatial_join"
        out_feature_class = "Target_addresses"
        arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
        print("Target addresses layer created.")
        logging.debug("Ending West Nile Virus Simulation!")
    except Exception as e:
        print(f"Error in main! {e}")

        map_doc = aprx.listMaps()[0]
        lyr = map_doc.listLayers("output_final_analysis")[0]

# Get the existing symbology.
        sym = lyr.symbology
# Set symbology for output_final_analysis layer.
        sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
        sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
        lyr.symbology = sym
        lyr.transparency = 50
        aprx.save()
# def render(output_final_analysis):


if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)

    etl()

    set_spatial_reference(arcpy.mp.ArcGISProject)

    target_addresses(arcpy.mp.ArcGISProject)

    export_map(arcpy.mp.ArcGISProject)

    main()
