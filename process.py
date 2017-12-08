import bpy
import os
import time
import sys
import getpass
import json
import pickle

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
    
    if scene.sequence_editor:
        for strip in scene.sequence_editor.sequences:
            if strip.frame_start <= frame_current < strip.frame_start+strip.frame_final_duration:
                if strip.channel == channel:
                    return strip
                else:
                    return None
    else:
        return None

def update_frame(scene):
    for overlay in settings['overlays']:
        object = scene.objects[overlay['position']]
        
        strip = get_current_strip(scene, sequence_channel)
        if strip:
            if strip.type in ['MOVIE', 'MOVIECLIP']:
                if overlay['type'] == 'FRAME':
                    object.data.body = '{:04}'.format(scene.frame_current)
                
            elif strip.type == 'IMAGE':
                elem = strip.strip_elem_from_frame(scene.frame_current)
                file_frame = get_frame_from_filename(elem.filename)
                object.data.body = '{:04}'.format(file_frame)
                
                if overlay['type'] == 'FILENAME':
                    if strip.type == 'IMAGE':
                        object.data.body = elem.filename

bpy.app.handlers.frame_change_pre.append(update_frame)


# MOVIECLIP
settings['sequences'][0]['path'] = os.path.normpath(settings['sequences'][0]['path'])
if sys.platform.startswith('linux'):
    settings['sequences'][0]['path'] = settings['sequences'][0]['path'].replace('//', '/')

path = settings['sequences'][0]['path']
files = settings['sequences'][0]['files']

# MOVIECLIP
if files:
    movieclip = movieclips.load(os.path.join(path, files[0]))
else:
    movieclip = movieclips.load(path)
x_res, y_res = movieclip.size

# SEQUENCER
if not scene.sequence_editor:
    scene.sequence_editor_create()
sequences = scene.sequence_editor.sequences

if os.path.isfile(path):
    filename = os.path.basename(settings['sequences'][0]['path'])
    frame_start = get_frame_from_filename(filename)
    sequence_strip = sequences.new_clip(
        name='sequence_clip',
        clip=movieclip,
        channel=sequence_channel,
        frame_start=frame_start
        )

elif os.path.isdir(path):
    files = settings['sequences'][0]['files']
    filename = os.path.basename(files[0])
    frame_start = int(filename.split('.')[-2])
    
    first_frame = os.path.join(path, files[0])
    sequence_strip = sequences.new_image(
        name='image_sequence',
        filepath=first_frame,
        channel=sequence_channel,
        frame_start=frame_start
        )

    for file in files[1:]:
        name = os.path.basename(file)
        sequence_strip.elements.append(name)

# SET OVERLAY
if settings['overlays']:
    overlay_scene = sequences.new_scene(
        name='overlay_scene',
        scene=scene,
        channel=overlay_channel,
        frame_start=frame_start
        )
    overlay_scene.frame_final_duration = sequence_strip.frame_duration
    overlay_scene.blend_type = 'ALPHA_OVER'
    
    for overlay in settings['overlays']:
        object = scene.objects[overlay['position']]
        object.hide_render = False
        if overlay['type'] == 'TEXT':
            object.data.body = overlay['body']
        elif overlay['type'] == 'FILENAME':
            object.data.body = filename
        elif overlay['type'] == 'NAME':
            object.data.body = overlay['name']
        elif overlay['type'] == 'DATE':
            object.data.body = time.strftime('%Y-%m-%d')
        elif overlay['type'] == 'USER':
            object.data.body = getpass.getuser()
        
        
# RENDER SETTINGS
scene.frame_start = frame_start
#scene.frame_end = frame_start+movieclip.frame_duration-1
scene.frame_end = frame_start+sequence_strip.frame_duration-1
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

