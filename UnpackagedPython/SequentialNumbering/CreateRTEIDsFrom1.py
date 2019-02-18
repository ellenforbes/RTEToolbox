inputFeatureClass = "Pickering_ON_20181220_StreetLightSurvey"
rteIDField = "RTE_ID"

codeblock = """rec=0 
def autoIncrement(): 
 global rec 
 pStart = 1  
 pInterval = 1 
 if (rec == 0):  
  rec = pStart  
 else:  
  rec += pInterval  
 return rec"""

arcpy.CalculateField_management(inputFeatureClass, rteIDField, "autoIncrement()" , "PYTHON_9.3", codeblock)
print("Calculated sequential numbers in field starting at 1, 2, 3...")

