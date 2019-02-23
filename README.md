# To Do List (0 denotes not started)


## RTE Installations
### 1. Create PIR - Edit Required (Low Priority)
Edit: Do some testing with times (tried to force time but not sure if it is working in Python 3.)
Edit: Add functionality to automatically label the file name Cityname_SP_DateTime_PIR
Edit: Add functionality to also create the summary stats (by date and by LED Designed)

### 0. Create Install Fields/Domains/CVs - Medium Priority

### 0. Maintenance Stats - High Priority
Statistics_analysis (in_table, out_table, statistics_fields, {case_field})

### 0. Create FIR - Medium Priority
New Tool, Export KMZ, Export Shapefile, Export Excel Table
LayerToKML_conversion (layer, out_kmz_file, {layer_output_scale}, {is_composite}, {boundary_box_extent}, {image_size}, {dpi_of_client}, {ignore_zvalue})
Create Summary Statistics (for summary page of excel, by LEDDesigned how many installs)
idea create selections in a loopfor each selection summarise the number of records marked installed.


## RTE Survey QC:
### 1. Calculate RTE IDs (1, 2, 3..) - Working Happy

### 2. Export Copy To Local - Edit Required (Low Priority)
Edit: Need to Add RemoveRelate_management (in_layer_or_view, relate_name)

### 3. Clean Street Names - Working Happy

### 4. Search for Nulls - Edit Required
High Priority: Needs Work - is in unpackaged, but not clean code

### 5. Create Design Fields - Edit Required
inc. calculate xy calc mount ratio, calc luminaire type field from fixture type
Medium Priority: Incompletee

### 0. Search for Duplicate IDs - Low Priority
New Tool, would search for duplicate pole ID's in the same street name.
Also a general duplicate tool to search for duplicates in RTE ID - dev this first.

### Stand Alone - Calculate Coordinates in WGS 84 - Working Happy

### Stand Alone - Calculate Mount Ratio - Working Happy

### Stand Alone - Calculate Sequential Numbers (Define Start and Interval) - Working Happy


## RTE Utility vs Survey Review
### 1. Join Preparation - Working Happy

### 2. Join and Calculate - Working Happy

### 0. Calculate Probable Matches - Medium Priority
New Tool, Create a Porbable Match on for where wattage is different.