import arcpy

inputFCSurveyRTE = "Cityname_SP_YYYYMMDD_Survey"
inputFCUtility = "ClientData"

arcpy.AddJoin_management (inputFCUtility, "TempForJoin", inputFCSurveyRTE, "TempForJoin", "KEEP_ALL")

matchQuery = inputFCSurveyRTE + ".TempForJoin IS NOT NULL"
print(matchQuery)
arcpy.SelectLayerByAttribute_management(inputFCUtility,"NEW_SELECTION",matchQuery)

arcpy.CalculateField_management(inputFCUtility,inputFCUtility+".EMatch","\"Match\"","PYTHON_9.3")
arcpy.CalculateField_management(inputFCUtility,inputFCUtility+".TempUpdateX","!" + inputFCSurveyRTE + ".TempUpdateX!","PYTHON_9.3")
arcpy.CalculateField_management(inputFCUtility,inputFCUtility+".TempUpdateY","!" + inputFCSurveyRTE + ".TempUpdateY!","PYTHON_9.3")

arcpy.RemoveJoin_management (inputFCUtility)

arcpy.SelectLayerByAttribute_management(inputFCUtility,"NEW_SELECTION","EMatch = 'Match'")

codeblock = """
def Update(shape, newX, newY):
    pnt = shape.getPart(0)
    pnt.X = newX
    pnt.Y = newY
    return pnt
"""
arcpy.CalculateField_management(inputFCUtility, "Shape", "Update (!Shape!, !TempUpdateX!, !TempUpdateY!)" , "PYTHON_9.3", codeblock)