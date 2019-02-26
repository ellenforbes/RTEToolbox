import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [PrepareForJoin, JoinAndCalculate]


class PrepareForJoin(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1. Join Preparation"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFCSurveyRTE","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("fieldRTEStreetName","RTE Street Name Field","Input", "Field","Required")
        param1.filter.list = ['Text']
        param1.parameterDependencies = [param0.name]
        param2 = arcpy.Parameter("fieldRTEPoleID","RTE Utility Pole ID","Input", "Field","Required")
        param2.filter.list = ['Text']
        param2.parameterDependencies = [param0.name] 
        param3 = arcpy.Parameter("fieldRTEWattage","RTE Wattage","Input", "Field","Required")
        param3.filter.list = ['Short']
        param3.parameterDependencies = [param0.name]
        param4 = arcpy.Parameter("inputFCUtility","Utility Dataset","Input","GPFeatureLayer","Required")
        param5 = arcpy.Parameter("fieldUtilityStreetName","Utility Street Name Field","Input", "Field","Required")
        param5.filter.list = ['Text']
        param5.parameterDependencies = [param4.name]
        param6 = arcpy.Parameter("fieldUtilityPoleID","Utility Utility Pole ID","Input", "Field","Required")
        param6.parameterDependencies = [param4.name] 
        param7 = arcpy.Parameter("fieldUtilityWattage","Utility Wattage","Input", "Field","Required")
        param7.parameterDependencies = [param4.name] 
        params = [param0, param1, param2, param3, param4, param5, param6, param7]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFCSurveyRTE = parameters[0].valueAsText
        fieldRTEStreetName = parameters[1].valueAsText
        fieldRTEPoleID = parameters[2].valueAsText
        fieldRTEWattage = parameters[3].valueAsText

        inputFCUtility = parameters[4].valueAsText
        fieldUtilityStreetName = parameters[5].valueAsText
        fieldUtilityPoleID = parameters[6].valueAsText
        fieldUtilityWattage = parameters[7].valueAsText

        arcpy.AddField_management(inputFCSurveyRTE, "TempForJoin", "Text", "", "", "100", "Temp For Join","NULLABLE", "NON_REQUIRED", "")
        arcpy.AddField_management(inputFCSurveyRTE, "TempUpdateX", "Double", "", "", "", "Temp Update X","NULLABLE", "NON_REQUIRED", "")
        arcpy.AddField_management(inputFCSurveyRTE, "TempUpdateY", "Double", "", "", "", "Temp Update Y","NULLABLE", "NON_REQUIRED", "")

        arcpy.AddField_management(inputFCUtility, "TempForJoin", "Text", "", "", "100", "Temp For Join","NULLABLE", "NON_REQUIRED", "")
        arcpy.AddField_management(inputFCUtility, "TempUpdateX", "Double", "", "", "", "Temp Update X","NULLABLE", "NON_REQUIRED", "")
        arcpy.AddField_management(inputFCUtility, "TempUpdateY", "Double", "", "", "", "Temp Update Y","NULLABLE", "NON_REQUIRED", "")

        expressionRTE = "!" + fieldRTEStreetName + "! + ' ' + str(!" + fieldRTEPoleID + "!) + ' ' + str(!" + fieldRTEWattage + "!)"

        arcpy.AddMessage(expressionRTE)

        arcpy.CalculateField_management(inputFCSurveyRTE, "TempForJoin", expressionRTE, "PYTHON_9.3")

        expressionUtility = "!" + fieldUtilityStreetName + "! + ' ' + str(!" + fieldUtilityPoleID + "!) + ' ' + str(!" + fieldUtilityWattage + "!)"

        arcpy.AddMessage(expressionUtility)

        arcpy.CalculateField_management(inputFCUtility, "TempForJoin", expressionUtility, "PYTHON_9.3")
  
        latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
        
        rows = arcpy.UpdateCursor(inputFCSurveyRTE, "", latLonRef)  
        for row in rows:  
            feat = row.shape  
            coord = feat.getPart()  
            lon = coord.X  
            lat = coord.Y  
            row.TempUpdateY = lat  
            row.TempUpdateX = lon  
            rows.updateRow(row)  

        #arcpy.CalculateField_management(inputFCUtility, "TempForJoin", "!TempForJoin!.replace(".0", "")", "PYTHON_9.3")

        return

class JoinAndCalculate(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "2. Join and Calculate"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFCSurveyRTE","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("inputFCUtility","Utility Dataset","Input","GPFeatureLayer","Required")
        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFCSurveyRTE = parameters[0].valueAsText
        inputFCUtility = parameters[1].valueAsText

        arcpy.AddJoin_management (inputFCUtility, "TempForJoin", inputFCSurveyRTE, "TempForJoin", "KEEP_ALL")

        matchQuery = inputFCSurveyRTE +".TempForJoin IS NOT NULL"
        arcpy.AddMessage(matchQuery)
        arcpy.SelectLayerByAttribute_management(inputFCUtility,"NEW_SELECTION",matchQuery)

        arcpy.CalculateField_management(inputFCUtility, inputFCUtility+".EMatch","\"Match\"","PYTHON_9.3")
        arcpy.CalculateField_management(inputFCUtility, inputFCUtility+".TempUpdateX","!" + inputFCSurveyRTE + ".TempUpdateX!","PYTHON_9.3")
        arcpy.CalculateField_management(inputFCUtility, inputFCUtility+".TempUpdateY","!" + inputFCSurveyRTE + ".TempUpdateY!","PYTHON_9.3")

        arcpy.RemoveJoin_management (inputFCUtility)

        arcpy.SelectLayerByAttribute_management(inputFCUtility,"NEW_SELECTION","EMatch = 'Match'")

        codeblock = """def Update(shape, newX, newY):
         pnt = shape.getPart(0)
         pnt.X = newX
         pnt.Y = newY
         return pnt
        """
        arcpy.CalculateField_management(inputFCUtility, "Shape", "Update (!Shape!, !TempUpdateX!, !TempUpdateY!)" , "PYTHON_9.3", codeblock)

        arcpy.DeleteField_management(inputFCSurveyRTE, ["TempForJoin", "TempUpdateX", "TempUpdateY"])
        arcpy.DeleteField_management(inputFCUtility, ["TempForJoin", "TempUpdateX", "TempUpdateY"])

        return