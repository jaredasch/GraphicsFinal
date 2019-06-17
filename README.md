# Graphics Final Project - Jared Asch & Clara Mohri

## Features Implemented ##

#### Loading Mesh Files ####
- Can parse .obj files with vertices and faces
- Support for triangular and quadrilateral faces 
- Scalable to work with large files
- MDL Syntax ```mesh :<filename without obj extension>```

#### Saving Coordinate System
- Can save coordinate system to be used with 
  - sphere
  - box 
  - line
  - torus
- MDL Syntax ```save_coord_system <name>```
  
  Example: 
  ```
  save_coord_system <name>
  torus shiny_purple -100 150 10 30 50 <name>
  ```
