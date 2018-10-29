import bpy
import os

from clip_editor import utils, argconfig
from clip_editor.blender.modules import render, sequencer
from clip_editor.blender.modules.scene import set_scene_from_args

args = argconfig.get_args()

context = bpy.context
scene = context.scene


def process():
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sequences = scene.sequence_editor.sequences

    inputpath = args.inputpath
    inputpath = utils.normpath(inputpath) if inputpath else None

    if inputpath and '#' in inputpath:
        dirname = os.path.dirname(inputpath)
        images = utils.find_images(inputpath)
        path = os.path.join(dirname, images[0])
    else:
        images = args.inputs
        path = args.inputpath

    sequence_strip, movieclip = sequencer.create_sequence(
        scene, images=images, path=path)
    x, y = movieclip.size
    scene.render.resolution_percentage = 100
    scene.render.resolution_x = x
    scene.render.resolution_y = y

    if args.colorspace:
        movieclip.colorspace_settings.name = args.colorspace
        if sequence_strip.type in ['MOVIE', 'IMAGE']:
            sequence_strip.colorspace_settings.name = args.colorspace
    if args.debug:
        bpy.ops.wm.save_as_mainfile(
            filepath='{}.blend'.format(args.output),
            check_existing=True,
            relative_remap=False)

    sequencer.set_frame_range(scene)
    set_scene_from_args(scene)
    render.render(scene)


process()
