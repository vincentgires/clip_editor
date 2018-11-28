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
    scene.render.alpha_mode = 'TRANSPARENT'

    # Camera
    camera_data = data.cameras.new('camera')
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 1
    camera_object = data.objects.new('camera', camera_data)
    camera_object.location = (0.0, 0.0, 10.0)
    scene.objects.link(camera_object)

    # Text
    textoverlays = _get_textoverlays()
    for overlay in textoverlays:
        position = overlay['position']
        subtype = overlay['subtype'] if 'subtype' in overlay else 'TEXT'

        font_curve = data.curves.new(type='FONT', name='font_curve')
        font_curve.size = 0.01
        font_object = data.objects.new('font_object', font_curve)
        font_object['position'] = position
        font_object['subtype'] = subtype

        # Add variable expression with render width and height
        # variable name: res_y and res_x
        x, y = 0, 1
        drivers = {
            'loc_x': font_object.driver_add('location', x).driver,
            'loc_y': font_object.driver_add('location', y).driver}
        for k, driver in drivers.items():
            driver.type = 'SCRIPTED'
            _create_variable_expression(
                driver, 'res_y', 'SCENE', scene, 'render.resolution_y')
            _create_variable_expression(
                driver, 'res_x', 'SCENE', scene, 'render.resolution_x')

        if isinstance(position, str):
            if 'TOP' in position:
                drivers['loc_y'].expression = '0.5*(res_y/res_x)'
                font_curve.align_y = 'TOP'
            elif 'BOTTOM' in position:
                drivers['loc_y'].expression = '-0.5*(res_y/res_x)'
                font_curve.align_y = 'BOTTOM'
            if 'LEFT' in position:
                drivers['loc_x'].expression = '-0.5'
                font_curve.align_x = 'LEFT'
            elif 'RIGHT' in position:
                drivers['loc_x'].expression = '0.5'
                font_curve.align_x = 'RIGHT'
            elif 'CENTER' in position:
                font_curve.align_x = 'CENTER'

        elif isinstance(position, tuple):
            # bottom left is 0,0
            x, y = position
            x_expr = '-0.5+({x}/res_x)'.format(x=x)
            y_expr = '-0.5*(res_y/res_x)+({y}/res_y)*(res_y/res_x)'.format(y=y)
            drivers['loc_x'].expression = x_expr
            drivers['loc_y'].expression = y_expr

        scene.objects.link(font_object)

    scene.update()
    return scene


if __name__ == '__main__':
    create_scene()
