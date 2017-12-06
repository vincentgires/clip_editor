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

def update_frame(scene):
    for overlay in settings['overlays']:
        if overlay['type'] == 'FRAME':
            objects = scene.objects[overlay['position']]
            objects.data.body = '{:04}'.format(scene.frame_current)

bpy.app.handlers.frame_change_pre.append(update_frame)

filename = os.path.basename(settings['sequences'][0]['path'])

# MOVIECLIP
settings['sequences'][0]['path'] = os.path.normpath(settings['sequences'][0]['path'])
if sys.platform.startswith('linux'):
    settings['sequences'][0]['path'] = settings['sequences'][0]['path'].replace('//', '/')

clip = movieclips.load(settings['sequences'][0]['path'])
x, y = clip.size

# SEQUENCER
if not scene.sequence_editor:
    scene.sequence_editor_create()

sequences = scene.sequence_editor.sequences

frame_start = int(filename.split('.')[-2])
sequence_strip = sequences.new_clip(
    name='sequence_clip',
    clip=clip,
    channel=1,
    frame_start=frame_start
    )

# SET OVERLAY
if settings['overlays']:
    overlay_scene = sequences.new_scene(
        name='overlay_scene',
        scene=scene,
        channel=2,
        frame_start=frame_start
        )
    overlay_scene.frame_final_duration = clip.frame_duration
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
scene.frame_end = frame_start+clip.frame_duration-1
scene.frame_start = frame_start
scene.render.resolution_x = x
scene.render.resolution_y = y
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

