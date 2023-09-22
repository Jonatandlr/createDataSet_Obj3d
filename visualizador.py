import open3d
import numpy as np
import random
from time import sleep

#seleccionamos la mesh
mesh = open3d.io.read_triangle_mesh("Objects/cocaLidar/cocaColaLIDAR.glb",True,True)

# # Obtiene la caja alineada con los ejes de la malla
bbox = mesh.get_axis_aligned_bounding_box()
center = bbox.get_center()

#rotate mesh
random_vector = np.random.rand(3)
random_unit_vector = random_vector / np.linalg.norm(random_vector)
R = open3d.geometry.get_rotation_matrix_from_axis_angle(random_unit_vector)
mesh.rotate(R,center)
meshCenter=mesh.get_center()
mesh.translate(-meshCenter)




# Add  texture and visualize
mesh = open3d.t.geometry.TriangleMesh.from_legacy(mesh)
mesh.material.material_name = 'defaultLit'
mesh.material.texture_maps['albedo'] = open3d.t.io.read_image("Objects/cocaLidar/texture.jpg")

open3d.visualization.gui.Application.instance.initialize()

vis = open3d.visualization.O3DVisualizer("nameVentana", 1280, 720)
#configuracion
vis.set_background((0., 0.78, 0., 1.0), None)
vis.add_geometry("meshname",mesh)

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

# agregar ventana
open3d.visualization.gui.Application.instance.add_window(vis)
open3d.visualization.gui.Application.instance.run()
vis.close()