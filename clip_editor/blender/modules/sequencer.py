import bpy
import os
import logging


def create_sequence(scene, images=None, path=None, channel=1, frame_start=1):
    """Create a sequence strip depending of the input

    Image sequence or a movieclip.
    Image sequence can be a list of images or a path with ####.
    """

    sequences = scene.sequence_editor.sequences
    movieclips = bpy.data.movieclips

    if path and os.path.isfile(path):
        dirname, basename = os.path.split(path)
        movieclip = movieclips.load(path)
        sequence_strip = sequences.new_clip(
            name=basename,
            clip=movieclip,
            channel=channel,
            frame_start=frame_start)
    elif path and os.path.isdir(path):
        dirname = path
        if not images:
            raise ValueError('Images attribute is empty')
        # movieclip is created to get the resolution of image sequences
        movieclip = movieclips.load(os.path.join(dirname, images[0]))
        first_frame = os.path.join(path, images[0])
        sequence_strip = sequences.new_image(
            name='image_sequence',
            filepath=first_frame,
            channel=channel,
            frame_start=frame_start)
        for image in images[1:]:
            name = os.path.basename(image)
            sequence_strip.elements.append(name)

    else:
        logging.error('Do not find any images')
        return None

    return sequence_strip, movieclip


def set_frame_range(scene):
    frame_start = 1
    frame_end = 1

    for sequence in scene.sequence_editor.sequences:
        if sequence.frame_start < frame_start:
            frame_start = sequence.frame_start

        strip_length = sequence.frame_final_duration
        strip_frame_end = sequence.frame_start+strip_length
        if strip_frame_end > frame_end:
            frame_end = strip_frame_end

    frame_end -= 1
    scene.frame_start = frame_start
    scene.frame_end = frame_end
    return (frame_start, frame_end)
