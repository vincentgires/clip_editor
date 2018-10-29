import bpy
import os
import sys
from clip_editor import utils
from clip_editor import argconfig
from clip_editor.blender.modules.scene import set_scene_from_args

args = argconfig.get_args()

data = bpy.data
movieclips = data.movieclips
context = bpy.context
scene = context.scene


IMAGE_FORMATS = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.exr': 'OPEN_EXR',
    '.tif': 'TIFF',
    '.tga': 'TARGA',
}


def process():
    # Remove all objects
    for obj in data.objects:
        data.objects.remove(obj)

    # Set Sequencer
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sequences = scene.sequence_editor.sequences

    path = args.inputpath
    path = utils.normpath(path)
    start_frame = args.startframe or 1

    if not os.path.isfile(path):
        return None

    dirname, basename = os.path.split(path)
    movieclip = movieclips.load(path)
    sequence_strip = sequences.new_clip(
        name=basename,
        clip=movieclip,
        channel=1,
        frame_start=start_frame)
    sequence_strip.use_translation = True

    x, y = movieclip.size

    sequence_strip.use_crop = True
    if args.croptop:
        sequence_strip.crop.max_y = args.croptop
        y -= args.croptop
    if args.cropbottom:
        sequence_strip.crop.min_y = args.cropbottom
        y -= args.croptop

    file, ext = os.path.splitext(args.output)

    scene.render.resolution_percentage = 100
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.image_settings.file_format = IMAGE_FORMATS[ext]

    set_scene_from_args(scene)

    for frame in args.frames:
        scene.frame_current = frame
        bpy.ops.render.render()
        image = bpy.data.images['Render Result']
        image.save_render('{}.{:04}{}'.format(file, frame, ext))


process()
