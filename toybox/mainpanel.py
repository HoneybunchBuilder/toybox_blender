import bpy


class ToyboxSettings(bpy.types.PropertyGroup):
    project_path: bpy.props.StringProperty(name="Project Path", default="../")


class OBJECT_PT_Toybox(bpy.types.Panel):
    bl_label = "Toybox"
    bl_idname = "OBJECT_PT_Toybox"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Toybox"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        layout.label(text="Toybox", icon='WORLD_DATA')

        layout.prop(context.scene.toybox, "project_path")

        row = layout.row()
        row.operator("tb.build")
        row.operator("tb.run")


def register():
    bpy.types.Scene.toybox = bpy.props.PointerProperty(type=ToyboxSettings)
