import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CreatePIR]

class CreatePIR(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create PIR"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFeatureClass","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("statusField","Status or Installation Field","Input", "Field","Required")
        param1.filter.list = ['Text']
        param1.parameterDependencies = [param0.name]  
        param2 = arcpy.Parameter("installDateField", "Install Date Field","Input", "Field","Required")
        param2.filter.list = ['Date']
        param2.parameterDependencies = [param0.name]  
        param3 = arcpy.Parameter("fromDate", "From Date (counts from midnight the previous day)", "Input", "Date","Required")
        param4 = arcpy.Parameter("toDate", "To Date (counts until midnight on this day)", "Input", "Date","Required")
        param5 = arcpy.Parameter("outputFolder", "Folder", "Output", "DEFolder","Required")
        
        params = [param0, param1, param2, param3, param4, param5]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        inputFeatureClass = parameters[0].valueAsText
        statusField = parameters[1].valueAsText
        installDateField = parameters[2].valueAsText
        fromDate =  parameters[3].valueAsText
        toDate =  parameters[4].valueAsText
        outputFolder = parameters[5].valueAsText

        # Build queries to select only installed lights and to define that selection between dates
        defQueryInstallation = statusField + " = 'Installed'"
        defQueryDate = installDateField + " > date '" + fromDate + "' AND " + installDateField + " < date '" + toDate + "'"
        print (defQueryInstallation)
        arcpy.AddMessage(defQueryDate)

        # Run selections on the field containing the install information and the field containing the install date
        queryInstallation = defQueryInstallation
        arcpy.MakeFeatureLayer_management (inputFeatureClass, "inputFeatureClassOut")
        arcpy.SelectLayerByAttribute_management("inputFeatureClassOut", "NEW_SELECTION", queryInstallation)
        queryDate = defQueryDate
        arcpy.SelectLayerByAttribute_management("inputFeatureClassOut", "SUBSET_SELECTION", queryDate)

        # Convert the selection on table to Excel
        # arcpy.TableToDBASE_conversion("inputFeatureClassOut", "C:\\Users\\ekitteridge\\Desktop\\ExcelOutput.xls")
        arcpy.TableToExcel_conversion("inputFeatureClassOut", "C:\\Users\\ekitteridge\\Desktop\\ExcelOutput.xls")

        return