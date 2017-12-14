import clip_editor

clip = clip_editor.Clip()

sequence = clip.sequences.new()

# from frame 0101 to the end of the sequence
sequence.path = '/my/image_sequence/path/filename.0101.exr'

# #### represent frame number
sequence.path = '/my/image_sequence/path/filename.####.exr'
sequence.find_images() # gets the list of all the images corresponding to the sequence

# or you can specify all the files for a directory
sequence.path = '/my/directory/'
sequence.files = [
    '991_0010_my_file.0101.exr',
    '991_0010_my_file.0102.exr',
    '991_0010_my_file.0103.exr',
    '991_0010_my_file.0104.exr',
    '991_0010_my_file.0105.exr'
    ]

frame_overlay = clip.overlays.new()
# available overlay types in clip_editor.OverlayType.items
frame_overlay.type = 'FRAME'
# available position in clip_editor.OverlayPositions.items
frame_overlay.position = 'BOTTOM_LEFT'
frame_overlay.body = 'my custon text'

clip.overlays.new(type='TEXT',
                  position='TOP_RIGHT',
                  body='my custom text')

# colorspace
clip.ocio = '/nwave/data/color/aces_1.0.3-nwave/config.ocio' # optional
clip.view_transform = 'sRGB D60 sim.' # optional
sequence.colorspace = 'ACES - ACEScg' # optional


clip.encode(output='/home/my_home/out.mov',
            display_bars=True)

