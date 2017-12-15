import os
import sys

current_dir = os.path.dirname(__file__)

template_path = os.path.join(current_dir, 'template.blend')
script_path = os.path.join(current_dir, 'process.py')

if sys.platform.startswith('linux'):
    blender_path = '/nwave/software/Blender/2.79/linux64/blender'
else:
    blender_path = '//nwave/software/Blender/2.79/win64/blender.exe'
