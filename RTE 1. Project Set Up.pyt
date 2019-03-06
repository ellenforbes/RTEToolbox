import arcpy
import datetime
from datetime import date

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [fClassSetUp, addReviewFields, addEMatchDomain]


class fClassSetUp(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1. Create Feature Class, RTE ID and Survey Fields"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fgdb","File Geodatabase","Input","DEWorkspace","Required")
        param1 = arcpy.Parameter("cityname","Cityname (no spaces)","Input","GPString","Required")
        param2 = arcpy.Parameter("sp","State or Province Initial","Input","GPString","Required")
        param3 = arcpy.Parameter("missed_light","Tick if Layer is for Missed Lights","Input","GPBoolean","Optional")

        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_fgdb = parameters[0].valueAsText
        cityname = parameters[1].valueAsText
        sp = parameters[2].valueAsText
        missed_light = parameters[3].valueAsText

        if missed_light == 'true':
            arcpy.AddMessage("The check box was checked")
            input_fc_name = cityname + "_" + sp + "_" + str(date.today().strftime("%Y%m%d")) + "_MissedLights"
        else: #in this case, the check box value is 'false', user did not check the box
            arcpy.AddMessage("The check box was not checked")
            input_fc_name = cityname + "_" + sp + "_" + str(date.today().strftime("%Y%m%d")) + "_Survey"

        input_fc = input_fgdb + "\\" +input_fc_name
        latLonRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  
        

        arcpy.CreateFeatureclass_management (input_fgdb, input_fc_name, "POINT", "", "DISABLED", "ENABLED", latLonRef)
        arcpy.AddMessage("Feature Class Created")
        arcpy.AddField_management(input_fc, "RTEID", "SHORT", "", "", "5", "RTE ID", "NULLABLE", "REQUIRED","")
        arcpy.AddMessage("RTE ID Field Added, Cannot Be Deleted")

        arcpy.CreateDomain_management(input_fgdb, "LumType", "Survey, Lists luminaire type found by surveyor", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "DecoSubT", "Survey", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "Technology", "Survey, Technology used in luminaire", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "HIDWatt", "Survey, Used by lamp wattage field", "SHORT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "ArmLength", "Survey, measured in feet by surveyor", "SHORT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "RoadClass", "Survey, roadway type luminaire is found on", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "PedActive", "Survey, indicates pedestrian activity", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "YesNo", "A Yes No list to be used in multiple fields", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "ArmOrient", "Survey, indicates arm orientation of lamp", "SHORT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "WireLoc", "Survey, indicates if wire is located overhead or underground", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "PoleMat", "Survey, indicates the material of the pole", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "PoleUse", "Survey, indicates the poles main use", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "Problems", "Survey, problems that may be encountered in a light change", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        arcpy.CreateDomain_management(input_fgdb, "Surveyor", "Survey, the identity of the surveyor", "TEXT", "CODED", "DEFAULT", "DEFAULT")

        #Process : Add Coded Value To Domain : arcpy.AddCodedValueToDomain_management (in_workspace, domain_name, code, code_description)
        #LumType
        LumTypeCVs = [
            ["Building Light - Decorative", "Building Light - Decorative"],
            ["Building Light - Wallpack", "Building Light - Wallpack"],
            ["Building Light - Other", "Building Light - Other"],
            ["Cobrahead", "Cobrahead"],
            ["Decorative - Acorn Post Top", "Decorative - Acorn Post Top"],
            ["Decorative - Bell Downlighting", "Decorative - Bell Downlighting"],
            ["Decorative - Caged Acorn","Decorative - Caged Acorn"],
            ["Decorative - Globe Post Top", "Decorative - Globe Post Top"],
            ["Decorative - Lantern Pendant", "Decorative - Lantern Pendant"],
            ["Decorative - Lantern Post Top", "Decorative - Lantern Post Top"],
            ["Decorative - Lantern Side Mount", "Decorative - Lantern Side Mount"],
            ["Decorative - Other Downlighting", "Decorative - Other Downlighting"],
            ["Decorative - Other Post Top", "Decorative - Other Post Top"],
            ["Decorative - Shoe Box", "Decorative - Shoe Box"],
            ["Decorative - Tear Drop", "Decorative - Tear Drop"],
            ["Decorative - Top Hat", "Decorative - Top Hat"],
            ["Floodlight - Tenon", "Floodlight - Tenon"],
            ["Floodlight - Yoke", "Floodlight - Yoke"],
            ["NEMA Head or Dusk to Dawn", "NEMA Head or Dusk to Dawn"],
            ["New Light Request", "New Light Request"],
            ["No Light", "No Light"],
            ["Offset Roadway", "Offset Roadway"],
        ]
        for LumType in LumTypeCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "LumType", LumType[0], LumType[1])

        #DecoSubT
        DecoSubTCVs = [
            ["Type 1", "Type 1"],
            ["Type 2", "Type 2"],
            ["Type 3", "Type 3"],
            ["Type 4", "Type 4"],
            ["Type 5", "Type 5"],
        ]
        for DecoSubT in DecoSubTCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "DecoSubT", DecoSubT[0], DecoSubT[1])

        #Tehcnology
        TechnologyCVs = [
            ["HID (HPS, LPS, MV, MH), Incandescent", "HID (HPS, LPS, MV, MH), Incandescent"],
            ["Induction", "Induction"],
            ["LED", "LED"],
        ]
        for Technology in TechnologyCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "Technology", Technology[0], Technology[1])

        #HIDWattages
        HIDWattCVs = [
            ["50", "50 W"],
            ["70", "70 W"],
            ["80", "80 W"],
            ["100", "100 W"],
            ["150", "150 W"],
            ["175", "175 W"],
            ["200", "200 W"],
            ["250", "250 W"],
            ["400", "400 W"],
            ["999", "No Clear Label"],
            ["999", "Other"],
        ]
        for HIDWatt in HIDWattCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "HIDWatt", HIDWatt[0], HIDWatt[1])

        #ArmLength
        ArmLengthCVs = [
            ["0", "No Arm"],
            ["1", "1 ft"],
            ["2", "2 ft"],
            ["4", "4 ft"],
            ["6", "6 ft"],
            ["8", "8 ft"],
            ["10", "10 ft"],
            ["12", "12 ft"],
            ["16", "16 ft and over"],
        ]
        for ArmLength in ArmLengthCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "ArmLength", ArmLength[0], ArmLength[1])

        #RoadClass
        RoadClassCVs = [
            ["Local", "Local"],
            ["Arterial", "Arterial"],
            ["Collector", "Collector"],
            ["Expressway", "Expressway"],
            ["Park", "Park"],
            ["Parking Lot", "Parking Lot"],
            ["Cul De Sac", "Cul De Sac"],
        ]
        for RoadClass in RoadClassCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "RoadClass", RoadClass[0], RoadClass[1])

        #PedActive
        PedActiveCVs = [
            ["Low", "Low"],
            ["Medium", "Medium"],
            ["High", "High"],
        ]
        for PedActive in PedActiveCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "PedActive", PedActive[0], PedActive[1])

        #YesNo
        YesNoCVs = [
            ["No", "No"],
            ["Yes", "Yes"],
            ["N/A", "N/A"],
        ]
        for YesNo in YesNoCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "YesNo", YesNo[0], YesNo[1])

        #ArmOrient
        ArmOrientCVs = [
            ["0", "Perpendicular To Road"],
            ["45", "At Angle With Road"],
            ["90", "Parallel To Road"],
            ["180", "Away From Road"],
        ]
        for ArmOrient in ArmOrientCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "ArmOrient", ArmOrient[0], ArmOrient[1])

        #WireLoc
        WireLocCVs = [
            ["Underground", "Underground"],
            ["Overhead", "Overhead"],
        ]
        for WireLoc in WireLocCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "WireLoc", WireLoc[0], WireLoc[1])

        #PoleMat
        PoleMatCVs = [
            ["Composite", "Composite"],
            ["Concrete", "Concrete"],
            ["Metal - Round", "Metal - Round"],
            ["Metal - Faceted", "Metal - Faceted"],
            ["Wood", "Wood"],
            ["Other", "Other"],    
        ]
        for PoleMat in PoleMatCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "PoleMat", PoleMat[0], PoleMat[1])

        #PoleUse
        PoleUseCVs = [
            ["Lighting", "Lighting"],
            ["Communication", "Communication"],
            ["Distribution", "Distribution"],
            ["Traffic Light", "Traffic Light"],
        ]
        for PoleUse in PoleUseCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "PoleUse", PoleUse[0], PoleUse[1])

        #Problems
        ProblemsCVs = [
            ["None", "None"],
            ["High Reach", "High Reach"],
            ["Pole Condition", "Pole Condition"],
            ["Restricted Area", "Restricted Area"],
            ["Tree Trimming Required", "Tree Trimming Required"],
        ]
        for Problems in ProblemsCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "Problems", Problems[0], Problems[1])

        #Surveyor
        SurveyorCVs = [
            ["ED", "ED"],
            ["EK", "EK"],
            ["Surveyor3", "Surveyor3"],
            ["Surveyor4", "Surveyor4"],
            ["Surveyor5", "Surveyor5"],
            ["Surveyor6", "Surveyor6"],
            ["Surveyor7", "Surveyor7"],
            ["Surveyor8", "Surveyor8"],
            ["Surveyor9", "Surveyor9"],
            ["Surveyor10", "Surveyor10"],
        ]
        for Surveyor in SurveyorCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "Surveyor", Surveyor[0], Surveyor[1])

        # Process: Add Field AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
        arcpy.AddField_management(input_fc, "FixType", "TEXT", "", "", "50", "FixtureType", "NON_NULLABLE", "NON_REQUIRED","LumType")
        arcpy.AddField_management(input_fc, "DecoSubT", "TEXT", "", "", "6", "Deco Subtype", "NULLABLE", "NON_REQUIRED","DecoSubT")
        arcpy.AddField_management(input_fc, "Technology", "TEXT", "", "", "40", "Technology", "NON_NULLABLE", "NON_REQUIRED","Technology")
        arcpy.AddField_management(input_fc, "LampWatt", "SHORT", "4", "", "", "Lamp Wattage", "NON_NULLABLE", "NON_REQUIRED","HIDWatt")
        arcpy.AddField_management(input_fc, "LampHeight", "SHORT", "4", "", "", "Lamp Height (ft)", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "ArmLength", "SHORT", "4", "", "", "Arm Length (ft)", "NULLABLE", "NON_REQUIRED","ArmLength")
        arcpy.AddField_management(input_fc, "Setback", "SHORT", "4", "", "", "Setback", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "RoadWidth", "SHORT", "4", "", "", "Road Width", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "RoadClass", "TEXT", "", "", "20", "Road Class", "NULLABLE", "NON_REQUIRED","RoadClass")
        arcpy.AddField_management(input_fc, "PedActive", "TEXT", "", "", "10", "Pedestrian Activity", "NULLABLE", "NON_REQUIRED","PedActive")
        arcpy.AddField_management(input_fc, "StreetName", "TEXT", "", "", "100", "Street Name", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "Intersect", "TEXT", "", "", "10", "Intersection", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "ArmOrient", "SHORT", "4", "", "", "ArmOrientation", "NULLABLE", "NON_REQUIRED","ArmOrient")
        arcpy.AddField_management(input_fc, "WireLoc", "TEXT", "", "", "20", "WireLocation", "NULLABLE", "NON_REQUIRED","WireLoc")
        arcpy.AddField_management(input_fc, "HVoltage", "TEXT", "", "", "10", "High Voltage", "NULLABLE", "NON_REQUIRED","YesNo")
        arcpy.AddField_management(input_fc, "PoleMat", "TEXT", "", "", "20", "Pole Material", "NULLABLE", "NON_REQUIRED","PoleMat")
        arcpy.AddField_management(input_fc, "PoleUse", "TEXT", "", "", "20", "Pole Useage", "NULLABLE", "NON_REQUIRED","PoleUse")
        arcpy.AddField_management(input_fc, "UtlPoleID", "TEXT", "", "", "20", "Utility Pole ID", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "Problems", "TEXT", "", "", "50", "Problems", "NULLABLE", "NON_REQUIRED","Problems")
        arcpy.AddField_management(input_fc, "SurvComs", "TEXT", "", "", "", "Survey Comments", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "SurvDate", "DATE", "", "", "", "Survey Date", "NON_NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "Surveyor", "TEXT", "", "", "30", "Surveyor", "NULLABLE", "NON_REQUIRED","Surveyor")

        return

class addReviewFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "2. (Optional) Add Fields For Utility Review"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fgdb","File Geodatabase","Input","DEWorkspace","Required")
        param1 = arcpy.Parameter("input_fc","Municipality Dataset","Input","GPFeatureLayer","Required")

        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_fgdb = parameters[0].valueAsText
        input_fc = parameters[1].valueAsText
    
        arcpy.CreateDomain_management(input_fgdb, "EMatch", "Indicates match between RTE survey and external data from utility or client", "TEXT", "CODED", "DEFAULT", "DEFAULT")

        #Process : Add Coded Value To Domain : arcpy.AddCodedValueToDomain_management (in_workspace, domain_name, code, code_description)
        #EMatch
        EMatchCVs = [
            ["Match", "Match"],
            ["Probable Match", "Probable Match"],
            ["RTE Only", "RTE Only"],
            ["Utility Only", "Utility Only"],
            ["Client Owned", "Client Owned"],
        ]
        for EMatch in EMatchCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "EMatch", EMatch[0], EMatch[1])

        # Process: Add Field AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
        arcpy.AddField_management(input_fc, "ExtID", "TEXT", "", "", "20", "External ID", "NULLABLE", "NON_REQUIRED","")
        arcpy.AddField_management(input_fc, "EMatch", "TEXT", "", "", "15", "External Match", "NULLABLE", "NON_REQUIRED","EMatch")
        arcpy.AddField_management(input_fc, "EMatchComs", "TEXT", "", "", "", "External Match Comments", "NULLABLE", "NON_REQUIRED","")

        return

class addEMatchDomain(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Stand Alone - Add EMatch Domain to Existing Column"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("input_fgdb","File Geodatabase","Input","DEWorkspace","Required")
        param1 = arcpy.Parameter("input_fc","Municipality Dataset","Input","GPFeatureLayer","Required")

        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_fgdb = parameters[0].valueAsText
        input_fc = parameters[1].valueAsText
    
        arcpy.CreateDomain_management(input_fgdb, "EMatch", "Indicates match between RTE survey and external data from utility or client", "TEXT", "CODED", "DEFAULT", "DEFAULT")
        EMatchCVs = [
            ["Match", "Match"],
            ["Probable Match", "Probable Match"],
            ["RTE Only", "RTE Only"],
            ["Utility Only", "Utility Only"],
            ["Client Owned", "Client Owned"],
        ]
        for EMatch in EMatchCVs:
            arcpy.AddCodedValueToDomain_management(input_fgdb, "EMatch", EMatch[0], EMatch[1])

        arcpy.AssignDomainToField_management (input_fc, "EMatch", "EMatch", "")
        return