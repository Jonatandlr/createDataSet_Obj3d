import open3d
import numpy as np
import random
from time import sleep
from PIL import Image
import os




def crearMesh(filenameMesh: str, filenameTexture: str):
    # read the object to transform it into mesh
    mesh = open3d.io.read_triangle_mesh(filenameMesh)

    #get the center of the object in order to be able to rotate it on its axis  
    bbox = mesh.get_axis_aligned_bounding_box()
    center = bbox.get_center()

    # opcion1
        # # valores aleatorios para rotar la malla
        # rotacion=round(random.uniform(1, 7), 2)
        # angle = round(random.uniform(0, 2), 2)
        # inclinacion=round(random.uniform(0,2), 2)
        # rotation_angles = np.array([[inclinacion], [rotacion], [angle]])

    #rotate mesh
    random_vector = np.random.rand(3)
    random_unit_vector = random_vector / np.linalg.norm(random_vector)
    R = open3d.geometry.get_rotation_matrix_from_axis_angle(random_unit_vector)
    mesh.rotate(R,center)

    # load texture 
    mesh = open3d.t.geometry.TriangleMesh.from_legacy(mesh) 
    mesh.material.material_name = 'defaultLit'
    mesh.material.texture_maps['albedo'] = open3d.t.io.read_image(filenameTexture)
    return mesh

def crearVentana(mesh, name, output):
    # create window 
    vis = open3d.visualization.O3DVisualizer(name, 1280, 720)
    # set window properties 
    vis.set_background((0., 0.78, 0., 1.0), None)
    vis.add_geometry("meshname", mesh)
    vis.reset_camera_to_default()
    vis.animation_time_step = 1.0
    vis.show_skybox(False)


    # Define arguments for some objects that are not output with reset_camera_to_defaul
    arg0 = 0.1
    arg1 = np.array([0.0, 0.0, 0.0], dtype=np.float32).reshape(3, 1)
    arg2 = np.array([0.0, 0.0, 0.2], dtype=np.float32).reshape(3, 1)
    arg3 = np.array([0.0, 1.0,0.0], dtype=np.float32).reshape(3, 1)

    # Call the function with the defined arguments
    vis.setup_camera(arg0, arg1, arg2, arg3)

    # add window to gui aplication 
    open3d.visualization.gui.Application.instance.add_window(vis)

    # export images 
    vis.export_current_image(output)
    sleep(0.1)
    
    # shutdown gui
    # correr esto para que no se cuelgue
    open3d.visualization.gui.Application.instance.run_one_tick()
    vis.close()


#meshes Path
meshes=[
    {
        "mesh": "Objects/cocaFotosMalas/cocaColaPhotoBad.glb",
        "texture": "Objects/cocaFotosMalas/texture.jpg",
        "output": "imagesObjects/coca/",
        "name": "CocaCola"
    }
]
mesh_array = []

#create meshes 
for mesh in meshes:
    for i in range(10):#the for is the amount of meshes (photos you will take)
        mesh_array.append(crearMesh(mesh["mesh"], mesh["texture"]))

# start gui
open3d.visualization.gui.Application.instance.initialize()

for i in range(len(mesh_array)):#here you create the photos with the windows
    print("creating " + meshes[i//10]["name"] +"_"+ str(i))
    crearVentana(mesh_array[i], meshes[i//10]["name"] +"_"+ str(i), meshes[i//10]["output"]+ "_"+str(i) + ".png")




