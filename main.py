import numpy as np
import bpy
from typing import Union,Tuple
bpy.ops.object.delete(use_global=False, confirm=False)

#class Star(bpy.ops.mesh.primitive_uv_sphere_add)

def create_sphere(position  = None, radius : float = None, component : str = None):
    # instantiate a UV sphere with a give
    # radius, at a given distance from the
    # world origin point
    if radius is None:
        print('Radius not provided. Using 0.1 as radius to create object')
        radius = 0.1
    if position is None:
        position = (0,0,0)
    if len(position) > 3:
        raise ValueError
#        print("provide (x), (x,y), or (x,y,z)"
    obj = bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=(position[0], position[1],position[2]),
        scale=(1, 1, 1)
    )
    # rename the object
    bpy.ops.object.shade_smooth()

    bpy.context.object.name = component
    # return the object reference
    return bpy.context.object

def create_torus(position, obj_name):
    # (same as the create_sphere method)
    obj = bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=np.sqrt(position[0]**2+position[1]**2+position[2]**2),
        minor_radius=0.05,
        major_segments=360
    )
    bpy.ops.object.shade_smooth()

    bpy.context.object.name = obj_name
    
    return bpy.context.object

def create_emission_shader(color, strength, mat_name):
    # create a new material resource (with its
    # associated shader)
    mat = bpy.data.materials.new(mat_name)
    # enable the node-graph edition mode
    mat.use_nodes = True
    
    # clear all starter nodes
    nodes = mat.node_tree.nodes
    nodes.clear()

    # add the Emission node
    node_emission = nodes.new(type="ShaderNodeEmission")
    # (input[0] is the color)
    node_emission.inputs[0].default_value = color
    # (input[1] is the strength)
    node_emission.inputs[1].default_value = strength
    
    # add the Output node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # link the two nodes
    links = mat.node_tree.links
    link = links.new(node_emission.outputs[0], node_output.inputs[0])

    # return the material reference
    return mat


p = ([0,0,0],[2,3,0])
r = (1,0.5)
comp = ["primary","secondary"]
#for n in range(2):
    # get a random radius (a float in [1, 5])
    
    # get a random distace to the origin point:
    # - an initial offset of 30 to get out of the sun's sphere
    # - a shift depending on the index of the planet
    # - a little "noise" with a random float
#    d = 30 + n * 12 + (random() * 4 - 2)
    # instantiate the planet with these parameters
    # and a custom object name
a = create_sphere(p[0], r[0], comp[0])
a.data.materials.append(
    create_emission_shader(
        (1, 0.66, 0.08, 1), 10, "AMat"
    )
)
b = create_sphere(p[1], r[1], comp[1])
b.data.materials.append(
    create_emission_shader(
        (1, 0.66, 0.08, 1), 10, "BMat"
    )
)
create_torus(p[1],'orbit')
