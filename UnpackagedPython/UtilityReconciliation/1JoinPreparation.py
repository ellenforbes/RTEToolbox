inputFCSurveyRTE = "Cityname_SP_YYYYMMDD_Survey"
inputFCUtility = "TestUtilityData"

fieldRTEStreetName = "StreetName"
fieldRTEPoleID = "UtlPoleID"
fieldRTEWattage = "LampWatt"

fieldUtilityStreetName = "StreetName"
fieldUtilityPoleID = "PoleID"
fieldUtilityWattage = "Wattage"

arcpy.AddField_management(inputFCSurveyRTE, "TempForJoin", "Text", "", "", "100", "Temp For Join","NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(inputFCUtility, "TempForJoin", "Text", "", "", "100", "Temp For Join","NULLABLE", "NON_REQUIRED", "")

expressionRTE = "!" + fieldRTEStreetName + "! + ' ' + str(!" + fieldRTEPoleID + "!) + ' ' + str(!" + fieldRTEWattage + "!)"

print(expression)

arcpy.CalculateField_management(inputFCSurveyRTE, "TempForJoin", expressionRTE, "PYTHON_9.3")

expressionUtility = "!" + fieldUtilityStreetName + "! + ' ' + str(!" + fieldUtilityPoleID + "!) + ' ' + str(!" + fieldUtilityWattage + "!)"

print(expression)

