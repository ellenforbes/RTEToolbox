import arcpy  
  
latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
  
inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey" 

rows = arcpy.UpdateCursor(inputFeatureClass, "", latLonRef)  
for row in rows:  
  feat = row.shape  
  coord = feat.getPart()  
  lon = coord.X  
  lat = coord.Y  
  row.PointY = lat  
  row.PointX = lon  
  rows.updateRow(row)  

arcpy.AddMessage(str(lat) + ", " + str(lon))  