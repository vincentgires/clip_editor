import bpy
import os
import tempfile
import shutil
import subprocess
from clip_editor.config import FFMPEG_BIN


def render(scene):
    """Wrapper around bpy.ops.render.render()

    Always render as image sequence and convert the result with FFmpeg
    that gives more control.
    """

    output = scene.render.filepath
    render_tmp = tempfile.mkdtemp()
    scene.render.filepath = os.path.join(render_tmp, 'render.####.jpg')
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.quality = 100

    bpy.ops.render.render(animation=True)

    # Convert image seq to movie
    command = [
        FFMPEG_BIN,
        '-framerate', str(scene.render.fps),
        '-i', '{}/render.%04d.jpg'.format(render_tmp),
        '-c:v', 'mjpeg',
        '-q:v', '1',
        output, '-y']
    subprocess.call(command)

    # Remove temp folder
    shutil.rmtree(render_tmp)
    scene.render.filepath = output
