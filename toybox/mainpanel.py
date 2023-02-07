import bpy


class ToyboxSettings(bpy.types.PropertyGroup):
    project_path: bpy.props.StringProperty(name="Project Path", default="../")
    project_name: bpy.props.StringProperty(
        name="Project Name", default="toybox-game")
    build_preset: bpy.props.EnumProperty(name="Build Preset", items=[
        ("x64-windows-ninja-llvm", "x64 Windows Ninja LLVM", ""),
        ("x64-windows-static-ninja-llvm", "x64 Windows Static Ninja LLVM", ""),
        ("x64-mingw-ninja-gcc", "x64 Mingw Ninja GCC", ""),
        ("x64-mingw-static-ninja-gcc", "x64 Mingw Static Ninja GCC", ""),
    ]
    )
    build_config: bpy.props.EnumProperty(name="Build Configuration", items=[
        ("debug", "Debug", ""),
        ("relwithdebinfo", "RelWithDebInfo", ""),
        ("release", "Release", ""),
    ]
    )


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
        layout.prop(context.scene.toybox, "project_name")
        layout.prop(context.scene.toybox, "build_preset")
        layout.prop(context.scene.toybox, "build_config")

        row = layout.row()
        row.operator("tb.build")
        row.operator("tb.run")


def register():
    bpy.types.Scene.toybox = bpy.props.PointerProperty(type=ToyboxSettings)
