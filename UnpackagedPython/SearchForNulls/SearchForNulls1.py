def createNewOrEmptyExistingFile(newFile):
    fileAlreadyExists = os.path.isfile(newFile)
    if fileAlreadyExists:
        os.remove(newFile)
    open(newFile, "w+")

inputFeatureClass = parameters[0].valueAsText


folderPath = "C:\\Users\\ekitteridge\\Desktop"
name = "\\NullsFound" + str(date.today().strftime("%Y%m%d")) + ".csv"
arcpy.AddMessage(name)
output = folderPath + name
arcpy.AddMessage(output)
createNewOrEmptyExistingFile(output)

arcpy.SelectLayerByLocation_management (inputFeatureClass,"WITHIN", boundary, "", "NEW_SELECTION", "INVERT")

with open(output, 'w', newline='') as ofile:
    writer = csv.writer(ofile)
    header = "RTE ID", "Luminaire Type", "Issue"
    writer.writerow(header)
    for row in arcpy.SearchCursor(inputFeatureClass):
        if "None" in row:
        output = row.RTEID, "Outside Boundary"
        print(output)
        writer.writerow(output)
arcpy.AddMessage("bounary searched")