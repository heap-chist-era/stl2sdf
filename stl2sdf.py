import os # to walk through directories, to rename files
import sys

# Libraries
import trimesh # for converting voxel grids to meshes (to import objects into simulators)

# Modules
import tools_sdf_generator

if __name__ == "__main__":

    print("Usage: ")
    print("python {} <FILEPATH> scaling_factor".format(sys.argv[0]))
    print("Example:\npython {} <FILEPATH> 1.0".format(sys.argv[0]))

    filename = sys.argv[1]
    scaling_factor = float(sys.argv[2])

    # Generate a folder to store the images
    print("Generating a folder to save the mesh")
    # Generate a folder with the same name as the input file, without its ".binvox" extension
    currentPathGlobal = os.path.dirname(os.path.abspath(__file__))
    directory = currentPathGlobal + "/" + filename + "_sdf"
    if not os.path.exists(directory):
        os.makedirs(directory)

    mesh = trimesh.load(filename)
    # scaling_factor = 100
    mesh.apply_scale(scaling=scaling_factor)

    mass = 0.00
    mass = mesh.volume # WATER density
    print("\n\nMesh volume: {} (used as mass)".format(mesh.volume))
    print("Mass (equal to volume): {0}".format(mass))
    print("Mesh convex hull volume: {}\n\n".format(mesh.convex_hull.volume))
    print("Mesh bounding box volume: {}".format(mesh.bounding_box.volume))

    print("Merging vertices closer than a pre-set constant...")
    mesh.merge_vertices()
    print("Removing duplicate faces...")
    mesh.remove_duplicate_faces()
    print("Making the mesh watertight...")
    trimesh.repair.fill_holes(mesh)
    # print("Fixing inversion and winding...")
    # trimesh.repair.fix_winding(mesh)
    # trimesh.repair.fix_inversion(mesh)
    trimesh.repair.fix_normals(mesh)

    print("\n\nMesh volume: {}".format(mesh.volume))
    print("Mesh convex hull volume: {}".format(mesh.convex_hull.volume))
    print("Mesh bounding box volume: {}".format(mesh.bounding_box.volume))

    print("Computing the center of mass: ")
    center_of_mass = mesh.center_mass
    print(center_of_mass)

    print("Computing moments of inertia: ")
    moments_of_inertia = mesh.moment_inertia
    print(moments_of_inertia)  # inertia tensor in meshlab

    print("Generating the STL mesh file")
    trimesh.exchange.export.export_mesh(
        mesh=mesh,
        file_obj=directory + "/mesh.stl",
        file_type="stl"
    )

    print("Generating the SDF file...")
    object_model_name = "mesh"

    tools_sdf_generator.generate_model_sdf(
        directory=directory,
        object_name=object_model_name,
        center_of_mass=center_of_mass,
        inertia_tensor=moments_of_inertia,
        mass=mass,
        model_stl_path=directory + "/mesh.stl",
        scale_factor = 1.0) #scale_normalisation_factor)
