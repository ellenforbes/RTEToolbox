import arcpy  
from arcpy import env  
env.workspace = r"C:\Projects\RTEToolbox\GDBandMXDforTesting\SurveyQC.gdb"  

#inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey"
  
fields = ["RTEID", "Technology", "LampWatt", "RoadClass"]  
 
for dirpath, dirnames, filenames in arcpy.da.Walk(env.workspace):  
    for filename in filenames:  
        for field in fields:  
            where = field + " IS NULL"  
            try:  
                with arcpy.da.SearchCursor(filename, fields, where) as cursor:  
                    for row in cursor:  
                        print("RTE ID {0}").format(row[0]) + " in " + filename + " has a NULL value in field " + field  
            except RuntimeError:  
                pass  
  
del row, cursor  