import bpy
import os
import sys
import tempfile
import shutil
import subprocess

from clip_editor import utils, argconfig
from clip_editor.config import FFMPEG_BIN
from clip_editor.blender.modules import render
from clip_editor.blender.modules.scene import set_scene_from_args

args = argconfig.get_args()

data = bpy.data
movieclips = data.movieclips
context = bpy.context
scene = context.scene


def process():
    # Remove all objects
    for obj in data.objects:
        data.objects.remove(obj)

    # Scene setup
    scene.use_nodes = True
    scene.render.use_multiview = True
    scene.render.views_format = 'STEREO_3D'
    scene.render.image_settings.views_format = 'STEREO_3D'
    scene.render.image_settings.stereo_3d_format.display_mode = 'ANAGLYPH'
    scene.render.image_settings.stereo_3d_format.anaglyph_type = 'RED_CYAN'

    # Clear default nodes
    node_tree = scene.node_tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Create nodes
    switchview_node = node_tree.nodes.new('CompositorNodeSwitchView')
    inputs = [utils.normpath(i) for i in args.inputs]
    for index, input in enumerate(inputs):
        # TODO: use animate image reader for path/files
        movieclip = movieclips.load(input)
        node = node_tree.nodes.new('CompositorNodeMovieClip')
        node.clip = movieclip
        node_tree.links.new(node.outputs[0], switchview_node.inputs[index])
    huesat_node = node_tree.nodes.new('CompositorNodeHueSat')
    huesat_node.inputs[2].default_value = 0
    node_tree.links.new(switchview_node.outputs[0], huesat_node.inputs[0])
    output_node = node_tree.nodes.new('CompositorNodeComposite')
    node_tree.links.new(huesat_node.outputs[0], output_node.inputs[0])

    x, y = movieclips[0].size
    # TODO: use args.startframe
    # start_frame = args.startframe or 1
    start_frame = 1
    scene.frame_start = start_frame
    scene.frame_end = start_frame + movieclips[0].frame_duration - 1
    scene.render.resolution_percentage = 100
    scene.render.resolution_x = x
    scene.render.resolution_y = y

    # TODO: place scene into VSE timeline to be able to add text overlay

    set_scene_from_args(scene)
    render.render(scene)


process()
