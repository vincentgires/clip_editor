import json

TEXTOVERLAY_TYPE = (
    'TEXT',
    'FILENAME',
    'NAME',
    'FRAME',
    'DATE',
    'USER')

TEXTOVERLAY_POSITION = (
    'TOP_LEFT',
    'TOP_CENTER',
    'TOP_RIGHT',
    'BOTTOM_LEFT',
    'BOTTOM_CENTER',
    'BOTTOM_RIGHT')


# def textoverlay(position, subtype, color=None):
#     color = color or (1.0, 1.0, 1.0)
#     if not (position in TEXTOVERLAY_POSITION and subtype in TEXTOVERLAY_TYPE):
#         return None
#     overlay = {
#         'position': position,
#         'subtype': subtype,
#         'color': color}
#     return json.dumps(overlay)


class TextOverlay():
    def __init__(self, position=None, subtype=None, color=None):
        self.color = color or (1.0, 1.0, 1.0)
        self.position = position or TEXTOVERLAY_POSITION[0]
        self.subtype = subtype or TEXTOVERLAY_TYPE[0]


class Clip():
    def encode(self):
        pass


class ImageSequence(Clip):
    pass


class Movie(Clip):
    pass
