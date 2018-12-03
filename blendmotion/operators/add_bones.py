import bpy

from blendmotion.core import add_bones
from blendmotion.error import OperatorError, error_and_log

class SelectAndAddBonesOperator(bpy.types.Operator):
    bl_idname = 'bm.select_and_add_bones'
    bl_label = 'Select base object'

    def list_objects(self, context):
        return [(name, name, name) for name, o in context.scene.objects.items() if o.type == 'ARMATURE']

    base_object_name = bpy.props.EnumProperty(name='Object', description=bl_label, items=list_objects)

    def execute(self, context):
        if self.base_object_name not in bpy.data.objects:
            return error_and_log(self, 'object "{}" not found'.format(self.base_object_name))

        obj = bpy.data.objects[self.base_object_name]
        try:
            add_bones(obj)
        except OperatorError as e:
            e.report(self)
            e.log()
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class AddBonesOperator(bpy.types.Operator):
    bl_idname = "mesh.addbmbones"
    bl_label  = "Kinematic Bones on Phobos model"
    bl_description = "Add kinematic bones on phobos model from selected mesh"
    bl_options = {'REGISTER', 'UNDO'}

    with_ik = bpy.props.BoolProperty(name="Enable IK", default=True)

    def execute(self, context):
        if len(context.selected_objects) == 0:
            return bpy.ops.bm.select_and_add_bones('INVOKE_DEFAULT')

        if len(context.selected_objects) != 1:
            return error_and_log(self, 'Single object must be selected')

        obj = context.selected_objects[0]
        try:
            add_bones(obj, with_ik=self.with_ik)
        except OperatorError as e:
            e.report(self)
            e.log()
            return {'CANCELLED'}

        return {'FINISHED'}
