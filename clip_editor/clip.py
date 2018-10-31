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


def textoverlay(position, subtype, color=None):
    color = color or (1.0, 1.0, 1.0)
    if not (position in TEXTOVERLAY_TYPE and subtype in TEXTOVERLAY_POSITION):
        return None
    overlay = {
        'position': position,
        'subtype': subtype,
        'color': color}
    return json.dumps(overlay)


class TextOverlay():
    pass


class Clip():
    def encode(self):
        pass


class ImageSequence(Clip):
    pass


class Movie(Clip):
    pass
