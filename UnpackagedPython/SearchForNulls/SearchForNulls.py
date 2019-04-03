import arcpy  
import csv

inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey"
fields = ["RTEID", "Technology", "LampWatt", "RoadClass"]  
outfile = r"C:\Projects\GIS_Data_Inventory.txt"
 
for filenames in arcpy.da.Walk(inputFeatureClass): 
    for filename in filenames:
        for field in fields:  
            where = field + " IS NULL"  
            try:  
                with arcpy.da.SearchCursor(filename, fields, where) as cursor:  
                    for row in cursor:  
                        print("RTE ID {0}").format(row[0]) + " has a NULL value in field " + field 
                        with open('outfile.txt', 'w') as outfile:
                            print >>outfile, ("RTE ID {0}").format(row[0]) + " has a NULL value in field " + field  
            except RuntimeError:  
                pass  

del row, cursor  


featureClass = "Longmeadow_MA_20190311_Survey"
fields = ["RTEID", "Technology", "LampWatt", "RoadClass"]
for field in fields:  
    cursor = arcpy.SearchCursor(featureClass)
    for row in cursor:
        cell = row.getValue(field)
        if cell == None:
            print(row["RTEID"])