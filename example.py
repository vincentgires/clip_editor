import clip_editor

clip = clip_editor.Clip()

sequence = clip.sequences.new()
# from frame 0101 to the end of the sequence:
sequence.path = '/my/image_sequence/path/filename.0101.exr'


frame_overlay = clip.overlays.new()
# available overlay types in clip_editor.OverlayType.items
frame_overlay.type = 'FRAME'
# available position in clip_editor.OverlayPositions.items
frame_overlay.position = 'BOTTOM_LEFT'
frame_overlay.body = 'my custon text'

clip.overlays.new(type='TEXT',
                  position='TOP_RIGHT',
                  body='my custom text')

clip.ocio = '/nwave/data/color/aces_1.0.3-nwave/config.ocio'
clip.encode(output='/home/my_home/out.mov',
            display_bars=True)

