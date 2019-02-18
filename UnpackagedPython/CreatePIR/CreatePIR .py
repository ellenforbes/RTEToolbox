#Define variables
inputFeatureClass = "Scugog_ON_SL_20180211_UTM17N"
statusField = "Status"
installDateField = "EditDate"
fromDate =  "2018-09-05 00:00:00"
toDate =  "2018-09-05 23:59:59"
outputExcel = "C:\\Users\\ekitteridge\\Desktop\\test.xls"

# Build queries to select only installed lights and to define that selection between dates
defQueryInstallation = statusField + " = 'Installed'"
defQueryDate = installDateField + " > date '" + fromDate + "' AND " + installDateField + " < date '" + toDate + "'"
print (defQueryInstallation)
print (defQueryDate)

# Run selections on the field containing the install information and the field containing the install date
queryInstallation = defQueryInstallation
arcpy.SelectLayerByAttribute_management(inputFeatureClass, "NEW_SELECTION", queryInstallation)
queryDate = defQueryDate
arcpy.SelectLayerByAttribute_management(inputFeatureClass, "SUBSET_SELECTION", queryDate)

# Convert the selection on table to Excel
arcpy.TableToExcel_conversion(inputFeatureClass, outputExcel)