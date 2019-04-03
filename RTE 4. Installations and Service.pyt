import arcpy
import re
from datetime import date

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CreateInstallLayer, CreateServiceLayer, CreatePIR, AddInstallQCFields, AddPicturesReqFields, CreateFIR]


class CreateInstallLayer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1. Copy IGA Layer and Add Installation Fields"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("iga_fc","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        params = [param0]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables

        project = arcpy.mp.ArcGISProject("CURRENT")
        iga_fc = parameters[0].valueAsText
        folder_location = project.homeFolder
        folder_parts = re.split(r"^(.*)\\(.*)_(.*)$",folder_location)
        cityname = folder_parts[2]
        sp = folder_parts[3]
        today = str(date.today().strftime("%Y%m%d"))
        input_fc_name = cityname + "_" + sp + "_" + today + "_" + "Installations"
        input_fgdb_name = "LayerCreationInstallations"
        input_fgdb =  folder_location + "\\" + input_fgdb_name + ".gdb"
        input_fc =  folder_location + "\\" + input_fgdb_name +".gdb\\" + input_fc_name
        
        arcpy.AddMessage("Creating " + cityname + "_" + sp + "_" + today + "_" + "Installations")
        arcpy.AddMessage("at " + input_fgdb)

        arcpy.CreateFileGDB_management (folder_location, input_fgdb_name)
        arcpy.FeatureClassToFeatureClass_conversion (iga_fc, input_fgdb, input_fc_name)
    
        arcpy.AddMessage("Copied data to local dataset, now adding installation fields.")
        arcpy.AddMessage("Why do paper maps never win at poker?")

        #Add Domains and Coded Values
        arcpy.CreateDomain_management(input_fgdb, "Status", "Installations, shows status of the installation", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "VPoleID", "Installations, checks surveyor entered utility pole ID", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "WireRepd", "Installations", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "ArmMods", "Installations", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "MiscMods", "Installations, ", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "TraffCon", "Installations, ", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "RepIssue", "Maintenance, this is the issue reported for maintenace", "TEXT", "CODED", "DEFAULT", "DEFAULT")

        StatusCVs = [
            ["Installed", "Installed"],
            ["Installed - With Issue", "Installed - With Issue"],
            ["Not Installed - No Pole Or Light", "Not Installed - No Pole Or Light"],
            ["Not Installed - High Voltage", "Not Installed - High Voltage"],
            ["Not Installed - No Access", "Not Installed - No Access"],
            ["Not Installed - Not Owned By Client", "Not Installed - Not Owned By Client"],
            ["No Replacement", "No Replacement"],
            ["No Replacement - Client Request", "No Replacement - Client Request"],
            ["Pending", "Pending"],
        ]
        for Status in StatusCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "Status", Status[0], Status[1])

        VPoleIDCVs = [
            ["Correct", "Correct"],
            ["Incorrect - Write ID In Comments", "Incorrect - Write ID In Comments"],
            ["No Clear Label", "No Clear Label"],
            ["No Label", "No Label"],
        ]
        for VPoleID in VPoleIDCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "VPoleID", VPoleID[0], VPoleID[1])

        WireRepdCVs = [
            ["1-15 ft", "1-15 ft"],
            ["16-30 ft", "16-30 ft"],
            ["31-45 ft", "31-45 ft"],
            ["46 ft +", "46 ft +"],
            ["No", "No"],
        ]
        for WireRepd in WireRepdCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "WireRepd", WireRepd[0], WireRepd[1])

        ArmModsCVs = [
            ["No", "No"],
            ["New 4ft", "New 4ft"],
            ["New 6ft", "New 6ft"],
            ["New 8ft", "New 8ft"],
            ["New 10ft", "New 10ft"],
            ["New 12ft", "New 12ft"],
            ["Remounted", "Remounted"],        
        ]
        for ArmMods in ArmModsCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "ArmMods", ArmMods[0], ArmMods[1])

        arcpy.AddMessage("...because they always fold.")

        MiscModsCVs = [
            ["Replace Bolt", "Replace Bolt"],
            ["Realign Arm", "Realign Arm"],
            ["Hand Hole Repair", "Hand Hole Repair"],     
        ]
        for MiscMods in MiscModsCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "MiscMods", MiscMods[0], MiscMods[1])

        TraffConCVs = [
            ["Flaggers", "Flaggers"],
            ["Flaggers and Police", "Flaggers and Police"],
            ["Police", "Police"],
            ["No", "No"], 
        ]
        for TraffCon in TraffConCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "TraffCon", TraffCon[0], TraffCon[1])

        RepIssueCVs = [
            ["Overlit", "Overlit"],
            ["Underlit", "Underlit"],
            ["Luminaire Damaged", "Luminaire Damaged"],
            ["Luminaire Flickering", "Luminaire Flickering"],
            ["Luminaire Knocked Down", "Luminaire Knocked Down"],
            ["Luminaire Out", "Luminaire Out"],
            ["No Power", "No Power"],
            ["Pole Knocked Down", "Pole Knocked Down"],
            ["Should Not Have Been Replaced", "Should Not Have Been Replaced"],
            ["Tree Branches", "Tree Branches"],
            ["Other", "Other - Explain In Comments"],
            ["None", "None"],
        ]
        for RepIssue in RepIssueCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "RepIssue", RepIssue[0], RepIssue[1])

        #Add Fields
        arcpy.AddField_management(input_fc, "Status", "TEXT", "", "", "50", "Status", "NULLABLE", "NON_REQUIRED","Status")
        arcpy.AddField_management(input_fc, "VPoleID", "TEXT", "", "", "40", "Verify Utility Pole ID", "NULLABLE", "NON_REQUIRED","VPoleID")
        arcpy.AddField_management(input_fc, "SmartNode", "TEXT", "", "", "20", "Smart Node", "NULLABLE", "NON_REQUIRED","SmartNode")
        arcpy.AddField_management(input_fc, "WireRepd", "TEXT", "", "", "10", "Wire Replaced", "NULLABLE", "NON_REQUIRED","WireRepd")
        arcpy.AddField_management(input_fc, "FuseRepd", "TEXT", "", "", "10", "Fuse Replaced", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "FuseHdRepd", "TEXT", "", "", "10", "Fuse Holder Replaced", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "ArmMods", "TEXT", "", "", "20", "Arm Modifications", "NULLABLE", "NON_REQUIRED","ArmMods")
        arcpy.AddField_management(input_fc, "MiscMods", "TEXT", "", "", "20", "Misc Modifications", "NULLABLE", "NON_REQUIRED","MiscMods")
        arcpy.AddField_management(input_fc, "SndConnctR", "TEXT", "", "", "10", "Secondary Connection Refresh", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "PowerAvail", "TEXT", "", "", "10", "Power Available", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "TraffCon", "TEXT", "", "", "20", "Traffic Control", "NULLABLE", "NON_REQUIRED","TraffCon")
        arcpy.AddField_management(input_fc, "Operator", "TEXT", "", "", "50", "Operator", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "InstlComs", "TEXT", "", "", "", "Install Comments", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "InstlDate", "DATE", "", "", "", "Install Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "IRepIssue", "TEXT", "", "", "30", "Reported Issue at Installation", "NULLABLE", "NON_REQUIRED","RepIssue")

        arcpy.AddMessage("Installation fields and domains added, now deleting non-required fields.")

        #Delete Excess Fields
        fields_to_keep = ["OBJECTID", "Shape", "RTEID", "FixType", "StreetName", "HVoltage", "UtlPoleID", "Problems", "ProjectNo", "PointX", "PointY", "LumType", "LEDDesign", "MiscParts", "InstlCode", "Status", "VPoleID", "SmartNode", "WireRepd", "FuseRepd", "FuseHdRepd", "ArmMods", "MiscMods", "SndConnctR", "PowerAvail", "TraffCon", "Operator", "InstlComs", "InstlDate", "IRepIssue"]
        all_field_names = [f.name for f in arcpy.ListFields(input_fc)]
        for field in all_field_names:
            if field not in fields_to_keep:
                arcpy.AddMessage("Currently deleting " + field)
                arcpy.DeleteField_management(input_fc, field)
            else:
                pass

        return

class CreateServiceLayer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "2. Copy IGA Layer and Create Service Layer"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("iga_fc","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        param1 = arcpy.Parameter("folder_location","Folder for f.Gdb Creation","Input", "DEFolder","Required")
        param2 = arcpy.Parameter("cityname","Cityname (no spaces)","Input","GPString","Required")
        param3 = arcpy.Parameter("sp","State or Province Initial","Input","GPString","Required")
        params = [param0, param1, param2, param3]
        return params


    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables

        #To Do - Calculate all Repair Status to None

        iga_fc = parameters[0].valueAsText
        folder_location = parameters[1].valueAsText
        cityname = parameters[2].valueAsText
        sp = parameters[3].valueAsText
        today = str(date.today().strftime("%Y%m%d"))
        input_fc_name = cityname + "_" + sp + "_" + today + "_" + "Service"
        input_fgdb_name = "LayerCreationService"
        input_fgdb =  folder_location + "\\" + input_fgdb_name + ".gdb"
        input_fc =  folder_location + "\\" + input_fgdb_name +".gdb\\" + input_fc_name

        arcpy.AddMessage(input_fgdb)
        arcpy.AddMessage(input_fc)

        arcpy.CreateFileGDB_management (folder_location, input_fgdb_name)
        arcpy.FeatureClassToFeatureClass_conversion (iga_fc, input_fgdb, input_fc_name)

    
        arcpy.AddMessage("Data Copied To Local")

        arcpy.CreateDomain_management(input_fgdb, "SvcType", "Mainenance, this is what action is take to remedy the problem", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "RepIssue", "Mainenance, the short decription of the issue", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "RepairS", "Mainenance, the status of the repair on reported issue", "TEXT", "CODED", "DEFAULT", "DEFAULT")

        RepairSCVs = [
            ["None", "None"],
            ["RTE Alerted", "RTE Alerted"],
            ["Not Included in Maintenance", "Not Included in Maintenance"],
            ["Waiting on Client", "Waiting on Client"],
            ["Contractor Notified", "Contractor Notified"],
            ["Waiting On Repair", "Waiting on Repair"],
            ["Waiting on Parts", "Waiting on Parts"],
            ["Repairs Complete", "Repairs Complete"],
        ]
        for RepairS in RepairSCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "RepairS", RepairS[0], RepairS[1])

        RepIssueCVs = [
            ["Overlit", "Overlit"],
            ["Underlit", "Underlit"],
            ["Luminaire Damaged", "Luminaire Damaged"],
            ["Luminaire Flickering", "Luminaire Flickering"],
            ["Luminaire Knocked Down", "Luminaire Knocked Down"],
            ["Luminaire Out", "Luminaire Out"],
            ["No Power", "No Power"],
            ["Pole Knocked Down", "Pole Knocked Down"],
            ["Should Not Have Been Replaced", "Should Not Have Been Replaced"],
            ["Tree Branches", "Tree Branches"],
            ["Other", "Other - Explain In Comments"],
            ["None", "None"],
        ]
        for RepIssue in RepIssueCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "RepIssue", RepIssue[0], RepIssue[1])
        print("RepIssue Domain Values Coded")

        SvcTypeCVs = [
            ["Deco - Changed Driver", "Deco - Changed Driver"],
            ["Deco - Changed Led Driver And Module", "Deco - Changed Led Driver And Module"],
            ["Deco - Changed Led Module", "Deco - Changed Led Module"],
            ["Deco - Tightened Loose Fixture", "Deco - Tightened Loose Fixture"],
            ["Defective Fixture - RMA Required", "Defective Fixture - RMA Required"],
            ["New Connection To Secondary", "New Connection To Secondary"],
            ["New Neutral Connection", "New Neutral Connection"],
            ["No Power Handhole Or Underground", "No Power Handhole Or Underground"],
            ["Pinched or Broken Wires Repaired", "Pinched or Broken Wires Repaired"],
            ["Reinstalled Old Fixture", "Reinstalled Old Fixture"],
            ["Replaced Fuse", "Replaced Fuse"],
            ["Replaced Fuse And Fuse Kit", "Replaced Fuse And Fuse Kit"],
            ["Replaced Photocell", "Replaced Photocell"],
            ["Replacement Fixture Installed", "Replacement Fixture Installed"],
            ["Reset Breaker", "Reset Breaker"],
            ["Tested - No Problem Found", "Tested - No Problem Found"],
            ["Tightened Loose Photocell", "Tightened Loose Photocell"],
            ["Tree Trimming", "Tree Trimming"],
        ]
        for SvcType in SvcTypeCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "SvcType", SvcType[0], SvcType[1])

        # Process: Add Field AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
        arcpy.AddField_management(input_fc, "RepairS", "TEXT", "", "", "30", "Repair Status", "NULLABLE", "NON_REQUIRED","RepairS")
        arcpy.AddField_management(input_fc, "FRepIssue", "TEXT", "", "", "30", "Reported Issue", "NULLABLE", "NON_REQUIRED","RepIssue")
        arcpy.AddField_management(input_fc, "FIssueDesc", "TEXT", "", "", "", "RTE Issue Description", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "FCaseNo", "TEXT", "", "", "15", "Case Number", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "FSvcRqDate", "Date", "", "", "", "Service Requested Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "FSvcDuDate", "Date", "", "", "", "Service Due Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "FSvcType", "TEXT", "", "", "50", "Service Type", "NULLABLE", "NON_REQUIRED","SvcType")
        arcpy.AddField_management(input_fc, "FSvcDate", "Date", "", "", "", "Service Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "FSvcComs", "TEXT", "", "", "", "Contractor Service Comments", "NULLABLE", "NON_REQUIRED","")
        #2nd Fields
        arcpy.AddField_management(input_fc, "SRepIssue", "TEXT", "", "", "30", "2nd Reported Issue", "NULLABLE", "NON_REQUIRED","RepIssue")
        arcpy.AddField_management(input_fc, "SIssueDesc", "TEXT", "", "", "", "2nd RTE Issue Description", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SCaseNo", "TEXT", "", "", "15", "2nd Case Number", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SSvcRqDate", "Date", "", "", "", "2nd Service Requested Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SSvcDuDate", "Date", "", "", "", "2nd Service Due Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SSvcType", "TEXT", "", "", "50", "2nd Service Type", "NULLABLE", "NON_REQUIRED","SvcType")
        arcpy.AddField_management(input_fc, "SSvcDate", "Date", "", "", "", "2nd Service Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SSvcComs", "TEXT", "", "", "", "2nd Contractor Service Comments", "NULLABLE", "NON_REQUIRED","")
        #3rd Fields
        arcpy.AddField_management(input_fc, "TRepIssue", "TEXT", "", "", "30", "3rd Reported Issue", "NULLABLE", "NON_REQUIRED","RepIssue")
        arcpy.AddField_management(input_fc, "TIssueDesc", "TEXT", "", "", "", "3rd RTE Issue Description", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "TCaseNo", "TEXT", "", "", "15", "3rd Case Number", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "TSvcRqDate", "Date", "", "", "", "3rd Service Requested Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "TSvcDuDate", "Date", "", "", "", "3rd Service Due Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "TSvcType", "TEXT", "", "", "50", "3rd Service Type", "NULLABLE", "NON_REQUIRED","SvcType")
        arcpy.AddField_management(input_fc, "TSvcDate", "Date", "", "", "", "3rd Service Date", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "TSvcComs", "TEXT", "", "", "", "3rd Contractor Service Comments", "NULLABLE", "NON_REQUIRED","")

        #Delete Excess Fields
        fields_to_keep = ["OBJECTID", "Shape", "RTE_ID", "RTEID", "LEDDesigned", "LEDDesign","RepairS", "FRepIssue", "FIssueDesc", "FCaseNo", "FSvcRqDate", "FSvcDuDate", "FSvcType", "FSvcDate", "FSvcComs", "SRepIssue", "SIssueDesc", "SCaseNo", "SSvcRqDate", "SSvcDuDate", "SSvcType", "SSvcDate", "SSvcComs", "TRepIssue", "TIssueDesc", "TCaseNo", "TSvcRqDate", "TSvcDuDate", "TSvcType", "TSvcDate", "TSvcComs"]
        all_field_names = [f.name for f in arcpy.ListFields(input_fc)]
        for field in all_field_names:
            if field not in fields_to_keep:
                arcpy.AddMessage("Currently deleting " + field)
                arcpy.DeleteField_management(input_fc, field)
            else:
                pass

        return

class CreatePIR(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "3. Create PIR"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fc","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("statusField","Status or Installation Field","Input", "Field","Required")
        param1.filter.list = ['Text']
        param1.parameterDependencies = [param0.name]  
        param2 = arcpy.Parameter("installDateField", "Install Date Field","Input", "Field","Required")
        param2.filter.list = ['Date']
        param2.parameterDependencies = [param0.name]  
        param3 = arcpy.Parameter("fromDate", "From Date (counts from midnight the previous day)", "Input", "Date","Required")
        param4 = arcpy.Parameter("toDate", "To Date (counts until midnight on this day)", "Input", "Date","Required")
        param5 = arcpy.Parameter("outputExcel", "File", "Output", "DEFile","Required")
        
        params = [param0, param1, param2, param3, param4, param5]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        input_fc = parameters[0].valueAsText
        statusField = parameters[1].valueAsText
        installDateField = parameters[2].valueAsText
        fromDate =  parameters[3].valueAsText
        toDate =  parameters[4].valueAsText
        outputExcel = parameters[5].valueAsText

        # Build queries to select only installed lights and to define that selection between dates
        defQueryInstallation = statusField + " = 'Installed'"
        defQueryDate = installDateField + " > date '" + fromDate + "' AND " + installDateField + " < date '" + toDate + "'"
        print (defQueryInstallation)
        arcpy.AddMessage(defQueryDate)

        # Run selections on the field containing the install information and the field containing the install date
        queryInstallation = defQueryInstallation
        arcpy.MakeFeatureLayer_management (input_fc, "input_fcOut")
        arcpy.SelectLayerByAttribute_management("input_fcOut", "NEW_SELECTION", queryInstallation)
        queryDate = defQueryDate
        arcpy.SelectLayerByAttribute_management("input_fcOut", "SUBSET_SELECTION", queryDate)

        # Convert the selection on table to Excel
        arcpy.TableToExcel_conversion("input_fcOut", outputExcel)

        return

class AddInstallQCFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "4. (Optional) Copy Installs Layer and Add Install QC Fields"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fgdb","File Geodatabase","Input","DEWorkspace","Required")
        param1 = arcpy.Parameter("input_fc","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        input_fgdb = parameters[0].valueAsText
        input_fc = parameters[1].valueAsText

        #To Do - Select a random 2%
        #To Do - Calculate Inspection field to say 'Inspection Pending'

        #Add Domains and Coded Values
        arcpy.CreateDomain_management(input_fgdb, "Inspection", "Installation QC, this tells us the status of the inspection", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        InspectionCVs = [
            ["Inspection Pending", "Inspection Pending"],
            ["Installation Correct", "Installation Correct"],
            ["Installation Wrong", "Installation Wrong"],
        ]
        for Inspection in InspectionCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "Inspection", Inspection[0], Inspection[1])

        #Add Fields
        arcpy.AddField_management(input_fc, "Inspection", "TEXT", "", "", "30", "Inspection", "NULLABLE", "NON_REQUIRED","Inspection")
        arcpy.AddField_management(input_fc, "ArmSecure", "TEXT", "", "", "10", "Arm Secure", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "LumSecure", "TEXT", "", "", "10", "Luminaire Secure", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "LumMDesign", "TEXT", "", "", "10", "Luminaire Matches Design", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "WireSecure", "TEXT", "", "", "10", "Wire Secured To Pole", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "AprvWire", "TEXT", "", "", "10", "Approved Wire", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "TDelayFuse", "TEXT", "", "", "10", "Time Delay Fuse", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "AprvFuseHd", "TEXT", "", "", "10", "Approved Fuse Holder", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "FuseHoldIC", "TEXT", "", "", "10", "Fuse Holder Install Correct", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "FuseHoldEC", "TEXT", "", "", "10", "Fuse Holder End Cap", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "ConnectSA", "TEXT", "", "", "10", "Connections Secured Approved", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "DripLoops", "TEXT", "", "", "10", "Drip Loops", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "HHGHCSec", "TEXT", "", "", "10", "Hand H Ground H Covers Secured", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "DecoCentPT", "TEXT", "", "", "10", "Deco Centered Post Top", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "InspcComs", "TEXT", "", "", "", "Inspection Comments", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "InspcDate", "TEXT", "", "", "", "Inspection Date", "NULLABLE", "NON_REQUIRED","")

class AddPicturesReqFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "5. (Optional) Copy Installs Layer and Add Pictures Required Fields"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fgdb","File Geodatabase","Input","DEWorkspace","Required")
        param1 = arcpy.Parameter("input_fc","Municipality Dataset","Input", ["GPFeatureLayer", "GPString"],"Required")
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        input_fgdb = parameters[0].valueAsText
        input_fc = parameters[1].valueAsText

        #To Do - Copy layer
        #To Do - Select a random 2%
        #To Do - Calculate PicType field to say 'Pictures Of HPS And LED Fixtures Required'
        #To Do - Make field deletions

        #Add Domains and Coded Values
        arcpy.CreateDomain_management(input_fgdb, "PicType", "Pictures layer, tells surveyor type of picture required", "TEXT", "CODED", "DEFAULT", "DEFAULT")

        PicTypeCVs = [
            ["Pictures Of HPS And LED Fixtures Required", "Pictures Of HPS And LED Fixtures Required"],
            ["Miscellaneous Picture Required", "Miscellaneous Picture Required"],
        ]
        for PicType in PicTypeCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "PicType", PicType[0], PicType[1])

        # Add Fields
        arcpy.AddField_management(input_fc, "PicType", "TEXT", "", "", "50", "Picture Type", "NULLABLE", "NON_REQUIRED","PicType")
        arcpy.AddField_management(input_fc, "PicComs", "TEXT", "", "", "", "Picture Comments", "NULLABLE", "NON_REQUIRED","")

class CreateFIR(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "6. Create FIR"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fc","Municipality Dataset","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("outputFolder", "Folder", "Input", "DEFolder","Required")
        param2 = arcpy.Parameter("outputExcel", "Excel File", "Output", "DEFile","Required")
        param3 = arcpy.Parameter("outputKML", "KML File", "Output", "DEFile","Required")
        
        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define variables
        input_fc = parameters[0].valueAsText
        outputFolder = parameters[1].valueAsText
        outputExcel = parameters[2].valueAsText
        outputKML =  parameters[3].valueAsText

        arcpy.MakeFeatureLayer_management (input_fc, "input_fcOut")

        # Converts Feature to Excel
        arcpy.TableToExcel_conversion("input_fcOut", outputExcel)

        # Converts Feature to Shapefile
        arcpy.FeatureClassToShapefile_conversion("input_fcOut", outputFolder)

        # Converts Feature to Excel
        arcpy.LayerToKML_conversion("input_fcOut", outputKML)

        return

