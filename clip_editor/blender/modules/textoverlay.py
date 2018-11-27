import bpy
from clip_editor import argconfig


def _get_textoverlays():
    args = argconfig.get_args()
    textoverlays = [dict(i) for i in args.textoverlay]
    return textoverlays


def _create_variable_expression(
        driver, name, target_type, target_id, data_path):
    variable = driver.variables.new()
    variable.type = 'SINGLE_PROP'
    variable.name = name
    target = variable.targets[0]
    target.id_type = target_type
    target.id = target_id
    target.data_path = data_path
    return variable


def create_scene():
    SCENE_NAME = 'TextOverlay'
    data = bpy.data
    scene = data.scenes.new(SCENE_NAME)

    # Camera
    camera_data = data.cameras.new('camera')
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 1
    camera_object = bpy.data.objects.new('camera', camera_data)
    camera_object.location = (0.0, 0.0, 10.0)
    scene.objects.link(camera_object)

    # Text
    textoverlays = _get_textoverlays()
    for overlay in textoverlays:
        position = overlay['position']
        subtype = overlay['subtype'] if 'subtype' in overlay else 'TEXT'

        font_curve = data.curves.new(type='FONT', name='font_curve')
        font_curve.size = 0.01
        font_object = bpy.data.objects.new('font_object', font_curve)
        font_object['position'] = position
        font_object['subtype'] = subtype

        if isinstance(position, str):
            x, y, z = 0, 1, 2
            driver_y = font_object.driver_add('location', y).driver
            driver_y.type = 'SCRIPTED'
            variable_yy = _create_variable_expression(
                driver_y, 'y', 'SCENE', scene, 'render.resolution_y')
            variable_yx = _create_variable_expression(
                driver_y, 'x', 'SCENE', scene, 'render.resolution_x')

            if 'TOP' in position:
                driver_y.expression = '0.5*(y/x)'
                font_curve.align_y = 'TOP'
            elif 'BOTTOM' in position:
                driver_y.expression = '-0.5*(y/x)'
                font_curve.align_y = 'BOTTOM'
            if 'LEFT' in position:
                font_object.location.x = -0.5
                font_curve.align_x = 'LEFT'
            elif 'RIGHT' in position:
                font_object.location.x = 0.5
                font_curve.align_x = 'RIGHT'
            elif 'CENTER' in position:
                font_curve.align_x = 'CENTER'

        elif isinstance(position, tuple):
            x, y = position
            width = scene.render.resolution_x
            height = scene.render.resolution_y
            bottom = -0.5 * (height / width)
            left = -0.5
            font_object.location.x = left + (x / width)
            font_object.location.y = bottom + (y / height) * (height / width)

        scene.objects.link(font_object)

    scene.update()
    return scene


if __name__ == '__main__':
    create_scene()
