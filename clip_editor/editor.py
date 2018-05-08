import os
import json
import subprocess
from clip_editor import config
from clip_editor import utils


def check_filters(collection, attribute, value):
    filters = collection.filters
    if attribute in filters:
        if value in filters[attribute]:
            return True
        else:
            return False
    return True


class Enum(object):
    def __init__(self, *args):
        self._items = args

    def __getattr__(self, value):
        if value in self._items:
            return value

    def __iter__(self):
        return self._items.__iter__()

    @property
    def items(self):
        return self._items


class Item(object):
    def __init__(self, parent=None, **kwargs):
        self._parent = parent
        self._create_attributes(kwargs)

    def _create_attributes(self, attributes):
        for key in attributes.keys():
            setattr(self, key, attributes[key])

    @property
    def attributes(self):
        attributes = {}
        for attr in vars(self):
            if not attr.startswith('_'):
                attributes[attr] = self[attr]
        return attributes

    def __getitem__(self, key):
        return getattr(self, key)

    def __setattr__(self, attribute, value):
        object.__setattr__(self, attribute, value)

        if self._parent:
            if not check_filters(self._parent, attribute, value):
                object.__setattr__(self, attribute, None)
                raise AttributeError('Wrong value')


class Collection(object):
    _ItemType = Item

    def __init__(self, filters=[], **kwargs):
        self._items = []
        self._filters = filters
        self._attributes = kwargs

    def __getattr__(self, value):
        if value in self._items:
            return value

    def __iter__(self):
        return self._items.__iter__()

    @property
    def items(self):
        return self._items

    @property
    def filters(self):
        return self._filters

    @property
    def attributes(self):
        return self._attributes.keys()

    def _check_attribute(self, attribute):
        return True if attribute in self._attributes else False

    def new(self, **kwargs):
        attributes = self._attributes.copy()

        for k in kwargs.keys():
            if not self._check_attribute(k):
                raise AttributeError('Wrong attribute')
            if k in attributes.keys():
                if check_filters(self, k, kwargs[k]):
                    attributes[k] = kwargs[k]
                else:
                    raise AttributeError('Wrong value')

        item = self._ItemType(self, **attributes)
        self._items.append(item)
        return item


OverlayType = Enum(
    'TEXT',
    'FILENAME',
    'NAME',
    'FRAME',
    'DATE',
    'USER')


OverlayPosition = Enum(
    'TOP_LEFT',
    'TOP_CENTER',
    'TOP_RIGHT',
    'BOTTOM_LEFT',
    'BOTTOM_CENTER',
    'BOTTOM_RIGHT')


class Sequence(Item):
    def find_images(self):
        images = []
        path = self.path
        dirname, basename = os.path.split(path)
        dirname = utils.normpath(dirname)

        if '#' not in basename:
            return None

        length = 0
        index = basename.find('#')

        for i in basename[index:]:
            if i == '#':
                length += 1
            else:
                break

        for file in os.listdir(dirname):
            if len(file) == len(basename):
                check = True
                for i in range(length):
                    if not file[index+i].isdigit():
                        check = False
                if check:
                    images.append(file)

        images.sort()
        return images


class Sequences(Collection):
    _ItemType = Sequence

    def __init__(self, name='', path=''):
        attributes = {
            'name': name,
            'path': path,
            'files': [],
            'colorspace': None}
        super(Sequences, self).__init__(**attributes)


class Overlays(Collection):
    def __init__(self, type='TEXT', position='BOTTOM_LEFT', body=''):
        attributes = {
            'type': type,
            'position': position,
            'body': body}
        filters = {
            'type': OverlayType,
            'position': OverlayPosition}
        super(Overlays, self).__init__(filters=filters, **attributes)


class Clip():
    def __init__(self, ocio=None):
        self.view_transform = None
        self.ocio = ocio
        self._sequences = Sequences()
        self._overlays = Overlays()

    @property
    def sequences(self):
        return self._sequences

    @property
    def overlays(self):
        return self._overlays

    def encode(self, output, fps=24, resolution=None,
               display_bars=False, bar_size=30, debug_file=False):

        output = utils.normpath(output)
        sequences_settings = []
        
        for seq in self.sequences:
            item = seq.attributes
            item['images'] = seq.find_images()
            sequences_settings.append(item)

        overlays_settings = [i.attributes for i in self.overlays]

        settings = {
            'sequences': sequences_settings,
            'output': output,
            'fps': fps,
            'resolution': resolution,
            'overlays': overlays_settings,
            'display_bars': display_bars,
            'bar_size': bar_size,
            'view_transform': self.view_transform,
            'debug_file': debug_file}

        settings = json.dumps(settings)

        command = [
            config.blender_path,
            config.template_path,
            '--background',
            '--factory-startup',
            '--enable-autoexec',
            '--python',
            config.script_path,
            '--',
            settings]

        env = os.environ.copy()
        if self.ocio:
            env['OCIO'] = self.ocio

        subprocess.call(command, env=env)
