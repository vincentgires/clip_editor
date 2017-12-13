import bpy
import os
import time
import sys
import getpass
import json

settings = sys.argv[-1]
settings = json.loads(settings)

data = bpy.data
movieclips = data.movieclips

context = bpy.context
scene = context.scene

sequence_channel = 1
overlay_channel = 2


def get_frame_from_filename(file):
    return int(file.split('.')[-2])


def get_current_strip(scene, channel):
    frame_current = scene.frame_current
    
    if not scene.sequence_editor:
        return None
    
    for strip in scene.sequence_editor.sequences:
        frame_end = strip.frame_start + strip.frame_final_duration
        if strip.frame_start <= frame_current < frame_end:
            if strip.channel == channel:
                return strip

def update_frame(scene):
    for overlay in settings['overlays']:
        object = scene.objects[overlay['position']]
        
        strip = get_current_strip(scene, sequence_channel)
        
        if not strip:
            return None
        
        if overlay['type'] == 'NAME':
            object.data.body = strip['sequence_name']
        
        if strip.type in ['MOVIE', 'MOVIECLIP']:
            if overlay['type'] == 'FRAME':
                object.data.body = '{:04}'.format(scene.frame_current)
            
            elif overlay['type'] == 'FILENAME':
                object.data.body = strip.name
                
        elif strip.type == 'IMAGE':
            elem = strip.strip_elem_from_frame(scene.frame_current)
            
            if overlay['type'] == 'FRAME':
                file_frame = get_frame_from_filename(elem.filename)
                object.data.body = '{:04}'.format(file_frame)
            
            if overlay['type'] == 'FILENAME':
                object.data.body = elem.filename

bpy.app.handlers.frame_change_pre.append(update_frame)


def create_image_sequence(scene, directory, elements):
    filename = elements[0]
    frame_start = int(filename.split('.')[-2])
    
    first_frame = os.path.join(directory, elements[0])
    sequence_strip = sequences.new_image(
        name='image_sequence',
        filepath=first_frame,
        channel=sequence_channel,
        frame_start=frame_start
        )

    for file in elements[1:]:
        name = os.path.basename(file)
        sequence_strip.elements.append(name)
    
    return sequence_strip


# SEQUENCER
if not scene.sequence_editor:
    scene.sequence_editor_create()
sequences = scene.sequence_editor.sequences


# GET FILES AND SET SEQUENCER
for sequence in settings['sequences']:
    path = sequence['path']
    if sys.platform.startswith('linux'):
        path = path.replace('//', '/')
    files = sequence['files']
    images = sequence['images']
    
    if os.path.isfile(path):
        dirname, basename = os.path.split(path)
        movieclip = movieclips.load(path)
        frame_start = get_frame_from_filename(basename)
        sequence_strip = sequences.new_clip(
            name=basename,
            clip=movieclip,
            channel=sequence_channel,
            frame_start=frame_start
            )
        
    elif os.path.isdir(path):
        dirname = path
        if files:
            movieclip = movieclips.load(os.path.join(dirname, files[0]))
            sequence_strip = create_image_sequence(scene, dirname, files)
            
    elif '#' in path:
        dirname = os.path.dirname(path)
        if images:
            movieclip = movieclips.load(os.path.join(dirname, images[0]))
            sequence_strip = create_image_sequence(scene, dirname, images)
        
    # movieclip is created also for image sequences to get the resolution
    x_res, y_res = movieclip.size
    
    # custom properties
    sequence_strip['sequence_name'] = sequence['name']
    
    
# SET OVERLAY
if settings['overlays']:
    overlay_scene = sequences.new_scene(
        name='overlay_scene',
        scene=scene,
        channel=overlay_channel,
        frame_start = sequence_strip.frame_start
        )
    overlay_scene.frame_final_duration = sequence_strip.frame_duration
    overlay_scene.blend_type = 'ALPHA_OVER'
    
    for overlay in settings['overlays']:
        object = scene.objects[overlay['position']]
        object.hide_render = False
        if overlay['type'] == 'TEXT':
            object.data.body = overlay['body']
        elif overlay['type'] == 'DATE':
            object.data.body = time.strftime('%Y-%m-%d')
        elif overlay['type'] == 'USER':
            object.data.body = getpass.getuser()
        
        
# RENDER SETTINGS
scene.frame_start = sequence_strip.frame_start
scene.frame_end = scene.frame_start + sequence_strip.frame_duration - 1
scene.render.resolution_x = x_res
scene.render.resolution_y = y_res
scene.render.resolution_percentage = 100
scene.render.filepath = settings['output']

if settings['display_bars']:
    scene.render.resolution_y += settings['bar_size']
    sequence_strip.use_translation = True
    sequence_strip.transform.offset_y = settings['bar_size']/2


# SAVE FILE
#bpy.ops.wm.save_as_mainfile(
    #filepath=settings['output']+'.blend',
    #check_existing=True,
    #relative_remap=False
    #)


# ENCODE
bpy.ops.render.render(animation=True)

