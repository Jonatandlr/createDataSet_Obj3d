import open3d
import numpy as np
import random
from time import sleep

#seleccionamos la mesh
mesh = open3d.io.read_triangle_mesh("Objects/cocaLidar/cocaColaLIDAR.glb")

# # Obtiene la caja alineada con los ejes de la malla
bbox = mesh.get_axis_aligned_bounding_box()
center = bbox.get_center()
mesh = open3d.t.geometry.TriangleMesh.from_legacy(mesh)

# Add  texture and visualize
mesh.material.material_name = 'defaultLit'
mesh.material.texture_maps['albedo'] = open3d.t.io.read_image("Objects/cocaLidar/texture.jpg")

open3d.visualization.gui.Application.instance.initialize()

vis = open3d.visualization.O3DVisualizer("nameVentana", 1280, 720)
#configuracion
vis.set_background((0., 0.78, 0., 1.0), None)
vis.add_geometry("meshname",mesh)
vis.reset_camera_to_default()
vis.animation_time_step = 1.0
vis.show_skybox(True)

# agregar ventana
open3d.visualization.gui.Application.instance.add_window(vis)
open3d.visualization.gui.Application.instance.run()
vis.close()