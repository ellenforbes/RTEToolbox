inputFeatureClass = "Cityname_SP_YYYYMMDD"
rteIDField = "RTEID"
startingNumber = "100"
intervalNumber = "2"

codeblock = """
rec=0 
def autoIncrement(): 
 global rec 
 pStart = """ + startingNumber + """  
 pInterval = """ + intervalNumber + """ 
 if (rec == 0):  
  rec = pStart  
 else:  
  rec += pInterval  
 return rec"""

arcpy.CalculateField_management(inputFeatureClass, rteIDField, "autoIncrement()" , "PYTHON_9.3", codeblock)
print("Calculated sequential numbers in field with user defined values")

