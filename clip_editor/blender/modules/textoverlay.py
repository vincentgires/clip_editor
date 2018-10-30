import bpy


def create_scene_overlay():
    '''Create a new scene and append it to VSE.'''

    data = bpy.data
    scene = data.scenes.new('TextOverlay')
