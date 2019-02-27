import arcpy
import re
import csv
import os
import datetime
from datetime import date

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CalcSeqNumbers, ExportCopyToLocal, CleanStreetNames, SearchForNulls, SearchOutsideBoundary, AddDesignFields, CalcMountRatio, CalcXY, CalcSeqNumbersAlt]

class CalcSeqNumbers(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1. Calculate RTE IDs (1, 2, 3...)"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("rteIDField","RTE ID Field","Input", "Field","Required")
        param1.filter.list = ['Short']
        param1.parameterDependencies = [param0.name]  
        
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        rteIDField = parameters[1].valueAsText

        codeblock = """rec=0 
def autoIncrement(): 
 global rec 
 pStart = 1  
 pInterval = 1 
 if (rec == 0):  
  rec = pStart  
 else:  
  rec += pInterval  
 return rec
 """

        arcpy.CalculateField_management(inputFeatureClass, rteIDField, "autoIncrement()" , "PYTHON_9.3", codeblock)
        arcpy.AddMessage("Calculated sequential numbers in field starting at 1, 2, 3...")

class ExportCopyToLocal(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "2. Export Copy To Local"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("folderLocation","Location","Input", "DEFolder","Required")
        
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        from datetime import date

        inputFeatureClass = parameters[0].valueAsText
        folderLocation = parameters[1].valueAsText
        citynameSP = "Cityname_SP"
        today = str(date.today().strftime("%Y%m%d"))
        out_name = citynameSP + "_" + today + "_" + "Inventory"

        arcpy.AddMessage(out_name)

        arcpy.CreateFileGDB_management (folderLocation, "InventoryLayerCreation")
        arcpy.FeatureClassToFeatureClass_conversion (inputFeatureClass, folderLocation +"\\InventoryLayerCreation.gdb", out_name)

        arcpy.AddMessage("Data Copied To Local")

class CleanStreetNames(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "3. Clean Street Names"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("streetNameField","Street Name Field","Input", "Field","Required")
        param1.filter.list = ['Text']
        param1.parameterDependencies = [param0.name]  
        
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        #import re

        inputFeatureClass = parameters[0].valueAsText
        streetNameField = parameters[1].valueAsText

        arcpy.CalculateField_management(inputFeatureClass, streetNameField, r"re.sub(' +', ' ',!" + streetNameField + "!)", "PYTHON_9.3")
        arcpy.AddMessage("Removed all accidental double spaces")

        arcpy.CalculateField_management(inputFeatureClass, streetNameField, r"!" + streetNameField + "!.strip().title()", "PYTHON_9.3")
        arcpy.AddMessage("Stripped trailing and leading spaces and changed all to title case")

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

        arcpy.AddMessage("Shortened all street and road abbreviations")

class SearchOutsideBoundary(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "4. Search For Points Outside Boundary"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("boundary","Municipality Boundary","Input", ["GPFeatureLayer", "GPString"],"Required")
        #param2 = arcpy.Parameter("folderPath","Output Folder","Input", "DEFolder","Required")

        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        #import csv
        #import os
        #from datetime import date

    

class SearchForNulls(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "5. Search For Nulls"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        
        params = [param0]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        rteIDField = parameters[1].valueAsText

        arcpy.AddMessage("Nulls Searched")

class AddDesignFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "6. Add Design Fields, Calc X and Y, Calc Mount Ratio"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("projectNo","Project Number","Input", "GPString","Required")
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        projectNo = str(parameters[1].valueAsText)
        latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  

        arcpy.AddMessage(projectNo)

        # Process : Add Field : arcpy.AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
        arcpy.AddField_management(inputFeatureClass, "Ownership", "TEXT", "", "", "60", "Ownership", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "UtlCompany", "TEXT", "", "", "60", "Utility Company", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "ProjectNo", "TEXT", "", "", "30", "Project No", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "PointX", "DOUBLE", "", "", "", "Point X", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "PointY", "DOUBLE", "", "", "", "Point Y", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "MountRatio", "DOUBLE", "", "", "", "Mount Ratio", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "LumType", "TEXT", "", "", "40", "Luminaire Type", "NULLABLE", "NON_REQUIRED","LumType")
        arcpy.AddField_management(inputFeatureClass, "DesignMod", "TEXT", "", "", "50", "Design Model", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "LEDDesign", "TEXT", "", "", "", "LED Designed", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "MiscParts", "TEXT", "", "", "", "Misc Parts", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(inputFeatureClass, "InstlCode", "TEXT", "", "", "10", "Install Code", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddMessage("Design Fields Added")

        calcMR = "(!RoadWidth!+!Setback!-!ArmLength!)/float(!LampHeight!)"
        arcpy.CalculateField_management(inputFeatureClass, "MountRatio", calcMR, "PYTHON_9.3")
        
        rows = arcpy.UpdateCursor(inputFeatureClass, "", latLonRef)  
        for row in rows:  
            feat = row.shape  
            coord = feat.getPart()  
            lon = coord.X  
            lat = coord.Y  
            row.PointY = lat  
            row.PointX = lon  
            rows.updateRow(row) 
        
        arcpy.CalculateField_management(inputFeatureClass, "ProjectNo", '"' + projectNo + '"', "PYTHON_9.3")
        arcpy.CalculateField_management(inputFeatureClass, "LumType", "!" + FixType + "!", "PYTHON_9.3")
        arcpy.CalculateField_management(inputFeatureClass, "ProjectNo", '"' + projectNo + '"', "PYTHON_9.3")

class CalcMountRatio(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Stand Alone - Calculate Mount Ratio"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("fieldRoadWidth","Field Containing Road Width","Input", "Field","Required")
        param1.filter.list = ['Short']
        param1.parameterDependencies = [param0.name]  
        
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        fieldRoadWidth = parameters[1].valueAsText
        calcMR = "(!" + fieldRoadWidth + "!+!Setback!-!ArmLength!)/float(!LampHeight!)"
        arcpy.CalculateField_management(inputFeatureClass, "MountRatio", calcMR, "PYTHON_9.3") 


class CalcXY(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Stand Alone - Calculate Coordinates in WGS84"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("pointXField","Point X Field","Input", "Field","Required")
        param1.filter.list = ['Double']
        param1.parameterDependencies = [param0.name]  
        param2 = arcpy.Parameter("pointYField","Point Y Field","Input", "Field","Required")
        param2.filter.list = ['Double']
        param2.parameterDependencies = [param0.name]  

        params = [param0, param1, param2]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        pointXField = parameters[1].valueAsText
        pointYField = parameters[2].valueAsText

        latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
        
        rows = arcpy.UpdateCursor(inputFeatureClass, "", latLonRef)  
        for row in rows:  
            feat = row.shape  
            coord = feat.getPart()  
            lon = coord.X  
            lat = coord.Y  
            row.pointYField = lat  
            row.pointXField = lon  
            rows.updateRow(row)  
        

        arcpy.AddMessage("X and Y calculated in WGS84")

class CalcSeqNumbersAlt(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Stand Alone - Calculate Sequential Numbers (Define Start and Interval)"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("rteIDField","RTE ID Field","Input", "Field","Required")
        param1.filter.list = ['Short']
        param1.parameterDependencies = [param0.name]  
        param2 = arcpy.Parameter("startingNumber","Start Number","Input", "GPLong","Required")
        param3 = arcpy.Parameter("intervalNumber","Interval Number","Input", "GPLong","Required")
        
        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        rteIDField = parameters[1].valueAsText
        startingNumber = parameters[2].valueAsText
        intervalNumber = parameters[3].valueAsText

        codeblock = """rec=0 
def autoIncrement(): 
 global rec 
 pStart = """ + startingNumber + """    
 pInterval = """ + intervalNumber + """  
 if (rec == 0):  
  rec = pStart  
 else:  
  rec += pInterval  
 return rec
 """

        arcpy.CalculateField_management(inputFeatureClass, rteIDField, "autoIncrement()" , "PYTHON_9.3", codeblock)
        arcpy.AddMessage("Calculated sequential numbers in field starting at 1, 2, 3...")