# stl2sdf

Converter of meshes from STL/OBJ to SDF format.

Takes as input a mesh file (STL/OBJ) and generates the corresponding corresponding .SDF file for importing the model into Gazebo.  
It uses the [TriMesh](https://github.com/mikedh/trimesh) library.  
It also allows to resize a mesh.

```bash
# Usage
python stl2sdf.py <FILENAME> <SCALING_FACTOR>

# Example:
python stl2sdf.py mesh.stl 1.5
```

### Warning:
The SDF files contain hard-coded references to STL meshes, which means STL meshes should stay in their directory.
Otherwise, you have to re-generate the SDF files.

### Example usage with Gazebo:

```bash
# Generate the SDF description file for your mesh (without re-sizing it)
python stl2sdf.py mesh.stl 1.0

# Launch Gazebo:
roslaunch gazebo_ros empty_world.launch gui:=true

# Spawn the object inside Gazebo
rosrun gazebo_ros spawn_model -sdf -file /path/to/sdf/file/mesh.sdf -model myModelName
```

### (optional) Trimesh installation
To install Trimesh, open a terminal and write:
```bash
pip install --user trimesh
```
