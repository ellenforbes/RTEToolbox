import re

inputFeatureClass = "Cityname_SP_YYYYMMDD"
streetNameField = "StreetName"

arcpy.CalculateField_management(inputFeatureClass, streetNameField, r"re.sub(' +', ' ',!" + streetNameField + "!)", "PYTHON_9.3")
print("Removed all accidental double spaces")

arcpy.CalculateField_management(inputFeatureClass, streetNameField, r"!" + streetNameField + "!.strip().title()", "PYTHON_9.3")
print("Stripped trailing and leading spaces and changed all to title case")

streetNameFixes = [
    ["' Road'", "' Rd'"],
    ["' Street'", "' St'"],
    ["' Avenue'", "' Ave'"],
    ["' Drive'", "' Dr'"],
    ["' Lane'", "' Ln'"],  
    ["' Manor'", "' Mnr'"],
    ["' Trail'", "' Trl'"],
    ["' Beach'", "' Bch'"],    
    ["' Highway'", "' Hwy'"],
    ["' Boulevard'", "' Blvd'"],
    ["' Bvd'", "' Blvd'"],
    ["' Court'", "' Ct'"],
    ["' Crt'", "' Ct'"],
    ["' Drive'", "' Dr'"],
    ["'.'", "''"],
]
for streetNameFix in streetNameFixes:
    arcpy.CalculateField_management(inputFeatureClass, streetNameField, r"!" + streetNameField + "!.replace(" + streetNameFix[0] + "," + streetNameFix[1] + ")", "PYTHON_9.3")

print("Shortened all street and road abbreviations")


#Deal with north, east, south, west mess :( not sure on logic here because these can feature at beginning and end + should be N or North

#Iterate through the streetNameField and flag any endings that are not found in streetNameFix[1] - hmmm - hard for me, need to use SearchCursor