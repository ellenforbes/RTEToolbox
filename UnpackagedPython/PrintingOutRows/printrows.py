import csv
import os

def createNewOrEmptyExistingFile(newFile):
    fileAlreadyExists = os.path.isfile(newFile)
    if fileAlreadyExists:
        os.remove(newFile)
    open(newFile, "w+")

filename = "C:\\Users\\ekitteridge\\Desktop\\filename.csv"
inputFeatureClass = "Cityname_SP_YYYYMMDD_Survey"
boundary = "Cityname_SP_YYYYMMDD_Boundary"
createNewOrEmptyExistingFile(filename)

arcpy.SelectLayerByLocation_management (inputFeatureClass,"WITHIN", boundary, "", "NEW_SELECTION", "INVERT")

with open(filename, 'w', newline='') as ofile:
    writer = csv.writer(ofile)
    header = "RTE ID", "Luminaire Type", "Issue"
    writer.writerow(header)
    for row in arcpy.SearchCursor(inputFeatureClass):
        output = row.RTEID, row.LumType, "Outside Boundary"
        print(output)
        writer.writerow(output)