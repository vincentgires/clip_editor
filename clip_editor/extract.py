import bpy
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, os.pardir)
sys.path.insert(0, parent_dir)
from clip_editor import utils
from clip_editor import argconfig

data = bpy.data
movieclips = data.movieclips
context = bpy.context
scene = context.scene

args = argconfig.get_args()

def process():
    # Remove all objects
    for obj in data.objects:
        data.objects.remove(obj)

    # Set Sequencer
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sequences = scene.sequence_editor.sequences

    path = args.input
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

    scene.render.resolution_percentage = 100
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.image_settings.file_format = 'JPEG'

    file, ext = os.path.splitext(args.output)
    for frame in args.frames:
        scene.frame_current = frame
        bpy.ops.render.render()
        image = bpy.data.images['Render Result']
        image.save_render('{}.{:04}{}'.format(file, frame, ext))


process()
