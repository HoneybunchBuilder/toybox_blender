import bpy
import os
import subprocess
import string


class BuildOperator(bpy.types.Operator):
    bl_idname = "tb.build"
    bl_label = "Build"

    def execute(self, context):
        abs_path = os.path.abspath(context.scene.toybox.project_path)
        config = context.scene.toybox.build_config
        preset = context.scene.toybox.build_preset

        subprocess.run("cmake --preset " + preset, cwd=abs_path)
        subprocess.run(
            "cmake --build --preset " + config + "-" + preset, cwd=abs_path)
        return {'FINISHED'}


class RunOperator(bpy.types.Operator):
    bl_idname = "tb.run"
    bl_label = "Run"

    def execute(self, context):
        abs_path = os.path.abspath(context.scene.toybox.project_path)
        config = context.scene.toybox.build_config
        preset = context.scene.toybox.build_preset
        preset_opts = preset.split('-')
        arch = preset_opts[0]
        plat = preset_opts[1]
        project_name = context.scene.toybox.project_name

        exe_path = abs_path + "/build/"+arch+"/"+plat+"/" + config

        subprocess.Popen(os.path.join(
            exe_path, project_name + ".exe"), cwd=exe_path)
        return {'FINISHED'}
