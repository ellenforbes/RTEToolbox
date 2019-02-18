import arcpy  
  
latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
  
inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey"
  
inputFeatureClassList = inputFeatureClass.split(";")  
  
for featureClass in inputFeatureClassList:  
 arcpy.AddMessage("Calculating XY coordinates for: " + featureClass)  
 arcpy.AddField_management(featureClass, "LAT", "DOUBLE")  
 arcpy.AddField_management(featureClass, "LON", "DOUBLE")  
 rows = arcpy.UpdateCursor(featureClass, "", latLonRef)  
 for row in rows:  
  feat = row.shape  
  coord = feat.getPart()  
  lon = coord.X  
  lat = coord.Y  
  row.LAT = lat  
  row.LON = lon  
  rows.updateRow(row)  
  #arcpy.AddMessage(str(lat) + ", " + str(lon))  