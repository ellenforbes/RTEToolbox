import arcpy  
from arcpy import env #not necessary if I can fix line 9
env.workspace = r"C:\Projects\RTEToolbox\GDBandMXDforTesting\SurveyQC.gdb"  #not necessary if I can fix line 9

#inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey"
  
fields = ["RTEID", "Technology", "LampWatt", "RoadClass"]  
 
for dirpath, dirnames, filenames in arcpy.da.Walk(env.workspace):  # I don't want it ot look in the whole work space but just in inputFeatureClass
    for filename in filenames:  # This therefore should not be necessary
        for field in fields:  
            where = field + " IS NULL"  
            try:  
                with arcpy.da.SearchCursor(filename, fields, where) as cursor:  
                    for row in cursor:  
                        print("RTE ID {0}").format(row[0]) + " in " + filename + " has a NULL value in field " + field  
            except RuntimeError:  
                pass  
  
del row, cursor  