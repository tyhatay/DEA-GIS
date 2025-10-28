# Determining the Efficiency Score of Forest Roads Based on Their Functional Status
This study was prepared with the support of the TÜBİTAK project coded 122O785.

This study examines the relationship between forest roads and forest resources, as well as the relationships between forest roads themselves, which form a systematic network. The aim is to measure the efficiency of forest roads planned and constructed using public resources by using different inputs and outputs with Data Envelopment Analysis. The goal is to ensure the effective and efficient use of this planning and construction process. By evaluating these efficiency scores, efforts to improve the current state of forest roads will be kept up to date. Furthermore, a package program serving as a guide for planners has been developed, and a program module has been created using Python programming for GIS applications based on programming.

Forest roads are planned and constructed according to the technical and geometric standards set forth in the Forest Roads Planning, Construction, and Maintenance Circular No. 292. Forest roads planned and constructed based on the timber production function can be evaluated according to different forest functions as a result of this study. It will be a pioneering model that can pave the way for a more consistent use of public resources.

# File design
Introduction to the files in the content:
**Arcpy GIS model:** This file contains files that can be used for ArcMap.

**Online Map:** This file contains online map files within the scope of the project.

**Sample data:** This file contains sample data.  


# How should the installation be performed?
This system has been tested with Arcmap10.8.

1. Enter any scenario data into the Arcpy GIS model file.
2. Open Arcmap.
3. Open the .tbx file from ArcCatalog. 
4. The modules that require installation are the first and last modules. Therefore, right-click on the first or last module and select properties. In the window that appears, select the “.py extension code file” with the same name located in the appropriate scenario in the “script file” section of the “Arcpy GIS model” folder.

Example:
![Screenshot of Module](https://tahayasin.com/VZA_DEA/kurulum.jpg)

5. Then, starting with tab B, run the modules for the calculation part of all input and output variables.
6. In the final step, redefine the script file and proceed directly to the data envelopment analysis.

# Ecological scenario variables

| **VARIABLE**                                            | **INPUT/OUTPUT** |
| ------------------------------------------------------- | --------------- |
| Road alignment                                              |	Input            |
| Slope gradient where the road passes                                  | Input            |
| Road width                                              |    Input            |
| Excavation slope height                                      |	Input            |
| Lost forest area                                          | Input            |
| Number of observed runoff and landslide areas along the road    | Input            |
| Distance of the road from riverbeds                          | Output			|
| Potential structure                                  | Output            |
| Areas connected by the road                          | Output            |     

# Economic scenario variables

| **VARIABLE**                                            | **INPUT/OUTPUT** |
| ------------------------------------------------------- | --------------- |
| Road alignment                                            | Input           |
| Slope gradient                                             | Input           |
| Construction area width                                  | Input           |
| Potential structure                                  | Input            |
| Curvature factor                                     | Input           |
| Winding factor                                   | Input           |
| Density of horizontal curves                               | Input           |
| Deformations on the road surface                          | Input           |
| Average road spacing distance                              | Output           |
| Road length and area opened for operation ((AA/YU*500 m)) | Output           |
| Forest roads passing through economically functional forests       | Output           |
| Amount of timber                                              | Output           |

# Social scenario variables

| **VARIABLE**                                            | **Input/Output** |
| ------------------------------------------------------- | --------------- |
| Road gradient                                               | Input           |
| Road length                                            | Input           |
| Straight and curved structure composition of the road (winding)   | Input           |
| Construction area width and lost forest area             | Input           |
| Transition to road protection forest for aesthetic purposes                | Output           |
| Access to agricultural and pasture areas                        | Output           |
| Service life                                              | Output           |
| Green (vegetation-covered) excavation slopes                | Output           |
| Population of surrounding villages                            | Output           |

# Technical scenario variables

| **VARIABLE**                                | **Input/Output** |
| ------------------------------------------- | --------------- |
| Road deformation intensity                   | Input           |
| Road alignment                            | Input           |
| Platform width                            | Input           |
| Meeting and stopping place                        | Input           |
| Shoulder width                            | Input           |
| Ditch width                            | Input           |
| Average road spacing distance                  | Output           |
| Sections connected by the road           | Output           |
| Forest area opened up for operation              | Output           |


## License

Supported by TÜBİTAK project code 122O785. All software, inputs, and outputs are licensed.

## Technologies Used

**Program:** ArcGIS 10.8, ArcMap 10.8, ArcCatalog 10.8, Spyder 5.4.3

**Programming Language:** Python 2.7

**Module:** arcpy, scipy 0.17.0, matplotlib 1.5.2, numpy 1.9.3, pandas 0.18.1

  
## Users

This project is intended for use by the following groups

- Forest Engineers
- Cartographers
- Environmental Engineers
- Urban and Regional Planners
- Mining Engineers

...and all groups professionally engaged in land planning and analysis

  ## Support

For more information on this topic, please email tyhatay@ktu.edu.tr.
