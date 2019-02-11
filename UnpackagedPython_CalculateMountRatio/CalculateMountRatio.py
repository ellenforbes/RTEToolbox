inputFeatureClass = "Cityname_SP_YYYYMMDD_Design"
fieldRoadWidth = "RoadWidth"
calcMR = "(!" + fieldRoadWidth + "!+!Setback!-!ArmLength!)/float(!LampHeight!)"
arcpy.CalculateField_management(inputFeatureClass, "MountRatio", calcMR, "PYTHON_9.3") 