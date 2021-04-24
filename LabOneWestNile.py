import arcpy


# Define the buffer function.
def buffer(layer, dist):
    units = " feet"
    dist = dist + units
    output_layer = layer + "_buf"

    fc_list = arcpy.ListFeatureClasses()
    for fc in fc_list:
        if output_layer == fc:
            arcpy.Delete_management(fc)
            print(f"Deleted {fc}")

    arcpy.Buffer_analysis(layer, output_layer, dist, "FULL", "ROUND", "ALL")
    print("Buffer created " + output_layer)
    return output_layer


# Define the intersect function.
def intersect(inter_list):
    print(inter_list)
    output_layer = input("Please name the intersect layer to be created: ")
    arcpy.Intersect_analysis(inter_list, output_layer)
    print("Intersect created.")
    return output_layer


# Define the main function.
def main():
    aprx = arcpy.mp.ArcGISProject(r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.aprx")
    for map in aprx.listMaps():
        print("Map: " + map.name)
        for lyr in map.listLayers():
            print("- " + lyr.name)

    # Create container for layers.
    layer_list = ["Mosquito_Larval_Sites", "Wetlands_Regulatory", "OSMP_Properties", "Lakes_and_Reservoirs"]
    print("These four map layers will be buffered to the extent you choose: ")
    print(layer_list)

    # Define workspace.
    resultsgeodatabase = r"C:\Users\Owner\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb\\"
    arcpy.env.workspace = resultsgeodatabase

    featureclass = arcpy.ListFeatureClasses()
    print(arcpy.ListFeatureClasses())

    for layer in layer_list:
        print(layer)

        # Ask user for buffer distance input.
        dist = input("Please type in a buffer distance between 1000-5000 feet: ")
        bufferlayer = buffer(layer, dist)

    featureclass = arcpy.ListFeatureClasses()
    print(arcpy.ListFeatureClasses())
    inter_list = ["Mosquito_Larval_Sites_buf", "Wetlands_Regulatory_buf", "OSMP_Properties_buf",
                  "Lakes_and_Reservoirs_buf"]
    output_intersectlayer = intersect(inter_list)

    target_features = "Boulder_addresses"
    join_features = output_intersectlayer
    out_feature_class = "spatial_join"

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
    print("Spatial join layer created.")

#    qry = "3,244"
#    arcpy.management.SelectLayerByAttribute("spatial_join", "New_Selection", qry)
#    print(f"There are " + qry + " addresses within the danger zone!")


main()
